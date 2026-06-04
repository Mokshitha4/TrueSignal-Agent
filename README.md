# TrueSignal

> **Enterprise-safe B2B intelligence middleware built on Crustdata APIs**

TrueSignal is a four-stage intelligence pipeline that transforms raw Crustdata JSON into actionable sales narratives. It strips PII before any AI call, verifies whether headcount growth is real or backfill churn, and compiles a ranked intelligence card with a single opening angle and a "never say this" warning.

Built as a portfolio demo for the Crustdata ecosystem — showing how to build enterprise-deployable tooling on top of their APIs.

---

## Why It Exists



1. **InfoSec blocks it** — raw contact data (mobile numbers, personal emails) cannot leave the corporate perimeter and cannot be sent to a third-party AI API
2. **The growth signal is wrong** — a company posting 74 jobs with -62 net headcount, isn't growing; it's bleeding. Generic "Congrats on the growth!" outreach embarrasses the sender
3. **Signals without a story are noise** — sales teams have data but can't explain *why* the combination of signals matters

TrueSignal solves all three before the LLM ever sees the data.

---

## Architecture

```
Company Name Input
        │
        ▼
┌───────────────────┐
│  1. Data Fetcher  │  Calls Crustdata APIs (company profile, contacts, jobs, posts)
│   fetcher.py      │  Free endpoints: /company/identify, /company/search/autocomplete
│                   │  Falls back to curated mock replica when credits are exhausted
└────────┬──────────┘
         │ raw payload (contains PII)
         ▼
┌───────────────────┐
│  2. CrustShield   │  Strips PII before any external API call
│  crustshield.py   │  • Drops contacts below 0.75 confidence score
│                   │  • Redacts: mobile, personal_email, home_address, DOB, national_id
│                   │  • Regex scan on free-text fields for embedded phone/email
│                   │  • Produces audit log (compliance artifact)
└────────┬──────────┘
         │ sanitized payload (no PII)
         ▼
┌───────────────────┐
│ 3. Churn Verifier │  Deterministic math — no AI involved
│ churn_verifier.py │  backfill_ratio = job_postings_90d ÷ net_headcount_delta_90d
│                   │  • < 0.35  → TRUE_GROWTH
│                   │  • 0.35–0.60 → BACKFILL_CHURN (WARN)
│                   │  • > 0.60  → BACKFILL_CHURN (CRITICAL)
│                   │  • negative delta + postings → CRITICAL (company is shrinking)
└────────┬──────────┘
         │ churn profile (verified signal)
         ▼
┌───────────────────┐
│ 4. Signal Compiler│  Sends clean context + churn verdict to LLM
│ signal_compiler.py│  • System prompt caches the persona (no hallucination)
│                   │  • Churn Verifier output is declared ground truth
│                   │  • Executive LinkedIn posts are highest-priority signal
│                   │  • Returns: narrative, H1/H2/H3 hypotheses, angle, avoid
└────────┬──────────┘
         │ IntelligenceCard
         ▼
  FastAPI / UI / CLI
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Web framework | FastAPI + Uvicorn |
| Frontend | Vanilla HTML/CSS/JS + Tailwind CSS (CDN) |
| LLM | GitHub Models — OpenAI-compatible endpoint |
| Data source | Crustdata REST API |
| PII filter | Custom regex + field-name matching (CrustShield) |
| Churn math | Pure Python — no ML |
| Data validation | Pydantic v2 |
| Config | python-dotenv |

---

## Directory Structure

```
TrueSignal-Agent/
│
├── app.py                  # FastAPI application — serves UI + API endpoints
├── main.py                 # CLI entry point (pipeline without web server)
│
├── fetcher.py              # Stage 1 — Crustdata API calls + mock fallback
├── crustshield.py          # Stage 2 — PII stripping + audit log
├── churn_verifier.py       # Stage 3 — backfill ratio analysis per department
├── signal_compiler.py      # Stage 4 — LLM call + intelligence card compilation
│
├── mock_data.py            # Crustdata replica — factual profiles for 9 companies
├── models.py               # Pydantic models (Contact, JobPosting, etc.)
├── output_formatter.py     # CLI terminal renderer
├── config.py               # API keys, thresholds, model settings
│
├── templates/
│   └── index.html          # Full-page dark UI (hero, pipeline loader, results card)
│
├── .env                    # Local secrets (not committed)
├── requirements.txt
└── README.md
```

---

## Setup

### 1. Clone and create a virtual environment

```bash
cd "TrueSignal-Agent"
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

The `.env` file is already present. Fill in your credentials:

```env
# GitHub PAT — classic token, no special scopes needed for GitHub Models
GITHUB_TOKEN=ghp_yourTokenHere

# Crustdata API key
CRUSTDATA_API_KEY=your_crustdata_key_here

# Set to true when Crustdata credits are exhausted (uses mock_data.py replica)
FORCE_MOCK_DATA=true
```

**Getting a GitHub token:**
1. Go to **github.com → Settings → Developer settings → Personal access tokens → Tokens (classic)**
2. Generate a new token — no special scopes needed
3. Paste it into `.env` as `GITHUB_TOKEN`

### 4. Start the web server

```bash
python -m uvicorn app:app --host 0.0.0.0 --port 8090
```

Open **http://localhost:8090** in your browser.

### 5. (Optional) Run the CLI pipeline

```bash
python main.py "Samsara"
python main.py "Rippling"
python main.py linkedin.com/company/deel
```

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | Serves the intelligence UI |
| `POST` | `/analyze` | Runs the full pipeline for a company name |
| `GET` | `/autocomplete?q=<query>` | Proxies Crustdata's free autocomplete endpoint |
| `GET` | `/docs` | FastAPI auto-generated OpenAPI docs |

### POST /analyze

**Request:**
```json
{ "company_name": "Rippling" }
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "company_name": "Rippling",
    "signal_narrative": "Rippling is in true growth mode — headcount expanding at 78% YoY...",
    "ranked_hypotheses": [
      {
        "rank": "H1",
        "hypothesis": "Their sales team is expanding faster than their data quality layer...",
        "evidence": "Positive headcount delta with job postings skewed toward net-new hires.",
        "confidence": "HIGH"
      },
      { "rank": "H2", "hypothesis": "...", "evidence": "...", "confidence": "MEDIUM" },
      { "rank": "H3", "hypothesis": "...", "evidence": "...", "confidence": "LOW"   }
    ],
    "recommended_angle": "Lead with scale — data quality compounds as a problem...",
    "avoid_angle": "Do not congratulate and then pitch retention — they are in acquisition mode.",
    "churn_alert": "CLEAR",
    "shield_summary": "1 contact(s) dropped | 4 PII field(s) redacted | 0 regex hit(s)"
  }
}
```

---

## Crustdata Integration

### Endpoints used

| Endpoint | Cost | Usage in TrueSignal |
|---|---|---|
| `GET /company/identify` | **Free** | Resolve company_id from name or LinkedIn URL — tried first before any paid call |
| `GET /company/search/autocomplete` | **Free** | Powers the typeahead dropdown in the UI |
| `POST /company/enrich` | 2 credits/record | Full company profile — headcount, funding, Glassdoor, web traffic |
| `POST /person/search` | Paid | Key contacts with confidence scores (pre-CrustShield) |
| `POST /job/search` | Paid | Job postings per department (90-day window) |
| `POST /social_post/professional_network/search/live` | Paid | Recent executive LinkedIn posts |

### Authentication

All requests use `Bearer` token authentication:

```python
HEADERS = {
    "Authorization": f"Bearer {CRUSTDATA_API_KEY}",
    "Content-Type": "application/json",
    "Accept": "application/json",
}
```

---

## Crustdata Replica (Mock Data)

When Crustdata credits are exhausted (`FORCE_MOCK_DATA=true`) or the API returns a 402, TrueSignal automatically falls back to `mock_data.py` — a curated replica with factual 2025-2026 data for 9 companies:

| Company | Stage | ARR | Key Signal |
|---|---|---|---|
| **Samsara** | Public (NYSE: IOT) | $1.62B | 29.6% YoY growth at scale |
| **Rippling** | Series G | $1.0B | 78% YoY, crossed $1B ARR March 2026 |
| **Deel** | Series E (Pre-IPO) | $1.4B | EBITDA+ 3 yrs, $22B payroll, IPO prep |
| **Notion** | Series C | Undisclosed | 100M users, 50%+ ARR from AI |
| **Linear** | Series C | Undisclosed | 226 employees, $35K total marketing spend |
| **Brex** | Acquired by Capital One | $700M | $5.15B deal closed April 2026 |
| **Ramp** | Series E (Raise Imminent) | $1.0B | 133% enterprise growth, $40B valuation talks |
| **Vercel** | Series E | Undisclosed | Next.js ecosystem, v0 AI deployment |
| **Retool** | Series C | Undisclosed | 100K+ internal tools, AI agent builder |

For any company not in this list, `mock_data.py` generates a deterministic profile using a hash of the company name — so the same name always returns the same consistent numbers.

---

## CrustShield — PII Middleware

CrustShield runs between the Crustdata fetch and the LLM call. PII is **stripped before the HTTP request body is built** — it never appears in any outbound API call.

### What gets stripped

| Field type | How it's handled |
|---|---|
| Known PII fields (`mobile_number`, `personal_email`, `home_address`, `date_of_birth`, `national_id`) | Replaced with `[REDACTED_BY_CRUSTSHIELD]` |
| Low-confidence contacts (score < 0.75) | Dropped entirely from the payload |
| Phone numbers in free text | Regex match → `[PHONE_REDACTED]` |
| Personal email domains in free text | Regex match → `[EMAIL_REDACTED]` |

### Audit log

Every redaction is logged in a `ShieldAuditLog` object:

```
1 contact(s) dropped | 6 PII field(s) redacted | 0 regex hit(s) in free text
```

This is the compliance artifact — enterprise customers can audit exactly what was stripped.

### Why not just prompt Claude to ignore PII?

"Please don't repeat PII" is not a compliance control. An enterprise InfoSec team needs **proof that PII never left the perimeter**, not a model's promise. CrustShield strips before the API call — the PII is literally absent from the HTTP request body.

---

## Churn Verifier — The Core Insight

A job posting is not evidence of growth. It is evidence of *intent to hire*.

```
backfill_ratio = job_postings_90d ÷ max(net_headcount_delta_90d, 1)
```

| Ratio | Classification | What it means |
|---|---|---|
| < 0.35 | TRUE_GROWTH (HIGH confidence) | Most hires are net-new |
| 0.35 – 0.60 | BACKFILL_CHURN (WARN) | Significant portion of hiring is replacement |
| > 0.60 | BACKFILL_CHURN (CRITICAL) | Majority of hiring is backfill |
| delta < 0 AND postings > 0 | BACKFILL_CHURN (CRITICAL) | Company is shrinking despite posting jobs |

The last case is the Deel/Brex problem: a company posting 74 jobs while losing 62 net headcount has a backfill ratio of ~1.2. Any outreach that says "Congrats on the growth!" will embarrass the sender.

The overall company classification aggregates department signals:
- ≥ 50% of departments in BACKFILL_CHURN → company is `BACKFILL_CHURN`
- ≥ 70% → alert level escalates to `CRITICAL`
- ≥ 60% of departments in TRUE_GROWTH → company is `TRUE_GROWTH`
- Otherwise → `MIXED`

---

## Signal Compiler — LLM Prompt Design

The system prompt is designed to prevent three common failure modes:

### 1. Hallucination prevention
```
Rules:
- Never fabricate data. Use only what is in the context block.
- Never output PII. The context block has already had PII stripped.
- The Churn Verifier output is ground truth. Do not contradict it.
```

### 2. Executive quote prioritization
```
- If a LinkedIn post contains a direct quote from an executive,
  treat it as the highest-priority signal.
```

This anchors the narrative to first-party evidence. When a VP Sales publicly posts "pipeline predictability is our #1 challenge," that is more reliable than any inferred signal.

### 3. No hedging
```
- Be direct. No hedging. These are hypotheses, not certainties,
  but state them with conviction.
```

Hedged intelligence ("this may suggest they could potentially...") is useless for sales. The output is actionable or it is noise.

### Context-aware fallback

When the LLM is unavailable, `signal_compiler.py` generates a context-aware mock response by parsing the context block for:
- Company stage (Public / Pre-IPO / Acquired / Growth)
- Churn classification
- Executive post signals

This means the demo produces distinct, relevant cards for each company even without a working LLM token.

---

## Configuration Reference

| Variable | Default | Description |
|---|---|---|
| `GITHUB_TOKEN` | *(required)* | GitHub PAT for GitHub Models API access |
| `GITHUB_MODEL` | `openai/gpt-4.1-mini` | Model to use via GitHub Models endpoint |
| `GITHUB_MAX_TOKENS` | `1500` | Max output tokens for LLM response |
| `CRUSTDATA_API_KEY` | *(required for live)* | Crustdata API key |
| `FORCE_MOCK_DATA` | `false` | Set `true` to skip all Crustdata calls |
| `CONFIDENCE_THRESHOLD` | `0.75` | Drop contacts below this CrustShield score |
| `BACKFILL_RATIO_WARN` | `0.35` | Backfill ratio threshold for WARN |
| `BACKFILL_RATIO_CRITICAL` | `0.60` | Backfill ratio threshold for CRITICAL |

---

## Running in Different Modes

### Full demo (no API credits needed)
```bash
# .env: FORCE_MOCK_DATA=true + valid GITHUB_TOKEN
python -m uvicorn app:app --port 8090
```

### Live Crustdata + live LLM
```bash
# .env: FORCE_MOCK_DATA=false + valid CRUSTDATA_API_KEY + valid GITHUB_TOKEN
python -m uvicorn app:app --port 8090
```

### CLI — quick pipeline test
```bash
python main.py "Samsara"
python main.py "Brex"
python main.py "a company you made up"
```

### CLI — force mock data inline
```bash
FORCE_MOCK_DATA=true python main.py "Rippling"
```

---

## Key Design Decisions

**Why separate the Churn Verifier from the Signal Compiler?**
The backfill ratio is deterministic math. You don't want to ask the LLM to figure out whether growth is real — you want to tell the LLM what the verified signal is, then ask for interpretation. Mixing these makes the system less reliable and harder to audit.

**Why not just prompt the LLM to strip PII?**
Because "please don't repeat PII" is not a compliance control. CrustShield strips before the API call — the PII is literally absent from the HTTP request body.

**Why JSON output from the LLM?**
The intelligence card needs to be consumed by downstream systems (CRM, Slack, email sequences). Asking for prose means you have to parse it. Asking for JSON means you get machine-readable intelligence directly. The schema is specified exactly — Claude will hallucinate field names if you don't pin them.

**Why Python?**
Crustdata's primary developer audience builds in Python. A script they can read and copy is more persuasive than a black-box app.

---

## Project Structure for Presentation

This project demonstrates three things to Crustdata:

1. **Enterprise deployability** — CrustShield makes Crustdata data usable inside companies with InfoSec controls. This removes the #1 blocker to enterprise adoption.

2. **Signal fidelity** — The Churn Verifier prevents the embarrassing "Congrats on the growth!" email to a company that's shedding headcount. This makes Crustdata-powered outreach more accurate than competitors.

3. **Developer experience** — The full pipeline is readable, modular, and extensible. Any Crustdata customer building on their API can plug CrustShield or the Churn Verifier into their existing stack.

