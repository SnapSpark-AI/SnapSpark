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
    
    imagename = "uploaded_images/"+file.filename
    img = PIL.Image.open(imagename)
    exif = {
        PIL.ExifTags.TAGS[k]: v
        for k, v in img._getexif().items
        if k in PIL.ExifTags.TAGS
    }
    north = exif['GPSinfo'][2]
    east = exif['GPSinfo'][4]
    latitude = (((north[0]*60)+north[1]*60)+north[2])/60/60
    longitude = (((east[0]*60)+east[1]*60)+east[2])/60/60
    os.chdir("uploaded_images")
    file_location = subprocess.run(['pwd'], capture_output=True, text=True)
    file_location = file_location.stdout
    mongo_store = {
        "imagename": imagename,
        "latitude": latitude,
        "longitude": longitude,
        "file_location": file_location
    }
    result = await db.imagesources.insert_one(mongo_store)
    
    if result.acknowledged:
        return {"message": "Image and metadata added successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to insert document")

@app.get("/imagesources/{imagename}")
async def read_image_source(imagename: str):
    doc = await db.imagesources.find_one({"imagename": imagename})
    if doc:
        return doc
    else:
        raise HTTPException(status_code=404, detail="Item not found")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=PORT)