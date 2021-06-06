from typing import Optional, Union, List, Dict

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()


# Multiple Models
class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: Optional[str] = None


class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None


class UserInDB(BaseModel):
    username: str
    hashed_password: str
    email: EmailStr
    full_name: Optional[str] = None


def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password


def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
    print("User saved! ..nor really")
    return user_in_db


@app.post("/user", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved


# Reduce Duplication
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None


class UserInA(UserBase):
    password: str


class UserOutA(UserBase):
    pass


class UserInDBA(UserBase):
    hashed_password: str

def fake_save_user_a(user_in: UserInA):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDBA(**user_in.dict(), hashed_password=hashed_password)
    print("User saved! ..nor really")
    return user_in_db


@app.post("/user_a", response_model=UserOutA)
async def create_user(user_in: UserInA):
    user_saved = fake_save_user_a(user_in)
    return user_saved


# Union or anyOf
class BaseItem(BaseModel):
    description: str
    type: str


class CarItem(BaseItem):
    type = "car"


class PlaneItem(BaseItem):
    type = "plane"
    size: int


items = {
    "item1": {"description": "All my friends drive a low rider", "type": "car"},
    "item2": {
        "description": "Music is my aeroplane, it's my aeroplane",
        "type": "plane",
        "size": 5,
    },
}

@app.get("/items/{item_id}", response_model=Union[PlaneItem, CarItem])
async def read_item(item_id: str):
    return items[item_id]


# List of models
class Item(BaseModel):
    name: str
    description: str


items = [
    {"name": "Foo", "description": "There comes my hero"},
    {"name": "Red", "description": "It's my aeroplane"},
]

@app.get("/items_a", response_model=List[Item])
async def read_items():
    return items


# Response with arbitrary dict
@app.get("/keyword-weights", response_model=Dict[str, float])
async def read_keyword_weights():
    return {"foo": 2.3, "bar": 3.4}
