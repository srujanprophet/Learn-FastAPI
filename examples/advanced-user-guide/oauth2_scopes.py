"""
Now we are declaring the OAuth2 security scheme with two available scopes, `me` and `items`.

Then, we modify the token *path operation* to return the scopes requested.

Then, we declare that the *path operation* for `/users/me/items/` required the scope `items`.

Then, updating the dependency `get_current_user`
"""
from datetime import datetime, timedelta
from typing import List, Optional

# importing and using Security from `fastapi`
from fastapi import Depends, FastAPI, HTTPException, Security, status
# can use `Security` to declare dependencies (like `Depends`), but `Security` also receives a parameter `scopes` with a list of scopes (strings).
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    # this is the one used by the dependecies
    SecurityScopes,
)
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, ValidationError

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Chains",
        "email": "alicechains@example.com",
        "hashed_password": "$2b$12$gSvqqUPvlXP2tfVFaWK1Be7DlH.PKZbv5H8KnzzVgXXbVxpva.pFm",
        "disabled": True,
    }
}


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
    scopes: List[str] = []


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# declaring the OAuth2 security scheme with two available scopes, `me` and `items`
# The `scopes` parameter receives a `dict` with each scope as a key and the description as the value
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={"me": "Read information about the current user.", "items": "Read items."},
)

app = FastAPI()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# using the same OAuth2 scheme we created before, declaring it as a dependency : `outh2_scheme`.
async def get_current_user(
    security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)
):
    """
    Because this dependency function doesn't have any scope requirements itself, we can use `Depends` with `oauth2_scheme`, we don't have to use `Security` when we don't need to specify security scopes.

    We also declare a special parameter of type `SecurityScopes`, imported from `fastapi.security`. 

    This parameter will be of type `SecurityScopes`.
    It will have a property `scopes` with a list containing all the scopes required by itself and all the dependencies that use this as a sub-dependency. That means, all the "dependants".

    The `security_scopes` object (of class `SecurityScopes`) also provides a `scope_str` attribute with a single string, containing those scopes separated by spaces. The `SecurityScopes` class is similar to `Request` (`Request` was used to get the request object directly).

    We create an `HTTPException` that we can re-use (`raise`) later at several points.

    In this exception, we include the scopes required (if any) as a string separated by spaces (using `scope_str`). We put that string separated by space (using `scope_str`). We put that string containing the scopes in the `WWW-Authenticate` header (this is part of the spec).
    """
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = f"Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    """
    We then verify that we get a `username`, and extract the scopes. And then we validate that data with the Pydantic model (catching the `ValidationError` exception), and if we get an error reading the JWT token or validating the data with Pydantic, we raise the `HTTPException` we created before.

    For that, we update the Pydantic model `TokenData` with a new property `scopes`.

    By validating the data with Pydantic we can make sure that we have, for example, exactly a `list` of `str` with the scopes and a `str` with the `username`.

    Instead of, for example, a `dict`, or something else, as it could break the application at some point later, making it a security risk.

    We cal also verify that we have a user with that username, and if not, we raise that same exception we created before.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=username)
    except (JWTError, ValidationError):
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    """
    We now verify that all the scopes required, by this dependency and all the dependants (including *path operations*), are included in the sdopes provided in the token received, otherwise raise an `HTTPException`.

    For this, we use `security_scopes.scopes`, that contains a `list` with all these scopes as `str`.
    """
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user


async def get_current_active_user(
    current_user: User = Security(get_current_user, scopes=["me"])
):
    """
    Passing a list of scopes, in this case with just one scope: `items` (it could have more). And the dependency function `get_current_active_user` can also declare sub-dependencies, not only with `Depends` but also with `Security`. Declaring its own sub-dependency function (`get_current_user`), and more scope requirements.

    In this case, it requires the scope `me` (it could required more than one scope).
    """
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Modifying the token *path operation* to return the scopes requested.

    We are still using the same `OAuth2PasswordRequestForm`. It includes a property `scopes` with a `list` of `str`, with each scope it received in the request.

    And we return the scopes as part of the JWT Token.
    """
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "scopes": form_data.scopes},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.get("/users/me/items")
async def read_own_items(
    current_user: User = Security(get_current_active_user, scopes=["items"])
):
    """
    In this case, we pas a dependency function `get_current_active_user` to `Security` (the same way we could do with `Depends`).
    """
    return [{"item_id": "Foo", "owner": current_user.username}]


@app.get("/status")
async def read_system_status(current_user: User = Depends(get_current_user)):
    return {"status": "ok"}


"""
`Security` is actually a subclass of `Depends`, and it has just one extra parameter. But by using `Security` instead of `Depends`, **FastAPI** will know that it can declare security scopes, use them internally, and document the API with OpenAPI.
But when we import `Query`, `Path`, `Depends`, `Security` and others from `fastapi`, those are actually functions that return special classes.
"""

"""DEPENDENCY TREE AND SCOPES
As the `get_current_active_user` dependency has as a sub-dependency on `get_current_user`, the scope `"me"` declared at `get_current_active_user` will be included in the list of required scopes in the `security_scopes.scopes` passed to `get_current_user`.

The `path operation` itself also declares a scope, `"items"`, so this will also be in the list of `security_scopes.scopes` passed to `get_current_user`.

Here's how the hierarchy of dependencies and scopes looks like:
- The *path operation* `read_own_items` has:
    - Required scopes `["items"]` with the dependency:
    - `get_current_active_user`:
        - The dependency function `get_current_active_user` has:
            - Required scopes `["me"]` with the dependency:
            - `get_current_user`:
                - The dependency function `get_current_user` has:
                    - No scopes by itself
                    - A dependency using `oauth2_scheme`.
                    - A `security_scopes` parameter has a property `scopes` with a `list` containing all these scopes declared above, so:
                        - `security_scopes.scopes` will contain `["me", "items"] for the *path operation* `read_own_items`.
                        - `security_scopes.scopes` will contain `["me"] for the *path operation* `read_users_me*, because it is declared in the dependency `get_current_active_user.`
                        - `security_scopes.scopes` will contain `[]` (nothing) for the *path operation* `read_users_me`, because it is declared in the dependency `get_current_active_user`.
                        - `security_scopes.scopes` will contain `[]` (nothing) for the *path operation* `read_system_status`, because it didn't declare any `Security` with `scopes`, and its dependency, `get_current_user`, doesn't declare any `scope` either.

The important "magic" thing here is that `get_current_user` will have a different list of `scopes` to check for each *path operation*.

All depending on the `scopes` declared in each *path operation* and each dependency in the dependency tree for that specific *path operation*.
"""

"""MORE DETAILS ABOUT `SecurityScopes`
We can use `SecurityScopes` at any point, and in multiple places, it doesn't have to be at the "root" dependency.

It will always have the security scopes declared in the current `Security` dependencies and all the dependants for **that specific** *path operation* and **that specific** dependency tree.

Because the `SecurityScopes` will have all the scopes declared by dependants, we can use it to verify that a token has the required scopes in a central dependency function, and then declare different scope requirements in different *path operations*.

They will be checked independently for each *path operation*.
"""

"""ABOUT THIRD PARTY INTEGRATIONS
In this example, we are using the OAuth2 "password" flow.

This is appropriate when we are logging in to our own application, probably with our own frontend.

Because we can trust it to receive the `username` and `password`, as we control it.

But if we are building an OAuth2 application that others would connect to (i.e., if we are building an authentication provider equivalent to Facebook, Google, GitHub, etc.) we should use one of the other flows. 

The most common is the implicit flow.

The most secure is the code flow, but is more complex to implement as it requires more steps. As it is more complex, many providers end up suggesting the implicit flow.

It's common that each authentication provider names their flows in a different way, to make it part of their brand. But in the end, they are implementing the same OAuth2 standard.
"""