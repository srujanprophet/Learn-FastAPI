from typing import List, Optional

from fastapi import FastAPI, Header

app = FastAPI()


# Import Header, Declare header parameters
@app.get("/items")
async def read_items(user_agent: Optional[str] = Header(None)):
    return {"User-Agent": user_agent}


# Automatic conversion
@app.get("/items_a")
async def read_items(
    strange_header: Optional[str] = Header(None, convert_underscores=False)
):
    return {"strange_header": strange_header}


# Duplicate headers
@app.get("/items_b")
async def read_items(x_token: Optional[List[str]] = Header(None)):
    return {"X-Token values": x_token}
