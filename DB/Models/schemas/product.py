from pydantic import BaseModel
from typing import Optional

class ProductCreate(BaseModel):
    categorial: str
    product: str
    composition: str
    popularity: int
    in_stock: bool


class ProductUpdate(BaseModel):
    categorial: Optional[str] = None
    product: Optional[str] = None
    composition: Optional[str] = None
    popularity: Optional[int] = None
    in_stock: Optional[bool] = None