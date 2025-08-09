from pydantic import BaseModel
from typing import Optional


class UserData(BaseModel):
    login: str
    password: str
    role: Optional[str] = None
