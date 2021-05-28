""" Examples for Query Parameters """
from typing import Optional

from fastapi import FastAPI

app = FastAPI()

fake_items_db = [{"item_name": "Football"},
                 {"item_name": "Pump"},
                 {"item_name": "Jacket"}]


@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    """ Return fake items with query parameters """
    return fake_items_db[skip: skip + limit]


@app.get("/items/{item_id}")
async def read_item_q(item_id: str, q: Optional[str] = None):
    """ Example with Optional Parameter """  # pylint: disable=C0103
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}


@app.get("/items_x/{item_id}")
async def read_item_x(item_id: str, q: Optional[str] = None,
                      short: bool = False):
    """ Bool type conversion in query parameter """  # pylint: disable=C0103
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description":
                "This is an amazing item that has a long description"}
        )
    return item


# Multiple path and query parameters
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: Optional[str] = None, short: bool = False
):
    """ Multiple path parameters and query parameters don't have to be declared
     in any specific order. They will be detected by name """
    # pylint: disable=C0103
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description":
                "This is an amazing item that has a long description"}
        )
    return item


# Required Query Parameters
@app.get("/items_y/{item_id}")
async def read_user_item_y(item_id: str, needy: str):
    """ To make a query parameter required, just not declare any default
    value """  # pylint: disable=C0103
    item = {"item_id": item_id, "needy": needy}
    return item
