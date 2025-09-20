import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def get_course_id():
    client = AsyncIOMotorClient('mongodb://localhost:27017')
    db = client.edtech_hardware
    course = await db.courses.find_one({})
    print(f"Course ID: {course['_id']}")
    print(f"Course Title: {course['title']}")
    client.close()

if __name__ == "__main__":
    asyncio.run(get_course_id())
