"""File dedicated to handling just users
"""
from fastapi import APIRouter

# creating "instance" the same way we would with the class `FastAPI`
router = APIRouter()


# using it to declare our *path operations*
@router.get("/users", tags=["users"])
async def read_users():
    """Can think of `APIRouter` as a "mini `FastAPI" class
    All the same options are supported
    All the same `parameters`, `dependencies`, `responses`, `tags`, etc.
    """
    return [{"username": "Rick"}, {"username": "Morty"}]



@router.get("/users/me", tags=["users"])
async def read_user_me():
    return {"username": "fakecurrentuser"}


@router.get("/users/{username}", tags=["users"])
async def read_user(username: str):
    return {"username": username}
