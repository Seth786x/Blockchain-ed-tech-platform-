from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from contextlib import asynccontextmanager
from typing import Any
import os
from dotenv import load_dotenv

from models import *
from routes import auth, courses, donations, resources, media
from config import MONGODB_URL, DATABASE_NAME, ALLOWED_ORIGINS
from blockchain_events import start_listener
from error_handlers import (
    validation_exception_handler,
    http_exception_handler,
    general_exception_handler,
    ErrorMiddleware
)

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    app.mongodb_client = AsyncIOMotorClient(MONGODB_URL)  # type: ignore
    app.mongodb = app.mongodb_client[DATABASE_NAME]  # type: ignore
    print(f"✅ Connected to MongoDB at {MONGODB_URL}")
    print(f"📊 Using database: {DATABASE_NAME}")
    start_listener()  # Start blockchain event listener
    yield
    
    # Shutdown
    app.mongodb_client.close()  # type: ignore
    print("🔌 Disconnected from MongoDB")

app = FastAPI(
    title="EdTech Hardware Learning Platform",
    description="Blockchain-based platform for computer hardware education with transparent donation system",
    version="1.0.0",
    lifespan=lifespan
)

# Add custom error handlers  
app.add_exception_handler(RequestValidationError, validation_exception_handler)  # type: ignore
app.add_exception_handler(StarletteHTTPException, http_exception_handler)  # type: ignore
app.add_exception_handler(Exception, general_exception_handler)  # type: ignore

# Add error logging middleware
app.add_middleware(ErrorMiddleware)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(courses.router, prefix="/api/courses", tags=["Courses"])
app.include_router(donations.router, prefix="/api/donations", tags=["Donations"])
app.include_router(resources.router, prefix="/api/resources", tags=["Resources"])
app.include_router(media.router, prefix="/api", tags=["Media & File Upload"])

@app.get("/")
async def root():
    return {
        "message": "EdTech Hardware Learning Platform API",
        "version": "1.0.0",
        "documentation": "/docs",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "database": "connected",
        "timestamp": "2024-01-01T00:00:00Z"
    }

@app.get("/api")
async def api_info():
    """Get API information and available endpoints"""
    return {
        "name": "EdTech Hardware Learning Platform API",
        "version": "1.0.0",
        "endpoints": {
            "authentication": "/api/auth",
            "courses": "/api/courses", 
            "donations": "/api/donations",
            "resources": "/api/resources"
        },
        "documentation": "/docs",
        "openapi_schema": "/openapi.json"
    }

if __name__ == "__main__":
    import uvicorn
    from config import HOST, PORT, DEBUG
    
    print("🚀 Starting EdTech Hardware Learning Platform Backend...")
    print(f"🌐 Server will run on: http://{HOST}:{PORT}")
    print(f"📚 API Documentation: http://{HOST}:{PORT}/docs")
    
    uvicorn.run(
        "main:app", 
        host=HOST, 
        port=PORT, 
        reload=DEBUG,
        log_level="info"
    )
