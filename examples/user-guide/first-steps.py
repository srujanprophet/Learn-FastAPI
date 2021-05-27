""" Basic starter fastapi code"""
from fastapi import FastAPI


app = FastAPI()


@app.get("/")
async def root():
    """ Return hello world at / endpoint """
    return {"message": "Hello World"}
