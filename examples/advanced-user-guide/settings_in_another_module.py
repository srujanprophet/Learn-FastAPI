"""SETTINGS IN ANOTHER MODULE
We could put these settings in another module file. For example we could have a file `config.py` and use it here
""" 
from fastapi import FastAPI

from config import settings

app = FastAPI()


@app.get("/info")
async def info():
    return {
        "app_name": settings.app_name,
        "admin_email": settings.admin_email,
        "items_per_user": settings.items_per_user,
    }
