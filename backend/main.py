from typing import Union

from fastapi import FastAPI

from aws import get_data
from pydantic import BaseModel
# from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.cors import CORSMiddleware
from recommender.py import recommendation

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

@app.post("/recommendation")
def update_item(item: Item):
    vector = get_data(item.img_base)
    pubinput=[['the lord of the rings: the two towers',0.2],['the lord of the rings: the two towers',0.7],['the lord of the rings: the two towers',0.1]]
    rec=recommendation(vector,'pubinput')   
    return {"recommendation": rec}

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"]
)
