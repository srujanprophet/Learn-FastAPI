
"""
In Python, there's a way to make an instance of a class a "callable".
Not the class itself (which is already a callable), but an instance of that class.
To do that, we declare a method `__call__`
"""
from fastapi import Depends, FastAPI

app = FastAPI()


class FixedContentQueryChecker:
    def __init__(self, fixed_content: str):
        """
        We can use `__init__` to declare the parameters of the instance that we can use to "parameterize" the dependency.
        """
        self.fixed_content = fixed_content

    def __call__(self, q: str = ""):
        """
        This `__call__` is what **FastAPI** will use to check for additional parameters and sub-dependencies, and this is what will be called to pass a value to the parameter in our *path operation function* later.
        """
        if q:
            return self.fixed_content in q
        return False

# creating an instance of this class, that way we are able to "parameterize"
# our dependency, that now has `"bar"` inside of it, as the attribute
# `checker.fixed_content`.
checker = FixedContentQueryChecker("bar")

"""
Then, we could use this `checker` in a `Depends(checker)`, instead of `Depends(FixedContentQueryChecker)`, because the dependency is the instance, `checker`, not the class itself.

And when solving the dependency, **FastAPI** will call this `checker` like
    `checker(q="somequery")`
...and pass whatever that returns as the value of the dependency in our *path operation function* as the parameter `fixed_content_included`
"""
@app.get("/query-checker/")
async def read_query_check(fixed_content_included: bool = Depends(checker)):
    return {"fixed_content_in_query": fixed_content_included}

