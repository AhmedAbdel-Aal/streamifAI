from typing import Union

from fastapi import FastAPI

from aws import get_data
from pydantic import BaseModel

class Item(BaseModel):
    img_base: str

    


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/img")
def update_item(item: Item):
    vector = get_data(item.img_base)
    return {"data": vector}
