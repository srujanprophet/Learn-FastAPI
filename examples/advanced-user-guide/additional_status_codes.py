"""
If we want to return additional status codes apart from the main one, we can do that by returning a `Response` directly, like a `JSONResponse`, and set the additional status code directly.

For example, if we want to have a *path operation* that allows to update items, and returns HTTP status codes of 200 "OK" when successful.

But we also want it to accept new items. And when the items didn't exist before, it creates them, and returns an HTTP status code of 201 "Created".

To achieve that, import `JSONResponse`, and return our content there directly, setting the `status_code` that we want
"""
from typing import Optional

from fastapi import Body, FastAPI, status
from fastapi.responses import JSONResponse

app = FastAPI()

items = {"foo": {"name": "Fighters", "size": 6}, "bar": {"name": "Tenders", "size": 3}}


@app.put("/items/{item_id}")
async def upsert_item(
    item_id: str, name: Optional[str] = Body(None), size: Optional[int] = Body(None),
):
    if item_id in items:
        item = items[item_id]
        item["name"] = name
        item["size"] = size
        return item
    else:
        item = {"name": name, "size": size}
        items[item_id] = item
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=item)

"""
If we return additional status codes and respones directly, the won't be included in the OpenAPI schema (the API docs), because FastAPI doesn't have a way to know beforehand what we are going to return.
"""