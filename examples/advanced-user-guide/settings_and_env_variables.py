"""
Import `BaseSettings` from Pydantic and create a sub-class, very much like with a Pydantic model.

The same way as with Pydantic models, we declare class atteributes with type annotations, and possibly default values.

We can use all the same validation features and tools we use for Pydantic models, like different data types and additional validations with `Field()`.

Then , when we create an instance of that `Settings` class (in this case, in the `settings` object), Pydantic will read the environment variables in a case-insensitive way, so, an upper-case variable `APP_NAME` will still be read for the attribute `app_name`.

Next it will convert and validate the data. So, when we use that `settings` object, we will have data of the types we declared (e.g. `items_per_user` will be an `int`)

Next, we would run the server passing the configurations as environment variables, for example we could set an `ADMIN_EMAIL` and `APP_NAME`.
"""
from fastapi import FastAPI
from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Awesome API"
    admin_email: str
    items_per_user: int = 50


settings = Settings()
app = FastAPI()


@app.get("/info")
async def info():
    """Using the new `settings` object in our application
    """
    return {
        "app_name": settings.app_name,
        "admin_email": settings.admin_email,
        "items_per_user": settings.items_per_user
    }
