"""In this file we will have reusable functions to interact with the data in
the database.
**CRUD** comes from: **C**reate, **R**ead, **U**pdate, and **D**elete.
...although in this example, we are only creating and reading
"""

"""
Import `Session` from `sqlalchemy.orm`, this will allow us to declare the type
of the `db` parameters and have better type checks and completion in our
functions.

Import `models` (the SQLAlchemy models) and `schemas` (the Pydantic *models*/
schemas).

Create utility functions to:
- Read a single user by ID and by email
- Read multiple users
- Read multiple items
"""

from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


"""Creating utility functions to create data.
The steps are:
- Create a SQLAlchemy model *instance* with our data.
- `add` that instance object to our database session.
- `commit` the changes to the database (so that they are saved).
- `refresh` our instance (so that it contains any new data from the database,
like the generated ID).
"""
def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commmit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
