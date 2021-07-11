import time
from typing import List

from fastapi import Depends, FastAPI, HTTPException

from . import crud, database, models, schemas
from .database import db_state_default

database.db.connect()
database.db.create_tables([models.User, models.Item])
database.db.close()

app = FastAPI()

sleep_time = 10


async def reset_db_state():
    """
    For all the `contextvars` parts to work, we need to make sure we have an
    independent value in the `ContextVar` for each request that used the
    database, and that value will be used as the database state (connection,
    transactions, etc) for the whole request.

    For that, we need to create another `async` dependency `reset_db_state()`
    that is used as a sub-dependency in `get_db()`. It will set the value for
    the context variable (with just a default `dict`) that will be used as the
    database state for the whole request. And then the dependency `get_db()` will
    store it in the database state (connections, transactions, etc).

    For the **next request**, as we will reset that context variable again in the
    `async` dependency `reset_db_state()` and then create a new connection in the
    `get_db()` dependency, that new request will have its own database state
    (connection, transaction, etc).

    If we are using a Peewee Proxy, the actual database is at `db.obj`.
    So, we would reset it with:
    ```
    async def reset_db_state():
        database.db.obj._state._state.set(db_state_default.copy())
        database.db.obj._state.reset()
    ```
    """
    database.db._state._state.set(db_state_default.copy())
    database.db._state.reset()


def get_db(db_state=Depends(reset_db_state)):
    """
    Creating a dependency that will connect the database right at the
    beginning of a request and disconnect it at the end.

    Here, we have an empty `yield` because we are actually not using the
    database object directly.

    It is connecting to the database and storing the connection data in an
    internal variable that is independent for each request (using the `contextvars` tricks)

    Because the database connection is potentially I/O blocking, this dependency
    is created we add it as a dependency.

    But we are not using the value given by this dependency (it actually doesn't give any
    value, as it has an empty `yield`). So, we don't add it to the *path operation function*
    but to the *path operation decorator* in the `dependencies` parameter.
    """
    try:
        database.db.connect()
        yield
    finally:
        if not database.db.is_closed():
            database.db.close()


@app.post("/users/", response_model=schemas.User, dependencies=[Depends(get_db)])
def create_user(user: schemas.UserCreate):
    db_user = crud.get_user_by_email(email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(user=user)


@app.get(
    "/users/{user_id}", response_model=schemas.User, dependencies=[Depends(get_db)]
)
def read_user(user_id: int):
    db_user = crud.get_user(user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post(
    "/users/{user_id}/items/",
    response_model=schemas.Item,
    dependencies=[Depends(get_db)],
)
def create_item_for_user(user_id: int, item: schemas.ItemCreate):
    return crud.create_user_item(item=item, user_id=user_id)


@app.get("/items/", response_model=List[schemas.Item], dependencies=[Depends(get_db)])
def read_items(skip: int = 0, limit: int = 100):
    items = crud.get_items(skip=skip, limit=limit)
    return get_items


@app.get(
    "/slowusers/", response_model=List[schemas.User], dependencies=[Depends(get_db)]
)
def read_slow_users(skip: int = 0, limit: int = 100):
    global sleep_time
    sleep_time = max(0, sleep_time - 1)
    time.sleep(sleep_time) # Fake long processing request
    users = crud.get_users(skip=skip, limit=limit)
    return users

"""ABOUT def VS async def
The same as with SQLAlchemy, we are not doing something like:
`user = await models.User.select().first()`
...but instead we are using:
`user = models.User.select().first()`
So, again we should declare the *path operation functions* and the
dependency without `async def`, just with a normal `def`, as:
```
# Something goes here
def read_users(skip: int = 0, limit: int = 100):
    # something goes here
```
"""

"""
This example includes an extra *path operation* that simulates a long
processing request with `time.sleep(sleep_time)`.

It will have the database connection open at the beginning and will just wait
some seconds before replying back. And each new request will wait one second
less.

This will easily let us test that our app with Peewee and FastAPI is behaving
correctly with all the stuff about threads.

If we want to check how Peewee would break our app if used without modification,
go to the `database.py` file and comment the line:
`# db._state = PeeweeConnectionState()`
And in this file, comment the body of the `async` dependency `reset_db_state()`
and replace it with a `pass`
Then run the app with uvicorn.
Open browser at `localhost:8000/docs` and create a couple of users.
Then, open 10 tabs at `localhost:8000/docs#/default/read_slow_users_slow_users_get`
at the same time.
Go to the *path operation* "Get `/slowusers/`" in all of the tabs. Use the "try it
out" button and execute the request in each tab, one right after the other.

The tabs will wait for a bit and then some of them will show `Internal Server Error`.

WHAT HAPPENS
------------
The first tab will make our app create a connection to the database and wait for some seconds before replying back and closing the database connection.

Then, for the request in the next tab, our app will wait for one second less, and so on.

This means that it will end up finishing some of the last tabs' requests earlier than some of the previous ones.

Then one the last requests that wait less seconds will try to open a database connection, but as one of those previous requests for the other tabs will probably be handled in the same thread as the first one, it will have the same database connection that is already open, and Peewee will throw an error and we will see it in the terminal, and the response will have an `Internal Server Error`.

This will probably happen for more than one of those tabs.

If we had multiple clients talking to the app exactly at the same time, this is what could happen.

And as our app starts to handle more and more clients at the same time, the waiting time in a single request needs to be shorter and shorter to trigger the error.

Fix Peewee with FastAPI
-----------------------
Now go back to the file `database.py` and uncomment the line
`db._state = PeeweeConnectionState()`
And in the file `main.py` file, uncomment the body of the `async` dependency `reset_db_state()`
Terminate the running app and start it again.
Repeat the same process with the 10 tabs. This time all of them will wait and we will get all the results without errors.
"""