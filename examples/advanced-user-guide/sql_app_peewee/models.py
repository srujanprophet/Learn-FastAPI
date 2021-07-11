"""
Creating the Peewee models (classes) for `User` and `Item`.

Importing `db` from `database` and using it here.
"""
import peewee

from .database import db


class User(peewee.Model):
    """
    Peewee creates several magic attributes.
    It will automatically add an `id` attribute as an integer to be the primary key.
    It will choose the name of the tables based on the class names.
    For the `Item`, it will create an attribute `owner_id` with the integer ID of the `User`. But we don't declare it anywhere.
    """
    email = peewee.CharField(unique=True, index=True)
    hashed_password = peewee.CharField()
    is_active = peewee.BooleanField(default=True)

    class Meta:
        database = db


class Item(peewee.Model):
    title = peewee.CharField(index=True)
    description = peewee.CharField(index=True)
    owner = peewee.ForeignKeyField(User, backref="items")

    class Meta:
        database = db