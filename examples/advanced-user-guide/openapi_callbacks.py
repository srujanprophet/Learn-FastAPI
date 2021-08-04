"""
We can create an API with a *path operation* that could trigger a request to an *external API* created by someone else (probably the same developer that would be *using* our API).

The process that happens when our API calls the *external API* is named a "callback". Because the software that the external developer wrote sends a request to our API and then our API *calls* back, sending a request to an *external API* (that was probably created by the same developer).

In this case, we could want to document how that external API *should* look like. What *path operation* it should have, what body it should expect, what response it should return, etc.

This code won't be executed in our app, we only need it to *document* how that *external API* should look like.

But, we already know how to easily create automatic documentation for an API with **FastAPI**.

So we are going to use that same knowledge to document how the *external API* should look like... by creating the *path operation(s) that the external API should implement (the ones our API will call).
"""
from typing import Optional

from fastapi import APIRouter, FastAPI
from pydantic import BaseModel, HttpUrl

app = FastAPI()


class Invoice(BaseModel):
    id: str
    title: Optional[str] = None
    customer: str
    total: float


class InvoiceEvent(BaseModel):
    description: str
    paid: bool


class InvoiceEventReceived(BaseModel):
    ok: bool


# creating a new `APIRouter` that will contain one or more callbacks
invoices_callback_router = APIRouter()


@invoices_callback_router.post(
    "{$callback_url}/invoices/{$request.body.id}", response_model=InvoiceEventReceived)
def invoice_notification(body: InvoiceEvent):
    """To create the callback *path operation* use the same `APIRouter` we created above.
    It should look just like a normal FastAPI *path operation*:
        - It should probably have a declaration of the body it should receive, e.g. `body: InvoiceEvent`.
        - And it could also have a declaration of the response it should return, e.g. `response_model=InvoiceEventReceived.`

    There are 2 main differences from a normal *path operation*:
        - It doesn't need to have any actual code, because our app will never call this code. It's only used to document the *external API*. So, the function could just have a `pass`.
        - The *path* can contain an OpenAPI 3 expression where it can use variables with parameters and parts of the original request sent to *our API*.
    """
    pass


@app.post("/invoices/", callbacks=invoices_callback_router.routes)
def create_invoce(invoice: Invoice, callback_url: Optional[HttpUrl] = None):
    """
    Create an invoice.

    This will (let's imagine) let the API user (some external developer) create an invoice.

    And this path operation will:

    * Send the invoice to the client
    * Collect the money from the client.
    * Send a notification back to the API user (the external developer), as a callback.
        * At this point is that the API will somehow send a POST request to the external API with the notification of the invoice event (e.g. "payment successful").

    At this point, we have the *callback path operation(s)* needed (the one(s) that the *external developer* should implement in the external API) in the callback router we created above.

    Now using the parameter `callbacks` in *our API's path operation decorator* to pass the attribute `.routes` (that's actually just a `list` of routes/*path operations*) from that callback router
    """
    # Send the invoice, collect the money, send the notification (the callback)
    return {"msg": "Invoice received"}

"""THE CALLBACK PATH EXPRESSION
The callback *path* can have an OpenAPI 3 expression that can contain parts of the original request sent to *our API*.

In this case, it's the `str`:
`"{$callback_url}/invoices/{$request.body.id}"
So, if our API user (the external developer) sends a request to *our API* to:
`https://yourapi.com/invoices/?callback_url=https://www.external.org/events`
with a JSON body of:
```json
{
    "id": "2expen51ve",
    "customer": "Mr. Richie Rich",
    "total": "9999"
}
```
Then *our API* will process the invoice, and at some point later, send a callback request to the `callback_url` (the *external API*):
`https://www.external.org/events/invoices/2expen51ive`
with a JSON body containing something like:
```json
{
    "description": "Payment celebration",
    "paid": true
}
``` 
and it would expect a response from that *external API* with a JSON body like:
```json
{
    "ok": true
}
```
"""