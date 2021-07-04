"""
Because **FastAPI** doesn't do any changes to a `Response` we return, we have to make sure it's contents are ready for it.

For example, we cannot put a Pydantic model in a `JSONResponse` without first converting it to a `dict` with all the data types (like `datetime`, `UUID`, etc) converted to JSON-compatible types.

For those use cases, we can use the `jsonable_encoder` to convert our data before passing it to a response
"""
from datetime import datetime
from typing import Optional

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class Item(BaseModel):
    title: str
    timestamp: datetime
    description: Optional[str] = None

app = FastAPI()


@app.put("/items/{id}")
def update_item(idL: str, item: Item):
    json_compatible_item_data = jsonable_encoder(item)
    return JSONResponse(content=json_compatible_item_data)


"""
The example above shows all the parts we need but it's not useful yet, as we could have just returned the `item` directly, and **FastAPI** would put it in a `JSONResponse` for us, converting it to a `dict`, etc. All that by default.

For example, if we want to return a custom response. We want to return an XML response.

We could put our XML content in a string, put it in a `Response`, and return it.
"""
from fastapi import Response

@app.get("/legacy")
def get_legacy_data():
    data = """<?xml version="1.0"?>
    <shampoo>
    <Header>
        Apply shampoo here.
    </Header>
    <Body>
    </shampoo>
    """
    return Response(content=data, media_type="application/xml")
