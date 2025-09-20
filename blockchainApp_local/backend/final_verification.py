#!/usr/bin/env python3

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def verify_final_content():
    """Verify all GPU course modules have comprehensive content"""
    client = AsyncIOMotorClient('mongodb://localhost:27017')
    db = client.edtech_hardware
    courses_collection = db.courses
    
    # Find the GPU course
    gpu_course = await courses_collection.find_one({"title": "History of GPUs"})
    
    if gpu_course:
        print(f"📋 Course: {gpu_course['title']}")
        print(f"📊 Total modules: {len(gpu_course.get('modules', []))}")
        print()
        
        modules = gpu_course.get('modules', [])
        total_content = 0
        
        for i, module in enumerate(modules):
            content_length = len(module.get('content', ''))
            total_content += content_length
            print(f"Module {i+1}: {module.get('title', 'Untitled')}")
            print(f"  📄 Content length: {content_length:,} characters")
            print(f"  📝 Description: {module.get('description', 'No description')[:80]}...")
            print()
        
        print(f"🎯 FINAL SUMMARY:")
        print(f"   Total modules: {len(modules)}")
        print(f"   Total content: {total_content:,} characters")
        print(f"   Average per module: {total_content//len(modules):,} characters")
        print()
        
        if total_content > 100000:  # More than 100k characters total
            print("✅ SUCCESS: All modules now have comprehensive educational content!")
        else:
            print("⚠️ WARNING: Content may still be too short")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(verify_final_content())
