from fastapi import APIRouter, HTTPException, Depends, Request
from typing import List, Optional, Dict, Any
from models import Course, CourseCreate
from routes.auth import get_current_user
from bson import ObjectId
from datetime import datetime

router = APIRouter()

@router.get("/categories")
async def get_course_categories(request: Request):
    """Get all available course categories"""
    db = request.app.mongodb
    
    # Get distinct categories from courses
    categories = await db.courses.distinct("category", {"is_published": True})
    
    # Get course count for each category
    category_info = []
    for category in categories:
        count = await db.courses.count_documents({
            "category": category, 
            "is_published": True
        })
        category_info.append({
            "name": category,
            "count": count
        })
    
    return category_info

@router.get("/featured")
async def get_featured_courses(request: Request):
    """Get featured courses for homepage"""
    db = request.app.mongodb
    
    # Get featured courses
    cursor = db.courses.find({
        "is_published": True,
        "is_featured": True
    }).sort("rating", -1).limit(6)
    
    featured_courses = []
    async for course in cursor:
        course["_id"] = str(course["_id"])
        featured_courses.append(course)
    
    return featured_courses

@router.get("/", response_model=List[Dict[str, Any]])
async def get_courses(
    request: Request,
    category: Optional[str] = None,
    difficulty: Optional[str] = None,
    limit: int = 50,
    skip: int = 0
):
    """Get all courses with optional filtering"""
    db = request.app.mongodb
    
    # Build filter
    filter_query: Dict[str, Any] = {"is_published": True}
    if category is not None:
        filter_query["category"] = category
    if difficulty is not None:
        filter_query["difficulty"] = difficulty
    
    # Get courses from database with modules
    cursor = db.courses.find(filter_query).skip(skip).limit(limit)
    courses = []
    
    async for course in cursor:
        course["_id"] = str(course["_id"])
        # Ensure modules are included
        if "modules" not in course:
            course["modules"] = []
        courses.append(course)
    
    return courses

@router.get("/enrolled")
async def get_enrolled_courses(
    request: Request,
    current_user: dict = Depends(get_current_user)
):
    """Get courses the current user is enrolled in"""
    db = request.app.mongodb
    
    # Get enrollments
    cursor = db.enrollments.find({"student_id": current_user["_id"]})
    enrollments = []
    
    async for enrollment in cursor:
        # Get course details - handle both ObjectId and string formats
        course_id = enrollment["course_id"]
        try:
            # Try to convert to ObjectId if it's not already
            if isinstance(course_id, str):
                course_id_obj = ObjectId(course_id)
            else:
                course_id_obj = course_id
                
            course = await db.courses.find_one({"_id": course_id_obj})
            
            if course:
                course["_id"] = str(course["_id"])
                enrollment["course"] = course
                enrollment["_id"] = str(enrollment["_id"])
                enrollments.append(enrollment)
            else:
                # Course not found, skip this enrollment (could be old/deleted course)
                print(f"Warning: Course {course_id} not found for enrollment {enrollment['_id']}")
                continue
                
        except Exception as e:
            print(f"Error processing enrollment {enrollment.get('_id', 'unknown')}: {e}")
            continue
    
    return enrollments

@router.get("/{course_id}", response_model=Course)
async def get_course(course_id: str, request: Request):
    """Get a specific course by ID"""
    db = request.app.mongodb
    
    try:
        course = await db.courses.find_one({"_id": ObjectId(course_id)})
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")
        
        course["_id"] = str(course["_id"])
        return course
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid course ID")

@router.post("/", response_model=Course)
async def create_course(
    course: CourseCreate,
    request: Request,
    current_user: dict = Depends(get_current_user)
):
    """Create a new course (instructors only)"""
    db = request.app.mongodb
    
    # Verify user is instructor or admin
    if current_user["role"] not in ["instructor", "admin"]:
        raise HTTPException(status_code=403, detail="Only instructors can create courses")
    
    # Create course document
    course_doc = {
        "title": course.title,
        "description": course.description,
        "category": course.category,
        "difficulty": course.difficulty,
        "duration": course.duration,
        "instructor": course.instructor,
        "modules": [],
        "thumbnail_url": course.thumbnail_url,
        "price": course.price,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "is_published": False,
        "enrollment_count": 0,
        "rating": 4.8,
        "rating_count": 0,
        "prerequisites": [],
        "learning_outcomes": [],
        "is_featured": False
    }
    
    # Save to database
    result = await db.courses.insert_one(course_doc)
    
    # Return created course
    created_course = await db.courses.find_one({"_id": result.inserted_id})
    created_course["_id"] = str(created_course["_id"])
    
    return created_course

@router.put("/{course_id}")
async def update_course(
    course_id: str,
    course_update: CourseCreate,
    request: Request,
    current_user: dict = Depends(get_current_user)
):
    """Update an existing course"""
    db = request.app.mongodb
    
    # Check if course exists
    course = await db.courses.find_one({"_id": ObjectId(course_id)})
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # Verify ownership (admin only for now since we don't track ownership)
    if current_user["role"] not in ["admin"]:
        raise HTTPException(status_code=403, detail="Not authorized to update this course")
    
    # Update course
    update_data = {
        "title": course_update.title,
        "description": course_update.description,
        "category": course_update.category,
        "difficulty": course_update.difficulty,
        "duration": course_update.duration,
        "instructor": course_update.instructor,
        "thumbnail_url": course_update.thumbnail_url,
        "price": course_update.price,
        "updated_at": datetime.utcnow()
    }
    
    await db.courses.update_one(
        {"_id": ObjectId(course_id)},
        {"$set": update_data}
    )
    
    return {"message": "Course updated successfully"}

@router.delete("/{course_id}")
async def delete_course(
    course_id: str,
    request: Request,
    current_user: dict = Depends(get_current_user)
):
    """Delete a course"""
    db = request.app.mongodb
    
    # Check if course exists
    course = await db.courses.find_one({"_id": ObjectId(course_id)})
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # Verify ownership (instructor or admin)
    if current_user["role"] not in ["admin"] and str(course["instructor_id"]) != current_user["_id"]:
        raise HTTPException(status_code=403, detail="Not authorized to delete this course")
    
    # Delete course
    await db.courses.delete_one({"_id": ObjectId(course_id)})
    
    return {"message": "Course deleted successfully"}

@router.post("/{course_id}/enroll")
async def enroll_in_course(
    course_id: str,
    request: Request,
    current_user: dict = Depends(get_current_user)
):
    """Enroll student in a course"""
    db = request.app.mongodb
    
    # Check if course exists
    course = await db.courses.find_one({"_id": ObjectId(course_id)})
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # Check if course is published
    if not course.get("is_published", False):
        raise HTTPException(status_code=400, detail="Course is not published")
    
    # Check if already enrolled
    existing_enrollment = await db.enrollments.find_one({
        "student_id": current_user["_id"],
        "course_id": course_id
    })
    
    if existing_enrollment:
        raise HTTPException(status_code=400, detail="Already enrolled in this course")
    
    # Create enrollment record
    enrollment_doc = {
        "student_id": current_user["_id"],
        "course_id": course_id,
        "enrolled_at": datetime.utcnow(),
        "status": "active",
        "progress_percentage": 0.0,
        "completed_modules": []
    }
    
    await db.enrollments.insert_one(enrollment_doc)
    
    return {"message": "Enrolled successfully"}

@router.get("/{course_id}/purchased")

@router.get("/{course_id}/progress")
async def get_course_progress(
    course_id: str,
    request: Request,
    current_user: dict = Depends(get_current_user)
):
    """Get student's progress in a course"""
    db = request.app.mongodb
    
    # Get enrollment
    enrollment = await db.enrollments.find_one({
        "student_id": current_user["_id"],
        "course_id": course_id
    })
    
    if not enrollment:
        raise HTTPException(status_code=404, detail="Not enrolled in this course")
    
    return {
        "progress_percentage": enrollment.get("progress_percentage", 0.0),
        "completed_modules": enrollment.get("completed_modules", []),
        "enrolled_at": enrollment["enrolled_at"]
    }

@router.post("/{course_id}/modules/{module_id}/complete")
async def complete_module(
    course_id: str,
    module_id: int,
    request: Request,
    current_user: dict = Depends(get_current_user)
):
    """Mark a module as completed"""
    db = request.app.mongodb
    
    # Get enrollment
    enrollment = await db.enrollments.find_one({
        "student_id": current_user["_id"],
        "course_id": course_id
    })
    
    if not enrollment:
        raise HTTPException(status_code=404, detail="Not enrolled in this course")
    
    # Get course to check module count
    course = await db.courses.find_one({"_id": ObjectId(course_id)})
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    total_modules = len(course.get("modules", []))
    if module_id >= total_modules:
        raise HTTPException(status_code=400, detail="Invalid module ID")
    
    # Update completed modules
    completed_modules = enrollment.get("completed_modules", [])
    if module_id not in completed_modules:
        completed_modules.append(module_id)
    
    # Calculate progress percentage
    progress_percentage = (len(completed_modules) / total_modules) * 100 if total_modules > 0 else 0
    
    # Update enrollment
    await db.enrollments.update_one(
        {"_id": enrollment["_id"]},
        {
            "$set": {
                "completed_modules": completed_modules,
                "progress_percentage": progress_percentage
            }
        }
    )
    
    return {"message": "Module completed", "progress_percentage": progress_percentage}

@router.get("/enrolled")
async def get_enrolled_courses(
    request: Request,
    current_user: dict = Depends(get_current_user)
):
    """Get courses the current user is enrolled in"""
    db = request.app.mongodb
    
    print(f"[ENROLLED COURSES] User ID: {current_user.get('_id', 'unknown')}")
    print(f"[ENROLLED COURSES] User ID type: {type(current_user.get('_id', 'unknown'))}")
    
    # Get enrollments
    cursor = db.enrollments.find({"student_id": current_user["_id"]})
    enrollments = []
    
    enrollment_count = 0
    async for enrollment in cursor:
        enrollment_count += 1
        print(f"[ENROLLED COURSES] Processing enrollment #{enrollment_count}: {enrollment.get('_id', 'unknown')}")
        print(f"[ENROLLED COURSES] Course ID: {enrollment.get('course_id', 'missing')} (type: {type(enrollment.get('course_id', 'missing'))})")
        
        # Get course details - handle both ObjectId and string formats
        course_id = enrollment["course_id"]
        try:
            # Try to convert to ObjectId if it's not already
            if isinstance(course_id, str):
                course_id_obj = ObjectId(course_id)
            else:
                course_id_obj = course_id
            
            print(f"[ENROLLED COURSES] Looking for course with ObjectId: {course_id_obj}")
                
            course = await db.courses.find_one({"_id": course_id_obj})
            
            if course:
                print(f"[ENROLLED COURSES] Course found: {course.get('title', 'untitled')}")
                course["_id"] = str(course["_id"])
                enrollment["course"] = course
                enrollment["_id"] = str(enrollment["_id"])
                enrollments.append(enrollment)
            else:
                # Course not found, skip this enrollment (could be old/deleted course)
                print(f"[ENROLLED COURSES] Warning: Course {course_id} not found for enrollment {enrollment['_id']}")
                continue
                
        except Exception as e:
            print(f"[ENROLLED COURSES] Error processing enrollment {enrollment.get('_id', 'unknown')}: {e}")
            print(f"[ENROLLED COURSES] Exception type: {type(e)}")
            import traceback
            traceback.print_exc()
            continue
    
    print(f"[ENROLLED COURSES] Found {len(enrollments)} valid enrollments out of {enrollment_count} total")
    return enrollments

@router.get("/{course_id}/purchased")
async def has_purchased_course(course_id: str, request: Request, current_user: dict = Depends(get_current_user)):
    db = request.app.mongodb
    buyer = current_user.get("wallet_address")
    if not buyer:
        raise HTTPException(status_code=400, detail="User has no wallet address")
    purchase = await db.purchases.find_one({"buyer": buyer.lower(), "courseId": int(course_id)})
    return {"purchased": bool(purchase)}
