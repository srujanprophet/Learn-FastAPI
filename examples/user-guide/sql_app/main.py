"""Main FastAPI app
"""

from typing import List

from fastapi import Depends, FastAPI, HTTPException, Request, Response
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

# creating the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

"""The middleware will create a new SQLAlchemy `SessionLocal` for each request, add it to the request and then close it once the request is finished
"""
@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response



"""Using the `SessionLocal` class in the `sql_app/databases.py` file to create a
dependency.

We need to have an independent database session/connection (`SessionLocal`) per request, use the same session through all the request and then close it after the request is finished.

And then a new session will be created for the next request.

For that, we will create a new dependenct with `yield`. Our dependency will
create a new SQLAlchemy `SessionLocal` that will be used in a single request,
and then close it once the request in finished.

And then, when using the dependency in a *path operation function*, we declare it with the type `Session` we imported directly from SQLAlchemy.

This will then give us better editor support inside the *path operation
function*, because the editor will know that the `db` parameter is of type
`Session`
"""

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


"""Standard FastAPI *path operations** code
We are creating the database session before each request in the dependency with `yield`, and then closing it afterwards.

And then we can create the required dependency in the *path operation function*, to get that session directly.

With that, we can just call `crud.get_user` directly from inside of the *path operation function* and use that session.
"""
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


"""Using SQLAlchemy code inside of the *path operation function* and in the dependency, and, in turn, it will go and communicate with an external database.

That could potentially require some "waiting".

But as SQLAlchemy doesn't have compatibility for using `await` directly, as would be something like:
`user = await db.query(User).first()`
...and instead we are using:
`user = db.query(User).first()`

Then we should declare the *path operation functions* and the dependency without `async def`, just with normal `def`.
"""
@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items", response_model=List[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items

"""
"""
