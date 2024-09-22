from fastapi import FastAPI, HTTPException, File, UploadFile, Form
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import mysql.connector
import sys
import os
import shutil
import subprocess
from PIL import Image, ExifTags

# NOTE: Always store API keys as environment variables
PORT = int(sys.argv[1])

origins = ["http://localhost:3000"]

app = FastAPI()

weather_api = os.getenv("WEATHER_API_DEFAULT")

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
    
    imagename = "/home/shubs/hackathon/SnapSpark/Backend/uploaded_images/" + file.filename
    img = Image.open(imagename)

    exif = img._getexif()

    if exif is not None:
        exif_data = {
            ExifTags.TAGS[k]: v
            for k, v in exif.items()
            if k in ExifTags.TAGS
        }
    else:
        exif_data = {}
    north = exif_data['GPSinfo'][2]
    east = exif_data['GPSinfo'][4]
    latitude = str((((north[0]*60)+north[1]*60)+north[2])/60/60)
    longitude = str((((east[0]*60)+east[1]*60)+east[2])/60/60)
    os.chdir("uploaded_images")
    file_location = subprocess.run(['pwd'], capture_output=True, text=True)
    file_location = file_location.stdout
    mydb = mysql.connector.connect(
        host="localhost",
        user=os.getenv("MYSQL_USR"),
        password=os.getenv("MYSQL_PASS"),
    )
    mycursor = mydb.cursor()

    mycursor.execute("CREATE DATABASE firedb")
    
    mydb = mysql.connector.connect(
        host="localhost",
        user=os.getenv("MYSQL_USR"),
        password=os.getenv("MYSQL_PASS"),
        database="firedb"
    )

    mycursor = mydb.cursor()

    mycursor.execute("CREATE TABLE coordinates (filename VARCHAR(255), latitude VARCHAR(255), longitude VARCHAR(255))")

    sql = "INSERT INTO coordinates (filename, latitude, longitude) VALUES (%s, %s, %s)"
    val = (file.filename, latitude, longitude)
    mycursor.execute(sql, val)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=PORT)