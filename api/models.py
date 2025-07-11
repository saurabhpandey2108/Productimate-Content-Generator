from pydantic import BaseModel
from typing import List

class StrategyRequest(BaseModel):
    platforms: List[str]
    content_goals: str

class InstagramPostRequest(BaseModel):
    content_topic: str
    tone: str
    persona: str

class FacebookPostRequest(BaseModel):
    content_topic: str
    tone: str
    audience: str

class LinkedInPostRequest(BaseModel):
    content_topic: str
    tone: str
    professional_insight: str

class CalendarRequest(BaseModel):
    brand_summary: str
    topic_list: List[str]

class RegenerateRequest(BaseModel):
    output_id: str