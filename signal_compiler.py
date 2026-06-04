import json
import time
import random
from dataclasses import dataclass

from openai import OpenAI
import openai as _openai

from churn_verifier import CompanyChurnProfile
from config import GITHUB_TOKEN, GITHUB_ENDPOINT, GITHUB_MODEL, GITHUB_MAX_TOKENS


@dataclass
class IntelligenceCard:
    company_name: str
    signal_narrative: str
    ranked_hypotheses: list[dict]
    recommended_angle: str
    avoid_angle: str
    churn_alert: str
    shield_summary: str


def build_context_block(sanitized_payload: dict, churn_profile: CompanyChurnProfile) -> str:
    company = sanitized_payload.get("company", {})
    contacts = sanitized_payload.get("contacts", [])
    posts = sanitized_payload.get("recent_posts", [])

    contact_lines = []
    for contact in contacts[:4]:
        contact_lines.append(
            f"  - {contact.get('full_name', 'Unknown')} | {contact.get('title', 'Unknown')} "
            f"| confidence {contact.get('confidence_score', 'N/A')}"
        )

    post_lines = []
    for post in posts[:5]:
        post_lines.append(
            f"  [{post.get('author_name', 'Unknown')} / {post.get('author_title', '')}] "
            f"on {post.get('posted_date', 'recent')}: "
            f"\"{post.get('content', '')}\""
        )

    churn_lines = []
    for dept in churn_profile.departments:
        churn_lines.append(
            f"  {dept.name}: {dept.classification} "
            f"(delta={dept.headcount_delta_90d:+d}, "
            f"postings={dept.job_postings_90d}, "
            f"backfill_ratio={dept.backfill_ratio})"
        )

    context = f"""
COMPANY PROFILE
---------------
Name: {company.get('company_name', 'Unknown')}
Industry: {company.get('industry', 'Unknown')}
Stage: {company.get('funding_stage', 'Unknown')}
Total Headcount: {company.get('headcount', 'Unknown')}
Headcount Delta (90d): {company.get('headcount_delta_90d', 'Unknown')}
Glassdoor Rating: {company.get('glassdoor_overall_rating', 'N/A')} ({company.get('glassdoor_trend', 'unknown trend')})
Recent Funding: {json.dumps(company.get('recent_funding', {}), indent=2)}

KEY CONTACTS (PII redacted by CrustShield)
-------------------------------------------
{chr(10).join(contact_lines) if contact_lines else "  No high-confidence contacts available"}

CHURN VERIFIER OUTPUT (verified, not raw)
------------------------------------------
Overall Classification: {churn_profile.overall_classification}
Alert Level: {churn_profile.alert_level}
Department Breakdown:
{chr(10).join(churn_lines)}

EXECUTIVE LINKEDIN POSTS (last 30 days)
-----------------------------------------
{chr(10).join(post_lines) if post_lines else "  No recent posts available"}
"""
    return context.strip()


def _mock_llm_response(context_block: str, reason: str) -> dict:
    """
    Context-aware mock response — extracts company name, churn signal, and
    executive quotes from the context block so each company gets a unique card.
    """
    print(reason)
    ctx = context_block.lower()
    raw = context_block  # preserve case for extraction

    # ── Extract company name ─────────────────────────────────────────────────
    company = "this company"
    for line in raw.splitlines():
        if line.strip().startswith("Name:"):
            company = line.split("Name:", 1)[1].strip()
            break

    # ── Extract first executive quote from posts ─────────────────────────────
    exec_quote = ""
    in_posts = False
    for line in raw.splitlines():
        if "EXECUTIVE LINKEDIN POSTS" in line:
            in_posts = True
            continue
        if in_posts and '"' in line:
            q = line.split('"', 1)
            if len(q) > 1:
                exec_quote = q[1].rstrip('"').strip()
                break

    # ── Extract stage ────────────────────────────────────────────────────────
    stage = ""
    for line in raw.splitlines():
        if line.strip().startswith("Stage:"):
            stage = line.split("Stage:", 1)[1].strip()
            break

    # ── Build per-signal narratives ─────────────────────────────────────────
    is_public   = "public" in stage.lower() or "nyse" in stage.lower() or "nasdaq" in stage.lower()
    is_acquired = "acquired" in stage.lower() or "capital one" in ctx
    is_pre_ipo  = "pre-ipo" in stage.lower() or "ipo" in ctx
    high_growth = "true_growth" in ctx

    if is_acquired:
        narrative = (
            f"{company} is mid-acquisition integration — headcount consolidation in go-to-market "
            f"is masking the real story: significant R&D investment to rebuild the product on the acquirer's platform. "
            f"Sales attrition is real but engineered; engineering headcount is growing. "
            f"Any outreach should acknowledge the transition, not pretend it hasn't happened."
        )
        h1 = {
            "rank": "H1",
            "hypothesis": f"{company} needs vendor consolidation tools — acquisition transitions create shadow IT and contract chaos as two procurement systems merge.",
            "evidence": f"Negative sales headcount delta alongside engineering growth signals active integration spend.",
            "confidence": "HIGH",
        }
        h2 = {
            "rank": "H2",
            "hypothesis": f"Champion-tracking is critical during this transition — {company}'s buyers are shifting roles as org charts redraw.",
            "evidence": "Acquisition integrations typically move 30-40% of key contacts within 90 days.",
            "confidence": "HIGH",
        }
        h3 = {
            "rank": "H3",
            "hypothesis": "The combined entity will need a unified data layer across two customer databases with overlapping segments.",
            "evidence": "Two separate CRMs and billing systems are now converging.",
            "confidence": "MEDIUM",
        }
        angle = f"Lead with how your product handles multi-entity data merges and contact continuity during M&A — {company} is living that problem right now."
        avoid = "Do not pitch them as a standalone growth company — they are in integration mode and messaging around scale will feel tone-deaf."

    elif is_pre_ipo:
        narrative = (
            f"{company} is in IPO preparation mode — every metric is being stress-tested for investor scrutiny. "
            f"Headcount is growing but IPO readiness hiring (IR, legal, SEC reporting) signals the primary internal focus. "
            f"Sales growth is real and strong, but the leadership team's bandwidth is split between customers and the S-1."
        )
        h1 = {
            "rank": "H1",
            "hypothesis": f"{company} needs audit-grade data quality in their CRM and revenue systems — IPO readiness demands clean, defensible pipeline reporting.",
            "evidence": "Active hiring for VP Investor Relations and Director of SEC Reporting signals IPO prep is underway.",
            "confidence": "HIGH",
        }
        h2 = {
            "rank": "H2",
            "hypothesis": "They need to harden compliance and data sovereignty controls ahead of public company obligations.",
            "evidence": f"Compliance and legal headcount growing — {company} is building the infrastructure the SEC and auditors will examine.",
            "confidence": "HIGH",
        }
        h3 = {
            "rank": "H3",
            "hypothesis": "Revenue recognition tooling will become critical — ASC 606 compliance at their scale requires automation.",
            "evidence": "ARR growth trajectory and multi-product revenue mix creates complex recognition scenarios.",
            "confidence": "MEDIUM",
        }
        angle = f"Frame your pitch around audit-readiness and defensible revenue data — {company} is 6-18 months from public markets and every investor deck needs clean numbers."
        avoid = "Do not open with product features — lead with compliance, auditability, and data integrity. Those are the only things the IPO team cares about right now."

    elif is_public:
        narrative = (
            f"{company} is a public company executing against quarterly guidance. "
            f"Growth is real (+{(raw.split('Revenue Growth:', 1)[1].split()[0] if 'Revenue Growth:' in raw else '~30%')}) "
            f"but Wall Street scrutiny means every sales dollar and headcount add has a cost-per-acquisition lens on it. "
            f"The opportunity is in operational efficiency, not just expansion."
        )
        h1 = {
            "rank": "H1",
            "hypothesis": f"{company}'s sales team is scaling fast — data hygiene at the rep level degrades as territories expand without updated contact intelligence.",
            "evidence": "Sales headcount growth outpacing data engineering investment — a pattern that leads to stale CRM records.",
            "confidence": "HIGH",
        }
        h2 = {
            "rank": "H2",
            "hypothesis": "As a public company, they need predictable pipeline forecasting — any tool that improves signal accuracy directly improves quarterly guidance credibility.",
            "evidence": f"{exec_quote[:80] + '...' if exec_quote and len(exec_quote) > 80 else exec_quote or 'Public company CFO cadence demands quarterly predictability.'}",
            "confidence": "HIGH",
        }
        h3 = {
            "rank": "H3",
            "hypothesis": "Glassdoor trend signals internal cultural friction from rapid scaling — employee NPS tooling and manager effectiveness data could be a wedge.",
            "evidence": "Declining or flat Glassdoor trend alongside aggressive headcount adds.",
            "confidence": "LOW",
        }
        angle = f"Lead with pipeline predictability and revenue forecasting accuracy — as a public company, {company}'s CFO is accountable to Wall Street guidance every 90 days."
        avoid = "Do not lead with headcount growth metrics as a proof point — they already track those obsessively. Show how you improve revenue per rep, not rep count."

    elif high_growth:
        exec_signal = f" Their executive team is publicly vocal: \"{exec_quote[:100]}...\"" if exec_quote else ""
        narrative = (
            f"{company} is in true growth mode — headcount is expanding across all departments and hiring velocity "
            f"is outpacing backfill. The primary risk is that data infrastructure does not scale with GTM velocity.{exec_signal}"
        )
        h1 = {
            "rank": "H1",
            "hypothesis": f"{company}'s sales team is expanding faster than their data quality layer — new AEs inherit stale contact records in a fast-moving territory map.",
            "evidence": "Positive headcount delta across sales with job postings skewed toward net-new hires.",
            "confidence": "HIGH",
        }
        h2 = {
            "rank": "H2",
            "hypothesis": "With 10+ product lines or fast multi-product expansion, their revenue operations needs cross-product attribution intelligence that most CRMs don't provide natively.",
            "evidence": "Multi-product growth companies consistently hit attribution gaps at this scale.",
            "confidence": "MEDIUM",
        }
        h3 = {
            "rank": "H3",
            "hypothesis": "PLG-to-enterprise motion will require contact enrichment at the account level — free users converting to enterprise buyers need immediate outreach intelligence.",
            "evidence": f"{company}'s growth motion creates a large pool of product-qualified leads that sales must prioritize accurately.",
            "confidence": "MEDIUM",
        }
        angle = f"Lead with scale — {company} is growing fast enough that data quality compounds as a problem. Every rep onboarded without clean data is a lost quarter."
        avoid = "Do not congratulate them on growth and then pitch retention — they are in net-new acquisition mode and retention framing will land cold."

    else:
        # BACKFILL_CHURN or MIXED
        narrative = (
            f"{company} shows mixed signals — job posting volume does not match net headcount additions in key departments. "
            f"Some roles being posted are backfill, not expansion. "
            f"Outreach that congratulates on growth will embarrass the sender — the real story is internal attrition."
        )
        h1 = {
            "rank": "H1",
            "hypothesis": f"{company} has elevated attrition in revenue-generating roles — they need champion-tracking to retain buyer relationships as their own reps churn.",
            "evidence": "Backfill ratio above warning threshold in sales or customer-facing departments.",
            "confidence": "HIGH",
        }
        h2 = {
            "rank": "H2",
            "hypothesis": "They need real-time contact verification — stale mobile numbers and personal emails are a direct cost when reps cycle out and take their network.",
            "evidence": "Low-confidence contacts dropped by CrustShield — a signal that contact data is aging faster than it is refreshed.",
            "confidence": "MEDIUM",
        }
        h3 = {
            "rank": "H3",
            "hypothesis": "Glassdoor decline plus backfill churn suggests a cultural friction point — employee engagement tooling could surface the root cause before it hits revenue.",
            "evidence": "Correlation between declining Glassdoor trend and elevated backfill ratios in the department breakdown.",
            "confidence": "LOW",
        }
        angle = f"Lead with contact continuity and champion-tracking — when {company}'s reps leave they take buyer relationships with them. That is the problem to solve."
        avoid = "Do not congratulate them on headcount growth — the churn verifier shows a meaningful portion of hiring is backfill, not expansion."

    return {
        "signal_narrative": narrative,
        "ranked_hypotheses": [h1, h2, h3],
        "recommended_angle": angle,
        "avoid_angle": avoid,
    }


SYSTEM_PROMPT = """You are TrueSignal, an enterprise sales intelligence compiler.

Your job is to synthesize B2B company signals into actionable intelligence for sales teams.
You receive structured company data that has already been:
1. Verified for PII compliance (personal data has been stripped)
2. Analyzed for headcount churn vs true growth (the Churn Verifier output is ground truth)

Your output must be a JSON object with exactly this structure:
{
  "signal_narrative": "2-4 sentences. What is the coherent story about what this company is going through right now? Synthesize multiple signals into a single narrative. Be specific -- use the actual numbers and data points provided.",
  "ranked_hypotheses": [
    {
      "rank": "H1",
      "hypothesis": "What does this company most likely need right now? Be specific about what product/capability would solve their inferred pain.",
      "evidence": "Which specific signals support this hypothesis?",
      "confidence": "HIGH|MEDIUM|LOW"
    },
    {
      "rank": "H2",
      "hypothesis": "...",
      "evidence": "...",
      "confidence": "..."
    },
    {
      "rank": "H3",
      "hypothesis": "...",
      "evidence": "...",
      "confidence": "..."
    }
  ],
  "recommended_angle": "One sentence. If you were opening a conversation with this company today, what is the single most relevant angle? Tie it to a specific signal.",
  "avoid_angle": "One sentence. What should the salesperson NOT say? (e.g., if churn is flagged, do not congratulate on growth)"
}

Rules:
- Never fabricate data. Use only what is in the context block.
- Never output PII. The context block has already had PII stripped -- do not invent contact details.
- The Churn Verifier output is ground truth. Do not contradict it.
- If a LinkedIn post contains a direct quote from an executive, treat it as the highest-priority signal.
- Be direct. No hedging. These are hypotheses, not certainties, but state them with conviction.
- Output only valid JSON. No prose before or after the JSON object."""


def call_llm(context_block: str) -> dict:
    if not GITHUB_TOKEN:
        return _mock_llm_response(
            context_block,
            "[Signal Compiler] No GITHUB_TOKEN found — using mock LLM response.",
        )

    client = OpenAI(base_url=GITHUB_ENDPOINT, api_key=GITHUB_TOKEN)

    user_prompt = f"""Here is the verified company intelligence package for analysis:

{context_block}

Synthesize this into a TrueSignal intelligence card. Output JSON only."""

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]

    max_retries = 5
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=GITHUB_MODEL,
                messages=messages,
                max_tokens=GITHUB_MAX_TOKENS,
            )
            break
        except _openai.RateLimitError:
            wait = (2 ** attempt) + random.random()
            print(f"[Signal Compiler] Rate limited (attempt {attempt + 1}/{max_retries}), sleeping {wait:.1f}s...")
            time.sleep(wait)
            if attempt == max_retries - 1:
                return _mock_llm_response(context_block, "[Signal Compiler] Rate limit exhausted — using mock response.")
        except _openai.AuthenticationError:
            return _mock_llm_response(
                context_block,
                "[Signal Compiler] GITHUB_TOKEN unauthorized — falling back to mock LLM response.",
            )
        except Exception as exc:
            print(f"[Signal Compiler] LLM call failed ({exc}) — using mock response.")
            return _mock_llm_response(context_block, "[Signal Compiler] LLM unreachable; using local heuristics.")

    raw_text = response.choices[0].message.content.strip()

    if raw_text.startswith("```"):
        raw_text = raw_text.split("```")[1]
        if raw_text.startswith("json"):
            raw_text = raw_text[4:]
    raw_text = raw_text.strip()

    try:
        return json.loads(raw_text)
    except json.JSONDecodeError as exc:
        print(f"[Signal Compiler] JSON parse error: {exc}")
        print(f"[Signal Compiler] Raw response: {raw_text[:500]}")
        return _mock_llm_response(context_block, "[Signal Compiler] JSON parse failed — using mock response.")


def run(
    sanitized_payload: dict,
    churn_profile: CompanyChurnProfile,
    shield_log,
) -> IntelligenceCard:
    print("[Signal Compiler] Building context block...")
    context_block = build_context_block(sanitized_payload, churn_profile)

    print("[Signal Compiler] Calling LLM...")
    parsed = call_llm(context_block)

    company_name = sanitized_payload.get("company", {}).get("company_name", "Unknown")

    card = IntelligenceCard(
        company_name=company_name,
        signal_narrative=parsed.get("signal_narrative", ""),
        ranked_hypotheses=parsed.get("ranked_hypotheses", []),
        recommended_angle=parsed.get("recommended_angle", ""),
        avoid_angle=parsed.get("avoid_angle", ""),
        churn_alert=churn_profile.alert_level,
        shield_summary=shield_log.summary(),
    )

    print(f"[Signal Compiler] Intelligence card compiled for {company_name}")
    return card
