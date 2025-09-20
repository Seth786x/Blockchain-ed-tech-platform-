"""
Security utilities and validation functions
"""
import re
import hashlib
from web3 import Web3
from typing import Optional

def validate_ethereum_address(address: str) -> bool:
    """Validate Ethereum address format"""
    if not address or not isinstance(address, str):
        return False
    
    # Check if it's a valid hex string with 0x prefix
    if not re.match(r'^0x[a-fA-F0-9]{40}$', address):
        return False
    
    return Web3.is_address(address)

def validate_transaction_hash(tx_hash: str) -> bool:
    """Validate Ethereum transaction hash format"""
    if not tx_hash or not isinstance(tx_hash, str):
        return False
    
    return re.match(r'^0x[a-fA-F0-9]{64}$', tx_hash) is not None

def sanitize_string_input(input_str: str, max_length: int = 255) -> str:
    """Sanitize string input to prevent injection attacks"""
    if not input_str:
        return ""
    
    # Remove potentially dangerous characters
    sanitized = re.sub(r'[<>"\']', '', input_str)
    
    # Truncate to max length
    return sanitized[:max_length].strip()

def validate_donation_amount(amount_eth: float) -> bool:
    """Validate donation amount"""
    if not isinstance(amount_eth, (int, float)):
        return False
    
    # Minimum 0.000001 ETH, Maximum 1000 ETH
    return 0.000001 <= amount_eth <= 1000.0

def generate_secure_token() -> str:
    """Generate a secure random token"""
    import secrets
    return secrets.token_urlsafe(32)

class RateLimiter:
    """Simple in-memory rate limiter"""
    def __init__(self):
        self.requests = {}
    
    def is_allowed(self, key: str, max_requests: int = 10, window_seconds: int = 60) -> bool:
        """Check if request is allowed based on rate limiting"""
        import time
        
        current_time = time.time()
        
        if key not in self.requests:
            self.requests[key] = []
        
        # Remove old requests outside the window
        self.requests[key] = [
            req_time for req_time in self.requests[key] 
            if current_time - req_time < window_seconds
        ]
        
        # Check if under limit
        if len(self.requests[key]) < max_requests:
            self.requests[key].append(current_time)
            return True
        
        return False

# Global rate limiter instance
rate_limiter = RateLimiter()
