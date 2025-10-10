from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    code: str
    name: str
    price: int

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    prd_id: int

    class Config:
        from_attributes = True