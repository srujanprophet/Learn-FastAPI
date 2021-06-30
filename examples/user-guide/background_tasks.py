"""Using `BackgroundTasks`
First, import `BackgroundTasks` and define a parameter in our *path operation function* with a type declaration of `BackgroundTasks`

Using `BackgroundTasks` also works with the dependency injection system, we can declare a parameter of type `BackgroundTasks` at multiple levels: in a *path operation function*, in a dependency (dependable), in a sub-dependency, etc.
"""
from typing import Optional

from fastapi import BackgroundTasks, Depends, FastAPI

app = FastAPI()

# dependency injection
def write_log(message: str):
    with open("log.txt", mode="a") as log:
        log.write(message)


def get_query(background_tasks: BackgroundTasks, q: Optional[str] = None):
    if q:
        message = f"found query: {q}\n"
        background_tasks.add_task(write_log, message)
    return q


# creating a task function
def write_notification(email: str, message=""):
    """Creating a function to be run as the background task.

    It is just a standard function that can receive parameters.

    It can be an `async def` or normal `def` function.

    In this case, the task function will write to a file (simulating sending an email).

    And as the write operation doesn't use `async` and `await`, we define the function with normal `def`
    """
    with open("log.txt", mode="w") as email_file:
        content = f"notification for {email}: {message}"
        email_file.write(content)


# adding the background task
@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    """Inside the *path operation function*, passing our task function to the *background tasks* object with the method `.add_task()`

    `.add_task()` receives as arguments:
        - A task function to be run in the background (`write_notification`)
        - Any sequence of arguments that should be passed to the task function in order (`email`)
        - Any keyword arguments that should be passed to the task function (`message="some notification`").
    """
    background_tasks.add_task(write_notification, email, message="some notification")
    return {"message": "Notification sent in the background"}


@app.post("/send-notification-a/{email}")
async def send_notification_a(
    email: str, background_tasks: BackgroundTasks, q: str = Depends(get_query)
):
    """In this, the messages will be written to the `log.txt` file *after* the response is sent.

    If there was a query in the request, it will be written to the log in a background task.

    And then another background task generated at the *path operation function* will write a message using the `email` path parameter.
    """
    message = f"message to {email}\n"
    background_tasks.add_task(write_log, message)
    return {"message": "Message sent"}
