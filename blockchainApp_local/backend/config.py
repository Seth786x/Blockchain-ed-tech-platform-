"""
Configuration settings for EdTech Hardware Learning Platform
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Database Configuration
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "edtech_hardware")

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secret-key-change-this-in-production")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Blockchain Configuration
ETHEREUM_RPC_URL = os.getenv("ETHEREUM_RPC_URL", "https://sepolia.infura.io/v3/your-infura-project-id")
PRIVATE_KEY = os.getenv("PRIVATE_KEY", "your-private-key-for-deployment")

# IPFS Configuration
IPFS_API_URL = os.getenv("IPFS_API_URL", "http://localhost:5001")

# Server Configuration
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8001"))
DEBUG = os.getenv("DEBUG", "True").lower() == "true"

# CORS Configuration
ALLOWED_ORIGINS = [
    "http://localhost:5173",  # Vite dev server
    "http://localhost:5174",  # Alternative Vite port
    "http://localhost:5175",  # Alternative Vite port
    "http://localhost:3000",  # Alternative frontend port
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
    "http://127.0.0.1:5175",
    "http://127.0.0.1:3000"
] 