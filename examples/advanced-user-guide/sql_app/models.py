"""Creating the database models
"""
# creating all the model(class) attributes
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
# creating the relationships, using `relationship` provided by SQLAlchemy ORM
from sqlalchemy.orm import relationship

# importing `Base` from `database` (the file `database.py`)
from .database import Base


class User(Base):
    """Classes that inherit from Base
    """
    __tablename__ = "users"

    # each of these attributes represents a column in its corresponding
    # database table
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    # this will become, more or less, a "magic" attribute that will contain
    # the values from other tables related to this one
    items = relationship("Item", back_populates="owner")


class Item(Base):
    """User and Item classes are the SQLAlchemy models
    The `__tablename__` attribute tells SQLAlchemy the name of the table to use in the database for each of these models.
    """
    __tablename__ = "items"

    # using `Column` from SQLAlchemy as the default value and passing a
    # SQLAlchemy class "type", as `Integer`,`String`, and `Boolean`, that
    # defines the type in the database, as an argument
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")

"""When accessing the attribute `items` in a `User`, as in `my_user.items`,
it will have a list of `Item` SQLAlchemy models (from the `items` table)
that have a foreign key pointing to this record in the `users` table.

When you access `my_user.items`, SQLAlchemy will actually go and fetch the
items from the database in the `items` table and populate them here.

And when accessing the attribute `owner` in an `Item`, it will contain a `User`
SQLAlchemy model from the `users` table. It will use the `owner_id` attribute/
column with its foreign key to know which record to get from the `users` table.
"""
