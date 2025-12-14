from sqlalchemy.orm import Session
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from sqlalchemy import desc, func
import json

from app.models.post import Post
from app.models.comment import Comment
from app.models.page import Page

class PostService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_recent_posts(self, page_id: str, limit: int = 15) -> List[Post]:
        """Get recent posts for a page with pagination"""
        posts = self.db.query(Post).filter(
            Post.page_id == page_id
        ).order_by(
            desc(Post.posted_at)
        ).limit(limit).all()
        
        return posts
    
    def get_posts_with_comments(self, page_id: str, limit: int = 10) -> List[Dict]:
        """Get posts with their comments included"""
        posts = self.db.query(Post).filter(
            Post.page_id == page_id
        ).order_by(
            desc(Post.posted_at)
        ).limit(limit).all()
        
        result = []
        for post in posts:
            post_data = {
                "id": post.id,
                "content": post.content,
                "post_type": post.post_type,
                "like_count": post.like_count,
                "comment_count": post.comment_count,
                "share_count": post.share_count,
                "posted_at": post.posted_at,
                "comments": []
            }
            
            # Get comments for this post
            comments = self.db.query(Comment).filter(
                Comment.post_id == post.id
            ).order_by(
                desc(Comment.commented_at)
            ).limit(10).all()
            
            for comment in comments:
                post_data["comments"].append({
                    "id": comment.id,
                    "user_name": comment.user_name,
                    "content": comment.content,
                    "commented_at": comment.commented_at
                })
            
            result.append(post_data)
        
        return result
    
    def get_top_performing_posts(self, page_id: str, days: int = 30, limit: int = 5) -> List[Post]:
        """Get top performing posts based on engagement"""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        posts = self.db.query(Post).filter(
            Post.page_id == page_id,
            Post.posted_at >= cutoff_date
        ).order_by(
            desc(Post.like_count + Post.comment_count * 2 + Post.share_count * 3)
        ).limit(limit).all()
        
        return posts
    
    def get_posts_by_date_range(self, page_id: str, start_date: datetime, end_date: datetime) -> List[Post]:
        """Get posts within a specific date range"""
        posts = self.db.query(Post).filter(
            Post.page_id == page_id,
            Post.posted_at >= start_date,
            Post.posted_at <= end_date
        ).order_by(
            desc(Post.posted_at)
        ).all()
        
        return posts
    
    def get_post_engagement_stats(self, page_id: str) -> Dict:
        """Get engagement statistics for a page's posts"""
        stats = self.db.query(
            func.count(Post.id).label('total_posts'),
            func.sum(Post.like_count).label('total_likes'),
            func.sum(Post.comment_count).label('total_comments'),
            func.sum(Post.share_count).label('total_shares'),
            func.avg(Post.like_count).label('avg_likes'),
            func.avg(Post.comment_count).label('avg_comments')
        ).filter(
            Post.page_id == page_id
        ).first()
        
        return {
            "total_posts": stats.total_posts or 0,
            "total_likes": stats.total_likes or 0,
            "total_comments": stats.total_comments or 0,
            "total_shares": stats.total_shares or 0,
            "average_likes": float(stats.avg_likes or 0),
            "average_comments": float(stats.avg_comments or 0)
        }
    
    def search_posts(self, page_id: str, keyword: str, limit: int = 10) -> List[Post]:
        """Search posts by keyword in content"""
        posts = self.db.query(Post).filter(
            Post.page_id == page_id,
            Post.content.ilike(f"%{keyword}%")
        ).order_by(
            desc(Post.posted_at)
        ).limit(limit).all()
        
        return posts