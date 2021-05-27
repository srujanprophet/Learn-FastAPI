""" Code for Path Parameters """
from enum import Enum

from fastapi import FastAPI


app = FastAPI()


@app.get("/items/{item_id}")
async def read_item(item_id):
    """ Return item id """
    return {"item_id": item_id}


# Path Parameters with types
@app.get("/items_n/{item_id}")
async def read_item_number(item_id: int):
    """ Return item id as integer """
    return {"item_id": item_id}


# Order Matters
@app.get("/users/me")
async def read_user_me():
    """ Return current user """
    return {"user_id": "the current user"}


@app.get("/users/{user_id}")
async def read_user(user_id: str):
    """ Return user by id """
    return {"user_id": user_id}


# Predefined Values
class ModelName(str, Enum):
    """ Define Model Names """
    ALEXNET = "alexnet"
    RESNET = "resnet"
    LENET = "lenet"


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    """ Get predefined models """
    if model_name == ModelName.ALEXNET:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}
