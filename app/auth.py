import hashlib
import secrets
from datetime import datetime, timedelta
from app.config import settings

class APIKeyManager:
    def __init__(self):
        self.api_keys = {}  # En producción: usar BD
        self.rate_limits = {}
    
    def generate_key(self, user_id: str) -> str:
        """Generate a new API key"""
        key = secrets.token_urlsafe(32)
        hashed = hashlib.sha256(key.encode()).hexdigest()
        self.api_keys[hashed] = {
            "user_id": user_id,
            "created_at": datetime.now(),
            "tier": "free",
            "requests_used": 0
        }
        return key
    
    def verify_key(self, key: str) -> dict | None:
        """Verify API key"""
        hashed = hashlib.sha256(key.encode()).hexdigest()
        return self.api_keys.get(hashed)
    
    def check_rate_limit(self, key: str) -> bool:
        """Check if key has exceeded rate limit"""
        key_data = self.verify_key(key)
        if not key_data:
            return False
        
        limits = {
            "free": 100,
            "pro": 1000,
            "enterprise": float('inf')
        }
        
        tier = key_data.get("tier", "free")
        used = key_data.get("requests_used", 0)
        limit = limits.get(tier, 100)
        
        return used < limit
    
    def increment_usage(self, key: str):
        """Increment request count"""
        hashed = hashlib.sha256(key.encode()).hexdigest()
        if hashed in self.api_keys:
            self.api_keys[hashed]["requests_used"] += 1

api_key_manager = APIKeyManager()
