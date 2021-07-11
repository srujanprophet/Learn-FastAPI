"""PEEWEE FOR ASYNC
Peewee was not designed for async frameworks, or with them in mind.

Peewee has some heavy assumptions about its defaults and about how it should be used.

If we are developing an application with an older non-async framework, and can work with all its defaults, **it can be a great tool**.

But if we need to change some of the defaults, support more than one predefined database, work with an async framework (like FastAPI), etc, we will need to add quite some complex extra code to override those defaults.
"""

"""TECHNICAL DETAILS
The Problem
------------
Peewee uses `threading.local` by default to store it's database "state" data (connections, transactions, etc).

`threading.local` creates a value exclusive to the current thread but an async framework would run all the code (e.g, for each request) in the same thread, and possibly not in order.

On top of that, an async framework could run some sync code in a threadpool (using `asyncio.run_in_executor`), but belonging to the same request.

This means that, with Peewee's current implementation, multiple tasks could be using the same `threading.local` variable and end up sharing the same connection and data (that they shouldn't), and at the same time, if they execute sync I/O-blocking code in a threadpool (as with normal `def` functions in FastAPI, in *path operations* and dependencies), that code won't have access to the database state variables, even while it's part of the same request and it should be able to get access to the same database state.

Context Variables
-----------------
Python 3.7 has `contextvars` that can create a local variable very similar to `threading.local` but also supporting these async features.

There are several things to have in mind.

The `ContextVar` has to be created at the top of the module, like:
`some_var = ContextVar("some_var", default="default value")
To set a value used in the current "context" (e.g. for the current request) use:
`some_var.set("new value")`
To get a value anywhere inside of the context (e.g. in any part handling the current request) use:
`some_var.get()`

Set context variables in the `async` dependency `reset_db_state()`
-------------------------------------------------------------------
If some part of the async code sets the value with `some_var.set("updated in function")` (e.g. like the `async` dependency), the rest of the code in it and the code that goes after (including code inside of `async` functions called with `await`) will see that new value.

So, in our case, if we set the Peewee state variable (with a default `dict`) in the `async` dependency, all the rest of the internal code in our app will see this value and will be able to reuse it for the whole request.

And the context variable would be set again for the next request, even if they are concurrent.

Set database state in the dependency `get_db()`
-----------------------------------------------
As `get_db()` is a normal `def` function **FastAPI** will make it run in a threadpool, with a *copy* of the "context", holding the same value for the context variable (the `dict` with the reset database state). Then it can add database state to that `dict`, like the connection, etc.

But if the value of the context variable (the default `dict`) was set in that normal `def` function, it would create a new value that would stay only in that thread of the threadpool, and the rest of the code (like the *path operation functions**) wouldn't have access to it. In `get_db()` we can only set values in the `dict`, but not entire `dict` itself.

Connect and disconnect in the dependency `get_db()`
---------------------------------------------------
Then , the next question would be, why not just connect and disconnect the database in the `async` dependency itself, instead of in `get_db()`?

The `async` dependency has to be `async` for the context variable to be preserved for the rest of the request, but creating and closing the database connection is potentially blocking, so it could degrade performance if it was there.

So we also need the normal `def` dependency `get_db()`.
"""
