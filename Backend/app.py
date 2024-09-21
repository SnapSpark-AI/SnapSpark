from fastapi import FastAPI, HTTPException, File, UploadFile, Form
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import urllib
import sys
import os
import shutil
import subprocess
import PIL.Image
import PIL.ExifTags
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# NOTE: Always store API keys as environment variables
PORT = int(sys.argv[1])

origins = ["http://localhost:3000"]

app = FastAPI()
mongo_uri = "mongodb://" + os.getenv("MONGO_USR") + ":" + urllib.parse.quote(os.getenv("MONGO_PASS")) + "@127.0.0.1:27001/"

client = AsyncIOMotorClient(mongo_uri)
db = client.myDatabase
logger.info(f"Connected to MongoDB, databases: {client.list_database_names()}")

UPLOAD_DIR = "uploaded_images"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    logger.info("Root endpoint accessed")
    return {"x": "y"}

@app.post("/upload_image/")
async def upload_image(
    item_id: int = Form(...), 
    imagename: str = Form(...), 
    latitude: float = Form(...), 
    longitude: float = Form(...), 
    file: UploadFile = File(...)
):
    logger.info(f"Uploading image: {imagename} with item_id: {item_id}, latitude: {latitude}, longitude: {longitude}")
    
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    mongodb_document = {
        "item_id": item_id,
        "imagename": imagename,
        "latitude": latitude,
        "longitude": longitude,
        "file_path": file_location
    }

    result = await db.imagesources.insert_one(mongodb_document)
    
    if result.acknowledged:
        logger.info(f"Image and metadata added successfully for item_id: {item_id}")
        return {"message": "Image and metadata added successfully", "item_id": item_id}
    else:
        logger.error("Failed to insert document into MongoDB")
        raise HTTPException(status_code=500, detail="Failed to insert document")

@app.get("/imagesources/{item_id}")
async def read_image_source(item_id: int):
    logger.info(f"Fetching image source for item_id: {item_id}")
    doc = await db.imagesources.find_one({"item_id": item_id})
    if doc:
        logger.info(f"Image source found for item_id: {item_id}")
        return doc
    else:
        logger.warning(f"Item not found for item_id: {item_id}")
        raise HTTPException(status_code=404, detail="Item not found")

if __name__ == "__main__":
    logger.info(f"Starting FastAPI server on http://127.0.0.1:{PORT}")
    uvicorn.run(app, host="127.0.0.1", port=PORT)
