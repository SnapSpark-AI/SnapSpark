from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
import uvicorn
import sys
import os

# NOTE: Always store API keys as environment variables
PORT = int(sys.argv[1])

app = FastAPI()

MONGO_URI = os.getenv('MONGODB_URI')

client = AsyncIOMotorClient(MONGO_URI)
db = client.myDatabase

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.post("/imagesources/{item_id}")
async def add_image_source(item_id: int, 
                           imagename: str, 
                           latitude: float, 
                           longitude: float):
    doc = {
        "item_id": item_id, 
        "imagename": imagename, 
        "latitude": latitude, 
        "longitude": longitude
    }
    
    result = await db.imagesources.insert_one(doc)
    if result.acknowledged:
        return {"message": "Document added successfully", "item_id": item_id}
    else:
        raise HTTPException(status_code=500, detail="Failed to insert document")

@app.get("/imagesources/{item_id}")
async def read_image_source(item_id: int):
    doc = await db.imagesources.find_one({"item_id": item_id})
    if doc:
        return doc
    else:
        raise HTTPException(status_code=404, detail="Item not found")

@app.post("/location_info/{item_id}")
async def add_location_info(item_id: int, 
                            latitude: str, 
                            longitude: str, 
                            instantaneous_temperature: float, 
                            instantaneous_humidity: int):
    doc = {
        "item_id": item_id,
        "latitude": latitude,
        "longitude": longitude,
        "instantaneous_temperature": instantaneous_temperature,
        "instantaneous_humidity": instantaneous_humidity
    }
    
    result = await db.location_info.insert_one(doc) 
    if result.acknowledged:
        return {"message": "Document added successfully", "item_id": item_id}
    else:
        raise HTTPException(status_code=500, detail="Failed to insert document")

@app.get("/location_info/{item_id}")
async def read_location_info(item_id: int):
    doc = await db.location_info.find_one({"item_id": item_id})
    if doc:
        return doc
    else:
        raise HTTPException(status_code=404, detail="Item not found")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=PORT)