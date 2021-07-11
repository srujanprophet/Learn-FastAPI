"""
The main issue with Peewee and FastAPI is that Peewee relies heavily on Python's `threading.local` and it doesn't have a direct way to override it or let us handle connections/sessions directly (as done by SQLAlchemy)

And `threading.local` is not compatible with the new async features of modern Python.

`threading.local` is used to have a "magic" variable that has a different value for each thread.
This was useful in older frameworks designed to have one single thread per request, no more, no less. Using this, each request would have its own database connection/session, which is the actual final goal.
But FastAPI, using the new async features, could handle more than one request on the same thread. And at the same time, for a single request, it could run multiple things in different threads (in a threadpool), depending on if we use `async def` or normal `def`. This is what gives all the performance improvements to FastAPI.

But Python3.7 and above provide a more advanced alternative to `threading.local`, that could also be used in the places where `threading.local` would be used, but is compatible with the new async features.

It'c called `contextvars`.

We are going to override the internal parts of Peewee that use `threading.local` and replace them with `contextvars`, with the corresponding updates.
"""
from contextvars import ContextVar

import peewee

DATABASE_NAME = "test.db"
db_state_default = {"closed": None, "conn": None, "ctx": None, "transactions": None}
db_state = ContextVar("db_state", default=db_state_default.copy())


class PeeweeConnectionState(peewee._ConnectionState):
    """
    This class inherits from a special internal class used by Peewee. It has all the logic to make Peewee use `contextvars` instead of `threading.local`.

    `contextvars` works a bit differently than `threading.local`. But the rest of Peewee's internal code assumes that this class works with `threading.local`.

    So, we need to do some extra tricks to make it work as if it was just using `threading.local`. The `__init__`, `_setattr__`, and `__getattr__` implement all the required tricks for this to be used by Peewee without knowing that it is now compatible with FastAPI.
    """
    def __init__(self, **kwargs):
        super().__setattr__("_state", db_state)
        super().__init__(**kwargs)

    def __setattr__(self, name, value):
        self._state.get()[name] = value

    def __getattr__(self, name):
        return self._state.get()[name]


"""
The argument:
`check_same_thread=False`
is equivalent to the one in the SQLAlchemy:
`connect_args={"check_same_thread": False}`
...it is needed only for `SQLite`.
"""
db = peewee.SqliteDatabase(DATABASE_NAME, check_same_thread=False)

# overwriting the `._state` internal attribute in the Peewee database `db` object using the new `PeeweeConnectionState`
db._state = PeeweeConnectionState()
