from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Request
from fastapi.responses import FileResponse
from typing import List, Optional
import os
import uuid
import shutil
from PIL import Image
import io
import hashlib
from pathlib import Path
from routes.auth import get_current_user

router = APIRouter()

# Configuration
UPLOAD_DIR = Path("uploads")
ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
THUMBNAIL_SIZE = (300, 200)
MAX_IMAGE_DIMENSION = 2048

# Create upload directory if it doesn't exist
UPLOAD_DIR.mkdir(exist_ok=True)
(UPLOAD_DIR / "courses").mkdir(exist_ok=True)
(UPLOAD_DIR / "profiles").mkdir(exist_ok=True)
(UPLOAD_DIR / "thumbnails").mkdir(exist_ok=True)

def validate_image(file: UploadFile) -> None:
    """Validate uploaded image file"""
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed types: {', '.join(ALLOWED_IMAGE_TYPES)}"
        )
    
    if file.size and file.size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size: {MAX_FILE_SIZE // (1024*1024)}MB"
        )

def create_thumbnail(image_path: Path, thumbnail_path: Path) -> None:
    """Create a thumbnail from the original image"""
    try:
        with Image.open(image_path) as img:
            # Convert to RGB if necessary (for PNG with transparency)
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            
            # Create thumbnail
            img.thumbnail(THUMBNAIL_SIZE, Image.Resampling.LANCZOS)
            img.save(thumbnail_path, "JPEG", quality=85, optimize=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating thumbnail: {str(e)}")

def optimize_image(image_path: Path) -> None:
    """Optimize image size and quality"""
    try:
        with Image.open(image_path) as img:
            # Convert to RGB if necessary
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            
            # Resize if too large
            if img.width > MAX_IMAGE_DIMENSION or img.height > MAX_IMAGE_DIMENSION:
                img.thumbnail((MAX_IMAGE_DIMENSION, MAX_IMAGE_DIMENSION), Image.Resampling.LANCZOS)
            
            # Save optimized image
            img.save(image_path, "JPEG", quality=85, optimize=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error optimizing image: {str(e)}")

@router.post("/upload/course-thumbnail")
async def upload_course_thumbnail(
    request: Request,
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    """Upload course thumbnail image"""
    validate_image(file)
    
    # Generate unique filename
    file_extension = file.filename.split(".")[-1] if file.filename else "jpg"
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = UPLOAD_DIR / "courses" / unique_filename
    thumbnail_path = UPLOAD_DIR / "thumbnails" / f"thumb_{unique_filename}"
    
    try:
        # Save uploaded file
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Optimize original image
        optimize_image(file_path)
        
        # Create thumbnail
        create_thumbnail(file_path, thumbnail_path)
        
        # Generate file hash for integrity
        with open(file_path, "rb") as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()
        
        return {
            "success": True,
            "filename": unique_filename,
            "url": f"/api/media/courses/{unique_filename}",
            "thumbnail_url": f"/api/media/thumbnails/thumb_{unique_filename}",
            "file_hash": file_hash,
            "file_size": os.path.getsize(file_path)
        }
        
    except Exception as e:
        # Cleanup on error
        if file_path.exists():
            file_path.unlink()
        if thumbnail_path.exists():
            thumbnail_path.unlink()
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@router.post("/upload/profile-avatar")
async def upload_profile_avatar(
    request: Request,
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    """Upload user profile avatar"""
    validate_image(file)
    
    # Generate filename based on user ID
    file_extension = file.filename.split(".")[-1] if file.filename else "jpg"
    unique_filename = f"avatar_{current_user['_id']}.{file_extension}"
    file_path = UPLOAD_DIR / "profiles" / unique_filename
    thumbnail_path = UPLOAD_DIR / "thumbnails" / f"thumb_{unique_filename}"
    
    try:
        # Remove existing avatar if it exists
        if file_path.exists():
            file_path.unlink()
        if thumbnail_path.exists():
            thumbnail_path.unlink()
        
        # Save uploaded file
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Optimize original image
        optimize_image(file_path)
        
        # Create thumbnail
        create_thumbnail(file_path, thumbnail_path)
        
        # Update user profile in database
        if request:
            db = request.app.mongodb
            await db.users.update_one(
                {"_id": current_user["_id"]},
                {"$set": {"avatar_url": f"/api/media/profiles/{unique_filename}"}}
            )
        
        return {
            "success": True,
            "filename": unique_filename,
            "url": f"/api/media/profiles/{unique_filename}",
            "thumbnail_url": f"/api/media/thumbnails/thumb_{unique_filename}"
        }
        
    except Exception as e:
        # Cleanup on error
        if file_path.exists():
            file_path.unlink()
        if thumbnail_path.exists():
            thumbnail_path.unlink()
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@router.post("/upload/multiple")
async def upload_multiple_images(
    files: List[UploadFile] = File(...),
    current_user: dict = Depends(get_current_user),
    folder: str = "courses"
):
    """Upload multiple images at once"""
    if len(files) > 10:
        raise HTTPException(status_code=400, detail="Maximum 10 files allowed")
    
    results = []
    for file in files:
        try:
            validate_image(file)
            
            # Generate unique filename
            file_extension = file.filename.split(".")[-1] if file.filename else "jpg"
            unique_filename = f"{uuid.uuid4()}.{file_extension}"
            file_path = UPLOAD_DIR / folder / unique_filename
            thumbnail_path = UPLOAD_DIR / "thumbnails" / f"thumb_{unique_filename}"
            
            # Save uploaded file
            with open(file_path, "wb") as buffer:
                content = await file.read()
                buffer.write(content)
            
            # Optimize and create thumbnail
            optimize_image(file_path)
            create_thumbnail(file_path, thumbnail_path)
            
            results.append({
                "filename": file.filename,
                "unique_filename": unique_filename,
                "url": f"/api/media/{folder}/{unique_filename}",
                "thumbnail_url": f"/api/media/thumbnails/thumb_{unique_filename}",
                "success": True
            })
            
        except Exception as e:
            results.append({
                "filename": file.filename,
                "error": str(e),
                "success": False
            })
    
    return {"results": results}

# Serve uploaded files
@router.get("/media/courses/{filename}")
async def serve_course_image(filename: str):
    """Serve course images"""
    file_path = UPLOAD_DIR / "courses" / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(file_path)

@router.get("/media/profiles/{filename}")
async def serve_profile_image(filename: str):
    """Serve profile images"""
    file_path = UPLOAD_DIR / "profiles" / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(file_path)

@router.get("/media/thumbnails/{filename}")
async def serve_thumbnail(filename: str):
    """Serve thumbnail images"""
    file_path = UPLOAD_DIR / "thumbnails" / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Thumbnail not found")
    return FileResponse(file_path)

@router.delete("/media/{folder}/{filename}")
async def delete_image(
    folder: str,
    filename: str,
    current_user: dict = Depends(get_current_user)
):
    """Delete uploaded image"""
    if folder not in ["courses", "profiles"]:
        raise HTTPException(status_code=400, detail="Invalid folder")
    
    file_path = UPLOAD_DIR / folder / filename
    thumbnail_path = UPLOAD_DIR / "thumbnails" / f"thumb_{filename}"
    
    deleted_files = []
    
    if file_path.exists():
        file_path.unlink()
        deleted_files.append(str(file_path))
    
    if thumbnail_path.exists():
        thumbnail_path.unlink()
        deleted_files.append(str(thumbnail_path))
    
    if not deleted_files:
        raise HTTPException(status_code=404, detail="Image not found")
    
    return {
        "success": True,
        "deleted_files": deleted_files,
        "message": "Image deleted successfully"
    }

@router.get("/info/{folder}/{filename}")
async def get_image_info(folder: str, filename: str):
    """Get information about uploaded image"""
    if folder not in ["courses", "profiles"]:
        raise HTTPException(status_code=400, detail="Invalid folder")
    
    file_path = UPLOAD_DIR / folder / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Image not found")
    
    # Get file stats
    stats = file_path.stat()
    
    # Get image dimensions
    try:
        with Image.open(file_path) as img:
            width, height = img.size
            format_name = img.format
    except Exception:
        width = height = format_name = None
    
    return {
        "filename": filename,
        "size": stats.st_size,
        "created": stats.st_ctime,
        "modified": stats.st_mtime,
        "width": width,
        "height": height,
        "format": format_name,
        "url": f"/api/media/{folder}/{filename}",
        "thumbnail_url": f"/api/media/thumbnails/thumb_{filename}"
    }
