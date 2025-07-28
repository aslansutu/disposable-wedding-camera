# main.py
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import shutil
from datetime import datetime
import os

app = FastAPI()

# Enable CORS for your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your frontend domain for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Serve static files from the uploads directory
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    filename = f"{datetime.utcnow().isoformat().replace(':', '-')}.png"
    filepath = os.path.join(UPLOAD_DIR, filename)

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"message": "Image saved", "filename": filename}

@app.get("/images/")
async def list_images():
    files = []
    for filename in os.listdir(UPLOAD_DIR):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
            files.append({
                "url": f"/uploads/{filename}",
                "filename": filename
            })
    return JSONResponse(content=files)
