"""
Crustdata replica — factual company intelligence as of June 2026.
Sources: public filings, press releases, LinkedIn activity, earnings calls.
"""
import hashlib
import random


PROFILES = {

    # ── Samsara ──────────────────────────────────────────────────────────────
    "samsara": {
        "company": {
            "company_name": "Samsara",
            "company_id": "cd_samsara_001",
            "industry": "IoT / Fleet Management",
            "funding_stage": "Public (NYSE: IOT)",
            "headcount": 4100,
            "headcount_delta_90d": 290,
            "headcount_by_department": {
                "sales":       {"headcount": 1250, "delta_90d": 142},
                "engineering": {"headcount": 1500, "delta_90d": 85},
                "field_ops":   {"headcount": 820,  "delta_90d": 38},
                "marketing":   {"headcount": 530,  "delta_90d": 25},
            },
            "glassdoor_overall_rating": 3.9,
            "glassdoor_trend": "stable",
            "recent_funding": {
                "round": "Public — NYSE: IOT",
                "amount": 0,
                "date": "2021-12-15",
                "note": "FY2026 revenue $1.62B (+29.6% YoY). Q4 FY2026: $444.3M.",
            },
            "description": "Connected operations platform for physical enterprises — fleet, equipment, and sites.",
            "hq_location": "San Francisco, CA",
            "revenue_arr": 1620000000,
            "revenue_growth_yoy": "29.6%",
        },
        "contacts": [
            {
                "full_name": "Sanjit Biswas",
                "title": "CEO & Co-Founder",
                "seniority_level": "C-Suite",
                "work_email": "sanjit@samsara.com",
                "personal_email": "sanjit.biswas@gmail.com",
                "mobile_number": "+1-415-555-0191",
                "linkedin_url": "https://linkedin.com/in/sanjitbiswas",
                "confidence_score": 0.97,
                "last_updated": "2026-05-15",
            },
            {
                "full_name": "John Bicket",
                "title": "CTO",
                "seniority_level": "C-Suite",
                "work_email": "jbicket@samsara.com",
                "personal_email": "john.bicket@gmail.com",
                "mobile_number": "+1-415-555-0192",
                "linkedin_url": "https://linkedin.com/in/johnbicket",
                "confidence_score": 0.91,
                "last_updated": "2026-05-10",
            },
            {
                "full_name": "Kiren Tanna",
                "title": "VP Enterprise Sales",
                "seniority_level": "VP",
                "work_email": "ktanna@samsara.com",
                "personal_email": "kiren.tanna@yahoo.com",
                "mobile_number": "+1-415-555-0193",
                "linkedin_url": "https://linkedin.com/in/kirentanna",
                "confidence_score": 0.83,
                "last_updated": "2026-04-28",
            },
        ],
        "job_postings": [
            {"job_title": f"Enterprise Account Executive — Fleet {i}", "department": "sales",
             "location": "Remote - US", "date_posted": "2026-04-10", "is_new_role": True}
            for i in range(1, 22)
        ] + [
            {"job_title": "Senior Software Engineer — IoT Platform", "department": "engineering",
             "location": "San Francisco, CA", "date_posted": "2026-04-18", "is_new_role": True},
            {"job_title": "Principal Engineer — Data Infrastructure", "department": "engineering",
             "location": "San Francisco, CA", "date_posted": "2026-04-20", "is_new_role": True},
            {"job_title": "Field Sales Engineer", "department": "field_ops",
             "location": "Atlanta, GA", "date_posted": "2026-04-22", "is_new_role": False},
            {"job_title": "Field Sales Engineer", "department": "field_ops",
             "location": "Chicago, IL", "date_posted": "2026-04-22", "is_new_role": False},
        ],
        "recent_posts": [
            {
                "author_name": "Sanjit Biswas",
                "author_title": "CEO & Co-Founder, Samsara",
                "content": "Samsara closed FY2026 with $1.62 billion in revenue — 29.6% year-over-year growth at scale. Q4 alone was $444 million. What is remarkable is sustaining near-30% compounding growth past the billion-dollar mark. Physical operations are the last frontier for digital transformation, and we are just getting started.",
                "posted_date": "2026-02-28",
                "engagement_rate": 0.14,
            },
            {
                "author_name": "John Bicket",
                "author_title": "CTO, Samsara",
                "content": "Our new AI-powered anomaly detection for fleet vehicles just shipped to 50,000+ enterprise customers. The gap between raw sensor data and actionable driver coaching is finally closed. Real-time inference at the edge, zero cloud round-trip latency.",
                "posted_date": "2026-05-02",
                "engagement_rate": 0.09,
            },
        ],
    },

    # ── Rippling ─────────────────────────────────────────────────────────────
    "rippling": {
        "company": {
            "company_name": "Rippling",
            "company_id": "cd_rippling_001",
            "industry": "HR / IT / Finance Automation",
            "funding_stage": "Series G",
            "headcount": 2800,
            "headcount_delta_90d": 310,
            "headcount_by_department": {
                "sales":       {"headcount": 920,  "delta_90d": 130},
                "engineering": {"headcount": 1050, "delta_90d": 120},
                "marketing":   {"headcount": 310,  "delta_90d": 30},
                "product":     {"headcount": 280,  "delta_90d": 18},
                "g_and_a":     {"headcount": 240,  "delta_90d": 12},
            },
            "glassdoor_overall_rating": 4.1,
            "glassdoor_trend": "improving",
            "recent_funding": {
                "round": "Series G",
                "amount": 200_000_000,
                "date": "2025-05-15",
                "note": "Valuation $16.8B. Crossed $1B ARR in March 2026 (+78% YoY). Super Bowl ad Feb 2026.",
            },
            "description": "Workforce management platform unifying HR, IT, and Finance in one compound product.",
            "hq_location": "San Francisco, CA",
            "revenue_arr": 1_000_000_000,
            "revenue_growth_yoy": "78%",
        },
        "contacts": [
            {
                "full_name": "Parker Conrad",
                "title": "CEO & Co-Founder",
                "seniority_level": "C-Suite",
                "work_email": "parker@rippling.com",
                "personal_email": "parkerconrad@gmail.com",
                "mobile_number": "+1-415-555-0201",
                "linkedin_url": "https://linkedin.com/in/parkerconrad",
                "confidence_score": 0.96,
                "last_updated": "2026-05-18",
            },
            {
                "full_name": "Vanessa Wu",
                "title": "Chief Revenue Officer",
                "seniority_level": "C-Suite",
                "work_email": "vwu@rippling.com",
                "personal_email": "vanessa.wu@icloud.com",
                "mobile_number": "+1-415-555-0202",
                "linkedin_url": "https://linkedin.com/in/vanessawu-cro",
                "confidence_score": 0.82,
                "last_updated": "2026-04-30",
            },
        ],
        "job_postings": [
            {"job_title": f"Mid-Market Account Executive — HRIS {i}", "department": "sales",
             "location": "Remote - US", "date_posted": "2026-04-15", "is_new_role": True}
            for i in range(1, 16)
        ] + [
            {"job_title": f"Enterprise Account Executive — Finance Product {i}", "department": "sales",
             "location": "New York, NY", "date_posted": "2026-04-20", "is_new_role": True}
            for i in range(1, 9)
        ] + [
            {"job_title": "Staff Engineer — Payroll Infrastructure", "department": "engineering",
             "location": "San Francisco, CA", "date_posted": "2026-05-01", "is_new_role": True},
            {"job_title": "Product Manager — IT Management", "department": "product",
             "location": "San Francisco, CA", "date_posted": "2026-05-03", "is_new_role": True},
        ],
        "recent_posts": [
            {
                "author_name": "Parker Conrad",
                "author_title": "CEO, Rippling",
                "content": "We crossed $1 billion in ARR in March. 78% growth. 10+ product lines each generating over $1M in ARR independently. The compound product is working. The Super Bowl spot was the signal to the market that Rippling is playing in a different league now.",
                "posted_date": "2026-03-18",
                "engagement_rate": 0.19,
            },
            {
                "author_name": "Parker Conrad",
                "author_title": "CEO, Rippling",
                "content": "The difference between a platform and a suite: in a suite, every product is a silo. In a platform, every product makes every other product better. That compounding effect is what you're seeing in our revenue trajectory.",
                "posted_date": "2026-04-28",
                "engagement_rate": 0.16,
            },
        ],
    },

    # ── Deel ─────────────────────────────────────────────────────────────────
    "deel": {
        "company": {
            "company_name": "Deel",
            "company_id": "cd_deel_001",
            "industry": "HR Tech / Global Payroll & Compliance",
            "funding_stage": "Series E (Pre-IPO)",
            "headcount": 9500,
            "headcount_delta_90d": 420,
            "headcount_by_department": {
                "sales":              {"headcount": 2600, "delta_90d": 180},
                "engineering":        {"headcount": 3100, "delta_90d": 140},
                "operations":         {"headcount": 1900, "delta_90d": 60},
                "compliance_legal":   {"headcount": 1000, "delta_90d": 30},
                "marketing":          {"headcount": 500,  "delta_90d": 10},
            },
            "glassdoor_overall_rating": 3.7,
            "glassdoor_trend": "stable",
            "recent_funding": {
                "round": "Series E",
                "amount": 300_000_000,
                "date": "2025-10-01",
                "note": "Valuation $17.3B. ARR ~$1.4B (+57.3% YoY). EBITDA+ for 3+ years. ~85% gross margins. Processing $22B annual payroll. IPO preparation underway.",
            },
            "description": "Global payroll, compliance, and employer-of-record platform — processing $22B in annual payroll.",
            "hq_location": "San Francisco, CA",
            "revenue_arr": 1_400_000_000,
            "revenue_growth_yoy": "57.3%",
        },
        "contacts": [
            {
                "full_name": "Alex Bouaziz",
                "title": "CEO & Co-Founder",
                "seniority_level": "C-Suite",
                "work_email": "alex@deel.com",
                "personal_email": "alex.bouaziz@gmail.com",
                "mobile_number": "+1-650-555-0301",
                "linkedin_url": "https://linkedin.com/in/alexbouaziz",
                "confidence_score": 0.95,
                "last_updated": "2026-05-20",
            },
            {
                "full_name": "Shuo Wang",
                "title": "Chief Revenue Officer",
                "seniority_level": "C-Suite",
                "work_email": "shuo@deel.com",
                "personal_email": "shuo.wang@outlook.com",
                "mobile_number": "+1-650-555-0302",
                "linkedin_url": "https://linkedin.com/in/shuowang",
                "confidence_score": 0.88,
                "last_updated": "2026-05-12",
            },
            {
                "full_name": "Elena Mishchenko",
                "title": "VP Global Compliance",
                "seniority_level": "VP",
                "work_email": "emishchenko@deel.com",
                "personal_email": "elena.m@gmail.com",
                "mobile_number": "+1-650-555-0303",
                "linkedin_url": "https://linkedin.com/in/elenamishchenko",
                "confidence_score": 0.79,
                "last_updated": "2026-04-25",
            },
        ],
        "job_postings": [
            {"job_title": f"Enterprise Account Executive — Global Payroll {i}", "department": "sales",
             "location": "Remote", "date_posted": "2026-04-10", "is_new_role": True}
            for i in range(1, 14)
        ] + [
            {"job_title": f"Senior Compliance Manager — APAC {i}", "department": "compliance_legal",
             "location": "Singapore", "date_posted": "2026-04-15", "is_new_role": True}
            for i in range(1, 5)
        ] + [
            {"job_title": "VP Investor Relations", "department": "g_and_a",
             "location": "New York, NY", "date_posted": "2026-05-02", "is_new_role": True},
            {"job_title": "Director of SEC Reporting", "department": "g_and_a",
             "location": "San Francisco, CA", "date_posted": "2026-05-05", "is_new_role": True},
            {"job_title": "Principal Engineer — Payroll Engine", "department": "engineering",
             "location": "Remote", "date_posted": "2026-04-28", "is_new_role": True},
        ],
        "recent_posts": [
            {
                "author_name": "Alex Bouaziz",
                "author_title": "CEO, Deel",
                "content": "We processed $22 billion in payroll last year. We have been EBITDA positive for over three years while growing at 57%. Both things are true. You do not have to choose between growth and profitability — you just have to build the right product in the right market.",
                "posted_date": "2026-04-15",
                "engagement_rate": 0.17,
            },
            {
                "author_name": "Shuo Wang",
                "author_title": "CRO, Deel",
                "content": "Global payroll compliance is the moat nobody talks about. We have legal entities in 150+ countries. That took years to build. It is not replicable quickly. Our enterprise sales cycle is shortening because buyers know this.",
                "posted_date": "2026-05-08",
                "engagement_rate": 0.11,
            },
        ],
    },

    # ── Notion ────────────────────────────────────────────────────────────────
    "notion": {
        "company": {
            "company_name": "Notion",
            "company_id": "cd_notion_001",
            "industry": "Productivity / AI Workspace",
            "funding_stage": "Series C",
            "headcount": 1900,
            "headcount_delta_90d": 85,
            "headcount_by_department": {
                "engineering": {"headcount": 820, "delta_90d": 48},
                "sales":       {"headcount": 380, "delta_90d": 22},
                "marketing":   {"headcount": 210, "delta_90d": 8},
                "product":     {"headcount": 290, "delta_90d": 12},
                "support":     {"headcount": 200, "delta_90d": -5},
            },
            "glassdoor_overall_rating": 4.3,
            "glassdoor_trend": "stable",
            "recent_funding": {
                "round": "Series C / Tender Offer",
                "amount": 270_000_000,
                "date": "2026-01-15",
                "note": "Valuation $11B. 100M users worldwide. AI add-on revenue doubled YoY. >50% of ARR from AI products. Launched Custom Agents early 2026.",
            },
            "description": "All-in-one AI workspace — notes, databases, wikis, and autonomous workflow agents.",
            "hq_location": "San Francisco, CA",
            "revenue_arr": None,
            "revenue_growth_yoy": "AI customer revenue doubled YoY",
        },
        "contacts": [
            {
                "full_name": "Ivan Zhao",
                "title": "CEO & Co-Founder",
                "seniority_level": "C-Suite",
                "work_email": "ivan@notion.so",
                "personal_email": "ivanzhao@gmail.com",
                "mobile_number": "+1-415-555-0401",
                "linkedin_url": "https://linkedin.com/in/ivanzhaof",
                "confidence_score": 0.96,
                "last_updated": "2026-05-18",
            },
            {
                "full_name": "Akshay Kothari",
                "title": "COO",
                "seniority_level": "C-Suite",
                "work_email": "akshay@notion.so",
                "personal_email": "akshay.kothari@icloud.com",
                "mobile_number": "+1-415-555-0402",
                "linkedin_url": "https://linkedin.com/in/akshay",
                "confidence_score": 0.90,
                "last_updated": "2026-05-10",
            },
            {
                "full_name": "Camille Ricketts",
                "title": "Head of Marketing",
                "seniority_level": "Director",
                "work_email": "camille@notion.so",
                "personal_email": "camille.r@gmail.com",
                "mobile_number": "+1-415-555-0403",
                "linkedin_url": "https://linkedin.com/in/camillerick",
                "confidence_score": 0.84,
                "last_updated": "2026-04-22",
            },
        ],
        "job_postings": [
            {"job_title": "Staff Engineer — AI Agents", "department": "engineering",
             "location": "San Francisco, CA", "date_posted": "2026-05-01", "is_new_role": True},
            {"job_title": "Senior ML Engineer — Notion AI", "department": "engineering",
             "location": "San Francisco, CA", "date_posted": "2026-05-03", "is_new_role": True},
            {"job_title": "Senior ML Engineer — Embeddings", "department": "engineering",
             "location": "San Francisco, CA", "date_posted": "2026-05-05", "is_new_role": True},
            {"job_title": "Enterprise Account Executive — EMEA", "department": "sales",
             "location": "London, UK", "date_posted": "2026-04-28", "is_new_role": True},
            {"job_title": "Enterprise Account Executive — APAC", "department": "sales",
             "location": "Singapore", "date_posted": "2026-04-28", "is_new_role": True},
            {"job_title": "Product Manager — Custom Agents", "department": "product",
             "location": "San Francisco, CA", "date_posted": "2026-04-20", "is_new_role": True},
        ],
        "recent_posts": [
            {
                "author_name": "Ivan Zhao",
                "author_title": "CEO, Notion",
                "content": "We just crossed 100 million users. More than half of our ARR now comes from AI products. We launched Custom Agents last quarter — they let any team automate repetitive workflows without writing a single line of code. The age of the AI-native workspace is not coming. It is here.",
                "posted_date": "2026-03-10",
                "engagement_rate": 0.21,
            },
            {
                "author_name": "Akshay Kothari",
                "author_title": "COO, Notion",
                "content": "The enterprise AI buying cycle is collapsing. Twelve months ago a CIO would pilot for six months before committing. Now they ask: when can we go live? Custom Agents changed the ROI conversation entirely.",
                "posted_date": "2026-04-18",
                "engagement_rate": 0.12,
            },
        ],
    },

    # ── Linear ────────────────────────────────────────────────────────────────
    "linear": {
        "company": {
            "company_name": "Linear",
            "company_id": "cd_linear_001",
            "industry": "Developer Tools / Project Management",
            "funding_stage": "Series C",
            "headcount": 226,
            "headcount_delta_90d": 18,
            "headcount_by_department": {
                "engineering": {"headcount": 148, "delta_90d": 12},
                "product":     {"headcount": 28,  "delta_90d": 2},
                "sales":       {"headcount": 24,  "delta_90d": 4},
                "marketing":   {"headcount": 10,  "delta_90d": 0},
                "g_and_a":     {"headcount": 16,  "delta_90d": 0},
            },
            "glassdoor_overall_rating": 4.8,
            "glassdoor_trend": "improving",
            "recent_funding": {
                "round": "Series C",
                "amount": 82_000_000,
                "date": "2025-11-01",
                "note": "Valuation $1.25B. Total funding $134M. Famously spent ~$35K on total marketing from founding to Series C. Pure PLG motion.",
            },
            "description": "Issue tracking and project management built for the speed and quality standards of high-performance engineering teams.",
            "hq_location": "San Francisco, CA",
            "revenue_arr": None,
            "revenue_growth_yoy": "Undisclosed — pure PLG",
        },
        "contacts": [
            {
                "full_name": "Karri Saarinen",
                "title": "CEO & Co-Founder",
                "seniority_level": "C-Suite",
                "work_email": "karri@linear.app",
                "personal_email": "karri.s@gmail.com",
                "mobile_number": "+1-415-555-0501",
                "linkedin_url": "https://linkedin.com/in/karrisaarinen",
                "confidence_score": 0.94,
                "last_updated": "2026-05-15",
            },
            {
                "full_name": "Jori Lallo",
                "title": "CTO & Co-Founder",
                "seniority_level": "C-Suite",
                "work_email": "jori@linear.app",
                "personal_email": "jori.lallo@gmail.com",
                "mobile_number": "+1-415-555-0502",
                "linkedin_url": "https://linkedin.com/in/jorilallo",
                "confidence_score": 0.91,
                "last_updated": "2026-05-10",
            },
        ],
        "job_postings": [
            {"job_title": "Senior Software Engineer — Core", "department": "engineering",
             "location": "Remote", "date_posted": "2026-05-10", "is_new_role": True},
            {"job_title": "Senior Software Engineer — AI Features", "department": "engineering",
             "location": "Remote", "date_posted": "2026-05-10", "is_new_role": True},
            {"job_title": "Enterprise Sales Lead", "department": "sales",
             "location": "San Francisco, CA", "date_posted": "2026-05-05", "is_new_role": True},
        ],
        "recent_posts": [
            {
                "author_name": "Karri Saarinen",
                "author_title": "CEO, Linear",
                "content": "From founding to our Series C, we spent approximately $35,000 on marketing. Total. The product grew because engineers told other engineers. That is the only distribution strategy that compounds without a budget. We are 226 people and a $1.25 billion company. Capital efficiency is not a constraint — it is a philosophy.",
                "posted_date": "2026-01-20",
                "engagement_rate": 0.28,
            },
            {
                "author_name": "Karri Saarinen",
                "author_title": "CEO, Linear",
                "content": "Speed is non-negotiable. Our median issue load time is under 20ms. Engineers don't notice it consciously — they just feel less friction. That feeling is the product. Jira's median is 3-4 seconds. That difference compounds across every interaction, every day.",
                "posted_date": "2026-04-05",
                "engagement_rate": 0.22,
            },
        ],
    },

    # ── Brex ─────────────────────────────────────────────────────────────────
    "brex": {
        "company": {
            "company_name": "Brex",
            "company_id": "cd_brex_001",
            "industry": "Fintech / Corporate Spend Management",
            "funding_stage": "Acquired by Capital One (April 2026)",
            "headcount": 1800,
            "headcount_delta_90d": -35,
            "headcount_by_department": {
                "sales":        {"headcount": 480,  "delta_90d": -28},
                "engineering":  {"headcount": 720,  "delta_90d": 15},
                "operations":   {"headcount": 290,  "delta_90d": -20},
                "marketing":    {"headcount": 160,  "delta_90d": -5},
                "g_and_a":      {"headcount": 150,  "delta_90d": 3},
            },
            "glassdoor_overall_rating": 3.5,
            "glassdoor_trend": "declining",
            "recent_funding": {
                "round": "Acquired by Capital One",
                "amount": 5_150_000_000,
                "date": "2026-04-01",
                "note": "50% cash / 50% Capital One stock. Capital One injecting ~$1B R&D. Prior peak private valuation was $12.3B in 2022. ARR ~$700M pre-acquisition.",
            },
            "description": "AI-powered corporate card and spend management — now a Capital One company.",
            "hq_location": "San Francisco, CA",
            "revenue_arr": 700_000_000,
            "revenue_growth_yoy": "Undisclosed post-acquisition",
        },
        "contacts": [
            {
                "full_name": "Pedro Franceschi",
                "title": "CEO",
                "seniority_level": "C-Suite",
                "work_email": "pedro@brex.com",
                "personal_email": "pedro.f@gmail.com",
                "mobile_number": "+1-415-555-0601",
                "linkedin_url": "https://linkedin.com/in/pedrofranceschi",
                "confidence_score": 0.93,
                "last_updated": "2026-05-10",
            },
            {
                "full_name": "Henrique Dubugras",
                "title": "Executive Chairman",
                "seniority_level": "C-Suite",
                "work_email": "henrique@brex.com",
                "personal_email": "h.dubugras@gmail.com",
                "mobile_number": "+1-415-555-0602",
                "linkedin_url": "https://linkedin.com/in/hdubugras",
                "confidence_score": 0.90,
                "last_updated": "2026-05-08",
            },
            {
                "full_name": "Michael Tannenbaum",
                "title": "CFO",
                "seniority_level": "C-Suite",
                "work_email": "mtannenbaum@brex.com",
                "personal_email": "m.tannenbaum@outlook.com",
                "mobile_number": "+1-415-555-0603",
                "linkedin_url": "https://linkedin.com/in/michaeltannenbaum",
                "confidence_score": 0.76,
                "last_updated": "2026-04-18",
            },
        ],
        "job_postings": [
            {"job_title": "Senior AI/ML Engineer — Fraud Detection", "department": "engineering",
             "location": "San Francisco, CA", "date_posted": "2026-05-01", "is_new_role": True},
            {"job_title": "Senior AI/ML Engineer — Spend Intelligence", "department": "engineering",
             "location": "San Francisco, CA", "date_posted": "2026-05-01", "is_new_role": True},
            {"job_title": "Principal Engineer — Capital One Integration", "department": "engineering",
             "location": "McLean, VA", "date_posted": "2026-04-20", "is_new_role": True},
            {"job_title": "Enterprise Account Executive", "department": "sales",
             "location": "Remote", "date_posted": "2026-04-15", "is_new_role": False},
            {"job_title": "Enterprise Account Executive", "department": "sales",
             "location": "Remote", "date_posted": "2026-04-15", "is_new_role": False},
            {"job_title": "Enterprise Account Executive", "department": "sales",
             "location": "Remote", "date_posted": "2026-04-15", "is_new_role": False},
        ],
        "recent_posts": [
            {
                "author_name": "Pedro Franceschi",
                "author_title": "CEO, Brex",
                "content": "Joining Capital One is not an exit — it is an acceleration. They have the distribution, the banking relationships, and $1 billion committed to our AI roadmap. Brex's technology plus Capital One's scale is genuinely a different company. We are building from that position now.",
                "posted_date": "2026-04-05",
                "engagement_rate": 0.18,
            },
            {
                "author_name": "Henrique Dubugras",
                "author_title": "Executive Chairman, Brex",
                "content": "A lot of people are asking about the journey from a $12B valuation to this deal. The honest answer: the macro shifted, the SMB market contracted, and we had to be realistic about the path to profitability as a standalone public company. Capital One gives us the foundation to build the best corporate finance product in the world.",
                "posted_date": "2026-04-08",
                "engagement_rate": 0.22,
            },
        ],
    },

    # ── Ramp ─────────────────────────────────────────────────────────────────
    "ramp": {
        "company": {
            "company_name": "Ramp",
            "company_id": "cd_ramp_001",
            "industry": "Fintech / AI Finance Automation",
            "funding_stage": "Series E (Raise Imminent)",
            "headcount": 2200,
            "headcount_delta_90d": 320,
            "headcount_by_department": {
                "sales":       {"headcount": 680,  "delta_90d": 130},
                "engineering": {"headcount": 860,  "delta_90d": 120},
                "marketing":   {"headcount": 270,  "delta_90d": 40},
                "operations":  {"headcount": 240,  "delta_90d": 20},
                "g_and_a":     {"headcount": 150,  "delta_90d": 10},
            },
            "glassdoor_overall_rating": 4.6,
            "glassdoor_trend": "improving",
            "recent_funding": {
                "round": "Series D / Series E (imminent)",
                "amount": 300_000_000,
                "date": "2025-08-01",
                "note": "Valuation $32B (late 2025). In active talks May 2026 to raise $750M at $40B+ valuation. ARR $1B — doubled from $500M in ~12 months. Enterprise customer growth 133% YoY. Launched AI procurement agents.",
            },
            "description": "Finance automation platform — corporate cards, bill pay, expense management, and AI procurement agents.",
            "hq_location": "New York, NY",
            "revenue_arr": 1_000_000_000,
            "revenue_growth_yoy": "133% (enterprise)",
        },
        "contacts": [
            {
                "full_name": "Eric Glyman",
                "title": "CEO & Co-Founder",
                "seniority_level": "C-Suite",
                "work_email": "eric@ramp.com",
                "personal_email": "eglyman@gmail.com",
                "mobile_number": "+1-646-555-0701",
                "linkedin_url": "https://linkedin.com/in/ericglyman",
                "confidence_score": 0.95,
                "last_updated": "2026-05-20",
            },
            {
                "full_name": "Karim Atiyeh",
                "title": "CTO & Co-Founder",
                "seniority_level": "C-Suite",
                "work_email": "karim@ramp.com",
                "personal_email": "karim.atiyeh@gmail.com",
                "mobile_number": "+1-646-555-0702",
                "linkedin_url": "https://linkedin.com/in/karimatiyeh",
                "confidence_score": 0.92,
                "last_updated": "2026-05-15",
            },
            {
                "full_name": "Stephanie Simon",
                "title": "VP Enterprise Sales",
                "seniority_level": "VP",
                "work_email": "ssimon@ramp.com",
                "personal_email": "stephanie.simon@icloud.com",
                "mobile_number": "+1-646-555-0703",
                "linkedin_url": "https://linkedin.com/in/stephaniecsales",
                "confidence_score": 0.81,
                "last_updated": "2026-05-08",
            },
        ],
        "job_postings": [
            {"job_title": f"Enterprise Account Executive — AI Finance {i}", "department": "sales",
             "location": "New York, NY", "date_posted": "2026-05-01", "is_new_role": True}
            for i in range(1, 14)
        ] + [
            {"job_title": f"Senior ML Engineer — AI Procurement Agents {i}", "department": "engineering",
             "location": "New York, NY", "date_posted": "2026-05-05", "is_new_role": True}
            for i in range(1, 7)
        ] + [
            {"job_title": "Director of Enterprise Marketing", "department": "marketing",
             "location": "New York, NY", "date_posted": "2026-04-25", "is_new_role": True},
            {"job_title": "Head of Corporate Development", "department": "g_and_a",
             "location": "New York, NY", "date_posted": "2026-05-10", "is_new_role": True},
        ],
        "recent_posts": [
            {
                "author_name": "Eric Glyman",
                "author_title": "CEO, Ramp",
                "content": "Ramp just crossed $1 billion in ARR. We went from $500M to $1B in roughly 12 months. Enterprise customer growth is 133% year over year. We launched a full fleet of AI procurement agents that handle compliance and vendor sourcing autonomously. The next chapter is going to be even bigger.",
                "posted_date": "2026-04-20",
                "engagement_rate": 0.23,
            },
            {
                "author_name": "Karim Atiyeh",
                "author_title": "CTO, Ramp",
                "content": "Our AI procurement agents just negotiated better SaaS renewal terms than the human doing it before. Not because the AI is smarter — because it is relentless and has perfect recall of every line in every contract. That is the power of AI applied to finance ops.",
                "posted_date": "2026-05-12",
                "engagement_rate": 0.17,
            },
        ],
    },

    # ── Vercel ────────────────────────────────────────────────────────────────
    "vercel": {
        "company": {
            "company_name": "Vercel",
            "company_id": "cd_vercel_001",
            "industry": "Developer Tools / Frontend Cloud",
            "funding_stage": "Series E",
            "headcount": 600,
            "headcount_delta_90d": 38,
            "headcount_by_department": {
                "engineering": {"headcount": 310, "delta_90d": 25},
                "sales":       {"headcount": 140, "delta_90d": 12},
                "marketing":   {"headcount": 80,  "delta_90d": 3},
                "support":     {"headcount": 70,  "delta_90d": -2},
            },
            "glassdoor_overall_rating": 4.3,
            "glassdoor_trend": "stable",
            "recent_funding": {
                "round": "Series E",
                "amount": 250_000_000,
                "date": "2024-05-16",
                "note": "Valuation $3.25B. Hosts millions of frontend deployments for Next.js ecosystem.",
            },
            "description": "Frontend cloud platform for deploying and globally scaling web applications.",
            "hq_location": "San Francisco, CA",
        },
        "contacts": [
            {
                "full_name": "Guillermo Rauch",
                "title": "CEO & Founder",
                "seniority_level": "C-Suite",
                "work_email": "rauch@vercel.com",
                "personal_email": "guillermo.r@gmail.com",
                "mobile_number": "+1-415-555-0801",
                "linkedin_url": "https://linkedin.com/in/guillermo",
                "confidence_score": 0.96,
                "last_updated": "2026-05-01",
            },
        ],
        "job_postings": [
            {"job_title": "Enterprise Sales Engineer", "department": "sales",
             "location": "Remote", "date_posted": "2026-05-08", "is_new_role": True},
            {"job_title": "Staff Infrastructure Engineer", "department": "engineering",
             "location": "San Francisco, CA", "date_posted": "2026-05-05", "is_new_role": True},
            {"job_title": "AI Product Engineer", "department": "engineering",
             "location": "Remote", "date_posted": "2026-05-03", "is_new_role": True},
        ],
        "recent_posts": [
            {
                "author_name": "Guillermo Rauch",
                "author_title": "CEO, Vercel",
                "content": "The v0 AI code generation model now deploys directly to Vercel with one click. Zero configuration. Global edge. Enterprise SLAs. The distance between idea and production has never been smaller.",
                "posted_date": "2026-04-22",
                "engagement_rate": 0.15,
            },
        ],
    },

    # ── Retool ────────────────────────────────────────────────────────────────
    "retool": {
        "company": {
            "company_name": "Retool",
            "company_id": "cd_retool_001",
            "industry": "Developer Tools / Low-code Internal Apps",
            "funding_stage": "Series C",
            "headcount": 500,
            "headcount_delta_90d": 22,
            "headcount_by_department": {
                "engineering": {"headcount": 255, "delta_90d": 15},
                "sales":       {"headcount": 115, "delta_90d": 9},
                "marketing":   {"headcount": 62,  "delta_90d": 1},
                "support":     {"headcount": 68,  "delta_90d": -3},
            },
            "glassdoor_overall_rating": 4.2,
            "glassdoor_trend": "stable",
            "recent_funding": {
                "round": "Series C",
                "amount": 45_000_000,
                "date": "2022-06-14",
                "note": "Valuation ~$3.2B. Powering 100K+ internal tools at companies like Amazon, Mercedes-Benz, DoorDash.",
            },
            "description": "Low-code platform for building internal tools, dashboards, and admin panels.",
            "hq_location": "San Francisco, CA",
        },
        "contacts": [
            {
                "full_name": "David Hsu",
                "title": "CEO & Co-Founder",
                "seniority_level": "C-Suite",
                "work_email": "david@retool.com",
                "personal_email": "davidhsu@gmail.com",
                "mobile_number": "+1-415-555-0901",
                "linkedin_url": "https://linkedin.com/in/dhsu",
                "confidence_score": 0.91,
                "last_updated": "2026-05-01",
            },
        ],
        "job_postings": [
            {"job_title": "Enterprise Account Executive", "department": "sales",
             "location": "San Francisco, CA", "date_posted": "2026-05-02", "is_new_role": True},
            {"job_title": "Senior Full Stack Engineer — AI Apps", "department": "engineering",
             "location": "San Francisco, CA", "date_posted": "2026-04-28", "is_new_role": True},
        ],
        "recent_posts": [
            {
                "author_name": "David Hsu",
                "author_title": "CEO, Retool",
                "content": "Retool AI lets non-engineers build autonomous agents that connect to internal databases, APIs, and workflows. Every ops team I talk to has a backlog of automation requests they cannot get engineering to prioritize. We just cleared that backlog.",
                "posted_date": "2026-04-30",
                "engagement_rate": 0.11,
            },
        ],
    },

}


# ── Lookup helpers ────────────────────────────────────────────────────────────

def _normalize(name: str) -> str:
    return name.lower().strip().replace(" ", "").replace("-", "").replace(".", "")


def _find_profile(company_name: str) -> dict | None:
    key = _normalize(company_name)
    for k, v in PROFILES.items():
        if key == _normalize(k):
            return v
    # partial match
    for k, v in PROFILES.items():
        if key in _normalize(k) or _normalize(k) in key:
            return v
    return None


def _generate_profile(company_name: str) -> dict:
    """Deterministically generate a plausible profile for any unlisted company."""
    seed = int(hashlib.md5(company_name.lower().encode()).hexdigest(), 16)
    rng = random.Random(seed)

    stages = ["Series A", "Series B", "Series C", "Series D", "Series E"]
    industries = [
        "SaaS / B2B Software", "Fintech", "HR Tech", "DevTools",
        "Data & Analytics", "Cybersecurity", "MarTech", "HealthTech",
    ]
    locations = ["San Francisco, CA", "New York, NY", "Austin, TX", "Seattle, WA", "Boston, MA"]

    stage = rng.choice(stages)
    stage_idx = stages.index(stage)
    base_hc = rng.randint(80, 400) * (stage_idx + 1)
    delta = rng.randint(-20, int(base_hc * 0.12))
    funding_amt = rng.randint(20, 300) * 1_000_000

    sales_hc  = int(base_hc * rng.uniform(0.20, 0.35))
    eng_hc    = int(base_hc * rng.uniform(0.35, 0.50))
    mkt_hc    = int(base_hc * rng.uniform(0.08, 0.15))
    other_hc  = base_hc - sales_hc - eng_hc - mkt_hc

    sales_delta = rng.randint(int(delta * 0.3), max(int(delta * 0.6), 1))
    eng_delta   = rng.randint(int(delta * 0.2), max(int(delta * 0.4), 1))

    glassdoor = round(rng.uniform(3.1, 4.6), 1)
    trend = rng.choice(["improving", "stable", "stable", "declining"])

    job_count = rng.randint(5, 25)
    postings = []
    for i in range(job_count):
        dept = rng.choice(["sales", "engineering", "marketing", "operations"])
        title_map = {
            "sales":       "Account Executive",
            "engineering": "Software Engineer",
            "marketing":   "Marketing Manager",
            "operations":  "Operations Analyst",
        }
        postings.append({
            "job_title": f"{'Senior ' if rng.random() > 0.5 else ''}{title_map[dept]} {i + 1}",
            "department": dept,
            "location": rng.choice(["Remote", "Remote - US", locations[stage_idx % len(locations)]]),
            "date_posted": "2026-04-15",
            "is_new_role": rng.random() > 0.35,
        })

    first_names = ["Jordan", "Taylor", "Alex", "Morgan", "Casey", "Riley", "Avery"]
    last_names  = ["Chen", "Patel", "Williams", "Rodriguez", "Johnson", "Lee", "Kim"]
    titles      = ["VP Sales", "CRO", "VP Engineering", "VP Marketing", "Head of Growth"]
    fn    = rng.choice(first_names)
    ln    = rng.choice(last_names)
    title = rng.choice(titles)
    slug  = company_name.lower().replace(" ", "")[:10]

    posts = [{
        "author_name":    f"{fn} {ln}",
        "author_title":   title,
        "content": rng.choice([
            f"Excited about our momentum heading into the back half of the year. Pipeline is strong and the team is executing.",
            f"The biggest challenge at scale is maintaining data quality across a fast-growing GTM team. We are investing heavily here.",
            f"Our NPS just crossed {rng.randint(50, 75)}. Revenue efficiency is the metric that matters most right now.",
            f"We doubled ARR in the last 12 months. The product-market fit signal is undeniable.",
        ]),
        "posted_date":    "2026-05-01",
        "engagement_rate": round(rng.uniform(0.04, 0.14), 2),
    }]

    return {
        "company": {
            "company_name": company_name,
            "company_id": f"cd_{slug}_{seed % 9999:04d}",
            "industry": rng.choice(industries),
            "funding_stage": stage,
            "headcount": base_hc,
            "headcount_delta_90d": delta,
            "headcount_by_department": {
                "sales":       {"headcount": sales_hc, "delta_90d": sales_delta},
                "engineering": {"headcount": eng_hc,   "delta_90d": eng_delta},
                "marketing":   {"headcount": mkt_hc,   "delta_90d": rng.randint(0, 8)},
                "operations":  {"headcount": other_hc, "delta_90d": delta - sales_delta - eng_delta},
            },
            "glassdoor_overall_rating": glassdoor,
            "glassdoor_trend": trend,
            "recent_funding": {"round": stage, "amount": funding_amt, "date": "2025-09-01"},
            "description": f"B2B SaaS platform serving {rng.choice(['mid-market', 'enterprise', 'SMB and mid-market'])} customers.",
            "hq_location": rng.choice(locations),
        },
        "contacts": [{
            "full_name":       f"{fn} {ln}",
            "title":           title,
            "seniority_level": "VP" if title.startswith("VP") else "C-Suite",
            "work_email":      f"{fn.lower()}.{ln.lower()}@{slug}.com",
            "personal_email":  f"{fn.lower()}{ln.lower()}@gmail.com",
            "mobile_number":   f"+1-415-555-{rng.randint(1000, 9999)}",
            "linkedin_url":    f"https://linkedin.com/in/{fn.lower()}-{ln.lower()}",
            "confidence_score": round(rng.uniform(0.76, 0.95), 2),
            "last_updated":    "2026-05-10",
        }],
        "job_postings": postings,
        "recent_posts":  posts,
    }


def get_mock_payload(company_name: str) -> dict:
    """Return a realistic Crustdata-shaped payload for any company name."""
    profile = _find_profile(company_name)
    if profile:
        return {
            "company":       profile["company"],
            "contacts":      profile["contacts"],
            "job_postings":  profile["job_postings"],
            "recent_posts":  profile["recent_posts"],
        }
    return _generate_profile(company_name)
