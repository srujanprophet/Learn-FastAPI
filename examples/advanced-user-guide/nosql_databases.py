# importing couchbase components
from typing import Optional

from couchbase import LOCKMODE_WAIT
from couchbase.bucket import Bucket
from couchbase.cluster import Cluster, PasswordAuthenticator
from fastapi import FastAPI
from pydantic import BaseModel

USERPROFILE_DOC_TYPE = "userprofile"


def get_bucket():
    """
    In **Couchbase**, a bucket is a set of documents, that can be of different types.

    They are generally all related to the same application

    The analogy in the relational database world would be a "database" (a specific database, not the database server).

    The analogy in **MongoDB** would be a "collection".

    In the code, a `Bucket` represents the main entrypoint of communcation with the database.

    This utility function will:
        - Connect to a **Couchbase** cluster (that might be a single machine)
            - Set defaults for timeouts.
        - Authenticate in the cluster.
        - Get a `Bucket` instance.
            - Set defaults for timeouts.
        - Return it.
    """
    cluster = Cluster(
        "couchbase://couchbasehost:8091?fetch_mutation_tokens=1&operation_timeout=30&n1ql_timeout=300"
    )
    authenticator = PasswordAuthenticator("username", "password")
    cluster.authenticate(authenticator)
    bucket: Bucket = cluster.open_bucket("bucket_name", lockmode=LOCKMODE_WAIT)
    bucket.timeout = 30
    bucket.n1ql_timeout = 300
    return bucket


class User(BaseModel):
    """
    As **CouchBase** documents are actually just JSON objects, we can model them with Pydantic.
    We will use this model in our *path operation function*, so, we don't include in the `hashed_password`
    """
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    """
    This will have the data that is actually stored in the database.
    We don't create it as a subclass of Pydantic's `BaseModel` but as a subclass of our own `User`, because it will have all the attributes in `User` plus a couple more
    """
    type: str = USERPROFILE_DOC_TYPE
    hashed_password: str


def get_user(bucket: Bucket, username: str):
    """
    Creating a function that will:
    - Take a username
    - Generate a document ID from it.
    - Get the document with that ID.
    - Put the contents of the document in a `UserInDB` model.

    By creating a function that is only dedicated to getting our user from a `username` (or any other parameter) independent of our *path operation function*, we can more easily re-use it in multiple parts and also add unit tests for it.
    """
    doc_id = f"userprofile::{username}"
    result = bucket.get(doc_id, quiet=True)
    if not result.value:
        return None
    user = UserInDB(**result.value)
    return user


# FastAPI specific code
app = FastAPI()


@app.get("/users/{username}", response_model=User)
def read_user(username: str):
    """As our code is calling Couchbase and we are not using the experimental Python `await` support, we should declare our function with normal `def` instead of `async def`.

    Also, Couchbase recommends not using a single `Bucket` object in multiple "threads", so, we can just get the bucket directly and pass it to our utility functions
    """
    bucket = get_bucket()
    user = get_user(bucket=bucket, username=username)
    return user

