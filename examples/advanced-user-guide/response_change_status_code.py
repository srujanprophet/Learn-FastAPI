"""
We can declare a parameter of type `Response` in our *path operation function*

And then we can set the `status_code` in that *temporal* response object.

And then we can return any object we need, as we normally would (a `dict`, a database model, etc.)

And if we declared a `response_model`, it will still be used to filter and convert the object we returned.

**FastAPI** wil use that *temporal* response to extract the status code (also cookies and headers), and will put them in the final response that contains the value we returned, filtered by any `response_model`.

We can also declare the `Response` parameter in dependencies, and set the status code in the,. But the last one to be set will win.
"""
from fastapi import FastAPI, Response, status

app = FastAPI()

tasks = {"foo": "Listen to the Bar Fighters"}


@app.put("/get-or-create-task/{task_id}", status_code=200)
def get_or_create_task(task_id: str, response: Response):
    if task_id not in tasks:
        tasks[task_id] = "This didn't exist before"
        response.status_code = status.HTTP_201_CREATED
    return tasks[task_id]
