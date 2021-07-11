"""
When we access a relationship in Peewee object, like in
`some_user.items`, Peewee doesn't provide a `list` of `Item`.

It provides a special custom object of class `ModelSelect`.

It's possible to create a `list` of its items with
`list(some_user.items)`.

But the object itself is not a `list`. And it's also not an
actual Python generator. Because of this, Pydantic doesn't know by default
how to convert it to a `list` of Pydantic *models*/ schemas.

But recent versions of Pydantic allow providing a custom class that
inherits from `pydantic.utils.GetterDict`, to provide the functionality
used when using the `orm_mode = True` to retrieve the values for ORM model
attributes.
"""
from typing import Any, List, Optional

import peewee
from pydantic import BaseModel
from pydantic.utils import GetterDict


class PeeweeGetterDict(GetterDict):
    """
    Creating a custom `PeeweeGetterDict` class and using it in
    all the same Pydantic *models* / schemas that use `orm_mode`

    Here, we are checking if the attribute that is being accessed
    (e.g. `.items` in `some_user.items`) is an instance of
    `peewee.ModelSelect`.
    And if that's the case, just return a `list` with it.
    And then we use it in the Pydantic *models* / schemas that use
    `orm_mode = True`, with the configuration variable
    `getter_dict = PeeweeGetterDict`.
    """
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstane(res, peewee.ModelSelect):
            return list(res)
        return res


class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: List[Item] = []

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict
