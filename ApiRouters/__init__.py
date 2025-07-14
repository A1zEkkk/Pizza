from fastapi import APIRouter

from ApiRouters.post.admin.auth import router as post_auth_router
from ApiRouters.get.admin.auth import router as get_auth_router

router = APIRouter()

for r in [post_auth_router, get_auth_router]:
    router.include_router(r)