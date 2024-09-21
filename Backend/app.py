from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
import uvicorn
import sys
import os

# NOTE: Always store API keys as environment variables

PORT = int(sys.argv[1])

app = FastAPI()

MONGO = os.environ['MONGODB_URI']

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/sourceimages/{item_id}")
def read_item(item_id: int, imagename: string, latitude: float, longitude: float):
    return {
        "item_id": item_id, 
        "imagename": imagename,
        "latitude": latitude, 
        "longitude": longitude
    }
    
@app.get("/sourceimages/{item_id}")
def read_item(instantaneous_temperature: float, instantaneous_humidity: int):
    return {
        "instantaneous_temperature": instantaneous_temperature,
        "instantaneous_humidity": instantaneous_humidity
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=PORT)
