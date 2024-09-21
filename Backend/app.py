from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
import uvicorn
import sys
import os

# NOTE: Always store API keys as environment variables

PORT = int(sys.argv[1])

app = FastAPI()

CONNECTION_STRING = os.environ['MONGODB_URI']

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/crowdsource/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {
        "item_id": item_id, 
        "stateorprovince": stateorprovince, 
        "city": city, 
        "latitude": latitude, 
        "longitude": longitude
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=PORT)
