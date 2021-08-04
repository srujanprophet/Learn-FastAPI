"""
First, we create a new database session with the new database.
For the tests we'll use a file `test.db` instead of `sql_app.db`.
But the rest of the session code is more or less the same.

Because now we are going to use a new database in a new file, we need to make sure we create the database with:
`Base.metadata.create_all(bind=engine)`
That is normally called in `main.py`, but the line in `main.py` uses the database file `sql_app.db`, and we need to make sure we create `test.db` for the tests. So, we add that line here, with the new file.
"""
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..database import Base
from ..main import app, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


# creating the dependency override and adding it to the overrides for our app
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_create_user():
    """Testing the app as normal.
    And all the modifications we made in the database during the tests will be in the `test.db` database instead of the main `sql_app.db`
    """
    response = client.post(
        "/users/",
        json={"email": "deadpool@example.com", "password": "chimichangas4life"},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == "deadpool@example.com"
    assert "id" in data
    user_id = data["id"]

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == "deadpool@example.com"
    assert data["id"] == user_id
