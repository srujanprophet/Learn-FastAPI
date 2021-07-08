"""
We can declare a parameter of type `Response` in our *path operation function*.
And then we can set headers in that *temporal* response object.

And then we can return any object we need, as we normally would (a `dict`, a database model, etc).

ANd if we declared a `response_model`, it will still be used to filter and convert the object we returned.

**FastAPI** will use that *temporal* response to extract the headers (also cookies and status code), and will put them in the final response that contains the value we returned, filtered by any `response_model`.

We can also declare the `Response` parameter in dependencies, and set headers (and cookies) in them
"""
from fastapi import FastAPI, Response

app = FastAPI()


@app.get("/headers-and-object/")
def get_headers(response: Response):
    response.headers["X-Cat-Dog"] = "alone in the world"
    return {"message": "Hello World"}


"""
We can also add headers when we return a `Response` directly.
Create a response and pass the headers as an additional parameter.
"""
from fastapi.responses import JSONResponse


@app.get("/headers/")
def get_headers():
    content = {"message": "Hello World"}
    headers = {"X-Cat-Dog": "alone in the world", "Content-Language": "en-US"}
    return JSONResponse(content=content, headers=headers)


"""
Custom proprietary headers can be added using the 'X-' prefix

But, if we have custom headers that we want a client in a browser to be able to see, we need to add them to our CORS configurations using the parameter `expose_headers`.
"""

