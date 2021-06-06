from typing import Optional

from fastapi import Body, FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

    class Config:
        schema_extra = {
            "example": {
                "name" : "Foo",
                "description": "A very nice item",
                "price": 35.4,
                "tax": 3.2
            }
        }


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results


# Field additional arguments
class ItemA(BaseModel):
    name: str = Field(..., example="Foo")
    description: Optional[str] = Field(None, example="A very nice item")
    price: float = Field(..., example=35.4)
    tax: Optional[float] = Field(None, example=3.2)


@app.put("/items_a/{item_id}")
async def update_item(item_id: int, item: ItemA):
    results = {"item_id": item_id, "item": item}
    return results


# example and examples in OpenAPI
## `body` with `example`
class ItemB(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


@app.put("/items_b/{item_id}")
async def update_item(
    item_id: int,
    item: ItemB = Body(
        ...,
        example={
            "name": "Foo",
            "description": "A very nice item",
            "price": 35.4,
            "tax": 3.2
        },
    ),
):
    results = {"item_id": item_id, "item": item}
    return results


## `body` with multiple `examples`
@app.put("/items_c/{item_id}")
async def update_item(
    *,
    item_id: int,
    item: ItemB = Body(
        ...,
        examples={
            "normal": {
                "summary": "A normal example",
                "description": "A **normal** item works correctly.",
                "value": {
                    "name": "Foo",
                    "description": "A very nice item",
                    "price": 35.4,
                    "tax": 3.2
                },
            },
            "converted": {
                "summary": "An example with converted data",
                "description": "FastAPI can convert price `strings` to actual `numbers` automatically",
                "value": {
                    "name": "Bar",
                    "price": "35.4",
                },
            },
            "invalid": {
                "summary": "Invalid data is rejected with error",
                "value": {
                    "name": "Baz",
                    "price": "thirty five point four",
                },
            },
        },
    ),
):
    results = {"item_id": item_id, "item": item}
    return results

