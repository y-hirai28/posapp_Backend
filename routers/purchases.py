from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload
from typing import List
from datetime import datetime
from database import get_db, Trade, TradeDetail, ProductMaster
from schemas.purchase import Purchase, PurchaseCreate, PurchaseResponse

router = APIRouter()

@router.post("/", response_model=PurchaseResponse)
async def create_purchase(purchase: PurchaseCreate, db: AsyncSession = Depends(get_db)):
    """
    購入API
    1-1: 取引テーブルへ登録
    1-2: 取引明細へ登録
    1-3: 合計や税金額を計算
    1-4: 取引テーブルを更新
    1-5: 合計金額、合計金額（税抜）をフロントへ返す
    """
    try:
        # 1-1: 取引テーブルへ登録
        # レジ担当者コード（空白の場合は'9999999999'）
        emp_cd = purchase.emp_cd if purchase.emp_cd else '9999999999'
        # 店舗コード（'30'固定）
        store_cd = '30'
        # POS機ID（'90'固定、モバイルレジという意味）
        pos_no = '90'

        db_trade = Trade(
            datetime=datetime.now(),  # 取引日時（現在日時システム日付）
            emp_cd=emp_cd,
            store_cd=store_cd,
            pos_no=pos_no,
            total_amt=0,  # 合計金額（初期値0）
            total_amt_ex_tax=0  # 合計金額（税抜）（初期値0）
        )
        db.add(db_trade)
        await db.flush()  # 取引一意キーを取得するためflush

        # 取引一意キーを取得
        trd_id = db_trade.trd_id

        # 1-2: 取引明細へ登録
        for idx, item in enumerate(purchase.items, start=1):
            db_detail = TradeDetail(
                trd_id=trd_id,  # 取引一意キー（1-1の登録後の値）
                dtl_id=idx,  # 取引明細一意キー（採番インクリメンタル 1〜/取引ごと）
                prd_id=item.product_id,  # 商品一意キー（パラメータ）
                prd_code=item.product_code,  # 商品コード（パラメータ）
                prd_name=item.product_name,  # 商品名称（パラメータ）
                prd_price=item.unit_price,  # 商品単価（パラメータ）
                tax_cd='10'  # 消費税区分（'10'固定）
            )
            db.add(db_detail)

        await db.flush()

        # 1-3: 合計や税金額を計算
        # 合計金額（税抜）= 商品単価の合計
        v_total_amt_ex_tax = sum(item.unit_price for item in purchase.items)
        # 合計金額（税込）= 合計金額（税抜） × 1.1
        v_total_amt = int(v_total_amt_ex_tax * 1.1)

        # 1-4: 取引テーブルを更新
        await db.execute(
            update(Trade)
            .where(Trade.trd_id == trd_id)
            .values(
                total_amt=v_total_amt,  # 合計金額
                total_amt_ex_tax=v_total_amt_ex_tax  # 合計金額（税抜）
            )
        )

        await db.commit()

        # 1-5: 合計金額、合計金額（税抜）をフロントへ返す
        return PurchaseResponse(
            success=True,  # 成否
            trd_id=trd_id,  # 取引一意キー
            total_amt=v_total_amt,  # 合計金額（税込）
            total_amt_ex_tax=v_total_amt_ex_tax  # 合計金額（税抜）
        )

    except Exception as e:
        await db.rollback()
        # エラー時はFalseを返す
        return PurchaseResponse(
            success=False,
            trd_id=0,
            total_amt=0,
            total_amt_ex_tax=0
        )

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