from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from DB.Models.cfg.settings import templates

router = APIRouter()

@router.get("/auth_admin", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/create_admin", response_class=HTMLResponse)
async def create_admin_page(request: Request):
    return templates.TemplateResponse(
        "admin.html",
        {
            "request": request,
            "title": "Login",
        }
    )