from fastapi import FastAPI

from ApiRouters import router

from fastapi.staticfiles import StaticFiles

from DB.InitModels.InitModels import lifespan



app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(router)
