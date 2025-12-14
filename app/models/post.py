from sqlalchemy import Column, String, Integer, Text, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Post(Base):
    __tablename__ = "posts"
    
    id = Column(String(100), primary_key=True)
    page_id = Column(String(100), ForeignKey("pages.id"))
    content = Column(Text)
    post_type = Column(String(50))  # 'post', 'repost', 'video', etc.
    media_urls = Column(JSON)
    like_count = Column(Integer, default=0)
    comment_count = Column(Integer, default=0)
    share_count = Column(Integer, default=0)
    posted_at = Column(DateTime)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    page = relationship("Page", back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Post(id='{self.id}', page='{self.page_id}', type='{self.post_type}')>"