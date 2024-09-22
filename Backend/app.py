from fastapi import FastAPI, HTTPException, File, UploadFile, Form
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.middleware.cors import CORSMiddleware
from inference_sdk import InferenceHTTPClient
import uvicorn
import mysql.connector
import sys
import os
import shutil
from cerebras.cloud.sdk import Cerebras
import httpx
from PIL import Image, ExifTags
from PIL.ExifTags import TAGS, GPSTAGS

# NOTE: Always store API keys as environment variables
PORT = int(sys.argv[1])

origins = ["http://localhost:3000"]

app = FastAPI()

WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"

global prediction_val

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
    file_location = f"/home/shubs/hackathon/SnapSpark/Backend/{UPLOAD_DIR}/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    imagename = f"/home/shubs/hackathon/SnapSpark/Backend/{UPLOAD_DIR}/" + file.filename
    latitude, longitude = get_lat_long(imagename)

    mydb = mysql.connector.connect(
        host="localhost",
        user=os.getenv("MYSQL_USR"),
        password=os.getenv("MYSQL_PASS"),
        database="firedb"
    )
    mycursor = mydb.cursor()

    mycursor.execute("""
        CREATE TABLE IF NOT EXISTS coordinates (
            id INT AUTO_INCREMENT PRIMARY KEY,
            filename VARCHAR(255),
            latitude FLOAT,
            longitude FLOAT
        )
    """)
    
    sql = "INSERT INTO coordinates (filename, latitude, longitude) VALUES (%s, %s, %s)"
    val = (file.filename, latitude, longitude)
    mycursor.execute(sql, val)
    mydb.commit()
    
    api_key = os.getenv("WEATHER_KEY")
    params = {
        "lat": latitude,
        "lon": longitude,
        "appid": api_key
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(WEATHER_API_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        mycursor.execute("""
            CREATE TABLE IF NOT EXISTS conditions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                filename VARCHAR(255),
                temperature FLOAT,
                humidity FLOAT,
                wind_speed FLOAT
            )
        """)

        sql = "INSERT INTO conditions (filename, temperature, humidity, wind_speed) VALUES (%s, %s, %s, %s)"
        val = (file.filename, temperature, humidity, wind_speed)
        mycursor.execute(sql, val)
        mydb.commit()

        ROBO_API_KEY = os.getenv("ROBO_API_KEY")

        CLIENT = InferenceHTTPClient(
            api_url="https://classify.roboflow.com",
            api_key=ROBO_API_KEY
        )

        result = CLIENT.infer(imagename, model_id="snapspark/1")
        confidence = float(result['predictions'][0]['confidence'])*100.0
        if result['predictions'][0]['class'] == "Low Risk":
            prediction_val = 100.0 - confidence
        else:
            prediction_val = confidence

            mycursor.close()
            mydb.close()

            return {
                "temperature": temperature,
                "humidity": humidity,
                "wind_speed": wind_speed
            }
    else:
        raise HTTPException(status_code=response.status_code, detail="Error fetching weather data")

@app.get("/result")
async def get_value():
    return {"value": prediction_val}

global cerebras_response

@app.post("/put_address")
async def put_address(
    address: UploadFile = File(...)
):
    client = Cerebras(
    # This is the default and can be omitted
    api_key=os.environ.get("CEREBRAS_API_KEY"),
    )
    prompt = "What are some wildfire safety precautions, if any, for someone living at "+address
    completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama3.1-8b",
    )
    cerebras_response = completion
    
@app.get("/ai-result")
async def get_value():
    return {"response": cerebras_response}
    
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=PORT)