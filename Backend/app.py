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

# NOTE: Always store API keys as environment variables
PORT = int(sys.argv[1])

origins = ["http://localhost:3000"]

app = FastAPI()
mongo_uri = "mongodb://" + os.getenv("MONGO_USR") + ":" + urllib.parse.quote(os.getenv("MONGO_PASS")) + "@127.0.0.1:27001/"

weather_api = os.getenv("WEATHER_API_DEFAULT")

client = AsyncIOMotorClient(mongo_uri)
db = client.myDatabase
print(client.list_database_names())
print(db.list_collection_names())
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
    return {"x": "y"}

@app.post("/upload_image/")
async def upload_image(
    file: UploadFile = File(...)
):

    file_location = f"{UPLOAD_DIR}/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    result = await db.imagesources.insert_one(mongodb_document)
    
    if result.acknowledged:
        return {"message": "Image and metadata added successfully", "item_id": item_id}
    else:
        raise HTTPException(status_code=500, detail="Failed to insert document")

@app.get("/imagesources/{item_id}")
async def read_image_source(item_id: int):
    doc = await db.imagesources.find_one({"item_id": item_id})
    if doc:
        return doc
    else:
        raise HTTPException(status_code=404, detail="Item not found")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=PORT)