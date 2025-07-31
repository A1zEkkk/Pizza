from fastapi import APIRouter
from fastapi.responses import JSONResponse, RedirectResponse, Response
from fastapi import Request
from DB.Models.product_model.product_manager import ProductManager
from DB.Models.repository.repository import BaseServiceAuthDB
from DB.Models.services.token_manager import TokenManager
from DB.Models.schemas.product import ProductCreate

rooter = APIRouter()

@rooter.post("/create-product")
async def create_product(response: Response, request: Request, product: ProductCreate):
    token_manager = TokenManager()
    access_token = request.cookies.get("access_token")
    access_token_is_alive = token_manager.access_is_alive(access_token)

    if access_token_is_alive:
        pass
    elif not access_token_is_alive:
        refresh_token = request.cookies.get("refresh_token")
        refresh_token_is_alive = token_manager.refresh_is_alive(refresh_token)