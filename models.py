from typing import Optional

from pydantic import BaseModel, Field


class Contact(BaseModel):
    full_name: str
    title: str
    seniority_level: Optional[str] = None
    linkedin_url: Optional[str] = None
    work_email: Optional[str] = None
    personal_email: Optional[str] = None
    mobile_number: Optional[str] = None
    confidence_score: float = 0.0


class JobPosting(BaseModel):
    job_title: str
    department: str
    location: Optional[str] = None
    date_posted: Optional[str] = None
    is_new_role: Optional[bool] = None


class LinkedInPost(BaseModel):
    author_name: str
    author_title: Optional[str] = None
    content: str
    posted_date: Optional[str] = None
    engagement_rate: Optional[float] = None


class CompanyProfile(BaseModel):
    company_name: str
    company_id: Optional[str] = None
    industry: Optional[str] = None
    funding_stage: Optional[str] = None
    headcount: Optional[int] = None
    headcount_delta_90d: Optional[int] = None
    headcount_by_department: dict = Field(default_factory=dict)
    glassdoor_overall_rating: Optional[float] = None
    glassdoor_trend: Optional[str] = None
    recent_funding: dict = Field(default_factory=dict)
