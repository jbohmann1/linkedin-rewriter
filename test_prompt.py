import json
import anthropic
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()

# ── Paste your test profile here ──────────────────────────────────────────────
headline    = "Data Analytics | AI | Leader"
about       = "A determined and goal-oriented student that has experience working alone and in a team. Strongly focused on the ability to complete tasks within short deadlines."
target_role = "Continuous Improvement Project Officer at CERN"
tone        = "conversational"
jobs = [
    {
        "title": "IT Consultant at ILGA World",
        "bullets": "Managing IT Tech support for staff, consultants and members\nCreated IT Risk assessment checklist for compliance\nDeveloped automation tools for faster data migration"
    },
    {
        "title": "Data and Statistics Consultant at UNHCR",
        "bullets": "Created an ai powered analytics tool for qualitative finance and admin data in python\nWorked on releasing the first company wide generative AI chatbot for finance and admin uses\nOptimized processes for accounts payable by removing triage cost and reducing resolution time"
    }
]

# ── Paste your current prompt function here ───────────────────────────────────
from main import build_prompt

prompt = build_prompt(headline, about, jobs, target_role, tone)

# ── Run it ────────────────────────────────────────────────────────────────────
message = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=2500,
    messages=[{"role": "user", "content": prompt}]
)

raw = message.content[0].text.strip()

# Strip markdown fences if present
if raw.startswith("```"):
    raw = raw.split("```")[1]
    if raw.startswith("json"):
        raw = raw[4:]
raw = raw.strip()

print("\n── RAW OUTPUT ──────────────────────────────────────────")
print(raw)

# Pretty print if it's valid JSON
try:
    parsed = json.loads(raw)
    print("\n── PARSED ──────────────────────────────────────────────")
    print("HEADLINE:", parsed.get("headline"))
    print("\nABOUT:", parsed.get("about"))
    for job in parsed.get("jobs", []):
        print(f"\nJOB: {job.get('title')}")
        for b in job.get("bullets", []):
            print(f"  • {b}")
except json.JSONDecodeError:
    print("\n⚠️  Output was not valid JSON — prompt needs adjustment")

print(f"\n── TOKENS USED: {message.usage.input_tokens} in / {message.usage.output_tokens} out ──")