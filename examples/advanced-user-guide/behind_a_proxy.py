"""
In some situations, we might need to use a **proxy** server like Traefik or Nginx with a configuration that adds an extra path prefix that is not seen by our application.

In these cases we can use `root_path` to configure our application.

The `root_path` is a mechanism provided by the ASGI specification. And it's also used internally when mounting sub-applications.
"""
from fastapi import FastAPI, Request

app = FastAPI()

"""CHECKING THE CURRENT `root_path`
We can get the current `root_path` used by our application for each request, it is part of the `scope` dictionary (that's part of the ASGI spec)
"""
@app.get("/app")
def read_main(request: Request):
    return {"message": "Hello World", "root_path": request.scope.get("root_path")}

"""SETTING THE `root_path` IN THE FASTAPI APP
Alternatively, if we don't have a way to provide a command line option like `--root-path` or equivalent, we can set the `root_path` parameter when creating our FastAPI app
"""
app = FastAPI(root_path="/api/v1")


@app.get("/app")
def read_main(request: Request):
    return {"message": "Hello World", "root_path": request.scope.get("root_path")}

"""ABOUT `root_path`
The server (Uvicorn) won't use that `root_path` for anything else than passing it to the app.

But if we go with our browser to `http://127.0.0.1:8000/app` we will see the normal response.
So, it won't be expect to be accessed at `http://127.0.0.1:8000/api/v1/app`.

Uvicorn will expect the proxy to access Uviocrn at `http://127.0.0.1:8000/app`, and then it would be the proxy's responsibility to add the extra `/api/v1` prefix on top.
"""

"""ABOUT PROXIES WITH A STRIPPED PATH PREFIX
A proxy with a stripped path prefix is only one of the ways to configure it.

Probably in many cases the default will be that the proxy doesn't have a stripped path prefix.

In a case like that (without a stripped path prefix), the proxy would listen on something like `http://testapp.com` and the browser goes to `http://testapp.com/api/v1/app` and our server (e.g, Uvicorn) listens on `http://127.0.0.1:8000` the proxy (without a stripped path prefix) would access Uvicorn at the same path `http://127.0.0.1:8000/api/v1/app`
"""

"""ADDITIONAL SERVERS
By default, **FastAPI** will create a `server` in the OpenAPI schema with the URL for the `root_path`.

But we can also provide other alternative `servers`, for example if we want the *same* docs UI to interact with a staging and production environments.

If we pass a custom list of `servers` and there's a `root_path` (because our API lives behind a proxy), **FastAPI* will insert a "server" with this `root_path` at the beginning of the list.
"""