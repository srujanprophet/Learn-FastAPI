from typing import Optional, Set

from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: Set[str] = []


@app.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    return item


'''
Tags
'''
@app.post("/items_a", response_model=Item, tags=["items"])
async def create_item(item: Item):
    return item


@app.get("/items_a", tags=["items"])
async def read_items():
    return [{"name": "Foo", "price": 42}]


@app.get("/users", tags=["users"])
async def read_users():
    return [{"username": "johndoe"}]


'''
Summary and Description
'''
@app.post(
    "/items_b",
    response_model=Item,
    summary="Create an item",
    description="Create an item with all the information, name, description, price, tax and a set of unique tags",
)
async def create_item(item: Item):
    return item


'''
Description from Docstring
'''
@app.post("/items_c", response_model=Item, summary="Create an item")
async def create_item(item: Item):
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price** : required
    - **tax**: If the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """
    return item


'''
Response Description
'''
@app.post(
    "/items_d",
    response_model=Item,
    summary="Create an item",
    response_description="The created item",
)
async def create_item(item: Item):
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price** : required
    - **tax**: If the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """
    return item


'''
Deprecate a Path Operation
'''
@app.get("/elements", tags=["items"], deprecated=True)
async def read_elements():
    return [{"item_id": "Foo"}]

