from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')
db = client.edtech_hardware

print(f'Total courses: {db.courses.count_documents({})}')
print('\nCourses by category:')

categories = db.courses.distinct('category')
for cat in sorted(categories):
    count = db.courses.count_documents({"category": cat})
    print(f'  {cat}: {count}')

print('\nAll course titles:')
courses = list(db.courses.find({}, {"title": 1, "category": 1}).sort("category", 1))
for course in courses:
    print(f'  • {course["title"]} ({course["category"]})')

client.close()
