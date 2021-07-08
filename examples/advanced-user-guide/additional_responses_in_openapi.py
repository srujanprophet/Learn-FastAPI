"""
We can pass to our *path operation decorators* a parameter `responses`.

It receives a `dict`, the keys are status codes for each response, like `200`, and the values are other `dict`s with the information for each of them.

Each of those response `dict`s can have a key `model`, containing a Pydantic model, just like `response_model`.

**FastAPI** will take that model, generate its JSON Schema and include it in the correct place in OpenAPI.
"""
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class Item(BaseModel):
    id: str
    value: str


class Message(BaseModel):
    message: str


app = FastAPI()


@app.get("/items/{item_id}", response_model=Item, responses={404: {"model": Message}})
async def read_item(item_id: str):
    """In this example, declaring another response with status code `404` and a Pydantic model `Message`

    We have to return the `JSONResponse` directly
    """
    if item_id == "foo":
        return {"id": "foo", "value": "there goes my hero"}
    else:
        return JSONResponse(status_code=404, content={"message": "Item not found"})


"""
We can use this same `responses` parameter to add different media types for the same main response.

For example, we can add an additional media type of `image/png`, declaring that our *path operation* can return a JSON object (with media type `application/json`) or a PNG image
"""
from typing import Optional

from fastapi.responses import FileResponse


@app.get(
    "/items_a/{item_id}",
    response_model=Item,
    responses={
        200: {
            "content": {"image/png": {}},
            "description": "Return the JSON item or an image.",
        }
    },
)
async def read_item(item_id: str, img: Optional[bool] = None):
    if img:
        # we have to return the image using a `FileResponse` directly
        return FileResponse("image.png", media_type="image/png")
    else:
        return {"id": "foo", "value": "there goes my hero"}


"""
We can also combine response information from multiple places, including the `response_model`, `status_code`, and `responses` parameters.

We can declare a `response_model`, using the default status code `200` or a custom one if we need), and then declare additional information for that same response in `responses`, directly in the OpenAPI schema.

**FastAPI** will keep the additional information from `responses`, and combine it with the JSON Schema from our model.

For example, we can declare a response with a status code `404` that uses a Pydantic model and has a custom `description`.

And a response model with a status code `200` that uses our `response_model`, but includes a custom `example`
"""
@app.get("/items_b/{item_id}",
    response_model=Item,
    responses={
        404: {"model": Message, "description": "The item was not found"},
        200: {
            "description": "Item requested by ID",
            "content": {
                "application/json": {
                    "example": {"id": "bar", "value": "The bar tenders"}
                }
            },
        },
    },
)
async def read_item(item_id: str):
    if item_id == "foo":
        return {"id": "foo", "value": "There goes my hero"}
    else:
        return JSONResponse(status_code=404, content={"message": "Item not found"})


"""
We might want to have some predefined responses that apply to many *path operations*, but we want to combine them with custom responses needed by each *path operation*.

For those cases, we can use the Python technique of "unpacking" a `dict` with `**dict_to_unpack`.

We can use that technique to re-use some predefined responses in our *path operations* and combine them with additional custom ones.
"""
from fastapi.responses import FileResponse

responses = {
    404: {"description": "Item not found"},
    302: {"description": "The item was moved"},
    403: {"description": "Not enough privileges"},
}


@app.get(
    "/items_c/{item_id}",
    response_model=Item,
    responses={**responses, 200: {"content": {"image/png": {}}}},
)
async def read_item(item_id: str, img: Optional[bool] = None):
    if img:
        return FileResponse("image.png", media_type="image/png")
    else:
        return {"id": "foo", "value": "there goes my hero"}
