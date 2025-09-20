#!/usr/bin/env python3

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def check_course_titles():
    """Check all course titles to see which ones we can enhance"""
    # Connect to MongoDB
    client = AsyncIOMotorClient('mongodb://localhost:27017')
    db = client.edtech_platform
    courses_collection = db.courses
    
    # Get all courses
    courses = await courses_collection.find({}).to_list(length=None)
    
    print("Available courses:")
    for course in courses:
        title = course.get('title', 'Untitled')
        modules_count = len(course.get('modules', []))
        print(f"- {title} ({modules_count} modules)")
        
        # Show first module content length as example
        if course.get('modules'):
            first_module = course['modules'][0]
            content_length = len(first_module.get('content', ''))
            print(f"  First module content length: {content_length} characters")
            if content_length < 200:
                print(f"  Sample content: {first_module.get('content', '')[:100]}...")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(check_course_titles())
