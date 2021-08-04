from fastapi import FastAPI

from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
# importing `StaticFiles`
from fastapi.staticfiles import StaticFiles

# disabling the automatic docs, as those use the CDN by default
# To disable, setting their URLs to `None` when creating our `FastAPI` app
app = FastAPI(docs_url=None, redoc_url=None)

# "mounting" a `StaticFiles()` instance in a specific path.
app.mount("/static", StaticFiles(directory="static"), name="static")

# creating the *path operations* for the custom docs.
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    """We can re-use FastAPI's internal functions to create the HTML pages for the docs, and pass them the needed arguments:
        - `openapi_url`: the URL where the HTML page for the docs can get the OpenAPI schema for our API. We can use here the attribute `app.openapi_url`.
        - `title`: the title of our API.
        - `oauth2_redirect_url`: we can use `app.swagger_ui_oauth2_redirect_url` here to use the default.
        - `swagger_js_url`: the URL where the HTML for our Swagger UI docs can get the **JavaScript** file. This is the one that our own app is now serving.
        - `swagger_css_url`: the URL where the HTML for our Swagger UI docs can get the **CSS** file. This is the one that our own app is now serving.
    And similarly for ReDoc...

    The *path operation* for `swagger_ui_redirect` is a helper for when we use OAuth2.
    If we integrate our API with an OAuth2 provider, we will be able to authenticate and come back to the API docs with the acquired credentials. And interact with it using the real OAuth2 authentication.
    Swagger UI will handle it behind the scenes for us, but it needs this "redirect" helper.
    """
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )


@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="/static/redoc.standalone.js",
    )


# creating a *path operation* to be able to test that everything works
@app.get("/users/{username}")
async def read_user(username: str):
    return {"message": f"Hello {username}"}