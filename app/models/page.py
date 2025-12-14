from sqlalchemy import Column, String, Integer, Text, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Page(Base):
    __tablename__ = "pages"
    
    id = Column(String(100), primary_key=True)  # LinkedIn page ID like "deepsolv"
    name = Column(String(200), nullable=False)
    url = Column(String(500))
    profile_picture = Column(String(500))
    description = Column(Text)
    website = Column(String(500))
    industry = Column(String(200))
    total_followers = Column(Integer, default=0)
    head_count = Column(String(50))
    specialities = Column(JSON)  # Store as JSON list
    company_type = Column(String(100))
    founded_year = Column(Integer)
    headquarters = Column(String(200))
    locations = Column(JSON)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    posts = relationship("Post", back_populates="page", cascade="all, delete-orphan")
    employees = relationship("SocialMediaUser", back_populates="page")
    
    def __repr__(self):
        return f"<Page(id='{self.id}', name='{self.name}', followers={self.total_followers})>"