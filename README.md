# LinkedIn Profile Rewriter

AI-powered LinkedIn rewrite tool. Users paste their profile, pay $7 via Stripe, get an improved version instantly.

## Stack
- **FastAPI** — backend + routing
- **Claude Haiku** — AI rewrites via Anthropic API
- **Stripe Checkout** — one-time payments
- **Redis (Upstash)** — temporary session storage
- **Jinja2** — server-rendered HTML templates
- **Tailwind CSS** — styling via CDN

---

## Local setup

### 1. Clone and install dependencies
```bash
git clone <your-repo>
cd linkedin-rewriter
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure environment
```bash
cp .env.example .env
# Edit .env and fill in your keys (see comments in the file)
```

### 3. Get your keys

**Anthropic API key**
- Sign up at console.anthropic.com
- Create an API key → paste as `ANTHROPIC_API_KEY`

**Stripe**
- Sign up at stripe.com
- Dashboard → Products → Add product: "LinkedIn Profile Rewrite", $7 one-time
- Copy the `price_xxx` ID → paste as `STRIPE_PRICE_ID`
- Developers → API keys → copy Secret key → paste as `STRIPE_SECRET_KEY`
- To test webhooks locally, install Stripe CLI:
  ```bash
  stripe listen --forward-to localhost:8000/webhook
  ```
  Copy the webhook signing secret → paste as `STRIPE_WEBHOOK_SECRET`

**Redis (free via Upstash)**
- Sign up at upstash.com
- Create a Redis database → copy the connection URL → paste as `REDIS_URL`
- Or run Redis locally: `docker run -p 6379:6379 redis`

### 4. Run locally
```bash
uvicorn main:app --reload
```
Open http://localhost:8000

In a second terminal, start the Stripe webhook listener:
```bash
stripe listen --forward-to localhost:8000/webhook
```

### 5. Test the payment flow
Use Stripe test card: `4242 4242 4242 4242`, any future date, any CVV.

---

## Deploy to Railway

1. Push code to GitHub
2. railway.app → New Project → Deploy from GitHub
3. Add all env vars from `.env` in the Railway dashboard
4. Set `BASE_URL` to your Railway URL (e.g. `https://yourapp.railway.app`)
5. Add Stripe webhook in dashboard:
   - Stripe → Developers → Webhooks → Add endpoint
   - URL: `https://yourapp.railway.app/webhook`
   - Event: `checkout.session.completed`
   - Copy signing secret → update `STRIPE_WEBHOOK_SECRET` in Railway

---

## Project structure
```
linkedin-rewriter/
├── main.py              # All routes + business logic
├── requirements.txt
├── Procfile             # Railway deployment
├── .env.example         # Copy to .env
├── .gitignore
└── templates/
    ├── base.html        # Nav, footer, Tailwind
    ├── index.html       # Landing page + input form
    ├── waiting.html     # Polls for Stripe confirmation
    └── result.html      # Before/after rewrite display
```

## Routes
| Route | Method | Purpose |
|-------|--------|---------|
| `/` | GET | Landing page + form |
| `/generate` | POST | Call Claude, store in Redis, redirect to Stripe |
| `/result` | GET | Show rewrite after payment confirmed |
| `/poll-status` | GET | JS polls this while waiting for webhook |
| `/webhook` | POST | Stripe webhook — marks session as paid |
