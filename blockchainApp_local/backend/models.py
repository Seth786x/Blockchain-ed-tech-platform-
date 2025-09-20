from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Optional, List
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    STUDENT = "student"
    INSTRUCTOR = "instructor"
    SCHOOL = "school"
    DONOR = "donor"
    ADMIN = "admin"

class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: str
    role: UserRole
    wallet_address: Optional[str] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: str = Field(alias="_id")
    created_at: datetime
    is_active: bool = True
    
    model_config = {"populate_by_name": True}

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Course Models
class HardwareComponent(str, Enum):
    CPU = "cpu"
    GPU = "gpu"
    RAM = "ram"
    MOTHERBOARD = "motherboard"
    STORAGE = "storage"
    PSU = "power_supply"
    COOLING = "cooling"
    CASE = "case"

class CourseLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

class CourseModule(BaseModel):
    title: str
    description: str
    content: str  # Module content text
    content_url: Optional[str] = None  # IPFS hash for additional content
    video_url: Optional[str] = None  # IPFS hash for videos
    image_urls: List[str] = []  # Multiple images for the module
    duration_minutes: Optional[int] = None
    order: int

class Course(BaseModel):
    id: str = Field(alias="_id")
    title: str
    description: str
    price: float = 0.0  # In ETH
    category: str
    difficulty: str
    duration: str
    instructor: str
    modules: List[CourseModule] = []
    thumbnail_url: Optional[str] = None  # Course thumbnail
    created_at: datetime
    updated_at: datetime
    is_published: bool = True
    enrollment_count: int = 0
    rating: float = 4.8
    rating_count: int = 0
    prerequisites: List[str] = []
    learning_outcomes: List[str] = []
    is_featured: Optional[bool] = False
    
    model_config = {"populate_by_name": True}

class CourseCreate(BaseModel):
    title: str
    description: str
    category: str
    difficulty: str
    duration: str
    instructor: str
    thumbnail_url: Optional[str] = None
    price: float = 0.0

# Donation Models
class DonationStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    ALLOCATED = "allocated"
    COMPLETED = "completed"

class Donation(BaseModel):
    id: str = Field(alias="_id")
    donor_id: str
    amount_eth: float
    amount_usd: float
    transaction_hash: str
    purpose: str
    target_school_id: Optional[str] = None
    status: DonationStatus
    created_at: datetime
    confirmed_at: Optional[datetime] = None
    
    model_config = ConfigDict(populate_by_name=True)

class DonationCreate(BaseModel):
    amount_eth: float
    purpose: str
    target_school_id: Optional[str] = None
    transaction_hash: str

# Resource Allocation Models
class ResourceType(str, Enum):
    HARDWARE_KIT = "hardware_kit"
    SOFTWARE_LICENSE = "software_license"
    EQUIPMENT = "equipment"
    FUNDING = "funding"

class ResourceRequest(BaseModel):
    id: str = Field(alias="_id")
    school_id: str
    resource_type: ResourceType
    description: str
    quantity: int
    estimated_cost_usd: float
    priority: int  # 1-5, 5 being highest
    status: str = "pending"  # pending, approved, allocated, delivered
    justification: str
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(populate_by_name=True)

class ResourceRequestCreate(BaseModel):
    resource_type: ResourceType
    description: str
    quantity: int
    estimated_cost_usd: float
    priority: int
    justification: str

# Progress Tracking
class StudentProgress(BaseModel):
    id: str = Field(alias="_id")
    student_id: str
    course_id: str
    completed_modules: List[int] = []
    progress_percentage: float = 0.0
    started_at: datetime
    last_accessed: datetime
    completed_at: Optional[datetime] = None
    certificate_ipfs: Optional[str] = None
    
    model_config = ConfigDict(populate_by_name=True)

# School Models
class School(BaseModel):
    id: str = Field(alias="_id")
    name: str
    address: str
    contact_email: EmailStr
    contact_phone: str
    principal_name: str
    wallet_address: str
    total_students: int
    verified: bool = False
    created_at: datetime
    
    model_config = ConfigDict(populate_by_name=True)

class SchoolCreate(BaseModel):
    name: str
    address: str
    contact_email: EmailStr
    contact_phone: str
    principal_name: str
    wallet_address: str
    total_students: int

# Blockchain Transaction Models
class TransactionType(str, Enum):
    DONATION = "donation"
    ALLOCATION = "allocation"
    PAYMENT = "payment"
    CERTIFICATE = "certificate"

class BlockchainTransaction(BaseModel):
    id: str = Field(alias="_id")
    transaction_hash: str
    from_address: str
    to_address: str
    amount_eth: float
    transaction_type: TransactionType
    gas_used: int
    gas_price: str
    block_number: int
    timestamp: datetime
    related_entity_id: str  # Could be donation_id, course_id, etc.
    
    model_config = ConfigDict(populate_by_name=True)