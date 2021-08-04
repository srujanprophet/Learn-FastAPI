"""
If we want to call asynchronous functions in our tests, our test functions have to be asynchronous. Pytest provides a neat library for this, called `pytest-asyncio`, that allows us to specify that some test functions are to be called asynchronously.
"""

"""HTTPX
Even if our **FastAPI** application uses normal `def` functions instead of `async def`, it is still an `async` application underneath.

The `TestClient` does some magic inside to call the asynchronous FastAPI application in our normal `def` test functions, using standard pytest. But that magic doesn't work anymore when we're using it inside asynchronous functions. By running our tests asynchronously, we can no longer use the `TestClient` inside our test functions.

Luckily, there's a nice alternative, called `HTTPX`

HTTPX is an HTTP client for Python 3 that allows us to query our FastAPI application similarly to how we did it with the `TestClient`.

The important difference between Requests and HTTPX for us is that with HTTPX we are not limited to synchronous, but can also make asynchronous requests.
"""
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Tomato"}

"""OTHER ASYNCHRONOUS FUNCTION CALLS
As the testing function is now asynchronous, we can now also call (and `await`)
other `async` functions apart from sending requests to our FastAPI application
in our tests, exactly as we would call them anywhere else in our code.
"""
