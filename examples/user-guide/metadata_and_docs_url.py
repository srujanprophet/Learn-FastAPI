"""
We can set the:
    - Title: used as our API's title/name, in OpenAPI and the automatic API docs UIs
    - Description: the description of our API, in OpenAPI and the automatic API docs UIs.
    - Version: the version of our API, e.g. `v2` or `2.5.0`
"""
from fastapi import FastAPI

app = FastAPI(
    title="My Super Project",
    description="This is a very fancy project, with auto docs for the API and everything.",
    version="2.5.0"
)


@app.get("/items")
async def read_items():
    return [{"name": "Foo"}]

"""
We can also add additional metadata for the different tags used to group our path operations with the parameter `openapi_tags`
It takes a list containing one dictionary for each tag.
Each dictionary can contain:
    - `name` (**required**): a `str` with the same tag name you use in the `tags` parameter in our *path operations* and `APIRouter`s.
    - `description`: a `str` with a short description for the tag. It can have Markdown and will be shown in the docs UI.
    - `externalDocs`: a `dict` describing external documentation with:
        - `description`: a `str` with a short description for the external docs.
        - `url` (**required**): a `str` with the URL for the external documentation.
"""
from fastapi import FastAPI

tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users. The **login** logic is also here",
    },
    {
        "name": "items",
        "description": "Manage items. So _fancy_ they have their own docs.",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
]

app = FastAPI(openapi_tags=tags_metadata)


# Using the `tags` parameter with our *path operations* (and `APIRouter`s) to
# assign them to different tags
@app.get("/users_a", tags=["users"])
async def get_users():
    return [{"name": "Harry"}, {"name": "Ron"}]


@app.get("/items_a", tags=["items"])
async def get_items():
    return [{"name": "wand"}, {"name": "flying broom"}]

"""
By default, the OpenAPI schema is served at `/openapi.json`
But we can configure it with the parameter `openapi_url`.
For example, to set it to be served at `/api/v1/openapi.json`

If we want to disable the OpenApi schema completely, we can set `openapi_url=None`, that will also disable the documentation user interfaces that use it.
"""
from fastapi import FastAPI

app = FastAPI(openapi_url="/api/v1/openapi.json")

@app.get("/items_b")
async def read_items():
    return [{"name": "Foo"}]

"""
We can configure the two documentation user interfaces included:
    - **Swagger UI**: served at `/docs`
        - We can set its URL with the parameter `docs_url`
        - We can disable it by setting `docs_url=None`
    - ReDoc: served at `redoc`
        - We can set its URL with the parameter `redoc_url`
        - We can disable it by setting `redoc_url=None`
"""
from fastapi import FastAPI

app = FastAPI(docs_url="/documentation", redoc_url=None)


@app.get("/items_c")
async def read_items():
    return [{"name": "Foo"}]

