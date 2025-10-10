from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List
from datetime import datetime
from database import get_db, Trade, TradeDetail, ProductMaster
from schemas.purchase import Purchase, PurchaseCreate, PurchaseItem

router = APIRouter()

@router.post("/", response_model=Purchase)
async def create_purchase(purchase: PurchaseCreate, db: AsyncSession = Depends(get_db)):
    total_amount = sum(item.subtotal for item in purchase.items)

    db_trade = Trade(
        datetime=datetime.now(),
        emp_cd=purchase.emp_cd if hasattr(purchase, 'emp_cd') else '9999999999',
        store_cd=purchase.store_cd if hasattr(purchase, 'store_cd') else '30',
        pos_no=purchase.pos_no if hasattr(purchase, 'pos_no') else '90',
        total_amt=int(total_amount)
    )
    db.add(db_trade)
    await db.flush()

    for idx, item in enumerate(purchase.items, start=1):
        # Get product info from ProductMaster
        product_result = await db.execute(select(ProductMaster).where(ProductMaster.prd_id == item.product_id))
        product = product_result.scalar_one_or_none()

        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")

        db_detail = TradeDetail(
            trd_id=db_trade.trd_id,
            dtl_id=idx,
            prd_id=product.prd_id,
            prd_code=product.code,
            prd_name=product.name,
            prd_price=product.price
        )
        db.add(db_detail)

    await db.commit()
    await db.refresh(db_trade)

    result = await db.execute(
        select(Trade)
        .options(selectinload(Trade.details).selectinload(TradeDetail.product))
        .where(Trade.trd_id == db_trade.trd_id)
    )
    trade_with_details = result.scalar_one()

    return trade_with_details

@router.get("/", response_model=List[Purchase])
async def get_purchases(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Trade)
        .options(selectinload(Trade.details).selectinload(TradeDetail.product))
    )
    trades = result.scalars().all()
    return trades

@router.get("/{purchase_id}", response_model=Purchase)
async def get_purchase(purchase_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Trade)
        .options(selectinload(Trade.details).selectinload(TradeDetail.product))
        .where(Trade.trd_id == purchase_id)
    )
    trade = result.scalar_one_or_none()
    if not trade:
        raise HTTPException(status_code=404, detail="Purchase not found")
    return trade