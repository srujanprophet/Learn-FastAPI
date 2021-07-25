"""Import and set up `SQLAlchemy`
"""
from typing import List

# importing databases
import databases
# importing sqlalchemy
import sqlalchemy
from fastapi import FastAPI
from pydantic import BaseModel

# SQLAlchemy specific code, as with any other app
# creating a `DATABASE_URL`
DATABASE_URL = "sqlite:///./test.db"
# DATABASE_URL = "postgresql://user:password@postgresserver/db"

# creating a `database` object.
database = databases.Database(DATABASE_URL)

# creating a `metadata` object.
metadata = sqlalchemy.MetaData()

# creating a table `notes` using the `metadata` object
notes = sqlalchemy.Table(
    "notes",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("text", sqlalchemy.String),
    sqlalchemy.Column("completed", sqlalchemy.Boolean),
)

# creating an `engine`
engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
# creating all the tables from the `metadata` object
metadata.create_all(engine)

"""creating Pydantic models for:
 - Notes to be created (`NoteIn`)
 - Notes to be returned (`Note`)

By creating these Pydantic models, the input data will be validated, serialized (converted), and annotated (documented).
"""
class NoteIn(BaseModel):
    text: str
    completed: bool


class Note(BaseModel):
    id: int
    text: str
    completed: bool

# creating our `FastAPI` application
app = FastAPI()

# creating event handlers to connect and disconnect from the database
@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


# creating the *path operation function* to read notes
@app.get("/notes/", response_model=List[Note])
async def read_notes():
    """The `response_model=List[Note]` uses `typing.List`
    That documents (and validates, serializes, filters) the output data, as a `list` of `Note`s.
    """
    query = notes.select()
    return await database.fetch_all(query)


# creating the *path operation function* to create notes
@app.post("/notes/", response_model=Note)
async def create_note(note: NoteIn):
    query = notes.insert().values(text=note.text, completed=note.completed)
    last_record_id = await database.execute(query)
    return {**note.dict(), "id": last_record_id}

"""ABOUT {**note.dict(), "id": last_record_id}

`note` is a Pydantic `Note` object.
`note.dict()` returns a `dict` with its data, something like:

```
{
    "text": "Some note",
    "completed": False,
}
but it doesn't have the `id` field.

So we create a new `dict`, that contains the key-value pairs from `note.dict()` with:
`{**note.dict()}
`**note.dict()` "unpacks" the key value pairs directly, so, `{**note.dict()}` would be, more or less, a copy of `note.dict()`.

And then, we extend that copy `dict`, adding another key-value pair: `"id": last_record_id`:
`{**note.dict(), "id": last_record_id}`

So, the final result returned would be something like:
```
{
    "id": 1,
    "text": "Some note",
    "completed": False,
}
```
"""