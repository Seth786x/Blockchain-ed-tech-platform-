#!/usr/bin/env python3

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def check_specific_course():
    client = AsyncIOMotorClient('mongodb://localhost:27017')
    db = client.edtech_hardware
    
    # Get the specific GPU course that's being viewed
    course = await db.courses.find_one({"title": "History of GPUs"})
    
    if course:
        print(f"=== CHECKING HISTORY OF GPUs COURSE ===")
        print(f"Course ID: {course['_id']}")
        print(f"Title: {course['title']}")
        print(f"Number of modules: {len(course.get('modules', []))}")
        
        if course.get('modules'):
            for i, module in enumerate(course['modules'][:3]):  # Check first 3 modules
                print(f"\n--- Module {i+1}: {module.get('title')} ---")
                print(f"Description: {module.get('description', 'No description')}")
                content = module.get('content', '')
                print(f"Content length: {len(content)} characters")
                print(f"Content preview: {content[:200]}...")
                print(f"Order: {module.get('order', 'No order')}")
    else:
        print("❌ History of GPUs course not found!")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(check_specific_course())
