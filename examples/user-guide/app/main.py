"""Here's where we import and use the class `FastAPI`

This will be the main file in the application that ties everything together.

And as the most of the logic will now live in its own specific module, the main file will be quite simple.
"""

# importing and creating a `FastAPI` class as normally
from fastapi import Depends, FastAPI

from .dependencies import get_token_header, get_query_token
from .internal import admin
from .routers import items, users

# declaring global dependencies that will be combined with the dependencies
# for each `APIRouter`
app = FastAPI(dependencies=[Depends(get_query_token)])

app.include_router(users.router)
app.include_router(items.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)


@app.get("/")
async def root():
    """We can also add *path operations* directly to the `FastAPI` app and it will work correctly, together with all the other *path operations* added with `app.include_router()`.
    """
    return {"message": "Hello Bigger Applications!"}

"""We can also use `.include_router() multiple times with the *same* router using different prefixes.

This can be useful, for example, to expose the same API under different prefixes, e.g. `/api/v1` and `/api/latest`.
"""

"""The same way we can include an `APIRouter` in a `FastAPI` application, we can include an `APIRouter` in another `APIRouter` using:
`router.include_router(other_router)`
Make sure to do it before including `router` in the `FastAPI` app, so that the *path operations* form `other_router` are also included.
"""
