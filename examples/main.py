# pylint: disable=C0103
""" Sample Hello World App """

from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    """ Item class """

    name: str
    price: float
    is_offer: Optional[bool] = None


@app.get("/")
def read_root():
    """ Hello world function """

    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    """ Return item by id"""

    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    """ Put Item by id """

    return {"item_price": item.price, "item_id": item_id}
