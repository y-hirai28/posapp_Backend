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
    """購入API用の商品情報（フロントエンドから受け取る）"""
    code: str             # 商品コード
    qty: int = 1          # 数量（デフォルト1）

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
    """購入API リクエスト"""
    items: List[TradeDetailCreate]
    emp_cd: Optional[str] = None  # レジ担当者コード（Noneの場合は'9999999999'）
    store_cd: Optional[str] = None  # 店舗コード（'30'固定）
    pos_no: Optional[str] = None    # POS機ID（'90'固定）

class PurchaseResponse(BaseModel):
    """購入API レスポンス"""
    success: bool                    # 成否（True/False）
    trd_id: int                      # 取引一意キー
    total_amt: int                   # 合計金額（税込）
    total_amt_ex_tax: int            # 合計金額（税抜）

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