from fastapi import APIRouter, Cookie, Depends, HTTPException
from DB.Models.repository.repository import AuthDBService
from DB.Models.services.token_manager import TokenManager

router = APIRouter()
token_manager = TokenManager()

@router.post("/refresh")
async def refresh_access_token(refresh_token: str = Cookie()):
    refresh_token_is_alive = token_manager.refresh_is_alive(refresh_token)
    if refresh_token_is_alive:
        kill_token = await token_manager.revoke_tokens(refresh_token)
        new_access_token = await token_manager.