from sqlalchemy.orm import Session
from typing import List, Dict, Optional
from sqlalchemy import func

from app.models.user import SocialMediaUser
from app.models.page import Page

class UserService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_page_employees(self, page_id: str, limit: int = 20) -> List[SocialMediaUser]:
        """Get employees for a specific page"""
        employees = self.db.query(SocialMediaUser).filter(
            SocialMediaUser.page_id == page_id
        ).limit(limit).all()
        
        return employees
    
    def get_employee_by_position(self, page_id: str, position_keyword: str) -> List[SocialMediaUser]:
        """Get employees by position/keyword"""
        employees = self.db.query(SocialMediaUser).filter(
            SocialMediaUser.page_id == page_id,
            SocialMediaUser.position.ilike(f"%{position_keyword}%")
        ).all()
        
        return employees
    
    def get_employee_distribution(self, page_id: str) -> Dict:
        """Get distribution of employees by position"""
        # Group by position and count
        results = self.db.query(
            SocialMediaUser.position,
            func.count(SocialMediaUser.id).label('count')
        ).filter(
            SocialMediaUser.page_id == page_id,
            SocialMediaUser.position.isnot(None)
        ).group_by(
            SocialMediaUser.position
        ).all()
        
        distribution = {}
        for position, count in results:
            distribution[position] = count
        
        return distribution
    
    def search_employees(self, page_id: str, name_keyword: str) -> List[SocialMediaUser]:
        """Search employees by name"""
        employees = self.db.query(SocialMediaUser).filter(
            SocialMediaUser.page_id == page_id,
            SocialMediaUser.name.ilike(f"%{name_keyword}%")
        ).all()
        
        return employees
    
    def get_total_employee_count(self, page_id: str) -> int:
        """Get total number of employees for a page"""
        count = self.db.query(func.count(SocialMediaUser.id)).filter(
            SocialMediaUser.page_id == page_id
        ).scalar()
        
        return count or 0
    
    def get_recently_added_employees(self, page_id: str, limit: int = 10) -> List[SocialMediaUser]:
        """Get most recently added employees"""
        employees = self.db.query(SocialMediaUser).filter(
            SocialMediaUser.page_id == page_id
        ).order_by(
            SocialMediaUser.created_at.desc()
        ).limit(limit).all()
        
        return employees