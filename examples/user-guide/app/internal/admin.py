"""It contins an `APIRouter` with some admin *path operations* that our organization shares between several projects.

For this example it will be super simple. But let's say that because it is shared with other projects in the organization, we cannot modify it and add a `prefix, `dependencies`, `tags`, etc. directly to the `APIRouter`
"""
from fastapi import APIRouter

router = APIRouter()

@router.post("/")
async def update_admin():
    return {"message": "Admin getting schwifty"}

"""We can declare all the `dependencies`, `tags` and `responses` without having to modify the original `APIRouter` by passing those parameters to `app.include_router()`

That way, the original `APIRouter` will keep unmodified, so we can still share that same `app/internal/admin.py` file with other projects in the organization.
"""