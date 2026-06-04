import copy
import re
from dataclasses import dataclass, field
from typing import Any

from config import CONFIDENCE_THRESHOLD, PII_FIELDS

PHONE_PATTERN = re.compile(r"(\+?\d[\d\s\-().]{7,}\d)")
EMAIL_PATTERN = re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}")
PERSONAL_EMAIL_DOMAINS = {
    "gmail.com",
    "yahoo.com",
    "hotmail.com",
    "outlook.com",
    "icloud.com",
    "protonmail.com",
    "me.com",
    "mac.com",
    "live.com",
    "msn.com",
    "aol.com",
}


@dataclass
class ShieldAuditLog:
    contacts_dropped: list[dict] = field(default_factory=list)
    fields_redacted: list[dict] = field(default_factory=list)
    regex_hits: list[dict] = field(default_factory=list)
    total_pii_removed: int = 0

    def summary(self) -> str:
        return (
            f"{len(self.contacts_dropped)} contact(s) dropped | "
            f"{self.total_pii_removed} PII field(s) redacted | "
            f"{len(self.regex_hits)} regex hit(s) in free text"
        )


def is_personal_email(email: str) -> bool:
    domain = email.split("@")[-1].lower()
    return domain in PERSONAL_EMAIL_DOMAINS


def strip_pii_from_value(value: Any, field_name: str, log: ShieldAuditLog, context: str = "") -> Any:
    """
    Recursively processes a value to remove known PII and redact PII found in free text.
    """
    if isinstance(value, dict):
        return {
            k: strip_pii_from_value(v, k, log, context=context)
            for k, v in value.items()
        }

    if isinstance(value, list):
        return [
            strip_pii_from_value(item, field_name, log, context=context)
            for item in value
        ]

    if isinstance(value, str):
        if field_name.lower() in [f.lower() for f in PII_FIELDS]:
            if value.strip():
                log.fields_redacted.append(
                    {"field": field_name, "context": context, "reason": "known_pii_field"}
                )
                log.total_pii_removed += 1
                return "[REDACTED_BY_CRUSTSHIELD]"

        phone_matches = PHONE_PATTERN.findall(value)
        for match in phone_matches:
            log.regex_hits.append(
                {"type": "phone_in_freetext", "field": field_name, "context": context}
            )
            value = value.replace(match, "[PHONE_REDACTED]")

        email_matches = EMAIL_PATTERN.findall(value)
        for match in email_matches:
            hit_type = "personal_email_in_freetext" if is_personal_email(match) else "work_email_in_freetext"
            log.regex_hits.append(
                {"type": hit_type, "field": field_name, "context": context}
            )
            value = value.replace(match, "[EMAIL_REDACTED]")

        return value

    return value


def filter_low_confidence_contacts(
    contacts: list[dict],
    log: ShieldAuditLog,
    threshold: float = CONFIDENCE_THRESHOLD,
) -> list[dict]:
    clean = []
    for contact in contacts:
        score = contact.get("confidence_score", 0) or 0
        if score < threshold:
            log.contacts_dropped.append(
                {
                    "full_name": contact.get("full_name", "unknown"),
                    "confidence_score": score,
                }
            )
            continue
        clean.append(contact)
    return clean


def run(raw_payload: dict) -> tuple[dict, ShieldAuditLog]:
    """
    Main CrustShield entry point.
    Returns sanitized payload + audit log.
    """
    log = ShieldAuditLog()
    payload = copy.deepcopy(raw_payload)

    print("[CrustShield] Starting PII scan...")

    payload["contacts"] = filter_low_confidence_contacts(
        payload.get("contacts", []), log
    )

    sanitized_contacts = []
    for contact in payload.get("contacts", []):
        sanitized = strip_pii_from_value(
            contact,
            field_name="contact",
            log=log,
            context=contact.get("full_name", "unknown"),
        )
        sanitized_contacts.append(sanitized)
    payload["contacts"] = sanitized_contacts

    for key in ["company", "job_postings", "recent_posts"]:
        if key in payload:
            payload[key] = strip_pii_from_value(payload[key], field_name=key, log=log, context=key)

    print(f"[CrustShield] Complete. {log.summary()}")
    return payload, log
