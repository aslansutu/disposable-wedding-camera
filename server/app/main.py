# main.py
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import shutil
from datetime import datetime
import requests
import os
import json
from os import environ

app = FastAPI()

client_url = environ.get("CLIENT_URL")

# Enable CORS for your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[client_url],  # Use the actual frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Serve static files from the uploads directory
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

EVENT_INFO_FILE = os.path.join(UPLOAD_DIR, "event_info.json")
EVENT_IMAGE_NAME = "event_image.png"

@app.get("/demo/{num}")
async def demo(num: int):
    if num < 1:
        return JSONResponse(content={"message": "Number must be greater than 0"}, status_code=400)
    
    for i in range(num):
        import random
        width = [200, 300, 400, 500, 600]
        height = [200, 300, 400, 500, 600]
        try:
            response = requests.get(f"https://picsum.photos/{random.choice(width)}/{random.choice(height)}", stream=True)
            if response.status_code == 200:
                filename = f"image_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}_{i}.jpg"
                file_path = os.path.join(UPLOAD_DIR, filename)
                with open(file_path, "wb") as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
            else:
                return JSONResponse(content={"message": f"Failed to fetch image #{i+1}"}, status_code=500)
        except Exception as e:
            return JSONResponse(content={"message": f"Error fetching image #{i+1}: {str(e)}"}, status_code=500)
        

@app.get("/reset")
async def reset():
    # Remove all files in the upload directory
    for filename in os.listdir(UPLOAD_DIR):
        file_path = os.path.join(UPLOAD_DIR, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            return JSONResponse(content={"message": f"Error deleting file {filename}: {str(e)}"}, status_code=500)

    # Remove the event info file
    if os.path.exists(EVENT_INFO_FILE):
        os.remove(EVENT_INFO_FILE)

    return JSONResponse(content={"message": "All files and event info reset successfully"})

@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    filename = f"{datetime.utcnow().isoformat().replace(':', '-')}.png"
    filepath = os.path.join(UPLOAD_DIR, filename)

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"message": "Image saved", "filename": filename}

@app.get("/info")
async def get_event_info():
    if os.path.exists(EVENT_INFO_FILE):
        with open(EVENT_INFO_FILE, "r") as f:
            info = json.load(f)
        return JSONResponse(content=info)
    else:
        return JSONResponse(content={"message": "Event info not set"}, status_code=404)
    
@app.post("/info")
async def set_event_info(
    title: str = Form(...),
    event_name: str = Form(...),
    description: str = Form(...),
    image: UploadFile = File(...)
):
    # Save event info (without image) to a JSON file
    info = {
        "title": title,
        "event_name": event_name,
        "description": description,
        "image": f"/uploads/{EVENT_IMAGE_NAME}"
    }
    with open(EVENT_INFO_FILE, "w") as f:
        json.dump(info, f)

    # Save the image as a special file
    image_path = os.path.join(UPLOAD_DIR, EVENT_IMAGE_NAME)
    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    return {"message": "Event info saved"}

@app.get("/images/")
async def list_images():
    files = []
    for filename in os.listdir(UPLOAD_DIR):
        # Skip the event image
        if filename == EVENT_IMAGE_NAME:
            continue
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
            files.append({
                "url": f"/uploads/{filename}",
                "filename": filename
            })
    return JSONResponse(content=files)
