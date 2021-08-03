"""
In some cases, we may want to override the logic used by the `Request` and `APIRoute` classes.
In particular, this may be a good alternative to logic in a middleware.
For example, if we want to read or manipulate the request body before it is processed by our application.
"""
import time
import gzip
from typing import Callable, List

from fastapi import APIRouter, Body, FastAPI, HTTPException, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.routing import APIRoute


class GzipRequest(Request):
    """
    First, we create a `GzipRequest` class, which will overwrite the `Request.body()` method to decompress the body in the presence of an appropriate header.
    If there's no `gzip` in the header, it will not try to decompress the body. That way, the same route class can handle gzip compressed or uncompressed   requests.
    """
    async def body(self) -> bytes:
        if not hasattr(self, "_body"):
            body = await super().body()
            if "gzip" in self.headers.getlist("Content-Encoding"):
                body = gzip.decompress(body)
            self._body = body
        return self._body


class GzipRoute(APIRoute):
    """
    Next, we create a custom subclass of `fastapi.routing.APIRoute` that will make use of the `GzipRequest`.
    This time, it will overwrite the method `APIRoute.get_route_handler()`.
    This method returns a function. And that function is what will receive a request and return the response.
    Here, we use it to create a `GzipRequest` from the original request.
    """
    def get_route_handler(self) -> Callable:
        """The only thing the function returned by this function does differently is convert the `Request` to a `GzipRequest`.
        Doing this, our `GzipRequest` will take care of decompressing the data (if necessary) before passing it to our *path operations*.
        After that, all of the processing logic is the same.
        But because of our changes in `GzipRequest.body`, the request body will be automatically decompressed when it is loaded by **FastAPI** when needed.
        """
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            """A `Request` has a `request.scope` attribute, that's just a Python `dict` containing the metadata related to the request.
            A `Request` also has a `request.receive`, that's a function to "receive" the body of the request.
            The `scope`, `dict` and `receive` function are both part of the ASGI specification.
            And those two things, `scope` and `receive`, are what is needed to create a new `Request` instance.
            """
            request = GzipRequest(request.scope, request.receive)
            return await original_route_handler(request)

        return custom_route_handler


class ValidationErrorLoggingRoute(APIRoute):
    """We can also use this same approach to access the request body in an exception handler.
    All we need to do is handler the request inside a `try/except` block
    """
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            """If an exception occurs, the `Request` instance will still be in scope, so we can read and make use of the request body when handling the error
            """
            try:
                return await original_route_handler(request)
            except RequestValidationError as exc:
                body = await request.body()
                detail = {"errors": exc.error(), "body": body.decode()}
                raise HTTPException(status_code=422, detail=detail)

        return custom_route_handler


app = FastAPI()
app.router.route_class = GzipRoute


@app.post("/sum")
async def sum_numbers(numbers: List[int] = Body(...)):
    return {"sum": sum(numbers)}


app.router.route_class = ValidationErrorLoggingRoute


@app.post("/")
async def sum_numbers(numbers: List[int] = Body(...)):
    return sum(numbers)


class TimedRoute(APIRoute):
    """We can also set the `route_class` parameter of an `APIRouter`
    """
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            before = time.time()
            response: Response = await original_route_handler(request)
            duration = time.time() - before
            response.headers["X-Response-Time"] = str(duration)
            print(f"route duration: {duration}")
            print(f"route response: {response}")
            print(f"route response headers: {response.headers}")
            return response

        return custom_route_handler


router = APIRouter(route_class=TimedRoute)


@app.get("/")
async def not_timed():
    return {"message": "Not timed"}


@app.get("/timed")
async def timed():
    """In this example, the *path operations* under the `router` will use the custom `TimedRoute` class, and will have an extra `X-Response-Time` header in the response with the time it took to generate the response
    """
    return {"message": "It's the time of my life"}


app.include_router(router)