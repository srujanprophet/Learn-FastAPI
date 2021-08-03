"""OVERRIDING DEPENDENCIES DURING TESTING
There are some scenarios where we might want to override a dependency during testing.
We don't want the original dependency to run (nor any of the sub-dependencies it might have).
Instead, we want to provide a different dependency that will run only during tests (possibly only some specific tests), and will provide a value that can be used where the value of the original dependency was used.
"""

"""USE CASES: EXTERNAL SERVICE
An example could be that we have an external authentication provider that we need to call.
We send it a token and it returns an authenticated user.
This provider might be charging us per request, and calling it might take some extra time than if we had a fixed mock user for tests.
We probably want to test the external provider once, but not necessarily call it for every test that runs.
In this case, we can override the dependency that calls that provider, and use a custom dependency that returns a mock user, only for or tests.
"""

"""USE THE `app.dependency_overrides` attribute
For these cases, our **FastAPI** application has an attribute `app.dependency_overrides`, it is a simple `dict`.
To override a dependency for testing, we put as a key the original dependency ( a function), and as the value, our dependency override (another function)
And then **FastAPI** will call that override instead of the original dependency.
"""
from typing import Optional

from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

app = FastAPI()


async def common_parameters(q: Optional[str] = None, skip: int  = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}


@app.get("/items")
async def read_items(commons: dict = Depends(common_parameters)):
    return {"message": "Hello Items!", "params": commons}


@app.get("/users/")
async def read_users(commons: dict = Depends(common_parameters)):
    return {"message": "Hello Users!", "params": commons}


client = TestClient(app)


async def override_dependency(q: Optional[str] = None):
    return {"q": q, "skip": 5, "limit": 10}


app.dependency_overrides[common_parameters] = override_dependency


def test_override_in_items():
    response = client.get("/items")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello Items!",
        "params": {"q": None, "skip": 5, "limit": 10},
    }


def test_override_in_items_with_q():
    response = client.get("/items/?q=foo")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello Items!",
        "params": {"q": "foo", "skip": 5, "limit": 10},
    }


def test_override_in_items_with_params():
    response = client.get("/items/?q=foo&skip=100&limit=200")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello Items!",
        "params": {"q": "foo", "skip": 5, "limit": 10}
    }

"""
We can set a dependency override for a dependency used anywhere in our **FastAPI** application.
The original dependency could be used in a *path operation function*, a *path operation decorator* (when we don't use the return value), a `.include_router()` call, etc.
FastAPI will still be able to override it.

Then we can reset our overrides (remove them) by setting `app.dependency_overrides` to be an empty `dict`:
`app.dependency.overrides = {}`

If we want to override a dependency only during some tests, we can set the override at the beginning of the test (inside the test funciton) and reset it at the end (at the end of the test function)
"""
