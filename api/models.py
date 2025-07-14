from pydantic import BaseModel
from typing import List, Literal

class StrategyRequest(BaseModel):
    platforms: List[str]
    content_goals: str

class InstagramPostRequest(BaseModel):
    content_topic: str
    tone: str
    persona: str
    length: Literal['short', 'medium', 'long'] | str = 'medium'

class FacebookPostRequest(BaseModel):
    content_topic: str
    tone: str
    audience: str
    length: Literal['short', 'medium', 'long'] | str = 'medium'

class LinkedInPostRequest(BaseModel):
    content_topic: str
    tone: str
    professional_insight: str
    length: Literal['short', 'medium', 'long'] | str = 'medium'

class CalendarRequest(BaseModel):
    brand_summary: str
    topic_list: List[str]

class RegenerateRequest(BaseModel):
    output_id: str