from fastapi import FastAPI

from contextlib import asynccontextmanager

from DB.InitModels.InitModels import init_models

from ApiRouters.post.admin.auth import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_models()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(router)