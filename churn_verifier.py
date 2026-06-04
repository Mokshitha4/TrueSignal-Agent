from dataclasses import dataclass

from config import BACKFILL_RATIO_CRITICAL, BACKFILL_RATIO_WARN


@dataclass
class DepartmentSignal:
    name: str
    headcount_current: int
    headcount_delta_90d: int
    job_postings_90d: int
    backfill_ratio: float
    classification: str
    confidence: str
    narrative_note: str


@dataclass
class CompanyChurnProfile:
    overall_classification: str
    departments: list[DepartmentSignal]
    churn_summary: str
    alert_level: str


def classify_department(name: str, delta: int, postings: int) -> DepartmentSignal:
    if postings == 0:
        if delta > 0:
            return DepartmentSignal(
                name=name,
                headcount_current=0,
                headcount_delta_90d=delta,
                job_postings_90d=0,
                backfill_ratio=0.0,
                classification="TRUE_GROWTH",
                confidence="MEDIUM",
                narrative_note=(
                    f"{name} grew by {delta} with no job postings; "
                    "likely internal transfers or contractor-to-FTE conversions."
                ),
            )
        return DepartmentSignal(
            name=name,
            headcount_current=0,
            headcount_delta_90d=delta,
            job_postings_90d=0,
            backfill_ratio=0.0,
            classification="INCONCLUSIVE",
            confidence="LOW",
            narrative_note=(
                f"{name} headcount flat or declining with no postings; "
                "possible hiring freeze or reorg."
            ),
        )

    if delta == 0:
        ratio = float(postings)
    elif delta < 0:
        ratio = postings / max(abs(delta), 1)
    else:
        ratio = postings / delta

    if delta < 0 and postings > 0:
        classification = "BACKFILL_CHURN"
        confidence = "HIGH"
        note = (
            f"CRITICAL: {name} lost {abs(delta)} net heads despite "
            f"{postings} job postings; attrition is overwhelming hiring."
        )
    elif ratio > BACKFILL_RATIO_CRITICAL:
        classification = "BACKFILL_CHURN"
        confidence = "HIGH"
        note = (
            f"{name}: {postings} postings vs only +{delta} net adds. "
            f"Backfill ratio {ratio:.1f}x indicates heavy replacement hiring."
        )
    elif ratio > BACKFILL_RATIO_WARN:
        classification = "BACKFILL_CHURN"
        confidence = "MEDIUM"
        note = (
            f"{name}: elevated backfill ratio ({ratio:.1f}x). "
            "Growth is real but attrition is meaningful."
        )
    else:
        classification = "TRUE_GROWTH"
        confidence = "MEDIUM" if ratio > 0.2 else "HIGH"
        note = (
            f"{name}: healthy growth signal. Backfill ratio {ratio:.1f}x "
            "is within normal range."
        )

    return DepartmentSignal(
        name=name,
        headcount_current=0,
        headcount_delta_90d=delta,
        job_postings_90d=postings,
        backfill_ratio=round(ratio, 2),
        classification=classification,
        confidence=confidence,
        narrative_note=note,
    )


def run(sanitized_payload: dict) -> CompanyChurnProfile:
    print("[Churn Verifier] Analyzing headcount signals...")

    company = sanitized_payload.get("company", {})
    job_postings = sanitized_payload.get("job_postings", [])

    dept_postings: dict[str, int] = {}
    for posting in job_postings:
        dept = posting.get("department", "other").lower().replace(" ", "_")
        dept_postings[dept] = dept_postings.get(dept, 0) + 1

    dept_headcounts = company.get("headcount_by_department", {})

    dept_signals = []
    for dept_name, dept_data in dept_headcounts.items():
        delta = dept_data.get("delta_90d", 0)
        postings = dept_postings.get(dept_name.lower(), 0)
        signal = classify_department(dept_name, delta, postings)
        signal.headcount_current = dept_data.get("headcount", 0)
        dept_signals.append(signal)

    churn_count = sum(1 for s in dept_signals if s.classification == "BACKFILL_CHURN")
    growth_count = sum(1 for s in dept_signals if s.classification == "TRUE_GROWTH")
    total = len(dept_signals) or 1

    churn_ratio = churn_count / total
    growth_ratio = growth_count / total

    if churn_ratio >= 0.5:
        overall = "BACKFILL_CHURN"
        alert = "CRITICAL" if churn_ratio >= 0.7 else "WARN"
    elif growth_ratio >= 0.6:
        overall = "TRUE_GROWTH"
        alert = "CLEAR"
    else:
        overall = "MIXED"
        alert = "WARN"

    churn_summary = " | ".join(s.narrative_note for s in dept_signals)

    print(f"[Churn Verifier] Overall: {overall} (alert={alert})")
    for s in dept_signals:
        print(f"   {s.name}: {s.classification} (ratio={s.backfill_ratio})")

    return CompanyChurnProfile(
        overall_classification=overall,
        departments=dept_signals,
        churn_summary=churn_summary,
        alert_level=alert,
    )
