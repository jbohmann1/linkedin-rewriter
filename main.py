import os
import uuid
import json
import stripe
import anthropic

from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
from redis import Redis

load_dotenv()

# ── Clients ──────────────────────────────────────────────────────────────────

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

claude = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

redis = Redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"), decode_responses=True)

STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")
STRIPE_PRICE_ID       = os.getenv("STRIPE_PRICE_ID")          # price_xxx from dashboard
BASE_URL              = os.getenv("BASE_URL", "http://localhost:8000")

TTL = 3600  # 1 hour — rewrites expire after this

# ── Prompt ───────────────────────────────────────────────────────────────────

def build_prompt(headline: str, about: str, bullets: str, target_role: str, tone: str) -> str:
    tone_guide = {
        "professional": "Clear, confident, formal — suitable for corporate / finance / law roles.",
        "conversational": "Warm, first-person, human — suitable for startups, creative industries, consulting.",
        "bold":           "Direct, high-impact, strong verbs — suitable for leadership, sales, entrepreneurship.",
    }
    return f"""You are an expert LinkedIn profile writer and career coach.

Rewrite the following LinkedIn profile sections for someone targeting: {target_role}
Tone: {tone} — {tone_guide.get(tone, '')}

Rules:
- Keep the person's authentic voice — do not sound like a robot or template
- Replace weak verbs (responsible for, helped, worked on) with strong action verbs
- Add specificity wherever possible — if no numbers are given, use relative language ("significantly", "50%+ improvement") not invented figures
- Remove clichés: results-driven, passionate, detail-oriented, team player
- Headline: max 220 characters, keyword-rich for recruiters, not just a job title
- About: 3–4 short paragraphs, first-person, ends with a soft CTA
- Experience bullets: start with a verb, one achievement per bullet, max 2 lines each

Return ONLY valid JSON with this exact structure — no markdown, no explanation:
{{
  "headline": "rewritten headline",
  "about": "rewritten about section",
  "bullets": ["rewritten bullet 1", "rewritten bullet 2", "rewritten bullet 3"]
}}

--- CURRENT PROFILE ---
Headline: {headline}

About: {about}

Experience bullets:
{bullets}
"""

# ── Routes ───────────────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def landing(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/generate")
async def generate(
    request: Request,
    headline: str    = Form(...),
    about: str       = Form(...),
    bullets: str     = Form(...),
    target_role: str = Form(...),
    tone: str        = Form("professional"),
):
    # Validate inputs
    if len(headline) < 10 or len(about) < 30:
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "error": "Please fill in all fields with enough detail."},
            status_code=422,
        )

    # Call Claude
    try:
        message = claude.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1500,
            messages=[{"role": "user", "content": build_prompt(headline, about, bullets, target_role, tone)}],
        )
        raw = message.content[0].text.strip()
        # Strip accidental markdown fences
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        rewrite = json.loads(raw)
    except Exception as e:
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "error": f"Generation failed — please try again. ({e})"},
            status_code=500,
        )

    # Store rewrite in Redis
    key = f"rewrite:{uuid.uuid4().hex}"
    redis.setex(key, TTL, json.dumps({
        "headline": rewrite.get("headline", ""),
        "about":    rewrite.get("about", ""),
        "bullets":  rewrite.get("bullets", []),
        "paid":     False,
        # originals for the before/after display
        "orig_headline": headline,
        "orig_about":    about,
        "orig_bullets":  bullets,
    }))

    # Create Stripe Checkout Session
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{"price": STRIPE_PRICE_ID, "quantity": 1}],
            mode="payment",
            metadata={"redis_key": key},
            success_url=f"{BASE_URL}/result?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{BASE_URL}/?cancelled=1",
        )
    except stripe.error.StripeError as e:
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "error": f"Payment setup failed: {e.user_message}"},
            status_code=500,
        )

    return RedirectResponse(session.url, status_code=303)


@app.get("/result", response_class=HTMLResponse)
async def result(request: Request, session_id: str):
    # Verify payment with Stripe (source of truth)
    try:
        session = stripe.checkout.Session.retrieve(session_id)
    except stripe.error.StripeError:
        raise HTTPException(status_code=404, detail="Session not found.")

    if session.payment_status != "paid":
        # Payment not confirmed yet — let the template poll
        return templates.TemplateResponse(
            "waiting.html",
            {"request": request, "session_id": session_id},
        )

    redis_key = session.metadata.get("redis_key")
    raw = redis.get(redis_key) if redis_key else None

    if not raw:
        raise HTTPException(status_code=410, detail="Rewrite expired. Please generate again.")

    data = json.loads(raw)
    return templates.TemplateResponse("result.html", {"request": request, "data": data})


@app.get("/poll-status")
async def poll_status(session_id: str):
    """HTMX/JS polls this while waiting for Stripe webhook."""
    try:
        session = stripe.checkout.Session.retrieve(session_id)
        if session.payment_status == "paid":
            return {"paid": True}
    except Exception:
        pass
    return {"paid": False}


@app.post("/webhook")
async def stripe_webhook(request: Request):
    payload    = await request.body()
    sig_header = request.headers.get("stripe-signature", "")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, STRIPE_WEBHOOK_SECRET)
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid webhook signature.")

    if event["type"] == "checkout.session.completed":
        session   = event["data"]["object"]
        redis_key = session.get("metadata", {}).get("redis_key")
        if redis_key:
            raw = redis.get(redis_key)
            if raw:
                data = json.loads(raw)
                data["paid"] = True
                redis.setex(redis_key, TTL, json.dumps(data))

    return {"ok": True}
