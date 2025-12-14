from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.api.endpoints import router

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="LinkedIn Insights Service",
    description="Scrape and analyze LinkedIn company pages",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {
        "service": "LinkedIn Insights API",
        "status": "running",
        "version": "1.0.0",
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "get_page": "/api/v1/pages/{page_id}",
            "search_pages": "/api/v1/pages",
            "page_posts": "/api/v1/pages/{page_id}/posts"
        }
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "linkedin-insights"}