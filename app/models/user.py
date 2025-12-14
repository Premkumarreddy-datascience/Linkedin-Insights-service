from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class SocialMediaUser(Base):
    __tablename__ = "social_media_users"
    
    id = Column(String(100), primary_key=True)
    page_id = Column(String(100), ForeignKey("pages.id"))
    name = Column(String(200))
    profile_url = Column(String(500))
    profile_picture = Column(String(500))
    position = Column(String(200))
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    page = relationship("Page", back_populates="employees")
    
    def __repr__(self):
        return f"<User(name='{self.name}', position='{self.position}')>"