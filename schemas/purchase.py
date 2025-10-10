from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from .product import Product

class TradeDetailBase(BaseModel):
    prd_id: int
    prd_code: str
    prd_name: str
    prd_price: int

class TradeDetailCreate(BaseModel):
    product_id: int
    quantity: int
    unit_price: int
    subtotal: int

class TradeDetail(TradeDetailBase):
    trd_id: int
    dtl_id: int
    product: Optional[Product] = None

    class Config:
        from_attributes = True

class TradeBase(BaseModel):
    emp_cd: str
    store_cd: str
    pos_no: str
    total_amt: int

class PurchaseCreate(BaseModel):
    items: List[TradeDetailCreate]
    emp_cd: Optional[str] = '9999999999'
    store_cd: Optional[str] = '30'
    pos_no: Optional[str] = '90'

class Purchase(BaseModel):
    trd_id: int
    datetime: datetime
    emp_cd: str
    store_cd: str
    pos_no: str
    total_amt: int
    details: List[TradeDetail] = []

    class Config:
        from_attributes = True

# Alias for compatibility
PurchaseItem = TradeDetail
PurchaseItemCreate = TradeDetailCreate