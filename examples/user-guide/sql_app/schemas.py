"""Creating an `ItemBase` and `UserBase` Pydantic  *models* (or "schemas") to
have common attributes while creating or reading data.

And creating an `ItemCreate` and `UserCreate` that inherit from them (so they
will have the same attributes), plus any additional data (attributes) needed for
creation.

So, the user will also have a `password` when creating it.

But for security, the `password` won't be in other Pydantic *models*, for
example, it won't be sent from the API when reading a user.
"""

from typing import List, Optional

from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None


class ItemCreate(ItemBase):
    pass


"""Creating Pydantic *models*(schemas) that will be used when reading data, when
returning it from the API.

For example, before creating an item, we don't know what will be the ID assigned
to it, but when reading it (when returning it from the API) we will already
know its ID.

The same way, when reading a user, we can now declare that `items` will contain
the items that belong to this user.

Not only the IDs of those items, but all the data that we defined in the
Pydantic *model* for reading items: `Item`
"""
class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        """This `Config` class is used to provide configurations to Pydantic
        """
        # setting the attribute `orm_mode = True`
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


"""Pydantic's `orm_mode` will tell the Pydantic *model* to read the data even if
it is not a `dict`, but ann ORM model (or any other arbitrary object with attributes).

This way, instead of only trying to get the `id` value from a `dict`, as in:
`id = data["id"]`
it will also try to get it from an attribute, as in:
`id = data.id`
And with this, the Pydantic *model* is compatible with ORMs, and we can just
declare it in the `response_model` argument in our *path operations*.

We will be able to return a database model and it will read the data from it.
"""
class User(UserBase):
    id: int
    is_active: bool
    items: List[Item] = []

    class Config:
        orm_mode = True
