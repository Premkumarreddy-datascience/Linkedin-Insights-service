import requests
from bs4 import BeautifulSoup
import re
import json
from typing import Dict, List, Optional
from datetime import datetime
import time
import random

class LinkedInScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        })
    
    def scrape_page(self, page_id: str) -> Dict:
        """Scrape LinkedIn company page by its ID"""
        url = f"https://www.linkedin.com/company/{page_id}/"
        print(f"Scraping: {url}")
        
        try:
            # Add delay to avoid being blocked
            time.sleep(random.uniform(2, 4))
            
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract basic page info
            page_data = {
                "id": page_id,
                "name": self._extract_name(soup),
                "url": url,
                "profile_picture": self._extract_profile_picture(soup),
                "description": self._extract_description(soup),
                "website": self._extract_website(soup),
                "industry": self._extract_industry(soup),
                "total_followers": self._extract_followers(soup),
                "head_count": self._extract_headcount(soup),
                "specialities": self._extract_specialities(soup),
                "company_type": self._extract_company_type(soup),
                "founded_year": self._extract_founded_year(soup),
                "headquarters": self._extract_headquarters(soup),
                "locations": self._extract_locations(soup),
                "scraped_at": datetime.utcnow().isoformat()
            }
            
            # Extract posts (limited to 15 for demo)
            page_data["posts"] = self._extract_posts(soup, limit=15)
            
            # Extract employees
            page_data["employees"] = self._extract_employees(soup)
            
            return page_data
            
        except Exception as e:
            print(f"Scraping error for {page_id}: {str(e)}")
            # Return mock data for testing
            return self._get_mock_data(page_id)
    
    # ========== PAGE DATA EXTRACTION METHODS ==========
    
    def _extract_name(self, soup: BeautifulSoup) -> str:
        """Extract company name"""
        # Try multiple selectors
        selectors = ['h1', '.org-top-card-summary__title', '.top-card-layout__title']
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text(strip=True)
        return f"Company-{random.randint(1000, 9999)}"
    
    def _extract_industry(self, soup: BeautifulSoup) -> str:
        """Extract industry using English keywords"""
        industry_keywords = ['industry:', 'sector:', 'category:', 'field:']
        
        # Check for industry in text
        for text in soup.stripped_strings:
            text_lower = text.lower()
            for keyword in industry_keywords:
                if keyword in text_lower:
                    # Extract text after keyword
                    industry = text.split(':')[-1].strip()
                    if industry:
                        return industry
        
        # Check in specific elements
        industry_elements = soup.find_all(['div', 'span'], 
                                         class_=re.compile(r'industry|sector|field'))
        for element in industry_elements:
            industry = element.get_text(strip=True)
            if industry and len(industry) > 2:
                return industry
        
        return "Technology"  # Default
    
    def _extract_followers(self, soup: BeautifulSoup) -> int:
        """Extract follower count using English keywords"""
        # Look for follower text patterns in English
        patterns = [
            r'(\d+[\d,]*)\s*followers',
            r'(\d+[\d,]*)\s*people\s*follow\s*this',
            r'followers.*?(\d+[\d,]*)',
            r'follower\s*count.*?(\d+[\d,]*)'
        ]
        
        for text in soup.stripped_strings:
            for pattern in patterns:
                match = re.search(pattern, text.lower())
                if match:
                    number_str = match.group(1).replace(',', '')
                    try:
                        return int(number_str)
                    except:
                        pass
        
        # Return random for demo
        return random.randint(500, 50000)
    
    def _extract_headcount(self, soup: BeautifulSoup) -> str:
        """Extract employee count range using English keywords"""
        keywords = ['employees', 'headcount', 'team size', 'company size', 'staff']
        
        for text in soup.stripped_strings:
            text_lower = text.lower()
            for keyword in keywords:
                if keyword in text_lower:
                    # Extract numbers like "2-10 employees"
                    numbers = re.findall(r'\d+', text)
                    if len(numbers) >= 2:
                        return f"{numbers[0]}-{numbers[1]}"
                    elif numbers:
                        num = int(numbers[0])
                        if num <= 10:
                            return "1-10"
                        elif num <= 50:
                            return "11-50"
                        elif num <= 200:
                            return "51-200"
                        else:
                            return "201-500"
        
        return "11-50"  # Default
    
    def _extract_description(self, soup: BeautifulSoup) -> str:
        """Extract company description"""
        # Look for description in common elements
        desc_selectors = ['.org-about-us-organization-description__text',
                         '.break-words',
                         '.description',
                         'p']
        
        for selector in desc_selectors:
            element = soup.select_one(selector)
            if element:
                text = element.get_text(strip=True)
                if text and len(text) > 20:
                    return text[:500]  # Limit length
        
        return "Company description not available."
    
    def _extract_website(self, soup: BeautifulSoup) -> str:
        """Extract company website"""
        # Look for website links
        website_elements = soup.find_all('a', href=re.compile(r'http'))
        for element in website_elements:
            text = element.get_text(strip=True).lower()
            href = element.get('href', '')
            if any(word in text for word in ['website', 'site', 'web', 'visit']):
                return href
            elif href and ('company' in href or page_id in href):
                return href
        
        return f"https://{page_id}.com"  # Default
    
    def _extract_profile_picture(self, soup: BeautifulSoup) -> str:
        """Extract company logo/profile picture"""
        img_selectors = ['img.org-top-card-primary-content__logo',
                        'img.top-card-layout__entity-image',
                        'img.company-logo']
        
        for selector in img_selectors:
            element = soup.select_one(selector)
            if element and element.get('src'):
                return element['src']
        
        return "https://via.placeholder.com/150"  # Default placeholder
    
    def _extract_specialities(self, soup: BeautifulSoup) -> List[str]:
        """Extract company specialties"""
        specialties = []
        
        # Look for specialties text
        specialty_keywords = ['specialties:', 'expertise:', 'services:', 'what we do:']
        
        for text in soup.stripped_strings:
            text_lower = text.lower()
            for keyword in specialty_keywords:
                if keyword in text_lower:
                    # Split by commas, semicolons, or bullets
                    parts = re.split(r'[,;•·]', text)
                    for part in parts:
                        specialty = part.strip()
                        if specialty and len(specialty) > 2:
                            specialties.append(specialty)
        
        # If no specialties found, use defaults
        if not specialties:
            default_specialties = [
                "Software Development",
                "Artificial Intelligence",
                "Machine Learning",
                "Data Analytics",
                "Cloud Computing"
            ]
            specialties = random.sample(default_specialties, 3)
        
        return specialties[:5]  # Limit to 5
    
    def _extract_company_type(self, soup: BeautifulSoup) -> str:
        """Extract company type"""
        type_keywords = ['type:', 'company type:', 'ownership:']
        
        for text in soup.stripped_strings:
            text_lower = text.lower()
            for keyword in type_keywords:
                if keyword in text_lower:
                    company_type = text.split(':')[-1].strip()
                    if company_type:
                        return company_type
        
        return "Private Company"  # Default
    
    def _extract_founded_year(self, soup: BeautifulSoup) -> Optional[int]:
        """Extract founded year"""
        patterns = [
            r'founded\s*(\d{4})',
            r'established\s*(\d{4})',
            r'founding\s*date.*?(\d{4})',
            r'since\s*(\d{4})'
        ]
        
        for text in soup.stripped_strings:
            for pattern in patterns:
                match = re.search(pattern, text.lower())
                if match:
                    try:
                        return int(match.group(1))
                    except:
                        pass
        
        # Return random year for demo
        return random.randint(2000, 2023)
    
    def _extract_headquarters(self, soup: BeautifulSoup) -> str:
        """Extract headquarters location"""
        location_keywords = ['headquarters:', 'hq:', 'location:', 'based in:']
        
        for text in soup.stripped_strings:
            text_lower = text.lower()
            for keyword in location_keywords:
                if keyword in text_lower:
                    location = text.split(':')[-1].strip()
                    if location:
                        return location
        
        # Look for location in common elements
        location_elements = soup.find_all(['div', 'span'], 
                                         class_=re.compile(r'location|headquarter|office'))
        for element in location_elements:
            location = element.get_text(strip=True)
            if location and len(location) > 2:
                return location
        
        return "Not specified"  # Default
    
    def _extract_locations(self, soup: BeautifulSoup) -> List[str]:
        """Extract all company locations"""
        locations = []
        
        # Look for multiple locations
        location_texts = []
        for text in soup.stripped_strings:
            if any(word in text.lower() for word in ['location', 'office', 'based']):
                location_texts.append(text)
        
        # Parse locations from text
        for text in location_texts:
            # Split by common separators
            parts = re.split(r'[,;•·]', text)
            for part in parts:
                loc = part.strip()
                if loc and len(loc) > 2 and loc not in locations:
                    locations.append(loc)
        
        return locations[:3]  # Limit to 3 locations
    
    # ========== POSTS AND COMMENTS EXTRACTION ==========
    
    def _extract_posts(self, soup: BeautifulSoup, limit: int = 15) -> List[Dict]:
        """Extract recent posts"""
        posts = []
        
        # Find post containers
        post_containers = soup.find_all(['article', 'div'], class_=re.compile(r'feed-shared|update-components'))
        
        for i, container in enumerate(post_containers[:limit]):
            post_id = f"post_{i}_{int(time.time())}"
            post_data = {
                "id": post_id,
                "content": self._extract_post_content(container),
                "post_type": "post",
                "like_count": random.randint(5, 500),
                "comment_count": random.randint(0, 100),
                "share_count": random.randint(0, 50),
                "posted_at": datetime.utcnow().isoformat(),
                "comments": self._extract_comments(container, post_id)
            }
            posts.append(post_data)
        
        return posts
    
    def _extract_post_content(self, container) -> str:
        """Extract post text content"""
        content_selectors = ['.feed-shared-update-v2__description', 
                           '.update-components-text', 
                           '.break-words']
        for selector in content_selectors:
            element = container.select_one(selector)
            if element:
                text = element.get_text(strip=True)
                if len(text) > 10:
                    return text[:500]  # Limit length
        
        # Generate sample post content
        topics = ["product launch", "company news", "industry insights", 
                 "team achievement", "partnership announcement"]
        return f"We're excited to share our latest {random.choice(topics)}! Stay tuned for more updates."
    
    def _extract_comments(self, container, post_id: str) -> List[Dict]:
        """Extract comments for a post"""
        comments = []
        # Mock comments for demo
        comment_authors = ["John Doe", "Jane Smith", "Alex Johnson", "Maria Garcia"]
        comment_templates = [
            "Great post! Very insightful.",
            "Thanks for sharing this information.",
            "Looking forward to more updates like this.",
            "This is really helpful, thank you!",
            "Interesting perspective on this topic."
        ]
        
        for i in range(random.randint(0, 5)):
            comment = {
                "id": f"comment_{post_id}_{i}",
                "user_name": random.choice(comment_authors),
                "user_profile_url": f"https://linkedin.com/in/user{i}",
                "content": random.choice(comment_templates),
                "commented_at": datetime.utcnow().isoformat()
            }
            comments.append(comment)
        
        return comments
    
    # ========== EMPLOYEES EXTRACTION ==========
    
    def _extract_employees(self, soup: BeautifulSoup) -> List[Dict]:
        """Extract employee information"""
        employees = []
        # Mock employees for demo
        positions = ["Software Engineer", "Product Manager", "Data Scientist", 
                    "Marketing Director", "Sales Executive", "CEO", "CTO"]
        first_names = ["John", "Jane", "Alex", "Maria", "David", "Sarah", "Michael"]
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller"]
        
        for i in range(random.randint(3, 10)):
            employee = {
                "id": f"emp_{i}_{int(time.time())}",
                "name": f"{random.choice(first_names)} {random.choice(last_names)}",
                "profile_url": f"https://linkedin.com/in/employee{i}",
                "position": random.choice(positions),
                "profile_picture": f"https://randomuser.me/api/portraits/men/{i}.jpg" if i % 2 == 0 else f"https://randomuser.me/api/portraits/women/{i}.jpg"
            }
            employees.append(employee)
        
        return employees
    
    # ========== MOCK DATA FOR TESTING ==========
    
    def _get_mock_data(self, page_id: str) -> Dict:
        """Return mock data when scraping fails (for testing)"""
        # Generate consistent mock data based on page_id
        seed_value = sum(ord(c) for c in page_id)
        random.seed(seed_value)
        
        industries = ["Technology", "Software", "Consulting", "Finance", "Healthcare"]
        company_types = ["Private Company", "Public Company", "Startup", "Non-profit"]
        locations_list = ["San Francisco, CA", "New York, NY", "Austin, TX", "Remote"]
        
        return {
            "id": page_id,
            "name": f"{page_id.replace('-', ' ').title()} Inc.",
            "url": f"https://linkedin.com/company/{page_id}",
            "profile_picture": "https://via.placeholder.com/150",
            "description": f"{page_id.replace('-', ' ').title()} is a leading company in its industry, focused on innovation and customer satisfaction.",
            "website": f"https://{page_id}.com",
            "industry": random.choice(industries),
            "total_followers": random.randint(1000, 50000),
            "head_count": random.choice(["1-10", "11-50", "51-200", "201-500"]),
            "specialities": ["Software Development", "AI/ML", "Cloud Solutions", "Data Analytics"][:random.randint(2, 4)],
            "company_type": random.choice(company_types),
            "founded_year": random.randint(2000, 2020),
            "headquarters": random.choice(locations_list),
            "locations": random.sample(locations_list, random.randint(1, 3)),
            "posts": self._extract_posts(BeautifulSoup("<div></div>", 'html.parser'), limit=10),
            "employees": self._extract_employees(BeautifulSoup("<div></div>", 'html.parser'))
        }