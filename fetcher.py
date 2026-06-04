from __future__ import annotations

from typing import Any, Dict, List, Tuple

import requests
import time

from config import CRUSTDATA_API_KEY, FORCE_MOCK_DATA

BASE_URL = "https://api.crustdata.com"
API_VERSION = "2025-11-01"

HEADERS = {
    "Authorization": f"Bearer {CRUSTDATA_API_KEY}",
    "Content-Type": "application/json",
    "Accept": "application/json",
    "x-api-version": API_VERSION,
}

COMPANY_ENRICH_ENDPOINT = f"{BASE_URL}/company/enrich"
COMPANY_IDENTIFY_ENDPOINT = f"{BASE_URL}/company/identify"
COMPANY_SEARCH_AUTOCOMPLETE_ENDPOINT = f"{BASE_URL}/company/search/autocomplete"
PERSON_SEARCH_ENDPOINT = f"{BASE_URL}/person/search"
PERSON_LIVE_SEARCH_ENDPOINT = f"{BASE_URL}/person/professional_network/search/live"
JOB_SEARCH_ENDPOINT = f"{BASE_URL}/job/search"
SOCIAL_POST_SEARCH_ENDPOINT = f"{BASE_URL}/social_post/professional_network/search/live"


def _normalize_company_profile_url(linkedin_url: str) -> str:
    if linkedin_url.startswith("http://") or linkedin_url.startswith("https://"):
        return linkedin_url.rstrip("/")

    if "/company/" in linkedin_url:
        slug = linkedin_url.split("/company/", 1)[1].strip("/")
    else:
        slug = linkedin_url.strip("/").replace("linkedin.com/", "")

    return f"https://www.linkedin.com/company/{slug}"


def _looks_like_url(value: str) -> bool:
    return value.startswith("http://") or value.startswith("https://") or "linkedin.com/" in value


def _company_name_from_linkedin_url(linkedin_url: str) -> str:
    slug = linkedin_url.rstrip("/").split("/company/", 1)[-1]
    slug = slug.split("/", 1)[0].strip()
    if not slug:
        return "Unknown"

    parts = [part for part in slug.replace("-", " ").replace("_", " ").split(" ") if part]
    return " ".join(part.capitalize() for part in parts) if parts else slug.capitalize()


def _first_present(mapping: Dict[str, Any], *keys: str) -> Any:
    for key in keys:
        value = mapping.get(key)
        if value not in (None, "", [], {}, ()):
            return value
    return None


def _is_error_response(data: Any) -> bool:
    return isinstance(data, dict) and "error" in data and len(data) <= 3


def _as_list(value: Any) -> List[Any]:
    if isinstance(value, list):
        return value
    if value in (None, ""):
        return []
    return [value]


def _rows_from_tabular_response(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    columns = data.get("columns")
    rows = data.get("data") or data.get("rows")
    if not isinstance(columns, list) or not isinstance(rows, list):
        return []

    normalized_rows: List[Dict[str, Any]] = []
    for row in rows:
        if isinstance(row, dict):
            normalized_rows.append(row)
            continue
        if isinstance(row, list):
            normalized_rows.append({str(column): row[index] if index < len(row) else None for index, column in enumerate(columns)})
    return normalized_rows


def _extract_collection(data: Any) -> List[Dict[str, Any]]:
    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]

    if not isinstance(data, dict) or _is_error_response(data):
        return []

    for key in ("records", "results", "items", "data", "rows", "people", "jobs", "job_listings", "posts", "companies", "profiles"):
        value = data.get(key)
        if isinstance(value, list):
            return [item for item in value if isinstance(item, dict)]

    tabular_rows = _rows_from_tabular_response(data)
    if tabular_rows:
        return tabular_rows

    return [data] if any(key not in {"available_fields", "matched_on", "match_type", "matches", "count"} for key in data.keys()) else []


def _coerce_department_map(value: Any) -> Dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _coerce_recent_funding(value: Any) -> Dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _make_filter_variants(company_id: Any, extra_filters: Dict[str, Any] | None = None) -> List[Dict[str, Any]]:
    extra_filters = extra_filters or {}
    dict_filters = {"company_id": company_id, **extra_filters}

    list_filters = [{"field": "company_id", "operator": "=", "value": company_id}]
    for field, value in extra_filters.items():
        operator = "in" if isinstance(value, list) else "="
        list_filters.append({"field": field, "operator": operator, "value": value})

    eq_filters = [{"field": "company_id", "op": "eq", "value": company_id}]
    for field, value in extra_filters.items():
        operator = "in" if isinstance(value, list) else "eq"
        eq_filters.append({"field": field, "op": operator, "value": value})

    return [dict_filters, list_filters, eq_filters]


def _flatten_company_profile(data: Any, fallback_name: str) -> Dict[str, Any]:
    if not isinstance(data, dict):
        return {}

    source: Dict[str, Any] = data
    matches = data.get("matches")
    if isinstance(matches, list) and matches:
        first_match = matches[0]
        if isinstance(first_match, dict):
            company_data = first_match.get("company_data")
            if isinstance(company_data, dict):
                source = company_data

    basic_info = source.get("basic_info") if isinstance(source.get("basic_info"), dict) else {}
    merged: Dict[str, Any] = {**basic_info, **data}
    merged.update(source)

    industry = _first_present(merged, "industry", "industries")
    if isinstance(industry, list):
        industry = ", ".join(str(item) for item in industry if item)

    company_name = _first_present(
        merged,
        "company_name",
        "name",
        "display_name",
        "legal_name",
    )
    if not company_name and isinstance(basic_info, dict):
        company_name = _first_present(basic_info, "company_name", "name")
    if not company_name:
        company_name = fallback_name
    if company_name == fallback_name and isinstance(source, dict):
        company_name = _first_present(source, "profile_name", "name") or company_name

    company_id = _first_present(
        merged,
        "crustdata_company_id",
        "company_id",
        "id",
    )
    if not company_id and isinstance(basic_info, dict):
        company_id = _first_present(basic_info, "crustdata_company_id", "company_id", "id")
    if not company_id and isinstance(source, dict):
        company_id = _first_present(source, "crustdata_company_id", "company_id", "id")

    headcount = _first_present(
        merged,
        "headcount",
        "employee_count",
        "employees",
    )
    if isinstance(headcount, str) and headcount.isdigit():
        headcount = int(headcount)

    headcount_delta_90d = _first_present(merged, "headcount_delta_90d", "employee_count_change_90d", "net_headcount_change_90d")
    if isinstance(headcount_delta_90d, str) and headcount_delta_90d.lstrip("+-").isdigit():
        headcount_delta_90d = int(headcount_delta_90d)

    hq_location = _first_present(merged, "hq_location", "headquarters", "location")

    normalized = {
        "company_name": company_name,
        "company_id": company_id,
        "crustdata_company_id": company_id,
        "professional_network_url": _first_present(basic_info, "professional_network_url") or _first_present(source, "professional_network_url"),
        "headcount": headcount,
        "headcount_delta_90d": headcount_delta_90d,
        "headcount_by_department": _coerce_department_map(
            _first_present(merged, "headcount_by_department", "department_headcounts")
        ),
        "funding_stage": _first_present(merged, "funding_stage", "stage"),
        "recent_funding": _coerce_recent_funding(_first_present(merged, "recent_funding", "last_funding")),
        "description": _first_present(merged, "description", "summary"),
        "industry": industry,
        "hq_location": hq_location,
        "glassdoor_overall_rating": _first_present(merged, "glassdoor_overall_rating"),
        "glassdoor_trend": _first_present(merged, "glassdoor_trend"),
        "web_traffic_trend": _first_present(merged, "web_traffic_trend"),
    }

    for key, value in data.items():
        if key not in normalized and key != "basic_info":
            normalized[key] = value

    return normalized


def _extract_first_record(data: Any) -> Dict[str, Any]:
    if isinstance(data, list):
        return next((item for item in data if isinstance(item, dict)), {})

    if isinstance(data, dict):
        if _is_error_response(data):
            return {}

        for key in ("records", "results", "items", "data", "rows", "people", "jobs", "job_listings", "posts", "companies", "profiles"):
            value = data.get(key)
            if isinstance(value, list) and value:
                return next((item for item in value if isinstance(item, dict)), {})

        tabular_rows = _rows_from_tabular_response(data)
        if tabular_rows:
            return tabular_rows[0]

        if any(key not in {"available_fields", "matched_on", "match_type", "matches", "count"} for key in data.keys()):
            return data

    return {}


def _extract_records(data: Any) -> List[Dict[str, Any]]:
    return _extract_collection(data)


def _records_from_response(data: Any) -> List[Dict[str, Any]]:
    return _extract_collection(data)


def _extract_urls(profile: Dict[str, Any]) -> List[str]:
    urls: List[str] = []
    for key in ("linkedin_url", "profile_url", "url"):
        value = profile.get(key)
        if isinstance(value, str) and value.strip():
            urls.append(value.strip())
    return urls


def _extract_person_data_list_from_enrich_response(data: Any) -> List[Dict[str, Any]]:
    return _extract_collection(data)


def _extract_company_data_from_enrich_response(data: Any) -> Dict[str, Any]:
    return _extract_first_record(data)


def _extract_company_identifiers(company: Dict[str, Any], fallback_profile_url: str) -> List[str]:
    identifiers: List[str] = []
    for value in (
        company.get("crustdata_company_id"),
        company.get("company_id"),
        company.get("id"),
        company.get("professional_network_url"),
        fallback_profile_url,
    ):
        if value in (None, "", [], {}, ()):
            continue
        if isinstance(value, str):
            identifiers.append(value)
        else:
            identifiers.append(str(value))

    deduped: List[str] = []
    for identifier in identifiers:
        if identifier not in deduped:
            deduped.append(identifier)
    return deduped


def _extract_company_name_hint(company: Dict[str, Any], fallback_linkedin_url: str) -> str:
    for key in ("company_name", "name", "profile_name"):
        value = company.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()

    basic_info = company.get("basic_info") if isinstance(company.get("basic_info"), dict) else {}
    for key in ("company_name", "name", "profile_name"):
        value = basic_info.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()

    return _company_name_from_linkedin_url(fallback_linkedin_url)


def _name_from_identifiers(identifiers: List[str]) -> str:
    for identifier in identifiers:
        if not isinstance(identifier, str):
            continue
        trimmed = identifier.strip()
        if not trimmed or trimmed.startswith("http") or trimmed.isdigit():
            continue
        return trimmed
    return ""


def _build_search_group(*conditions: Dict[str, Any]) -> Dict[str, Any]:
    return {"op": "and", "conditions": list(conditions)} if len(conditions) > 1 else conditions[0]


def _normalize_person_record(profile: Dict[str, Any]) -> Dict[str, Any]:
    basic_profile = profile.get("basic_profile") if isinstance(profile.get("basic_profile"), dict) else {}
    experience = profile.get("experience") if isinstance(profile.get("experience"), dict) else {}
    current = {}
    if isinstance(experience.get("employment_details"), dict):
        current_details = experience["employment_details"].get("current")
        if isinstance(current_details, dict):
            current = current_details

    social_handles = profile.get("social_handles") if isinstance(profile.get("social_handles"), dict) else {}
    professional_network = profile.get("professional_network") if isinstance(profile.get("professional_network"), dict) else {}
    contact = profile.get("contact") if isinstance(profile.get("contact"), dict) else {}

    full_name = _first_present(basic_profile, "name", "professional_network_name") or "Unknown"
    title = _first_present(basic_profile, "current_title", "headline") or _first_present(current, "title") or "Unknown"
    seniority_level = _first_present(current, "seniority_level")
    linkedin_url = _first_present(
        social_handles,
        "professional_network_identifier.profile_url",
        "professional_network_identifier.url",
    )
    if not linkedin_url and isinstance(social_handles.get("professional_network_identifier"), dict):
        linkedin_url = _first_present(social_handles["professional_network_identifier"], "profile_url", "url")

    contact_flags = [
        bool(contact.get("has_business_email")),
        bool(contact.get("has_personal_email")),
        bool(contact.get("has_phone_number")),
    ]
    confidence_score = round(0.55 + 0.15 * sum(contact_flags), 2)

    return {
        "full_name": full_name,
        "title": title,
        "seniority_level": seniority_level,
        "work_email": None,
        "personal_email": None,
        "mobile_number": None,
        "linkedin_url": linkedin_url,
        "confidence_score": confidence_score,
        "last_updated": _first_present(basic_profile, "last_updated") or _first_present(profile, "metadata.updated_at"),
        "source_profile": profile,
        "followers": professional_network.get("followers"),
        "has_business_email": contact.get("has_business_email"),
    }


def _normalize_job_record(job: Dict[str, Any]) -> Dict[str, Any]:
    job_details = job.get("job_details") if isinstance(job.get("job_details"), dict) else {}
    location = job.get("location") if isinstance(job.get("location"), dict) else {}
    metadata = job.get("metadata") if isinstance(job.get("metadata"), dict) else {}

    title = _first_present(job_details, "title", "job_title") or "Unknown"
    department = _infer_department_from_title(str(title))
    return {
        "job_title": title,
        "department": department,
        "location": _first_present(location, "raw", "city", "state", "country") or "Unknown",
        "date_posted": _first_present(metadata, "date_added", "date_updated") or "",
        "is_new_role": True,
        "source_job": job,
    }


def _normalize_post_record(post: Dict[str, Any]) -> Dict[str, Any]:
    content = _first_present(post, "content", "text", "description") or ""
    if isinstance(content, dict):
        content = _first_present(content, "description", "text") or ""
    author = post.get("author") if isinstance(post.get("author"), dict) else {}
    return {
        "author_name": _first_present(post, "author_name") or _first_present(author, "name") or "Unknown",
        "author_title": _first_present(post, "author_title") or _first_present(author, "title") or "",
        "content": content,
        "posted_date": _first_present(post, "posted_date", "date_posted", "metadata.date_added") or "",
        "engagement_rate": _first_present(post, "engagement_rate") or 0,
        "source_post": post,
    }


def _post_json(endpoint: str, payload: Dict[str, Any]) -> requests.Response:
    return requests.post(endpoint, headers=HEADERS, json=payload, timeout=30)


def _first_successful_json(endpoint_candidates: List[Tuple[str, Dict[str, Any]]]) -> tuple[Any, requests.Response | None]:
    last_response: requests.Response | None = None

    for endpoint, payload in endpoint_candidates:
        for attempt in range(3):
            try:
                response = _post_json(endpoint, payload)
                last_response = response
                if response.status_code == 200:
                    return response.json(), response

                try:
                    import json as _json
                    payload_snip = _json.dumps(payload, default=str)[:1000]
                except Exception:
                    payload_snip = str(payload)
                print(f"[Fetcher] {endpoint} returned {response.status_code}: {response.text[:500]}")
                print(f"[Fetcher] Payload: {payload_snip}")
                if response.status_code >= 500:
                    time.sleep(1 + attempt)
                    continue
                break
            except requests.RequestException as exc:
                print(f"[Fetcher] {endpoint} request failed: {exc}")
                if attempt < 2:
                    time.sleep(1 + attempt)
                    continue
                break

    return {}, last_response


def _infer_department_from_title(title: str) -> str:
    text = title.lower()
    if any(token in text for token in ("sales", "account executive", "ae", "account manager")):
        return "sales"
    if any(token in text for token in ("data", "analytics", "bi", "warehouse")):
        return "data_engineering"
    if any(token in text for token in ("engineer", "engineering", "backend", "frontend", "platform")):
        return "engineering"
    if any(token in text for token in ("marketing", "growth", "demand gen", "brand")):
        return "marketing"
    return "other"


def company_autocomplete(query: str, limit: int = 8) -> List[Dict[str, Any]]:
    """
    Free endpoint — returns matching company suggestions for typeahead UIs.
    Returns list of {name, domain, linkedin_url} dicts (best-effort).
    """
    if not CRUSTDATA_API_KEY or not query.strip():
        return []
    try:
        resp = requests.get(
            COMPANY_SEARCH_AUTOCOMPLETE_ENDPOINT,
            headers=HEADERS,
            params={"query": query.strip(), "limit": limit},
            timeout=5,
        )
        if resp.status_code != 200:
            return []
        data = resp.json()
        results = data if isinstance(data, list) else data.get("results", data.get("companies", []))
        out = []
        for item in results[:limit]:
            out.append({
                "name": item.get("name") or item.get("company_name") or "",
                "domain": item.get("domain") or item.get("primary_domain") or "",
                "linkedin_url": item.get("linkedin_url") or item.get("professional_network_url") or "",
            })
        return out
    except Exception:
        return []


def fetch_company_profile(linkedin_url: str) -> Dict[str, Any]:
    if _looks_like_url(linkedin_url) or "/company/" in linkedin_url:
        profile_url = _normalize_company_profile_url(linkedin_url)
        company_name_guess = _company_name_from_linkedin_url(linkedin_url)
        candidates = [
            # /company/identify is FREE — try it first for plain names and URLs
            (COMPANY_IDENTIFY_ENDPOINT, {"professional_network_profile_urls": [profile_url]}),
            (COMPANY_IDENTIFY_ENDPOINT, {"names": [company_name_guess]}),
            (COMPANY_ENRICH_ENDPOINT, {"professional_network_profile_urls": [profile_url]}),
            (COMPANY_ENRICH_ENDPOINT, {"names": [company_name_guess]}),
        ]
    else:
        profile_url = None
        company_name_guess = linkedin_url.strip()
        candidates = [
            # /company/identify is FREE — always try it first
            (COMPANY_IDENTIFY_ENDPOINT, {"names": [company_name_guess]}),
            (COMPANY_ENRICH_ENDPOINT, {"names": [company_name_guess]}),
        ]

    try:
        data, response = _first_successful_json(candidates)

        if not data and response is not None:
            try:
                info = response.json()
            except Exception:
                info = {}

            if isinstance(info, dict):
                available = info.get("available_fields", [])
                if isinstance(available, list):
                    subset = ["basic_info"] if "basic_info" in available else []
                    if subset:
                        print(f"[Fetcher] Adjusting company fields to available subset: {subset}")
                    retry_candidates = [(COMPANY_ENRICH_ENDPOINT, {"names": [company_name_guess], "fields": subset})]
                    if profile_url:
                        retry_candidates.insert(0, (COMPANY_ENRICH_ENDPOINT, {"professional_network_profile_urls": [profile_url], "fields": subset}))
                    data, _ = _first_successful_json(retry_candidates)

        flattened = _flatten_company_profile(_extract_first_record(data), company_name_guess)
        if flattened:
            return flattened
        return _extract_first_record(data)
    except requests.RequestException as exc:
        print(f"[Fetcher] Company profile fetch failed: {exc}")
        return {}


def fetch_key_contacts(company_id: str, limit: int = 5) -> List[Dict[str, Any]]:
    fields = [
        "full_name",
        "title",
        "seniority_level",
        "work_email",
        "personal_email",
        "mobile_number",
        "linkedin_url",
        "confidence_score",
        "last_updated",
    ]

    identifiers = _as_list(company_id)
    if not identifiers:
        return []

    company_name = _name_from_identifiers(identifiers)
    company_profile_url = next((value for value in identifiers if isinstance(value, str) and value.startswith("http")), None)
    if not company_name:
        company_name = str(identifiers[0])

    title_filter = {
        "op": "or",
        "conditions": [
            {"field": "experience.employment_details.current.title", "type": "(.)", "value": "VP|Director|Head|Chief"},
            {"field": "experience.employment_details.title", "type": "(.)", "value": "VP|Director|Head|Chief"},
        ],
    }

    payloads: List[Dict[str, Any]] = []
    if company_profile_url:
        payloads.append(
            {
                "filters": _build_search_group({"field": "experience.employment_details.current.company_professional_network_profile_url", "type": "=", "value": company_profile_url}, title_filter),
                "fields": ["basic_profile", "experience", "professional_network", "social_handles", "contact"],
                "limit": limit,
            }
        )
        payloads.append(
            {
                "filters": _build_search_group({"field": "experience.employment_details.past.company_professional_network_profile_url", "type": "=", "value": company_profile_url}, title_filter),
                "fields": ["basic_profile", "experience", "professional_network", "social_handles", "contact"],
                "limit": limit,
            }
        )
        payloads.append(
            {
                "filters": {"field": "experience.employment_details.current.company_professional_network_profile_url", "type": "=", "value": company_profile_url},
                "fields": ["basic_profile", "experience", "professional_network", "social_handles", "contact"],
                "limit": limit,
            }
        )

    payloads.append(
        {
            "filters": _build_search_group(
                {"field": "experience.employment_details.company_name", "type": "in", "value": [company_name]},
                title_filter,
            ),
            "fields": ["basic_profile", "experience", "professional_network", "social_handles", "contact"],
            "limit": limit,
        }
    )
    payloads.append(
        {
            "filters": _build_search_group(
                {"field": "experience.employment_details.current.company_name", "type": "in", "value": [company_name]},
                title_filter,
            ),
            "fields": ["basic_profile", "experience", "professional_network", "social_handles", "contact"],
            "limit": limit,
        }
    )
    payloads.append(
        {
            "filters": {"field": "experience.employment_details.current.company_name", "type": "=", "value": company_name},
            "fields": ["basic_profile", "experience", "professional_network", "social_handles", "contact"],
            "limit": limit,
        }
    )

    try:
        data, response = _first_successful_json(
            [(PERSON_SEARCH_ENDPOINT, payload) for payload in payloads]
        )

        if not data and response is not None:
            try:
                info = response.json()
            except Exception:
                info = {}

            if isinstance(info, dict):
                available = info.get("available_fields", [])
                if isinstance(available, list):
                    subset = [field for field in fields if field in available]
                    if subset:
                        print(f"[Fetcher] Adjusting contact fields to available subset: {subset}")
                        data, _ = _first_successful_json(
                            [(PERSON_SEARCH_ENDPOINT, {"filters": payload["filters"], "fields": subset, "limit": limit}) for payload in payloads[:2]]
                        )

        records = _extract_records(data)
        if not records:
            return []
        return [_normalize_person_record(profile) for profile in records]
    except requests.RequestException as exc:
        print(f"[Fetcher] Contacts fetch failed: {exc}")
        return []


def fetch_job_postings(company_id: str, days_back: int = 90) -> List[Dict[str, Any]]:
    fields = ["job_title", "department", "location", "date_posted", "is_new_role"]
    identifiers = _as_list(company_id)
    if not identifiers:
        return []

    company_id_value = identifiers[0]
    company_profile_url = next((value for value in identifiers if isinstance(value, str) and value.startswith("http")), None)
    company_name = _name_from_identifiers(identifiers) or (
        _company_name_from_linkedin_url(company_profile_url) if isinstance(company_profile_url, str) else str(company_id_value)
    )

    payloads: List[Dict[str, Any]] = []
    if isinstance(company_id_value, int) or (isinstance(company_id_value, str) and company_id_value.isdigit()):
        payloads.append(
            {
                "filters": {"field": "company.basic_info.crustdata_company_id", "type": "=", "value": int(company_id_value)},
                "fields": ["job_details.title"],
                "limit": 1,
            }
        )
    if isinstance(company_id_value, int) or (isinstance(company_id_value, str) and company_id_value.isdigit()):
        payloads.append(
            {
                "filters": _build_search_group(
                    {"field": "company.basic_info.crustdata_company_id", "type": "=", "value": int(company_id_value)},
                    {"field": "metadata.date_added", "type": "=>", "value": f"-{days_back}d"},
                ),
                "fields": [
                    "job_details.title",
                    "job_details.url",
                    "company.basic_info.name",
                    "company.basic_info.crustdata_company_id",
                    "company.basic_info.primary_domain",
                    "company.basic_info.professional_network_id",
                    "company.basic_info.website",
                    "location.raw",
                    "metadata.date_added",
                ],
                "sorts": [{"field": "metadata.date_added", "order": "desc"}],
                "limit": min(100, 20),
            }
        )

    payloads.append(
        {
            "filters": _build_search_group(
                    {"field": "company.basic_info.name", "type": "=", "value": company_name},
                    {"field": "metadata.date_added", "type": "=>", "value": f"-{days_back}d"},
            ),
            "fields": [
                "job_details.title",
                "job_details.url",
                "company.basic_info.name",
                "company.basic_info.crustdata_company_id",
                "company.basic_info.primary_domain",
                "company.basic_info.professional_network_id",
                "company.basic_info.website",
                "location.raw",
                "metadata.date_added",
            ],
            "sorts": [{"field": "metadata.date_added", "order": "desc"}],
            "limit": min(100, 20),
        }
    )

    try:
        data, response = _first_successful_json(
            [(JOB_SEARCH_ENDPOINT, payload) for payload in payloads]
        )

        if response is not None and response.status_code >= 500:
            print("[Fetcher] Job search returned server error; skipping jobs for now.")
            try:
                import json

                print("[Fetcher] Job search payloads attempted:")
                for p in payloads:
                    try:
                        print(json.dumps(p, default=str)[:1000])
                    except Exception:
                        print(str(p))
            except Exception:
                pass
            return []

        if not data and response is not None:
            try:
                info = response.json()
            except Exception:
                info = {}

            if isinstance(info, dict):
                available = info.get("available_fields", [])
                if isinstance(available, list):
                    subset = [field for field in fields if field in available]
                    if subset:
                        print(f"[Fetcher] Adjusting job fields to available subset: {subset}")
                        data, _ = _first_successful_json(
                            [(JOB_SEARCH_ENDPOINT, {"filters": payload["filters"], "fields": subset, "sorts": payload.get("sorts", []), "limit": payload.get("limit", 20)}) for payload in payloads]
                        )

        rows = _extract_records(data)
        if not rows:
            return []
        return [_normalize_job_record(job) for job in rows]
    except requests.RequestException as exc:
        print(f"[Fetcher] Job postings fetch failed: {exc}")
        return []


def fetch_recent_posts(company_id: str, limit: int = 10) -> List[Dict[str, Any]]:
    fields = ["author_name", "author_title", "content", "posted_date", "engagement_rate"]
    identifiers = _as_list(company_id)
    if not identifiers:
        return []

    company_id_value = identifiers[0]
    company_profile_url = next((value for value in identifiers if isinstance(value, str) and value.startswith("http")), None)
    company_name = _name_from_identifiers(identifiers) or (
        _company_name_from_linkedin_url(company_profile_url) if isinstance(company_profile_url, str) else str(company_id_value)
    )

    filter_type_payloads: List[Dict[str, Any]] = []
    field_payloads: List[Dict[str, Any]] = []
    if company_name:
        filter_type_payloads.append(
            {
                "filters": [{"field": "COMPANY", "value": company_name}],
                "limit": limit,
            }
        )
        filter_type_payloads.append(
            {
                "filters": [{"field": "AUTHOR_COMPANY", "value": company_name}],
                "limit": limit,
            }
        )
        field_payloads.append(
            {
                "filters": [{"field": "company.basic_info.name", "type": "=", "value": company_name}],
                "limit": limit,
            }
        )
        field_payloads.append(
            {
                "filters": [{"field": "company.basic_info.name", "type": "(.)", "value": company_name}],
                "limit": limit,
            }
        )

    if isinstance(company_profile_url, str):
        filter_type_payloads.append(
            {
                "filters": [{"field": "COMPANY", "value": company_profile_url}],
                "limit": limit,
            }
        )
        field_payloads.append(
            {
                "filters": [{"field": "company.basic_info.company_professional_network_profile_url", "type": "=", "value": company_profile_url}],
                "limit": limit,
            }
        )
        field_payloads.append(
            {
                "filters": [{"field": "company.basic_info.company_linkedin_profile_url", "type": "=", "value": company_profile_url}],
                "limit": limit,
            }
        )

    try:
        data, response = _first_successful_json(
            [(SOCIAL_POST_SEARCH_ENDPOINT, payload) for payload in field_payloads]
        )

        if not data and response is not None:
            try:
                info = response.json()
            except Exception:
                info = {}

            if isinstance(info, dict):
                error = info.get("error")
                if isinstance(error, dict):
                    message = str(error.get("message", ""))
                    if "Expected a list" in message:
                        retry_payloads = []
                        for payload in field_payloads:
                            filters_value = payload.get("filters")
                            if isinstance(filters_value, dict):
                                retry_payloads.append({**payload, "filters": [filters_value]})
                        if retry_payloads:
                            data, _ = _first_successful_json(
                                [(SOCIAL_POST_SEARCH_ENDPOINT, payload) for payload in retry_payloads]
                            )

                    if "filter_type" in message and "not supported" in message:
                        print("[Fetcher] Social posts require field-based filters; skipping filter_type variants.")
                    elif "Invalid filter_type" in message:
                        data, _ = _first_successful_json(
                            [(SOCIAL_POST_SEARCH_ENDPOINT, payload) for payload in filter_type_payloads]
                        )

                if isinstance(error, dict) and "Expected a list" in str(error.get("message")):
                    retry_payloads = []
                    for payload in field_payloads:
                        filters_value = payload.get("filters")
                        if isinstance(filters_value, dict):
                            retry_payloads.append({**payload, "filters": [filters_value]})
                    if retry_payloads:
                        data, _ = _first_successful_json(
                            [(SOCIAL_POST_SEARCH_ENDPOINT, payload) for payload in retry_payloads]
                        )

                available = info.get("available_fields", [])
                if isinstance(available, list):
                    subset = [field for field in fields if field in available]
                    if subset:
                        print(f"[Fetcher] Adjusting posts fields to available subset: {subset}")
                        active_payloads = field_payloads or filter_type_payloads
                        data, _ = _first_successful_json(
                            [(SOCIAL_POST_SEARCH_ENDPOINT, {"filters": payload["filters"], "fields": subset, "limit": limit}) for payload in active_payloads[:2]]
                        )

        rows = _extract_records(data)
        if not rows:
            return []
        return [_normalize_post_record(post) for post in rows]
    except requests.RequestException as exc:
        if isinstance(exc.response, requests.Response) and exc.response.status_code == 403:
            print("[Fetcher] Social posts endpoint is permission-gated for this key; skipping.")
        print(f"[Fetcher] Recent posts fetch failed: {exc}")
        return []



def _get_mock(company_name: str) -> Dict[str, Any]:
    from mock_data import get_mock_payload
    payload = get_mock_payload(company_name)
    contacts = payload.get("contacts", [])
    jobs = payload.get("job_postings", [])
    posts = payload.get("recent_posts", [])
    print(f"[Fetcher] Mock data loaded for '{payload['company']['company_name']}': "
          f"{len(contacts)} contacts, {len(jobs)} job postings, {len(posts)} posts")
    return payload


def fetch_all(company_input: str) -> Dict[str, Any]:
    # Derive a plain company name for mock lookup
    if "/company/" in company_input:
        company_name_hint = _company_name_from_linkedin_url(company_input)
    else:
        company_name_hint = company_input.strip()

    if FORCE_MOCK_DATA:
        print("[Fetcher] FORCE_MOCK_DATA enabled — using replica data.")
        return _get_mock(company_name_hint)

    if not CRUSTDATA_API_KEY:
        print("[Fetcher] Missing CRUSTDATA_API_KEY — using replica data.")
        return _get_mock(company_name_hint)

    print(f"[Fetcher] Pulling Crustdata profile for: {company_input}")

    try:
        company = fetch_company_profile(company_input)
        company_id = company.get("crustdata_company_id") or company.get("company_id") or company.get("id")
        company_profile_url = company.get("professional_network_url")
        if not company_profile_url and _looks_like_url(company_input):
            company_profile_url = _normalize_company_profile_url(company_input)
        company_name = _extract_company_name_hint(company, company_input)

        if not company_id:
            raise ValueError("Could not resolve company_id from Crustdata response")

        print(f"[Fetcher] Resolved live company_id: {company_id}")

        identifiers = [company_id, company_name]
        if company_profile_url:
            identifiers.insert(1, company_profile_url)

        contacts = fetch_key_contacts(identifiers)
        job_postings = fetch_job_postings(identifiers)
        posts = fetch_recent_posts(identifiers)

        raw_payload = {
            "company": company,
            "contacts": contacts,
            "job_postings": job_postings,
            "recent_posts": posts,
        }

        print(
            f"[Fetcher] Got: {len(contacts)} contacts, {len(job_postings)} job postings, {len(posts)} recent posts"
        )

        return raw_payload

    except (requests.RequestException, ValueError) as exc:
        print(f"[Fetcher] API error: {exc} — falling back to replica data.")
        return _get_mock(company_name_hint)
