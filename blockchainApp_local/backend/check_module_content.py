import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def check_module_content():
    client = AsyncIOMotorClient('mongodb://localhost:27017')
    db = client.edtech_hardware
    
    # Get a sample course
    course = await db.courses.find_one({})
    
    print(f"=== CHECKING COURSE MODULE CONTENT ===")
    print(f"Sample course: {course.get('title', 'unknown')}")
    
    if 'modules' in course and course['modules']:
        print(f"Number of modules: {len(course['modules'])}")
        
        # Check first module
        first_module = course['modules'][0]
        print(f"\n--- Module 1 Structure ---")
        print(f"Title: {first_module.get('title', 'missing')}")
        print(f"Available keys: {list(first_module.keys())}")
        
        if 'content' in first_module:
            content = first_module['content']
            print(f"Content type: {type(content)}")
            print(f"Content length: {len(content)} characters")
            print(f"\n--- Content Preview (first 300 chars) ---")
            print(content[:300] + "...")
        else:
            print("❌ No 'content' field found!")
            
        # Check if there are other content fields
        for key in first_module.keys():
            if key not in ['title', 'duration', 'order']:
                value = first_module[key]
                if isinstance(value, str) and len(value) > 50:
                    print(f"\n--- {key.upper()} field ---")
                    print(f"Length: {len(value)} characters")
                    print(f"Preview: {value[:200]}...")
    else:
        print("❌ No modules found in course!")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(check_module_content())
