from fastapi import APIRouter, HTTPException, Depends, Request
from typing import List, Optional
from models import Donation, DonationCreate, DonationStatus
from routes.auth import get_current_user
from bson import ObjectId
from datetime import datetime, timedelta
import re
from web3 import Web3

router = APIRouter()

def validate_transaction_hash(tx_hash: str) -> bool:
    """Validate Ethereum transaction hash format"""
    if not tx_hash or not isinstance(tx_hash, str):
        return False
    return re.match(r'^0x[a-fA-F0-9]{64}$', tx_hash) is not None

def validate_donation_amount(amount_eth: float) -> bool:
    """Validate donation amount - accepts micro-donations"""
    if not isinstance(amount_eth, (int, float)):
        return False
    return 0.000001 <= amount_eth <= 1000.0  # Minimum 0.000001 ETH (1 Gwei)

@router.get("/", response_model=List[Donation])
async def get_donations(
    request: Request,
    status: Optional[DonationStatus] = None,
    limit: int = 20,
    skip: int = 0,
    current_user: dict = Depends(get_current_user)
):
    """Get donations (filtered by user role)"""
    db = request.app.mongodb
    
    # Build filter based on user role
    filter_query = {}
    
    if current_user["role"] == "donor":
        # Donors can only see their own donations
        filter_query["donor_id"] = current_user["_id"]
    elif current_user["role"] == "school":
        # Schools can see donations allocated to them
        filter_query["target_school_id"] = current_user["_id"]
    elif current_user["role"] not in ["admin", "instructor"]:
        # Students can see all public donations
        filter_query["status"] = {"$in": ["confirmed", "allocated"]}
    
    if status:
        filter_query["status"] = status
    
    # Get donations from database
    cursor = db.donations.find(filter_query).sort("created_at", -1).skip(skip).limit(limit)
    donations = []
    
    async for donation in cursor:
        donation["_id"] = str(donation["_id"])
        donations.append(donation)
    
    return donations

@router.get("/{donation_id}", response_model=Donation)
async def get_donation(
    donation_id: str,
    request: Request,
    current_user: dict = Depends(get_current_user)
):
    """Get a specific donation by ID"""
    db = request.app.mongodb
    
    try:
        donation = await db.donations.find_one({"_id": ObjectId(donation_id)})
        if not donation:
            raise HTTPException(status_code=404, detail="Donation not found")
        
        # Check access control
        if current_user["role"] == "donor" and donation["donor_id"] != current_user["_id"]:
            raise HTTPException(status_code=403, detail="Not authorized to view this donation")
        
        donation["_id"] = str(donation["_id"])
        return donation
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid donation ID")

@router.post("/", response_model=Donation)
async def create_donation(
    donation: DonationCreate,
    request: Request,
    current_user: dict = Depends(get_current_user)
):
    """Create a new donation record"""
    db = request.app.mongodb
    
    # Verify user is donor or admin
    if current_user["role"] not in ["donor", "admin"]:
        raise HTTPException(status_code=403, detail="Only donors can create donations")
    
    # Validate donation amount
    if not validate_donation_amount(donation.amount_eth):
        raise HTTPException(status_code=400, detail="Invalid donation amount (must be between 0.000001 and 1000 ETH)")
    
    # Validate transaction hash format
    if not validate_transaction_hash(donation.transaction_hash):
        raise HTTPException(status_code=400, detail="Invalid transaction hash format")
    
    # Check if transaction hash already exists
    existing_donation = await db.donations.find_one({"transaction_hash": donation.transaction_hash})
    if existing_donation:
        raise HTTPException(status_code=400, detail="Transaction hash already recorded")
    
    # Get current ETH price (simplified - in production use real API)
    eth_to_usd_rate = 2000.0  # Should be fetched from price API
    
    # Create donation document
    donation_doc = {
        "donor_id": current_user["_id"],
        "amount_eth": donation.amount_eth,
        "amount_usd": donation.amount_eth * eth_to_usd_rate,
        "transaction_hash": donation.transaction_hash,
        "purpose": donation.purpose[:500],  # Limit purpose length
        "target_school_id": donation.target_school_id,
        "status": DonationStatus.PENDING,
        "created_at": datetime.utcnow(),
        "confirmed_at": None
    }
    
    # Save to database
    result = await db.donations.insert_one(donation_doc)
    
    # Return created donation
    created_donation = await db.donations.find_one({"_id": result.inserted_id})
    created_donation["_id"] = str(created_donation["_id"])
    
    return created_donation

@router.get("/stats/total")
async def get_donation_stats(request: Request):
    """Get total donation statistics"""
    db = request.app.mongodb
    
    # Calculate total statistics
    pipeline = [
        {"$match": {"status": {"$in": ["confirmed", "allocated", "completed"]}}},
        {"$group": {
            "_id": None,
            "total_eth": {"$sum": "$amount_eth"},
            "total_usd": {"$sum": "$amount_usd"},
            "total_donations": {"$sum": 1}
        }}
    ]
    
    stats_result = await db.donations.aggregate(pipeline).to_list(1)
    
    if stats_result:
        stats = stats_result[0]
    else:
        stats = {"total_eth": 0.0, "total_usd": 0.0, "total_donations": 0}
    
    # Count unique schools helped
    schools_helped = await db.donations.distinct("target_school_id")
    stats["schools_helped"] = len([s for s in schools_helped if s is not None])
    
    return stats

@router.get("/stats/monthly")
async def get_monthly_donation_stats(request: Request):
    """Get monthly donation statistics"""
    db = request.app.mongodb
    
    # Get monthly stats for the last 12 months
    pipeline = [
        {"$match": {
            "status": {"$in": ["confirmed", "allocated", "completed"]},
            "created_at": {"$gte": datetime.utcnow() - timedelta(days=365)}
        }},
        {"$group": {
            "_id": {
                "year": {"$year": "$created_at"},
                "month": {"$month": "$created_at"}
            },
            "total_eth": {"$sum": "$amount_eth"},
            "total_usd": {"$sum": "$amount_usd"},
            "count": {"$sum": 1}
        }},
        {"$sort": {"_id.year": 1, "_id.month": 1}}
    ]
    
    monthly_stats = await db.donations.aggregate(pipeline).to_list(None)
    
    return monthly_stats

@router.post("/{donation_id}/allocate")
async def allocate_donation(
    donation_id: str,
    school_id: str,
    request: Request,
    current_user: dict = Depends(get_current_user)
):
    """Allocate donation to a specific school (admin only)"""
    db = request.app.mongodb
    
    # Verify admin role
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Only admins can allocate donations")
    
    # Check if donation exists
    donation = await db.donations.find_one({"_id": ObjectId(donation_id)})
    if not donation:
        raise HTTPException(status_code=404, detail="Donation not found")
    
    # Check if donation is confirmed
    if donation["status"] != DonationStatus.CONFIRMED:
        raise HTTPException(status_code=400, detail="Donation must be confirmed before allocation")
    
    # Check if school exists
    school = await db.schools.find_one({"_id": ObjectId(school_id)})
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    
    # Update donation status
    await db.donations.update_one(
        {"_id": ObjectId(donation_id)},
        {
            "$set": {
                "status": DonationStatus.ALLOCATED,
                "target_school_id": school_id,
                "allocated_at": datetime.utcnow()
            }
        }
    )
    
    # TODO: Trigger smart contract allocation
    # This would integrate with the blockchain smart contract
    
    return {"message": "Donation allocated successfully"}

@router.get("/leaderboard")
async def get_donor_leaderboard(request: Request):
    """Get top donors leaderboard"""
    db = request.app.mongodb
    
    # Get top donors by total amount donated
    pipeline = [
        {"$match": {"status": {"$in": ["confirmed", "allocated", "completed"]}}},
        {"$group": {
            "_id": "$donor_id",
            "total_eth": {"$sum": "$amount_eth"},
            "total_usd": {"$sum": "$amount_usd"},
            "donation_count": {"$sum": 1}
        }},
        {"$sort": {"total_eth": -1}},
        {"$limit": 10}
    ]
    
    leaderboard = await db.donations.aggregate(pipeline).to_list(None)
    
    # Get donor details
    for entry in leaderboard:
        donor = await db.users.find_one({"_id": ObjectId(entry["_id"])})
        if donor:
            entry["donor_name"] = donor.get("full_name", "Anonymous")
            entry["donor_username"] = donor.get("username", "anonymous")
        else:
            entry["donor_name"] = "Anonymous"
            entry["donor_username"] = "anonymous"
    
    return leaderboard

@router.post("/{donation_id}/confirm")
async def confirm_donation(
    donation_id: str,
    request: Request,
    current_user: dict = Depends(get_current_user)
):
    """Confirm a donation (admin only)"""
    db = request.app.mongodb
    
    # Verify admin role
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Only admins can confirm donations")
    
    # Check if donation exists
    donation = await db.donations.find_one({"_id": ObjectId(donation_id)})
    if not donation:
        raise HTTPException(status_code=404, detail="Donation not found")
    
    # Update donation status
    await db.donations.update_one(
        {"_id": ObjectId(donation_id)},
        {
            "$set": {
                "status": DonationStatus.CONFIRMED,
                "confirmed_at": datetime.utcnow()
            }
        }
    )
    
    return {"message": "Donation confirmed successfully"}

@router.get("/schools/{school_id}")
async def get_school_donations(
    school_id: str,
    request: Request,
    current_user: dict = Depends(get_current_user)
):
    """Get donations for a specific school"""
    db = request.app.mongodb
    
    # Check if school exists
    school = await db.schools.find_one({"_id": ObjectId(school_id)})
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    
    # Get donations for this school
    cursor = db.donations.find({"target_school_id": school_id}).sort("created_at", -1)
    donations = []
    
    async for donation in cursor:
        donation["_id"] = str(donation["_id"])
        donations.append(donation)
    
    return donations
