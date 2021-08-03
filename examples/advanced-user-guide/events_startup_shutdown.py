"""
We can define event handlers (functions) that need to be executed before the application starts up, or when the application is shutting down.
These functions can be declared as `async def` or normal `def`.

To add a function that should be run before the application starts, declare it with the event `"startup`"

To add a function that should be run when the application is shutting down, declare it with the event `"shutdown"`
"""
from fastapi import FastAPI

app = FastAPI()

items = {}


@app.on_event("startup")
async def startup_event():
    """The `startup` event handler will initialize the items "database" (just a `dict`) with some values.
    We can add more than one event handler function. And our application won't start receiving requests until all the `startup` event handlers have completed.
    """
    items["foo"] = {"name": "Fighters"}
    items["bar"] = {"name": "Tenders"}


@app.get("/items/{item_id}")
async def read_items(item_id: str):
    return items[item_id]


@app.on_event("shutdown")
def shutdown_event():
    """This `shutdown` event handler function will write a text line `"Application shutdown`" to a file `log.txt`.
    """
    with open("log.txt", mode="a") as log:
        log.write("Application shutdown")


@app.get("/items/")
async def read_items():
    return [{"name": "Foo"}]
