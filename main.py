""" Sample Hello World App """
from typing import Optional

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    """ Hello world function """
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    """ Return item by id"""
    return {"item_id": item_id, "q": q}
