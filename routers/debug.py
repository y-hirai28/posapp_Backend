from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from database import get_db

router = APIRouter(prefix="/debug", tags=["debug"])

@router.get("/db-info")
async def get_db_info(db: AsyncSession = Depends(get_db)):
    """データベース接続情報を確認"""
    result = await db.execute(text("SELECT DATABASE() as current_db"))
    db_name = result.scalar()

    # 商品マスタの件数も確認
    count_result = await db.execute(text("SELECT COUNT(*) FROM product_master"))
    product_count = count_result.scalar()

    # サンプル商品コードを取得
    sample_result = await db.execute(text("SELECT code, name FROM product_master LIMIT 3"))
    samples = sample_result.fetchall()

    return {
        "database": db_name,
        "product_count": product_count,
        "sample_products": [{"code": s[0], "name": s[1]} for s in samples]
    }
