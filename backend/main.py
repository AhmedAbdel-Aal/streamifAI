from typing import Union

from fastapi import FastAPI

from aws import get_data
from pydantic import BaseModel
# from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.cors import CORSMiddleware

class Item(BaseModel):
    img_base: str

    


app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:3000",
    "http://0.0.0.0:3000",
]



@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/img")
def update_item(item: Item):
    vector = get_data(item.img_base)
    return {"data": vector}

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"]
)
