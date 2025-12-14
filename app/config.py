from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "LinkedIn Insights Service"
    database_url: str = "mysql+pymysql://user:password@localhost/linkedin_insights"
    redis_url: str = "redis://localhost:6379/0"
    scrape_timeout: int = 30
    max_posts_per_page: int = 25
    cache_ttl: int = 3600  # 1 hour
    
    class Config:
        env_file = ".env"

settings = Settings()