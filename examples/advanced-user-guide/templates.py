from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

# importing `Jinja2Templates`
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# creating a `templates` object that we can re-use later
templates = Jinja2Templates(directory="templates")


# declaring a `Request` parameter in the *path operation* that will
# return a template
@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    """Using the `templates` we created to render and return a `TemplateResponse`
    , passing the `request` as one of the key-value pairs in the Jinja2 "context"
    """
    return templates.TemplateResponse("item.html", {"request": request, "id": id})