#!/usr/bin/env python3
"""
Database initialization script for EdTech Hardware Learning Platform
Creates sample data for testing and development
"""

import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
from passlib.context import CryptContext
from dotenv import load_dotenv

load_dotenv()

# Database connection
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "edtech_hardware")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

async def init_database():
    """Initialize database with sample data"""
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client[DATABASE_NAME]
    
    print("🚀 Initializing EdTech Hardware Learning Platform Database...")
    
    # Clear existing data (for development)
    print("🗑️  Clearing existing data...")
    await db.users.delete_many({})
    await db.courses.delete_many({})
    await db.schools.delete_many({})
    await db.donations.delete_many({})
    await db.resource_requests.delete_many({})
    await db.enrollments.delete_many({})
    
    # Create sample users
    print("👥 Creating sample users...")
    users_data = [
        {
            "email": "admin@edtech.com",
            "username": "admin",
            "full_name": "Platform Administrator",
            "role": "admin",
            "wallet_address": "0x1234567890123456789012345678901234567890",
            "hashed_password": get_password_hash("admin123"),
            "created_at": datetime.utcnow(),
            "is_active": True
        },
        {
            "email": "instructor@edtech.com",
            "username": "tech_instructor",
            "full_name": "John Smith",
            "role": "instructor",
            "wallet_address": "0x2345678901234567890123456789012345678901",
            "hashed_password": get_password_hash("instructor123"),
            "created_at": datetime.utcnow(),
            "is_active": True
        },
        {
            "email": "student@edtech.com",
            "username": "student_alice",
            "full_name": "Alice Johnson",
            "role": "student",
            "wallet_address": "0x3456789012345678901234567890123456789012",
            "hashed_password": get_password_hash("student123"),
            "created_at": datetime.utcnow(),
            "is_active": True
        },
        {
            "email": "donor@edtech.com",
            "username": "generous_donor",
            "full_name": "Bob Wilson",
            "role": "donor",
            "wallet_address": "0x4567890123456789012345678901234567890123",
            "hashed_password": get_password_hash("donor123"),
            "created_at": datetime.utcnow(),
            "is_active": True
        },
        {
            "email": "school@edtech.com",
            "username": "tech_school",
            "full_name": "Tech Academy Principal",
            "role": "school",
            "wallet_address": "0x5678901234567890123456789012345678901234",
            "hashed_password": get_password_hash("school123"),
            "created_at": datetime.utcnow(),
            "is_active": True
        }
    ]
    
    users_result = await db.users.insert_many(users_data)
    print(f"✅ Created {len(users_result.inserted_ids)} users")
    
    # Get user IDs for reference
    admin_user = await db.users.find_one({"email": "admin@edtech.com"})
    instructor_user = await db.users.find_one({"email": "instructor@edtech.com"})
    student_user = await db.users.find_one({"email": "student@edtech.com"})
    donor_user = await db.users.find_one({"email": "donor@edtech.com"})
    school_user = await db.users.find_one({"email": "school@edtech.com"})
    
    # Create sample courses
    print("📚 Creating sample courses...")
    courses_data = [
        {
            "title": "CPU Fundamentals",
            "description": "Learn the basics of Central Processing Units, their architecture, and how they work.",
            "component": "cpu",
            "level": "beginner",
            "instructor_id": str(instructor_user["_id"]),
            "modules": [
                {
                    "title": "Introduction to CPUs",
                    "description": "What is a CPU and why is it important?",
                    "content_url": "QmSampleContent1",
                    "video_url": "QmSampleVideo1",
                    "duration_minutes": 15,
                    "order": 1
                },
                {
                    "title": "CPU Architecture",
                    "description": "Understanding CPU cores, cache, and clock speed",
                    "content_url": "QmSampleContent2",
                    "video_url": "QmSampleVideo2",
                    "duration_minutes": 20,
                    "order": 2
                }
            ],
            "thumbnail_url": "QmSampleThumbnail1",
            "price": 0.01,  # 0.01 ETH
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "is_published": True
        },
        {
            "title": "GPU Deep Dive",
            "description": "Advanced course on Graphics Processing Units and parallel computing.",
            "component": "gpu",
            "level": "intermediate",
            "instructor_id": str(instructor_user["_id"]),
            "modules": [
                {
                    "title": "GPU vs CPU",
                    "description": "Understanding the differences between GPU and CPU",
                    "content_url": "QmSampleContent3",
                    "video_url": "QmSampleVideo3",
                    "duration_minutes": 18,
                    "order": 1
                },
                {
                    "title": "GPU Architecture",
                    "description": "CUDA cores, memory bandwidth, and parallel processing",
                    "content_url": "QmSampleContent4",
                    "video_url": "QmSampleVideo4",
                    "duration_minutes": 25,
                    "order": 2
                }
            ],
            "thumbnail_url": "QmSampleThumbnail2",
            "price": 0.02,  # 0.02 ETH
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "is_published": True
        },
        {
            "title": "RAM Essentials",
            "description": "Master Random Access Memory concepts and optimization.",
            "component": "ram",
            "level": "beginner",
            "instructor_id": str(instructor_user["_id"]),
            "modules": [
                {
                    "title": "What is RAM?",
                    "description": "Understanding memory types and speeds",
                    "content_url": "QmSampleContent5",
                    "video_url": "QmSampleVideo5",
                    "duration_minutes": 12,
                    "order": 1
                }
            ],
            "thumbnail_url": "QmSampleThumbnail3",
            "price": 0.005,  # 0.005 ETH
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "is_published": True
        }
    ]
    
    courses_result = await db.courses.insert_many(courses_data)
    print(f"✅ Created {len(courses_result.inserted_ids)} courses")
    
    # Create sample schools
    print("🏫 Creating sample schools...")
    schools_data = [
        {
            "name": "Tech Academy High School",
            "address": "123 Education Street, Tech City, TC 12345",
            "contact_email": "principal@techacademy.edu",
            "contact_phone": "+1-555-0123",
            "principal_name": "Dr. Sarah Johnson",
            "wallet_address": "0x6789012345678901234567890123456789012345",
            "total_students": 500,
            "verified": True,
            "created_at": datetime.utcnow()
        },
        {
            "name": "Digital Learning Center",
            "address": "456 Innovation Ave, Digital Town, DT 67890",
            "contact_email": "admin@digitallearning.edu",
            "contact_phone": "+1-555-0456",
            "principal_name": "Mr. Michael Chen",
            "wallet_address": "0x7890123456789012345678901234567890123456",
            "total_students": 300,
            "verified": False,
            "created_at": datetime.utcnow()
        }
    ]
    
    schools_result = await db.schools.insert_many(schools_data)
    print(f"✅ Created {len(schools_result.inserted_ids)} schools")
    
    # Create sample donations
    print("💰 Creating sample donations...")
    donations_data = [
        {
            "donor_id": str(donor_user["_id"]),
            "amount_eth": 0.1,
            "amount_usd": 200.0,
            "transaction_hash": "0xabc123def456ghi789jkl012mno345pqr678stu901vwx234yz567",
            "purpose": "Hardware equipment for computer labs",
            "target_school_id": str(schools_result.inserted_ids[0]),
            "status": "confirmed",
            "created_at": datetime.utcnow(),
            "confirmed_at": datetime.utcnow()
        },
        {
            "donor_id": str(donor_user["_id"]),
            "amount_eth": 0.05,
            "amount_usd": 100.0,
            "transaction_hash": "0xdef456ghi789jkl012mno345pqr678stu901vwx234yz567abc123",
            "purpose": "Software licenses for programming courses",
            "target_school_id": None,
            "status": "pending",
            "created_at": datetime.utcnow(),
            "confirmed_at": None
        }
    ]
    
    donations_result = await db.donations.insert_many(donations_data)
    print(f"✅ Created {len(donations_result.inserted_ids)} donations")
    
    # Create sample resource requests
    print("📋 Creating sample resource requests...")
    requests_data = [
        {
            "school_id": str(schools_result.inserted_ids[0]),
            "resource_type": "hardware_kit",
            "description": "Computer hardware kits for hands-on learning",
            "quantity": 25,
            "estimated_cost_usd": 5000.0,
            "priority": 5,
            "status": "approved",
            "justification": "Students need hands-on experience with real hardware components",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "school_id": str(schools_result.inserted_ids[0]),
            "resource_type": "software_license",
            "description": "Programming software licenses",
            "quantity": 50,
            "estimated_cost_usd": 2000.0,
            "priority": 4,
            "status": "pending",
            "justification": "Need development tools for programming courses",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
    ]
    
    requests_result = await db.resource_requests.insert_many(requests_data)
    print(f"✅ Created {len(requests_result.inserted_ids)} resource requests")
    
    # Create sample enrollments
    print("🎓 Creating sample enrollments...")
    enrollments_data = [
        {
            "student_id": str(student_user["_id"]),
            "course_id": str(courses_result.inserted_ids[0]),  # CPU Fundamentals
            "enrolled_at": datetime.utcnow(),
            "status": "active",
            "progress_percentage": 50.0,
            "completed_modules": [0]  # Completed first module
        },
        {
            "student_id": str(student_user["_id"]),
            "course_id": str(courses_result.inserted_ids[2]),  # RAM Essentials
            "enrolled_at": datetime.utcnow(),
            "status": "active",
            "progress_percentage": 100.0,
            "completed_modules": [0]  # Completed all modules
        }
    ]
    
    enrollments_result = await db.enrollments.insert_many(enrollments_data)
    print(f"✅ Created {len(enrollments_result.inserted_ids)} enrollments")
    
    print("\n🎉 Database initialization completed successfully!")
    print("\n📊 Sample Data Summary:")
    print(f"   👥 Users: {len(users_result.inserted_ids)}")
    print(f"   📚 Courses: {len(courses_result.inserted_ids)}")
    print(f"   🏫 Schools: {len(schools_result.inserted_ids)}")
    print(f"   💰 Donations: {len(donations_result.inserted_ids)}")
    print(f"   📋 Resource Requests: {len(requests_result.inserted_ids)}")
    print(f"   🎓 Enrollments: {len(enrollments_result.inserted_ids)}")
    
    print("\n🔑 Test Accounts:")
    print("   Admin: admin@edtech.com / admin123")
    print("   Instructor: instructor@edtech.com / instructor123")
    print("   Student: student@edtech.com / student123")
    print("   Donor: donor@edtech.com / donor123")
    print("   School: school@edtech.com / school123")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(init_database()) 