from fastapi import FastAPI

from contextlib import asynccontextmanager

from DB.InitModels.InitModels import init_models



@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_models()
    yield


app = FastAPI(lifespan=lifespan)
