from typing import List, Optional, Set, Dict

from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl

app = FastAPI()

# List fields
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: list = []


@app.put("/items_a/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results


# List fields with type parameters
class ItemA(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: List[str] = []


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: ItemA):
    results = {"item_id": item_id, "item": item}
    return results


# Set types
class ItemB(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: Set[str] = set()


@app.put("/items_b/{item_id}")
async def update_item(item_id: int, item: ItemB):
    results = {"item_id": int, "item": item}
    return results


# Nested Models
class Image(BaseModel):
    url: str
    name: str

class ItemC(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: Set[str] = []
    image: Optional[Image] = None


@app.put("/items_c/{item_id}")
async def update_item(item_id: int, item: ItemC):
    results = {"item_id": item_id, "item": item}
    return results


# Special types and validation
class ImageA(BaseModel):
    url: HttpUrl
    name: str

class ItemD(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: Set[str] = set()
    image: Optional[ImageA] = None


@app.put("/items_d/{item_id}")
async def update_item(item_id: int, item: ItemD):
    results = {"item_id": item_id, "item": item}
    return results


''' Attributes with lists of submodels '''
class ItemE(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: Set[str] = set()
    images: Optional[List[ImageA]] = None


@app.put("/items_e/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results


# Deeply Nested Models
class Offer(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    items: List[ItemE]


@app.post("/offers")
async def create_offer(offer: Offer):
    return offer


# Bodies of pure lists
@app.post("/images/multiple")
async def create_multiple_images(images: List[ImageA]):
    return images


# Bodies of arbitrary dictS
@app.post("/index-weights")
async def create_index_weights(weights: Dict[int, float]):
    return weights

