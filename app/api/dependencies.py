from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.page_service import PageService
from app.services.post_service import PostService
from app.services.user_service import UserService

def get_page_service(db: Session = Depends(get_db)) -> PageService:
    return PageService(db)

def get_post_service(db: Session = Depends(get_db)) -> PostService:
    return PostService(db)

def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)