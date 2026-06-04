import os

from dotenv import load_dotenv

load_dotenv()

CRUSTDATA_API_KEY = os.getenv("CRUSTDATA_API_KEY", "")

# GitHub Models (OpenAI-compatible endpoint)
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
GITHUB_ENDPOINT = os.getenv("GITHUB_ENDPOINT", "https://models.github.ai/inference")
GITHUB_MODEL = os.getenv("GITHUB_MODEL", "openai/gpt-5-nano")
GITHUB_MAX_TOKENS = int(os.getenv("GITHUB_MAX_TOKENS", "1500"))

# Temporary toggle to force mock data while wiring the pipeline
FORCE_MOCK_DATA = os.getenv("FORCE_MOCK_DATA", "false").lower() in {"1", "true", "yes"}

# Helpful warnings to prevent accidental secret leaks or confusion during runs
if not CRUSTDATA_API_KEY:
    print("[config] Warning: CRUSTDATA_API_KEY not set. The fetcher will use mock data.")
if not GITHUB_TOKEN:
    print("[config] Warning: GITHUB_TOKEN not set. The signal compiler will use mock LLM fallback.")

# CrustShield thresholds
CONFIDENCE_THRESHOLD = 0.75
PII_FIELDS = [
    "mobile",
    "mobile_number",
    "phone",
    "personal_phone",
    "personal_email",
    "home_email",
    "home_address",
    "date_of_birth",
    "national_id",
]

# Churn verifier thresholds
BACKFILL_RATIO_WARN = 0.35
BACKFILL_RATIO_CRITICAL = 0.60
