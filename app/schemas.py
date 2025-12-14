from pydantic import BaseModel, HttpUrl
from typing import Optional, List, Dict, Any
from datetime import datetime

# Response schemas
class PageResponse(BaseModel):
    id: str
    name: str
    url: Optional[str] = None
    profile_picture: Optional[str] = None
    description: Optional[str] = None
    website: Optional[str] = None
    industry: Optional[str] = None
    total_followers: int = 0
    head_count: Optional[str] = None
    specialities: List[str] = []
    company_type: Optional[str] = None
    founded_year: Optional[int] = None
    headquarters: Optional[str] = None
    locations: List[str] = []
    created_at: datetime
    updated_at: datetime
    post_count: int = 0
    employee_count: int = 0

class PostResponse(BaseModel):
    id: str
    content: Optional[str] = None
    post_type: Optional[str] = None
    like_count: int = 0
    comment_count: int = 0
    share_count: int = 0
    posted_at: Optional[datetime] = None
    comments: List[Dict[str, Any]] = []

class SearchResponse(BaseModel):
    pages: List[Dict[str, Any]]
    pagination: Dict[str, Any]
    filters_applied: Dict[str, Any]

# Request schemas
class PageSearchRequest(BaseModel):
    name: Optional[str] = None
    industry: Optional[str] = None
    min_followers: Optional[int] = None
    max_followers: Optional[int] = None
    page: int = 1
    limit: int = 10

# Put
class PageUpdate(BaseModel):
    name: Optional[str]
    industry: Optional[str]
    description: Optional[str]
    website: Optional[str]
    headquarters: Optional[str]
    founded_year: Optional[int]
    total_followers: Optional[int]