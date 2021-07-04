from fastapi import FastAPI

# importing `StaticFiles`
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# "Mount" a `StaticFiles()` instance in a specific path
app.mount("/static", StaticFiles(directory="static"), name="static")

"""
The first `/static` refers to the sub-path this "sub-application" will be
"mounted" on . So, any path that starts with `"/static"` will be handled
by it.

The `directory="static"` refers to the name of the directory that contains
our static files

The `name="static"` gives it a name that can be used internally by **FastAPI**

All these parameters can be different than `"static"`.
"""