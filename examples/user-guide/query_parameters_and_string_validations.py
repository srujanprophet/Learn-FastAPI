from typing import List, Optional

from fastapi import FastAPI, Query

app = FastAPI()


# Add Regular Expressions
@app.get("/items/")
async def read_items(
    q: Optional[str] = Query(None, min_length=3, max_length=50, regex="^fixedquery$")
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# Default Values
@app.get("/items_x/")
async def read_items_x(q: str = Query("fixedquery", min_length=3)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# Make it Required
@app.get("/items_y")
async def read_items_y(q: str = Query(..., min_length=3)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        result.update({"q": q})
    return results


# Query Parameter List/Multiple Values
@app.get("/items_z")
async def read_items_z(q: List[str] = Query(["foo", "bar"])):
    query_items = {"q": q}
    return query_items


# Query Parameter List/Multiple Values using list
@app.get("/items_a")
async def read_items_a(q: list = Query([])):
    query_items = {"q": q}
    return query_items


# Declare more metadata
@app.get("/items_b")
async def read_items_b(
    q: Optional[str] = Query(
        None,
        title="Query string",
        description="Query string for the items to search in the database that have a good match",
        min_length=3)
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# Alias Parameters
@app.get("/items_c")
async def read_items_c(q: Optional[str] = Query(None, alias="item-query")):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# Deprecating parameters
@app.get("/items_d")
async def read_items_d(
    q: Optional[str] = Query(
        None,
        alias="item-query",
        title="Query string",
        description="Query string for the items to search in the database that have a good match",
        min_length=3,
        max_length=50,
        regex="^fixedquery$",
        deprecated=True,
    )
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

