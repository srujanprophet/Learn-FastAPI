"""
We can declare a parameter of type `Response` in our *path operation function*.

And then we can set cookies in that *temporal* response object.

And then we can return any object we need, as we normally would (a `dict`, a database model, etc).

And if we declared a `response_model`, it will still be used to filter and convert the object we returned.

**FastAPI** will use that *temporal* response to extract the cookies (also headers and status code), and will put them in the final response that contains the value we returned, filtered by any `response_model`.

We can also declare the `Response` parameter in dependencies, and set cookies (and headers) in them.
"""
from fastapi import FastAPI, Response

app = FastAPI()


@app.post("/cookie-and-object/")
def create_cookie(response: Response):
    response.set_cookie(key="fakesession", value="fake-cookie-session-value")
    return {"message": "Come to the dark side, we have cookies"}


"""
We can also create cookies when returning a `Response` directly in our code.

To do that, we can create a response, then set cookies in it, and then return it.
"""
from fastapi.responses import JSONResponse


@app.post("/cookie/")
def create_cookie():
    content = {"message": "Come to the dark side, we have cookies"}
    response = JSONResponse(content=content)
    response.set_cookie(key="fakesession", value="fake-cookie-session-value")
    return response
