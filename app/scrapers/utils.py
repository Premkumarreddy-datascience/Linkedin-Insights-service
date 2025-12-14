import random
import time
from typing import Optional

def get_random_user_agent() -> str:
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
    ]
    return random.choice(user_agents)

def rate_limit_delay(min_seconds: int = 2, max_seconds: int = 5) -> None:
    """Add random delay to avoid detection"""
    time.sleep(random.uniform(min_seconds, max_seconds))