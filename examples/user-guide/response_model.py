from typing import List, Optional

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: List[str] = []


# Response Model
@app.post("/items", response_model=Item)
async def create_item(item: Item):
    return item


# Return the same input data
class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: Optional[str] = None

#### Don't do this in production
@app.post("/user", response_model=UserIn)
async def create_user(user: UserIn):
    return user


# Add an output model
class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None


@app.post("/user_a", response_model=UserOut)
async def create_user(user: UserIn):
    return user


# Response Model encoding parameters
items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []}
}


@app.get("/items/{item_id}", response_model=Item, response_model_exclude_unset=True)
async def read_item(item_id: str):
    return items[item_id]


# `response_model_include` and `response_model_exclude`
items_a = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The Bar Fighters", "price": 62, "tax": 20.2},
    "baz": {
        "name": "Baz",
        "description": "There goes my baz",
        "price": 50.2,
        "tax": 10.5,
    },
}


@app.get(
    "/items/{item_id}/name",
    response_model=Item,
    response_model_include={"name", "description"},
)
async def read_item_name(item_id: str):
    return items[item_id]


@app.get("/items/{item_id}/public", response_model=Item, response_model_exclude={"tax"})
async def read_item_public_data(item_id: str):
    return items[item_id]


# Using lists instead of sets
@app.get(
    "/items_a/{item_id}/name",
    response_model=Item,
    response_model_include=["name", "description"],
)
async def read_item_name(item_id: str):
    return items[item_id]


@app.get("/items_a/{item_id}/public", response_model=Item, response_model_exclude=["tax"])
async def read_item_public_data(item_id: str):
    return items[item_id]

