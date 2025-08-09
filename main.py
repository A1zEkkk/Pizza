from fastapi import FastAPI

from fastapi.staticfiles import StaticFiles

from DB.InitModels.InitModels import lifespan



app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")