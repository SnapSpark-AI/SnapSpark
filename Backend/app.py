from fastapi import FastAPI
import uvicorn
import sys
import os

# NOTE: Always store API keys as environment variables

PORT = int(sys.argv[1])

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=PORT)
