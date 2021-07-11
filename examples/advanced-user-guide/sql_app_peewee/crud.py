"""
There are some differences with SQLAlchemy.

We don't pass a `db` attribute around. Instead we use the models
directly. This is because the `db` object is a global object, that
includes all the connection logic. That's why we had to do all the
`contextvars` updates.

Also, when returning several objects, like in `get_users`, we directly
call `list`, like in:
`list(models.User.select())`
This is for the same reason that we had to create a custom `PeeweeGetterDict`.
But bu returning something that is already a `list` instead of the `peewee.ModelSelect`
the `response_model` in the *path operation* with `List[models.User]` will work
correctly.
"""
from .import models, schemas


def get_user(user_id: int):
    return models.User.filter(models.User.id == user_id).first()


def get_user_by_email(email: str):
    return models.User.filter(models.User.email == email).first()


def get_users(skip: int = 0, limit: int = 100):
    return list(models.User.select().offset(skip).limit(limit))


def create_user(user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db_user.save()
    return db_user


def get_items(skip: int = 0, limit: int = 100):
    return list(models.Item.select().offset(skip).limit(limit))


def create_user_item(item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db_item.save()
    return db_item