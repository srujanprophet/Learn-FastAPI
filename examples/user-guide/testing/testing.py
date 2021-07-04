from fastapi import FastAPI

# importing `TestClient`
from fastapi.testclient import TestClient

app = FastAPI()


@app.get("/")
async def read_main():
    return {"msg": "Hello World"}


# creating a `TestClient`, passing it to our **FastAPI**
client = TestClient(app)

# creating functions with a name that starts with `test_` (standard pytest conventions)
def test_read_main():
    """Using the `TestClient` object the same way as we do with `requests`
    """
    response = client.get("/")
    # writing simple `assert` statements with the standard Python expression that we need to check (again, standard `pytest`)
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}
