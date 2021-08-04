"""
Hiding our documentation user interfaces in production *shouldn't* be the way to protect our API.

That doesn't add any extra security to our API, the *path operations* will still be available where they are.

If there's a security flaw in our code, it will still exist.

Hiding the documentation just makes it more difficult to understand how to interact with our API, and could make it more difficult for us to debug it in production. It could be comsidered simply a from of Securoty through obscurity.

If we want to secure our API, there are several better things we can do, for example:
    - Make sure we have well defined Pydantic models for our request bodies and respnonses.
    - Configure any required permissions and roles using dependencies.
    - Never store plaintext passwords, only password hashes.
    - Implement and use well-known cryptographic tools, like Passlib and JWT tokens, etc.
    - Add more granular permission controls with OAuth2 scopes where needed.
    - ...etc.

Nevertheless, we might have a very specific use case where we really need to disable the API docs for some environment (e.g. for production) or depending on configurations from environment variables.

We can easily use the same Pydantic settings to configure our generated OpenAPI and the docs UI.
"""
from fastapi import FastAPI
from pydantic import BaseSettings


class Settings(BaseSettings):
    """Declaring the setting `openapi_url` with the same default of `"/openapi.json"`.
    """
    openapi_url: str = "/openapi.json"


settings = Settings()

# using the setting when creating the `FastAPI` app. Then we can disable OpenAPI
# (including the UI docs) by setting the environment variable `OPENAPI_URL` to the empty string.
app = FastAPI(openapi_url=settings.openapi_url)


@app.get("/")
def root():
    return {'message': 'Hello World'}
