import sys

import crustshield
import churn_verifier
import signal_compiler
from fetcher import fetch_all
from output_formatter import format_card


def run_pipeline(linkedin_url: str) -> None:
    """
    Full TrueSignal pipeline.
    """
    print(f"\n{'=' * 60}")
    print(f"TrueSignal Agent -- {linkedin_url}")
    print(f"{'=' * 60}\n")

    print("[ Stage 1 / 4 ] Fetching Crustdata signals...")
    raw_payload = fetch_all(linkedin_url)

    print("\n[ Stage 2 / 4 ] Running CrustShield PII filter...")
    sanitized_payload, shield_log = crustshield.run(raw_payload)

    print("\n[ Stage 3 / 4 ] Running Churn Verifier...")
    churn_profile = churn_verifier.run(sanitized_payload)

    print("\n[ Stage 4 / 4 ] Compiling Signal Narrative...")
    intelligence_card = signal_compiler.run(sanitized_payload, churn_profile, shield_log)

    print("\n" + "=" * 60)
    print("TRUESIGNAL INTELLIGENCE CARD")
    print("=" * 60)
    format_card(intelligence_card)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py linkedin.com/company/samsara | 'Samsara'")
        sys.exit(1)

    run_pipeline(sys.argv[1])
