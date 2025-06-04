from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pathlib import Path
import shutil
import os
from datetime import datetime
from typing import List
import json

app = FastAPI(title="Wedding Camera API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create uploads directory if it doesn't exist
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Store photo metadata
PHOTOS_DB = Path("photos.json")
if not PHOTOS_DB.exists():
    with open(PHOTOS_DB, "w") as f:
        json.dump([], f)

def get_photos():
    with open(PHOTOS_DB, "r") as f:
        return json.load(f)

def save_photo(photo_data):
    photos = get_photos()
    photos.append(photo_data)
    with open(PHOTOS_DB, "w") as f:
        json.dump(photos, f)

@app.get("/")
async def read_root():
    return {"message": "Welcome to Wedding Camera API"}

@app.get("/photos")
async def get_all_photos():
    """Get all photos with pagination"""
    photos = get_photos()
    return photos

@app.post("/photos")
async def upload_photo(file: UploadFile = File(...)):
    """Upload a new photo"""
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    # Generate unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{file.filename}"
    file_path = UPLOAD_DIR / filename
    
    # Save the file
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Save metadata
    photo_data = {
        "id": timestamp,
        "filename": filename,
        "original_name": file.filename,
        "uploaded_at": timestamp,
        "url": f"/photos/{filename}"
    }
    save_photo(photo_data)
    
    return photo_data

@app.get("/photos/{filename}")
async def get_photo(filename: str):
    """Get a specific photo by filename"""
    file_path = UPLOAD_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Photo not found")
    return FileResponse(file_path)

@app.delete("/photos/{filename}")
async def delete_photo(filename: str):
    """Delete a photo"""
    file_path = UPLOAD_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Photo not found")
    
    # Remove file
    file_path.unlink()
    
    # Update metadata
    photos = get_photos()
    photos = [p for p in photos if p["filename"] != filename]
    with open(PHOTOS_DB, "w") as f:
        json.dump(photos, f)
    
    return {"message": "Photo deleted successfully"} 