from signal_compiler import IntelligenceCard


def format_card(card: IntelligenceCard) -> None:
    """
    Terminal output formatter.
    """
    alert_colors = {
        "CLEAR": "\033[92m",
        "WARN": "\033[93m",
        "CRITICAL": "\033[91m",
    }
    reset = "\033[0m"
    bold = "\033[1m"

    alert_color = alert_colors.get(card.churn_alert, "")

    print(f"\n{bold}Company:{reset} {card.company_name}")
    print(f"{bold}Churn Alert:{reset} {alert_color}{card.churn_alert}{reset}")
    print(f"{bold}CrustShield:{reset} {card.shield_summary}")

    print(f"\n{bold}-- SIGNAL NARRATIVE --{reset}")
    print(card.signal_narrative)

    print(f"\n{bold}-- RANKED HYPOTHESES --{reset}")
    for hypothesis in card.ranked_hypotheses:
        conf = hypothesis.get("confidence", "LOW")
        conf_color = (
            "\033[92m" if conf == "HIGH" else "\033[93m" if conf == "MEDIUM" else "\033[91m"
        )
        print(f"\n  {bold}{hypothesis.get('rank', '')}{reset} [{conf_color}{conf}{reset}]")
        print(f"  {hypothesis.get('hypothesis', '')}")
        print(f"  Evidence: {hypothesis.get('evidence', '')}")

    print(f"\n{bold}-- RECOMMENDED ANGLE --{reset}")
    print(f"  [+] {card.recommended_angle}")

    print(f"\n{bold}-- AVOID --{reset}")
    print(f"  [-] {card.avoid_angle}")
    print()
