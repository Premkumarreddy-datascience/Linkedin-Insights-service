from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Comment(Base):
    __tablename__ = "comments"
    
    id = Column(String(100), primary_key=True)
    post_id = Column(String(100), ForeignKey("posts.id"))
    user_name = Column(String(200))
    user_profile_url = Column(String(500))
    content = Column(Text)
    commented_at = Column(DateTime)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    post = relationship("Post", back_populates="comments")
    
    def __repr__(self):
        return f"<Comment(id='{self.id}', post='{self.post_id}')>"