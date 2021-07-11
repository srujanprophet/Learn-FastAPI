"""
A middleware doesn't have to be made for FastAPI or Starlette to work, as long as it follows the ASGI spec.

In general, ASGI middleware are classes that expect to receive an ASGI app as the first argument. So, in the documentation for third-party ASGI middlewares they will probably tell us to do something like:
```
from unicorn import UnicornMiddleware

app = SomeASGIApp()

new_app = UnicornMiddleware(app, some_config="rainbow")
```

But FastAPI provides a simpler way to do it that makes sure that the internal middlewares to handle server errors and custom exception handlers work properly.

For that, we use `app.add_middleware()`
```
from fastapi import FastAPI
from unicorn import UnicornMiddleware

app = FastAPI()

app.add_middleware(UnicornMiddleware, some_config="rainbow")
```
`app.add_middleware()` receives a middleware class as the first argument and any additional arguments to be passed to the middleware.
"""

"""HTTPSRedirectMiddleware
Enforces that all incoming requests must either be `https` or `wss`.

Any incoming requests to `http` or `ws` will be redirected to the secure scheme instead.
"""
from fastapi import FastAPI
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

app = FastAPI()

app.add_middleware(HTTPSRedirectMiddleware)


@app.get("/")
async def main():
    return {"message": "Hello World"}


"""TrustedHostMiddleware
Enforces that all incoming requests have a correctly set `Host` header, in order to guard against HTTP Host Header attacks.

The following arguments are supported:
- `allowed_hosts` - A list of domain names that should be allowed as hostnames. Wildcard domains such as `*.example.com` are supported for matching subdomains to allow any hostname either `allowed_hosts=["*"]` or omit the middleware.

If an incoming request does not validate correctly then a `400` response will be sent.
"""
from fastapi.middleware.trustedhost import TrustedHostMiddleware

app.add_middleware(
    TrustedHostMiddleware, allowed_hosts=["example.com", "*"]
)


@app.get("/a")
async def main_a():
    return {"message": "Hello World"}


"""GZipMiddleware
Handles GZip responses for any request that includes`"gzip"` in the `Accept-Encoding` header.

The middleware will handle both standard and streaming responses.

The following arguments are supported:
- `minimum_size` - Do not GZip responses that are smaller than this minimum size in bytes. Defaults to `500`.
"""
from fastapi.middleware.gzip import GZipMiddleware

app.add_middleware(GZipMiddleware, minimum_size=1000)


@app.get("/b")
async def main_b():
    return "somebigcontent"
