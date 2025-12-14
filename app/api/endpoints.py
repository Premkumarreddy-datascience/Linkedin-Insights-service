from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.database import get_db
from app.models.page import Page
from app.schemas import PageUpdate

from app.services.page_service import PageService
from app.services.post_service import PostService
from app.services.user_service import UserService

from app.api.dependencies import (
    get_page_service,
    get_post_service,
    get_user_service
)

router = APIRouter()

# PAGE – GET OR SCRAPE (CORE FEATURE)


@router.get("/pages/{page_id}")
def get_page_details(
    page_id: str,
    refresh: bool = False,
    page_service: PageService = Depends(get_page_service)
):
    page = page_service.get_or_scrape_page(page_id, force_refresh=refresh)

    if not page:
        raise HTTPException(status_code=404, detail="Page not found")

    return {
        "id": page.id,
        "name": page.name,
        "industry": page.industry,
        "followers": page.total_followers,
        "description": page.description,
        "website": page.website,
        "headquarters": page.headquarters,
        "founded_year": page.founded_year,
        "last_updated": page.updated_at
    }

# PAGE – SEARCH & LIST

@router.get("/pages")
def search_pages(
    name: Optional[str] = None,
    industry: Optional[str] = None,
    min_followers: Optional[int] = None,
    max_followers: Optional[int] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    page_service: PageService = Depends(get_page_service)
):
    filters = {
        "name": name,
        "industry": industry,
        "min_followers": min_followers,
        "max_followers": max_followers
    }

    pages, total = page_service.search_pages(filters, page, limit)

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "pages": [
            {
                "id": p.id,
                "name": p.name,
                "industry": p.industry,
                "followers": p.total_followers
            }
            for p in pages
        ]
    }

# POSTS – RECENT POSTS

@router.get("/pages/{page_id}/posts/recent")
def get_recent_posts(
    page_id: str,
    limit: int = Query(15, ge=1, le=50),
    post_service: PostService = Depends(get_post_service)
):
    posts = post_service.get_recent_posts(page_id, limit)
    return {"page_id": page_id, "recent_posts": posts}

# POSTS – POSTS WITH COMMENTS

@router.get("/pages/{page_id}/posts/with-comments")
def get_posts_with_comments(
    page_id: str,
    limit: int = Query(10, ge=1, le=20),
    post_service: PostService = Depends(get_post_service)
):
    return {
        "page_id": page_id,
        "posts": post_service.get_posts_with_comments(page_id, limit)
    }

# POSTS – TOP PERFORMING


@router.get("/pages/{page_id}/top-posts")
def get_top_posts(
    page_id: str,
    days: int = Query(30, ge=1, le=365),
    limit: int = Query(5, ge=1, le=20),
    post_service: PostService = Depends(get_post_service)
):
    return {
        "page_id": page_id,
        "top_posts": post_service.get_top_performing_posts(page_id, days, limit)
    }

# POSTS – ENGAGEMENT STATS

@router.get("/pages/{page_id}/engagement")
def get_engagement_stats(
    page_id: str,
    post_service: PostService = Depends(get_post_service)
):
    return {
        "page_id": page_id,
        "engagement": post_service.get_post_engagement_stats(page_id)
    }

# POSTS – SEARCH POSTS

@router.get("/pages/{page_id}/posts/search")
def search_posts(
    page_id: str,
    keyword: str = Query(..., min_length=2),
    limit: int = Query(10, ge=1, le=50),
    post_service: PostService = Depends(get_post_service)
):
    return {
        "page_id": page_id,
        "results": post_service.search_posts(page_id, keyword, limit)
    }

# EMPLOYEES – LIST

@router.get("/pages/{page_id}/employees")
def get_employees(
    page_id: str,
    limit: int = Query(20, ge=1, le=100),
    user_service: UserService = Depends(get_user_service)
):
    return {
        "page_id": page_id,
        "employees": user_service.get_page_employees(page_id, limit),
        "total": user_service.get_total_employee_count(page_id)
    }

# EMPLOYEES – FILTER BY POSITION

@router.get("/pages/{page_id}/employees/search")
def search_employees(
    page_id: str,
    position: Optional[str] = None,
    name: Optional[str] = None,
    user_service: UserService = Depends(get_user_service)
):
    if position:
        employees = user_service.get_employee_by_position(page_id, position)
    elif name:
        employees = user_service.search_employees(page_id, name)
    else:
        raise HTTPException(status_code=400, detail="Provide position or name")

    return {"page_id": page_id, "employees": employees}

# EMPLOYEES – DISTRIBUTION

@router.get("/pages/{page_id}/employees/distribution")
def employee_distribution(
    page_id: str,
    user_service: UserService = Depends(get_user_service)
):
    return {
        "page_id": page_id,
        "distribution": user_service.get_employee_distribution(page_id)
    }

# EMPLOYEES – RECENTLY ADDED

@router.get("/pages/{page_id}/employees/recent")
def recent_employees(
    page_id: str,
    limit: int = Query(10, ge=1, le=50),
    user_service: UserService = Depends(get_user_service)
):
    return {
        "page_id": page_id,
        "employees": user_service.get_recently_added_employees(page_id, limit)
    }

# HEALTH – DATABASE

@router.get("/health/db")
def db_health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"database": "connected"}
