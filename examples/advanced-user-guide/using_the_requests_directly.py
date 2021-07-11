"""
Up to now, we have been declaring the parts of the request that we need with their types.

Taking data from:
    - The path as parameters
    - Headers
    - Cookies
    - etc.

And by doing so, **FastAPI** is validating that data, converting it and generating documentation for our API automatically.

But there are situations where we might need to access the `Request` object directly.

Let's imagine that we want to get the client's IP address/host inside of our *path operation function*.

For that, we need to access the request directly.
"""
from fastapi import FastAPI, Request

app = FastAPI()


@app.get("/items/{item_id}")
def read_root(item_id: str, request: Request):
    client_host = request.client.host
    return {"client_host": client_host, "item_id": item_id}