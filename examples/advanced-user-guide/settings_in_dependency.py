"""
In some occasions it might be useful to provide the settings from a dependency,
instead of having a global object with `settings` that is used everywhere.

This could be especially useful during testing, as it's very easy to override a
dependency with our own custom settings.

Here, we create a dependency that returns a new `config.Settings()`
And the, we can require it form the *path operation function* as a dependency
and use it anywhere we need it.
"""
from functools import lru_cache

from fastapi import Depends, FastAPI

from config import Settings

app = FastAPI()


@lru_cache
def get_settings():
    """Reading a file from disk is normally a costly (slow) operation, so we
    probably want to do it only once and then re-use the same settings object,
    instead of reading it for each request.
    But every time we do:
    `Settings()`
    a new `Settings` object would be created, and at creation it would read the
    `.env` file again.
    If the dependency function was just like:
    ```python
    def get_settings():
        return Settings()
    ```
    we would create that object for each request, and we would be reading the `.env`
    file for each request.
    But as we are using the `@lru_cache` decorator on top, the `Settings` object will
    be created only once, the first time it's called.
    Then for any subsequent calls of `get_settings()` in the dependencies for the next
    requests, instead of executing the internal code of `get_settings()` and creating a
    neww `Settings` object, it will return the same object that was returned on the first
    call, again and again.
    """
    return config.Settings()


@app.get("/info")
async def info(settings: Settings = Depends(get_settings)):
    return {
        "app_name": settings.app_name,
        "admin_email": settings.admin_email,
        "items_per_user": settings.items_per_user,
    }

"""`lru_cache` TECHNICAL DETAILS
`@lru_cache()` modifies the function it decorates to return the same value
that was returned the first time, instead of computing it again, executing
the code of the function every time.

So, the function below it will be executed once for each combination of arguments.
And then the values returned by each of those combinations of arguments will be used
again and again whenever the function is called with exactly the same combination of
arguments.

For example, if we have a function:
```python
def say_hi(name: str, salutation: str = "Ms."):
    return f"Hello {salutation} {name}"
```
In the case of dependency `get_settings()`, the function doesn't even take any arguments,
so it always returns the same value.

That way, it behaves almost as if it was just a global variable. But as it uses a
dependency function, then we can override it easily for testing.

`@lru_cache` is part of `functools` which is part of Python's standard library.  
"""