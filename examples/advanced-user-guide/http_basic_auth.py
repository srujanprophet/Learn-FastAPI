"""
For the simplest cases, we can use HTTP Basic Auth.

In HTTP Basic Auth, the application expects a header that contains a username and a password.

If it doesn't receive it, it returns an HTTP 401 "Unauthorized" error.

And returns a header `WWW-Authenticate` with a value of `Basic`, and am optional `realm` parameter.

That tells the browser to show the integrated prompt for a username and password.

Then, when we type that username and password, the browser sends them in the header automatically.
"""
from fastapi import Depends, FastAPI, HTTPException, status
# importing `HTTPBasic` and `HTTPBasicCredentials`.
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()

# creating a "`security scheme" using `HTTPBasic`.
security = HTTPBasic()


# using that `security` with a dependency in our *path operation*
@app.get("/users/me")
def read_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    """
    Returns an object of type `HTTPBasicCredentials`.
    It contains the `username` and `password` sent.
    """
    return {"username": credentials.username, "password": credentials.password}


"""CHECK THE USERNAME
Using a dependency to check if the username and password are correct.

For this, using the Python standard module `secrets` to check the username and password
"""
import secrets


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    """
    This will ensure that `credentials.username` is `"stanleyjobson"`, and that `credentials.password` is `"swordfish"`. This would be similar to:
    ```
    if not (credentials.username == "stanleyjobson") or not (credentials.password == "swordfish"):
        # returrn some erro
        ...
    ```
    But by using the `secrets.compare_digest()` it will be secure against a type of attacks called "timing attacks".

    After detecting that the credentials are incorrect, return an `HTTPException` with a status code 401 (the same returned when no credentials are provided) and add the header `WWW-Authenticate` to make the browser show the login prompt again.
    """
    correct_username = secrets.compare_digest(credentials.username, "stanleyjobson")
    correct_password = secrets.compare_digest(credentials.password, "swordfish")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@app.get("/users_a/me")
def read_current_user(username: str = Depends(get_current_username)):
    return {"username": username}


"""TIMING ATTACKS
Let's imagine some attackers are trying to guess the username and password.

And they send a request with a username `johndoe` and a password `love123`.

Then the Python code in our application would be equivalent to something like:
```
if "johndoe" == "stanleyjobson" and "love123" == "swordfish":
    ...
```
But right at the moment Python compares the first `j` in `johndoe` to the first `s` in `stanleyjobson`, it will return `False`, because it already knows that those two strings are not the same, thinking that "there's no need to waste more computation comparing the rest of the letters". And our application will say "incorrect user or password".

But then the attackers try with username `stanleyjobsox` and password `love123`.
And our application code does something like:
```
if "stanleyjobsox" == "stanleyjobson" and "love123" == "swordfish":
    ...
```
Python will have to compare the whole `stanleyjobso` in bnoth `stanleyjobsox` and `stanleyjobson` before realizing that both strings are not the same. So it will take some extra microseconds to reply back "incorrect user or password".

**THE TIME TO ANSWER HELPS TH ATTACKERS**
At that point, by noticing that the server took some microseconds longer to send the "incorrect user or password" response, the attackers will know that they got *something* right, some of the initial letters were right.

And they can try again knowing that it's probably something more similar to `stanleyjobsox` than to `johndoe`.

**A "PROFESSIONAL" ATTACK**
Of course, the attackers would not try all this by hand, they would write a program to do it, possibly with thousands or millions of tests per second. And would get just one extra correct letter at a time.

But doing that, in some minutes or hours the attackers would have guessed the correct username and password, with the "help" of our application, just using the time taken to answer.

**FIX IT WITH `secrets.compare_digest()`
In our code, we are actually using `secrets.compare_digest()`.

In short, it will take the same time to compare `stanleyjobsox` to `stanleyjobson` than it takes to compare `johndoe` to `stanleyjobson`. And the same for the password.

That way, using `secrets.compare_digest()` in our application code, it will be sage against the whole range of security attacks.
"""