from fastapi import APIRouter, HTTPException, Depends, Request
from typing import List, Optional
from models import ResourceRequest, ResourceRequestCreate, School, SchoolCreate, ResourceType
from routes.auth import get_current_user
from bson import ObjectId
from datetime import datetime

router = APIRouter()

@router.get("/schools", response_model=List[School])
async def get_schools(
    request: Request,
    verified: Optional[bool] = None,
    limit: int = 20,
    skip: int = 0
):
    """Get all schools with optional filtering"""
    db = request.app.mongodb
    
    # Build filter
    filter_query = {}
    if verified is not None:
        filter_query["verified"] = verified
    
    # Get schools from database
    cursor = db.schools.find(filter_query).skip(skip).limit(limit)
    schools = []
    
    async for school in cursor:
        school["_id"] = str(school["_id"])
        schools.append(school)
    
    return schools

@router.get("/schools/{school_id}", response_model=School)
async def get_school(school_id: str, request: Request):
    """Get a specific school by ID"""
    db = request.app.mongodb
    
    try:
        school = await db.schools.find_one({"_id": ObjectId(school_id)})
        if not school:
            raise HTTPException(status_code=404, detail="School not found")
        
        school["_id"] = str(school["_id"])
        return school
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid school ID")

@router.post("/schools", response_model=School)
async def create_school(
    school: SchoolCreate,
    request: Request,
    current_user: dict = Depends(get_current_user)
):
    """Register a new school"""
    db = request.app.mongodb
    
    # Verify user is school admin or admin
    if current_user["role"] not in ["school", "admin"]:
        raise HTTPException(status_code=403, detail="Only school administrators can register schools")
    
    # Check if school with this wallet already exists
    existing_school = await db.schools.find_one({"wallet_address": school.wallet_address})
    if existing_school:
        raise HTTPException(status_code=400, detail="School with this wallet address already exists")
    
    # Create school document
    school_doc = {
        "name": school.name,
        "address": school.address,
        "contact_email": school.contact_email,
        "contact_phone": school.contact_phone,
        "principal_name": school.principal_name,
        "wallet_address": school.wallet_address,
        "total_students": school.total_students,
        "verified": False,
        "created_at": datetime.utcnow()
    }
    
    # Save to database
    result = await db.schools.insert_one(school_doc)
    
    # Return created school
    created_school = await db.schools.find_one({"_id": result.inserted_id})
    created_school["_id"] = str(created_school["_id"])
    
    return created_school

@router.put("/schools/{school_id}/verify")
async def verify_school(
    school_id: str,
    request: Request,
    current_user: dict = Depends(get_current_user)
):
    """Verify a school (admin only)"""
    db = request.app.mongodb
    
    # Verify admin role
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Only admins can verify schools")
    
    # Check if school exists
    school = await db.schools.find_one({"_id": ObjectId(school_id)})
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    
    # Update school verification status
    await db.schools.update_one(
        {"_id": ObjectId(school_id)},
        {"$set": {"verified": True}}
    )
    
    return {"message": "School verified successfully"}

@router.get("/requests", response_model=List[ResourceRequest])
async def get_resource_requests(
    request: Request,
    status: Optional[str] = None,
    school_id: Optional[str] = None,
    limit: int = 20,
    skip: int = 0,
    current_user: dict = Depends(get_current_user)
):
    """Get resource requests with optional filtering"""
    db = request.app.mongodb
    
    # Build filter based on user role
    filter_query = {}
    
    if current_user["role"] == "school":
        # Schools can only see their own requests
        filter_query["school_id"] = current_user["_id"]
    elif current_user["role"] not in ["admin", "instructor"]:
        # Students can see approved requests
        filter_query["status"] = "approved"
    
    if status:
        filter_query["status"] = status
    if school_id:
        filter_query["school_id"] = school_id
    
    # Get requests from database
    cursor = db.resource_requests.find(filter_query).sort("created_at", -1).skip(skip).limit(limit)
    requests = []
    
    async for req in cursor:
        req["_id"] = str(req["_id"])
        requests.append(req)
    
    return requests

@router.get("/requests/{request_id}", response_model=ResourceRequest)
async def get_resource_request(
    request_id: str,
    request: Request,
    current_user: dict = Depends(get_current_user)
):
    """Get a specific resource request by ID"""
    db = request.app.mongodb
    
    try:
        req = await db.resource_requests.find_one({"_id": ObjectId(request_id)})
        if not req:
            raise HTTPException(status_code=404, detail="Resource request not found")
        
        # Check access control
        if current_user["role"] == "school" and req["school_id"] != current_user["_id"]:
            raise HTTPException(status_code=403, detail="Not authorized to view this request")
        
        req["_id"] = str(req["_id"])
        return req
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid request ID")

@router.post("/requests", response_model=ResourceRequest)
async def create_resource_request(
    resource_request: ResourceRequestCreate,
    request: Request,
    current_user: dict = Depends(get_current_user)
):
    """Create a new resource request"""
    db = request.app.mongodb
    
    # Verify user is school or admin
    if current_user["role"] not in ["school", "admin"]:
        raise HTTPException(status_code=403, detail="Only schools can create resource requests")
    
    # Create request document
    request_doc = {
        "school_id": current_user["_id"],
        "resource_type": resource_request.resource_type,
        "description": resource_request.description,
        "quantity": resource_request.quantity,
        "estimated_cost_usd": resource_request.estimated_cost_usd,
        "priority": resource_request.priority,
        "status": "pending",
        "justification": resource_request.justification,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    # Save to database
    result = await db.resource_requests.insert_one(request_doc)
    
    # Return created request
    created_request = await db.resource_requests.find_one({"_id": result.inserted_id})
    created_request["_id"] = str(created_request["_id"])
    
    return created_request

@router.put("/requests/{request_id}/approve")
async def approve_resource_request(
    request_id: str,
    request: Request,
    current_user: dict = Depends(get_current_user)
):
    """Approve a resource request (admin only)"""
    db = request.app.mongodb
    
    # Verify admin role
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Only admins can approve requests")
    
    # Check if request exists
    req = await db.resource_requests.find_one({"_id": ObjectId(request_id)})
    if not req:
        raise HTTPException(status_code=404, detail="Resource request not found")
    
    # Update request status
    await db.resource_requests.update_one(
        {"_id": ObjectId(request_id)},
        {
            "$set": {
                "status": "approved",
                "approved_at": datetime.utcnow(),
                "approved_by": current_user["_id"],
                "updated_at": datetime.utcnow()
            }
        }
    )
    
    return {"message": "Resource request approved successfully"}

@router.put("/requests/{request_id}/allocate")
async def allocate_resource_request(
    request_id: str,
    allocation_amount: float,
    request: Request,
    current_user: dict = Depends(get_current_user)
):
    """Allocate funds to a resource request (admin only)"""
    db = request.app.mongodb
    
    # Verify admin role
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Only admins can allocate resources")
    
    # Check if request exists and is approved
    req = await db.resource_requests.find_one({"_id": ObjectId(request_id)})
    if not req:
        raise HTTPException(status_code=404, detail="Resource request not found")
    
    if req["status"] != "approved":
        raise HTTPException(status_code=400, detail="Request must be approved before allocation")
    
    # Update request status
    await db.resource_requests.update_one(
        {"_id": ObjectId(request_id)},
        {
            "$set": {
                "status": "allocated",
                "allocated_amount": allocation_amount,
                "allocated_at": datetime.utcnow(),
                "allocated_by": current_user["_id"],
                "updated_at": datetime.utcnow()
            }
        }
    )
    
    return {"message": "Resources allocated successfully"}

@router.get("/stats/schools")
async def get_school_stats(request: Request):
    """Get school statistics"""
    db = request.app.mongodb
    
    # Count total schools
    total_schools = await db.schools.count_documents({})
    verified_schools = await db.schools.count_documents({"verified": True})
    
    # Count total students
    pipeline = [
        {"$group": {"_id": None, "total_students": {"$sum": "$total_students"}}}
    ]
    student_result = await db.schools.aggregate(pipeline).to_list(1)
    total_students = student_result[0]["total_students"] if student_result else 0
    
    return {
        "total_schools": total_schools,
        "verified_schools": verified_schools,
        "pending_schools": total_schools - verified_schools,
        "total_students": total_students
    }

@router.get("/stats/requests")
async def get_request_stats(request: Request):
    """Get resource request statistics"""
    db = request.app.mongodb
    
    # Count requests by status
    pipeline = [
        {"$group": {
            "_id": "$status",
            "count": {"$sum": 1},
            "total_cost": {"$sum": "$estimated_cost_usd"}
        }}
    ]
    
    stats_result = await db.resource_requests.aggregate(pipeline).to_list(None)
    
    stats = {
        "pending": {"count": 0, "total_cost": 0},
        "approved": {"count": 0, "total_cost": 0},
        "allocated": {"count": 0, "total_cost": 0},
        "delivered": {"count": 0, "total_cost": 0}
    }
    
    for result in stats_result:
        status = result["_id"]
        if status in stats:
            stats[status] = {"count": result["count"], "total_cost": result["total_cost"]}
    
    return stats

@router.get("/schools/{school_id}/requests")
async def get_school_requests(
    school_id: str,
    request: Request,
    current_user: dict = Depends(get_current_user)
):
    """Get resource requests for a specific school"""
    db = request.app.mongodb
    
    # Check if school exists
    school = await db.schools.find_one({"_id": ObjectId(school_id)})
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    
    # Get requests for this school
    cursor = db.resource_requests.find({"school_id": school_id}).sort("created_at", -1)
    requests = []
    
    async for req in cursor:
        req["_id"] = str(req["_id"])
        requests.append(req)
    
    return requests
