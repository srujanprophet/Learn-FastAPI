"""
First, creating the main, top-level, **FastAPI** application,
and its *path operations*
"""

from fastapi import FastAPI

app = FastAPI()


@app.get("/app")
def read_main():
    return {"message": "Hello World from main app"}

"""
Then, creating our sub-application, and its *path operations*.

This sub-application is just another standard FastAPI application, but this is the one that will be "mounted"
"""
subapi = FastAPI()


@subapi.get("/sub")
def read_sub():
    return {"message": "Hello World from sub API"}


"""
In our top-level application, `app`, mounting the sub-application `subapi`.

In this case, it will be mounted at the path `/subapi`
"""
app.mount("/subapi", subapi)

"""TECHNICAL DETAILS: `root_path`
When we mount a sub-application as described above, FastAPI will take care of communicating the mount path for the sub-application using a mechanism from the ASGI specification called a `root_path`

That way, the sub-application will know to use that path prefix for the docs UI

And the sub-application could also have its own mounted sub-applications and everything would work correctly, because FastAPI handles all these `root_path`s automatically.
"""