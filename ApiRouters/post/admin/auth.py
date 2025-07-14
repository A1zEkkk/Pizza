import fastapi.openapi.utils
from fastapi import APIRouter, Response, Request,HTTPException, Form
from DB.Models.repository.repository import AuthDBService
from DB.Models.services import TokenManager
from DB.Models.cfg.settings import Settings

router = APIRouter()

#Нужно реализовать работу с request

@router.post("/create_admin")
async def create_user(response: Response, login: str = Form(...), password: str = Form(...)):
    bd_service = AuthDBService()
    tokens = await bd_service.create_user(login=login, password=password, role="admin")

    if tokens is None:
        return {"message": "Пользователь уже существует"}

    access_token = tokens["access_token"]
    refresh_token = tokens["refresh_token"]

    response.set_cookie(
        key="access_token",
        httponly=True,
        value=access_token
    )
    response.set_cookie(
        key="refresh_token",
        httponly=True,
        value=refresh_token
    )

    return {"message": "Куки были добавлены"}

@router.post("/auth_admin")
async def auth_user(response: Response, login: str = Form(...), password: str = Form(...)):
    #Нужно будет доавить фильтр пароля
    bd_service = AuthDBService()
    tokens = await bd_service.authenticate_user(login=login, password=password)

    if tokens is None:
        return {"message": "неверный логин или пароль"} #Имеется ввиду, что пользователя нету в бд

    if tokens is False:
        return {"message": "Неверный логин или пароль"} #Имеетсся ввиду, что неверный данные

    access_token = tokens["access_token"]
    refresh_token = tokens["refresh_token"]

    response.set_cookie(
        key="access_token",
        httponly=True,
        value=access_token
    )
    response.set_cookie(
        key="refresh_token",
        httponly=True,
        value=refresh_token
    )

    return {"message": "Куки были добавлены"}


@router.get("/logout") #Нужно будет создать delete
async def logout(request: Request, response: Response):
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")

    if access_token is None and refresh_token is None:
        raise HTTPException(status_code=401, detail="Необходимо авторизоваться")

    token_manager = TokenManager()

    if access_token and refresh_token:
        tokens = (access_token, refresh_token)
        revoke_tokens = await token_manager.revoke_tokens(tokens)
        if revoke_tokens:
            response.delete_cookie(
                key="access_token",
                httponly=True
            )
            response.delete_cookie(
                key="refresh_token",
                httponly=True
            )

            return {"detail": "Вы вышли из системы"}


        raise HTTPException(status_code=400, detail="Ошибка при удалении токенов")

    response.delete_cookie(
        key="access_token",
        httponly=True
    )
    response.delete_cookie(
        key="refresh_token",
        httponly=True
    )

    return {"message": "was logout" }


