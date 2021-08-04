import pytest
from httpx import AsyncClient

from async_tests_main import app

# the marker `@pytest.mark.asyncio` tells pytest that this function should be
# called asynchronously
@pytest.mark.asyncio
async def test_root():
    # creating an `AsyncClient` with the app, and sending async requests to it,
    # using `await`. This is the equivalent to `response = client.get('/') that
    # we used to make our request with the `TestClient`
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Tomato"}
