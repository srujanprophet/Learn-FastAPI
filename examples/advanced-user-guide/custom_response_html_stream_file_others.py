"""
We can also declare the `Response` that we want to be used, in the *path operation decorator*.

The contents that we return from our *path operation function* will be put inside of that `Response`.

And if that `Response` has a JSON media type (`application/json`), like is the case with `JSONResponse` and `UJSONResponse`, the data we return will be automatically converted (and filtered) with any Pydantic `response_model` that we declared in the *path operation decorator*.
"""

from fastapi import FastAPI
# importing the `Response` class (sub-class) and declaring it in the *path operation decorator*
from fastapi.responses import ORJSONResponse

app = FastAPI()


@app.get("/items/", response_class=ORJSONResponse)
async def read_items():
    """
    The parameter `response_class` will also be used to define the "media type" of the response.
    In this case, the HTTP header `Content-Type` will be set to `application/json`.
    And it will be documented as such in OpenAPI
    """
    return [{"item_id": "Foo"}]


"""
To return a response with HTML directly from **FastAPI**, using `HTMLResponse`
"""
# importing `HTMLResponse`
from fastapi.responses import HTMLResponse


@app.get("/items_a/", response_class=HTMLResponse)
async def read_items():
    """
    The parameter `response_class` will also be used to define the "media type" of the response.
    In this case, the HTTP header `Content-Type` will be set to `text/html`
    And it will be documented as such in OpenAPI.
    """
    return """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Look ma! HTML!</h1>
        </body>
    </html>
    """


"""
We can also override the response directly in our *path operation*, by returning it.
The same example from above, returning an `HTMLResponse`, could look like:
"""
@app.get("/items_b")
async def read_items():
    """
    A `Response` returned directly by our *path operation function* won't be documented in OpenAPI (for example, the `Content-Type` won't be documented) and won't be visible in the automatic interactive docs.
    The actual `Content-Type` header, status_code, etc. will come from the `Response` object we returned.
    """
    html_content = """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Look ma! HTML!</h1>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)


"""
If we want to override the response from inside of the function but at the same time document the "media type" in OpenAPI, we can use the `response_class` parameter AND return a `Response` object.

The `response_class` will then be used only to document the OpenAPI *path operation*, but our `Response` will be used as is.

In this example, the function `generate_html_response()` already generates and returns a `Response` instead of returning the HTML in a `str`.

By returning the result of calling `generate_html_response()`, we are already returning a `Response` that will override the defaul **FastAPI** behavior.

But as we passed the `HTMLResponse` in the `response_class` too, **FastAPI** will know how to document it in OpenAPI and the interactive docs as HTML with `text/html`
"""
def generate_html_response():
    html_content = """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Look ma! HTML!</h1>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)


@app.get("/items_c/", response_class=HTMLResponse)
async def read_items():
    return generate_html_response()


"""
The main `Response` class, all the other responses inherit from it.

We can return it directly.

It accepts the following parameters:
    - `content` - A `str` or `bytes`
    - `status_code` - An `int` HTTP status code
    - `headers` - A `dict` of strings
    - `media_type` - A `str` giving the media type. E.g. `"text/html"`.

FastAPI (actually Starlette) will automatically include a Content-Length header. It will also include a Content-Type header, based on the media_type and appending a charset for text types.
"""
from fastapi import Response

@app.get("/legacy")
def get_legacy_data():
    data = """<?xml version="1.0"?>
    <shampoo>
    <Header>
        Apply shampoo here.
    </Header>
    <Body>
        You'll have to use soap here.
    </Body>
    </shampoo>
    """
    return Response(content=data, media_type="application/xml")


"""
`HTMLResponse` takes some text or bytes and returns an HTML response.

`PlainTextResponse` takes some text or bytes and returns a plain text response.
"""
from fastapi.responses import PlainTextResponse


@app.get("/", response_class=PlainTextResponse)
async def main():
    return "Hello World"


"""
`JSONResponse` takes some data and returns an `application/json` encoded response. This is the default response used in **FastAPI**.

`ORJSONResponse` is a fast alternative JSON response using `orjson`.

`UJSONResponse` is an alternative JSON response using `ujson`.
"""
from fastapi.responses import UJSONResponse


@app.get("/items_d/", response_class=UJSONResponse)
async def read_items():
    """
    `ujson` is less careful than Python's built-in implementation in how it handles some edge-cases.
    It is possible that `ORJSONResponse` might be a faster alternative.
    """
    return [{"item_id": "Foo"}]


"""
`RedirectResponse` returns an HTTP redirect. Uses a 307 status code (Temporary Redirect) by default.
We can return a `RedirectResponse` directly,

or we can use it in the `response_class` parameter. If we do that, then we can return the URL directly from our *path operation* function.
"""
from fastapi.responses import RedirectResponse


@app.get("/typer")
async def redirect_typer():
    return RedirectResponse("https://typer.tiangolo.com")


@app.get("/fastapi", response_class=RedirectResponse)
async def redirect_fastapi():
    """
    In this case, the `status_code` used will be the default one for the `RedirectResponse`, which is `307`.
    """
    return "https://fastapi.tiangolo.com"


@app.get("/pydantic", response_class=RedirectResponse, status_code=302)
async def redirect_pydantic():
    """
    We can also use the `status_code` parameter combined with the `response_class` parameter
    """
    return "https://pydantic-docs.helpmanual.io/"


"""
`StreamingResponse` takes an async generator or a normal generator/iterator and streams the response body.
"""
from fastapi.responses import StreamingResponse


async def fake_video_streamer():
    for i in range(10):
        yield b"some fake video bytes"


@app.get("/a")
async def main():
    return StreamingResponse(fake_video_streamer())


some_file_path = "large-video-file.mp4"


@app.get("/b")
def main():
    """
    If we have a file-like object (e.g. the object returned by `open()`), we can return it in a `StreamingResponse`.
    This includes many libraries to interact with cloud storage, video processing, and others.
    Here, as we are using standard `open()` that doesn't support `async` and `await`, we declare the path operation with normal `def`.
    """
    file_like = open(some_file_path, mode="rb")
    return StreamingResponse(file_like, media_type="video/mp4")


"""
`FileResponse` asynchronously streams a file as the response.

Takes a different set of arguments to instantiate than the other response types:
    - `path` - The filepath to the file to stream
    - `headers` - Any custom headers to include, as a dictionary.
    - `media_type` - A string giving the media type. If unset, the filename or path will be used to infer a media type.
    - `filename` - If set, this will be included in the response `Content-Disposition`

File responses will include appropriate `Content-Length`, `Last-Modified`, and `ETag` headers.
"""
from fastapi.responses import FileResponse


@app.get("/c")
async def main():
    return FileResponse(some_file_path)


# we can also use the `response_class` parameter.
@app.get("/d", response_class=FileResponse)
async def main():
    """
    In this case, we can return the file path directly from our *path operation* function
    """
    return some_file_path


"""
When creating a **FastAPI** class instance or an `APIRouter` we can specify which response class to use by default.

The parameter that defines this is `default_response_class`.

In this example, **FastAPI** will use `ORJSONResponse` by default, in all *path operations*, instead of `JSONResponse`.
"""
from fastapi.responses import ORJSONResponse


@app.get("/items_e")
async def read_items():
    """
    We can still override `response_class` in *path operations* as before.
    """
    return [{"item_id": "Foo"}]
