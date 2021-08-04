"""THE NOTMAL PROCESS
A `FastAPI` application (instance) has an `.openapi()` method that is expected to return the OpenAPI schema.

As part of the application object creation, a *path operation* for `/openapi.json` (or for whatever we set our `openapi_url`) is registered.

It just returns a JSON response with the result of the application's `.openapi()` method.

By default, what the method `.openapi()` does is check property `.openapi_schema` to see if it has contents and return them.

If it doesn't, it generates them using the utility function at `fastapi.openapi.utils.get_openapi`.

And that function `get_openapi()` receives as parameters:
    - `title`: The OpenAPI title, shown in the docs.
    - `version`: The version of our API, e.b. `2.5.0`
    - `openapi_version`: The version of the OpenAPI specification used. By default, the latest `3.0.2`
    - `description`: The description of our API
    - `routes`: A list of routes, these are each of the registered *path operations*. They are taken from `app.routes`.
"""
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

# writing all our **FastAPI** application as normally
app = FastAPI()


@app.get("/items/")
async def read_items():
    return [{"name": "Foo"}]


def custom_openapi():
    """Using the same utility function to generate the OpenAPI schema, inside a `custom_openapi()` function

    We can use the property `.openapi_schema` as a "cache", to store our generated schema. That way, our application won't have to generate the schema every time a user opens our API docs.
    It will be generated only once, and then the same cached schema will be used for the next requests.
    """
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Custom title",
        version="7.7.3",
        description="This is a very custom OpenAPI schema",
        routes=app.routes,
    )
    # we can add the ReDoc extension, adding a custom `x-logo` to the `info` "object" in the OpenAPI schema
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

# replacing the `openapi()` method with our new function
app.openapi = custom_openapi