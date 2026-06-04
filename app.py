import asyncio
import logging
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO, format="[%(name)s] %(message)s")
logger = logging.getLogger("truesignal")

BASE_DIR = Path(__file__).parent
INDEX_HTML = BASE_DIR / "templates" / "index.html"

app = FastAPI(title="TrueSignal Intelligence")


class AnalyzeRequest(BaseModel):
    company_name: str


def _run_pipeline(company_name: str) -> dict:

    from fetcher import fetch_all
    import crustshield
    import churn_verifier
    import signal_compiler

    logger.info("Pipeline start: %s", company_name)
    raw_payload = fetch_all(company_name)
    sanitized_payload, shield_log = crustshield.run(raw_payload)
    churn_profile = churn_verifier.run(sanitized_payload)
    card = signal_compiler.run(sanitized_payload, churn_profile, shield_log)

    return {
        "company_name": card.company_name,
        "signal_narrative": card.signal_narrative,
        "ranked_hypotheses": card.ranked_hypotheses,
        "recommended_angle": card.recommended_angle,
        "avoid_angle": card.avoid_angle,
        "churn_alert": card.churn_alert,
        "shield_summary": card.shield_summary,
    }


@app.get("/")
async def index():
    return FileResponse(str(INDEX_HTML), media_type="text/html")


@app.get("/autocomplete")
async def autocomplete(q: str = ""):
    """
    Proxies Crustdata's free /company/search/autocomplete endpoint.
    Falls back to an empty list when credits are exhausted or key is missing.
    """
    if not q.strip():
        return []
    from fetcher import company_autocomplete
    results = await asyncio.to_thread(company_autocomplete, q.strip())
    return results


@app.post("/analyze")
async def analyze(req: AnalyzeRequest):
    company = req.company_name.strip()
    if not company:
        return JSONResponse({"status": "error", "message": "Company name is required."}, status_code=400)
    try:
        result = await asyncio.to_thread(_run_pipeline, company)
        return {"status": "success", "data": result}
    except Exception as exc:
        logger.exception("Pipeline failed for %s", company)
        return JSONResponse({"status": "error", "message": str(exc)}, status_code=500)
