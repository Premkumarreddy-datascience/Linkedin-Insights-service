# Linkedin Insights Service

A **production-style FastAPI backend** that scrapes, stores, and analyzes LinkedIn company data such as **company pages, posts, employees, and engagement metrics**.

This project is designed with **clean architecture**, **service-layer abstraction**, **Docker-based deployment**, and **RESTful APIs**.

---

## Key Features

-  Fetch or scrape LinkedIn company pages
-  Store and retrieve company posts
-  Engagement analytics
-  Employee listing, search, and distribution analysis
-  Auto-refresh outdated data
-  Fully Dockerized (FastAPI + MySQL)
-  Postman collection for API testing
-  Pytest-based backend tests

---

## Tech Stack

The project uses a modern, production-ready technology stack focused on performance, scalability, and maintainability.

| Category | Technology | Purpose |
|--------|-----------|---------|
| Backend Framework | FastAPI | High-performance API framework for building RESTful services |
| Programming Language | Python | Core backend development language |
| ASGI Server | Uvicorn | Runs the FastAPI application |
| ORM | SQLAlchemy | Database ORM for query building and model management |
| Data Validation | Pydantic | Request/response validation and serialization |
| Database | MySQL | Relational database for persistent storage |
| Database Driver | PyMySQL | Python–MySQL database connector |
| API Documentation | Swagger UI (OpenAPI) | Interactive API documentation |
| Testing Framework | Pytest | Unit and API testing |
| Async HTTP Client | HTTPX | Used for API testing |
| Environment Management | python-dotenv | Load environment variables securely |
| Migrations | Alembic | Database schema migrations |
| Message Broker | Redis | Used with Celery for async tasks |
| Containerization | Docker | Application containerization |
| Version Control | Git | Source code version control |
| IDE / Editor | VS Code | Development environment |
| OS | Windows / Linux | Development & deployment environments |


## Project Structure

```
Linkedin-Insights-service/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── schemas.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── page.py
│   │   ├── post.py
│   │   ├── user.py
│   │   └── comment.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── page_service.py
│   │   ├── post_service.py
│   │   ├── user_service.py
│   │   └── comment_service.py
│   ├── scrapers/
│   │   ├── __init__.py
│   │   └── linkedin_scraper.py
│   └── api/
│       ├── __init__.py
│       ├── endpoints.py
│       └── dependencies.py
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env
├── Postman Collection.json
├── tests/
│   ├── __init__.py
│   ├── test_health.py
│   ├── test_pages.py
│   ├── test_posts.py
│   └── test_search.py
└── README.md
```

## Requirements

To run this project successfully, ensure the following software and system requirements are met.

### Software Requirements
- Python **3.9 or higher**
- MySQL **8.0 or higher**
- Docker **20+**
- Docker Compose **v2+**
- Git
- Postman (for API testing)

### Python Dependencies
All required Python packages are listed in `requirements.txt`

### System Requirements
- Minimum **4 GB RAM** (8 GB recommended)
- Minimum **10 GB free disk space**
- Stable internet connection (for scraping)

### Network / Port Requirements
Ensure the following ports are available:
- **8000** → FastAPI service
- **3307** → MySQL database
- **6379** → Redis (optional)

### Supported Operating Systems
- Windows 10 / 11
- Linux (Ubuntu 20.04+ recommended)
- macOS (Docker-based)


## Database Schema

The project uses MySQL with the following core tables:
- pages
- posts
- comments
- social_media_users

Each table is linked using foreign keys for relational integrity.

## Configuration

### Environment Variables
Create .env file:
```bash
#Database
DATABASE_URL=mysql+pymysql://username:password@db:3307/linkedin_db
REDIS_URL=redis://redis:6379/0
#Scraping
SCRAPE_TIMEOUT=30
MAX_POSTS_PER_PAGE=25
CACHE_TTL=3600
```

##  Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Application

```bash
# Clone/Create project folder
git clone <repo-url>   # or create manually
cd Linkedin-Insights-service

# Start all services
docker-compose up -d

# Check status
docker-compose ps
```

### 3. Verify It's Working

```bash
# Test the API
curl http://localhost:8000/

# Should return:
# {"message":"LinkedIn Insights Service API","status":"running"}

# Open API documentation
# Browser: http://localhost:8000/docs
```

### 4. View Logs
```bash
# view all logs
docker-compose logs

# Follow web service logs
docker-compose logs -f web

# Check specific service
docker-compose logs db
docker-compose logs redis
```

## Check Database
```bash
# Connect to MySQL
docker-compose exec db mysql -uroot -p linkedin_db

# Common queries
SHOW TABLES;
SELECT * FROM pages LIMIT 5;
```

## Database Seeding (CMD+SQL)
### Open MySQL inside Docker
```bash
docker-compose exec db mysql -u root -p
```
Password
```bash
Enter passwrod
```
USE the database which has been created:
```sql
USE linkedin_db;
```
### Insert Pages
```sql
Insert Records into all tables pages, posts, users, comments
```
### Verify Query
```sql
SELECT COUNT(*) FROM pages;
SELECT page_id, COUNT(*) FROM posts GROUP BY page_id;
SELECT page_id, COUNT(*) FROM social_media_users GROUP BY page_id;
```


## Access Points

| Service | URL |
| :--- | :--- |
| API | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |
| MySQL | localhost:3307 |
| Redis | localhost:6379 |

## API Endpoints Summary
### Health
```
GET /api/v1/health/db
```

### Pages
```
GET /api/v1/pages/{page_id}

GET /api/v1/pages
```

### Posts
```
GET /api/v1/pages/{page_id}/posts/recent

GET /api/v1/pages/{page_id}/posts/with-comments

GET /api/v1/pages/{page_id}/posts/search

GET /api/v1/pages/{page_id}/top-posts

GET /api/v1/pages/{page_id}/engagement
```

### Employees
```
GET /api/v1/pages/{page_id}/employees

GET /api/v1/pages/{page_id}/employees/search

GET /api/v1/pages/{page_id}/employees/distribution

GET /api/v1/pages/{page_id}/employees/recent
```

## Testing
```bash
docker-compose exec web pytest
```
This will test Database Connection and all Service Layers

## Postman Usage
- Import Postman Collection.JSON file into Postman
- set variables:
```
base_url = http://localhost:8000/api/v1
page_id = google
```
Change page_id to test any company






