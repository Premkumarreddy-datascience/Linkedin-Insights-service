from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import json

from app.models.page import Page
from app.models.post import Post
from app.models.user import SocialMediaUser
from app.models.comment import Comment
from app.scrapers.linkedin_scraper import LinkedInScraper

class PageService:
    def __init__(self, db: Session):
        self.db = db
        self.scraper = LinkedInScraper()
    
    def get_or_scrape_page(self, page_id: str, force_refresh: bool = False) -> Page:
        """Get page from DB or scrape if not exists/outdated"""
        page = self.db.query(Page).filter(Page.id == page_id).first()
        
        should_refresh = force_refresh or not page
        if page and not force_refresh:
            one_day_ago = datetime.utcnow() - timedelta(days=1)
            if page.updated_at < one_day_ago:
                should_refresh = True
        
        if should_refresh:
            # Scrape fresh data
            scraped_data = self.scraper.scrape_page(page_id)
            
            if page:
                # Update existing page
                self._update_page(page, scraped_data)
            else:
                # Create new page
                page = self._create_page(scraped_data)
                self.db.add(page)
            
            # Save related data
            self._save_posts(page.id, scraped_data.get("posts", []))
            self._save_employees(page.id, scraped_data.get("employees", []))
            
            self.db.commit()
            self.db.refresh(page)
        
        return page
    
    def search_pages(self, filters: Dict, page: int = 1, limit: int = 10) -> Tuple[List[Page], int]:
        """Search pages with filters and pagination"""
        query = self.db.query(Page)
        
        # Apply filters
        if filters.get("name"):
            query = query.filter(Page.name.ilike(f"%{filters['name']}%"))
        
        if filters.get("industry"):
            query = query.filter(Page.industry.ilike(f"%{filters['industry']}%"))
        
        if filters.get("min_followers"):
            query = query.filter(Page.total_followers >= filters["min_followers"])
        
        if filters.get("max_followers"):
            query = query.filter(Page.total_followers <= filters["max_followers"])
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        offset = (page - 1) * limit
        pages = query.offset(offset).limit(limit).all()
        
        return pages, total
    
    def get_page_posts(self, page_id: str, limit: int = 15) -> List[Post]:
        """Get recent posts for a page"""
        posts = self.db.query(Post).filter(
            Post.page_id == page_id
        ).order_by(
            Post.posted_at.desc()
        ).limit(limit).all()
        
        return posts
    
    def _create_page(self, data: Dict) -> Page:
        """Create Page object from scraped data"""
        page = Page(
            id=data["id"],
            name=data.get("name", ""),
            url=data.get("url", ""),
            profile_picture=data.get("profile_picture", ""),
            description=data.get("description", ""),
            website=data.get("website", ""),
            industry=data.get("industry", ""),
            total_followers=data.get("total_followers", 0),
            head_count=data.get("head_count", ""),
            specialities=json.dumps(data.get("specialities", [])),
            company_type=data.get("company_type", ""),
            founded_year=data.get("founded_year"),
            headquarters=data.get("headquarters", ""),
            locations=json.dumps(data.get("locations", []))
        )
        return page
    
    def _update_page(self, page: Page, data: Dict):
        """Update existing page with new data"""
        page.name = data.get("name", page.name)
        page.profile_picture = data.get("profile_picture", page.profile_picture)
        page.description = data.get("description", page.description)
        page.website = data.get("website", page.website)
        page.industry = data.get("industry", page.industry)
        page.total_followers = data.get("total_followers", page.total_followers)
        page.head_count = data.get("head_count", page.head_count)
        page.specialities = json.dumps(data.get("specialities", []))
        page.company_type = data.get("company_type", page.company_type)
        page.founded_year = data.get("founded_year", page.founded_year)
        page.headquarters = data.get("headquarters", page.headquarters)
        page.locations = json.dumps(data.get("locations", []))
        page.updated_at = datetime.utcnow()
    
    def _save_posts(self, page_id: str, posts_data: List[Dict]):
        """Save posts and their comments"""
        for post_data in posts_data:
            # Check if post already exists
            post = self.db.query(Post).filter(Post.id == post_data["id"]).first()
            
            if not post:
                post = Post(
                    id=post_data["id"],
                    page_id=page_id,
                    content=post_data.get("content", ""),
                    post_type=post_data.get("post_type", "post"),
                    media_urls=json.dumps([]),
                    like_count=post_data.get("like_count", 0),
                    comment_count=post_data.get("comment_count", 0),
                    share_count=post_data.get("share_count", 0),
                    posted_at=datetime.fromisoformat(post_data.get("posted_at")) if post_data.get("posted_at") else datetime.utcnow()
                )
                self.db.add(post)
                self.db.flush()  # Get the post ID
            
            # Save comments
            self._save_comments(post.id, post_data.get("comments", []))
    
    def _save_comments(self, post_id: str, comments_data: List[Dict]):
        """Save comments for a post"""
        for comment_data in comments_data:
            comment = Comment(
                id=comment_data["id"],
                post_id=post_id,
                user_name=comment_data.get("user_name", ""),
                user_profile_url=comment_data.get("user_profile_url", ""),
                content=comment_data.get("content", ""),
                commented_at=datetime.fromisoformat(comment_data.get("commented_at")) if comment_data.get("commented_at") else datetime.utcnow()
            )
            self.db.add(comment)
    
    def _save_employees(self, page_id: str, employees_data: List[Dict]):
        """Save employee information"""
        for emp_data in employees_data:
            employee = SocialMediaUser(
                id=emp_data["id"],
                page_id=page_id,
                name=emp_data.get("name", ""),
                profile_url=emp_data.get("profile_url", ""),
                profile_picture=emp_data.get("profile_picture", ""),
                position=emp_data.get("position", "")
            )
            self.db.add(employee)