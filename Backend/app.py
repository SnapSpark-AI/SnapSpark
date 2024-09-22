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
from PIL.ExifTags import TAGS, GPSTAGS

# NOTE: Always store API keys as environment variables
PORT = int(sys.argv[1])

origins = ["http://localhost:3000"]

app = FastAPI()

weather_api = os.getenv("WEATHER_API_DEFAULT")

UPLOAD_DIR = "uploaded_images"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

def get_lat_long(image_path):
    def _get_if_exist(data, key):
        return data[key] if key in data else None
    
    def _convert_to_degrees(value):
        d = float(value[0])
        m = float(value[1])
        s = float(value[2])
        return d + (m / 60.0) + (s / 3600.0)

    image = Image.open(image_path)
    exif_data = image._getexif()
    
    if not exif_data:
        raise ValueError("No EXIF metadata found")
    gps_info = {}
    for tag, value in exif_data.items():
        tag_name = TAGS.get(tag, tag)
        if tag_name == "GPSInfo":
            for gps_tag in value:
                gps_info[GPSTAGS.get(gps_tag, gps_tag)] = value[gps_tag]
    
    gps_latitude = _get_if_exist(gps_info, "GPSLatitude")
    gps_latitude_ref = _get_if_exist(gps_info, "GPSLatitudeRef")
    gps_longitude = _get_if_exist(gps_info, "GPSLongitude")
    gps_longitude_ref = _get_if_exist(gps_info, "GPSLongitudeRef")
    
    if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
        latitude = _convert_to_degrees(gps_latitude)
        longitude = _convert_to_degrees(gps_longitude)
        
        if gps_latitude_ref != "N":
            latitude = -latitude
        if gps_longitude_ref != "E":
            longitude = -longitude
        
        return str(latitude), str(longitude)
    else:
        raise ValueError("GPS data not found")

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
    latitude, longitude = get_lat_long(imagename)
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