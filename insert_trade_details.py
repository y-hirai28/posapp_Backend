import asyncio
import sys
from sqlalchemy import text
from database import engine

# Windows環境でのaiomysql対応
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

async def insert_trade_details():
    async with engine.begin() as conn:
        # 最新のtrd_idを取得
        result = await conn.execute(text("SELECT MAX(trd_id) FROM trade"))
        trd_id = result.scalar()

        if not trd_id:
            print("trade テーブルにデータがありません")
            return

        print(f"trd_id = {trd_id} にtrade_detailを追加します...")

        # 既存のdetailを確認
        result = await conn.execute(text(f"SELECT COUNT(*) FROM trade_detail WHERE trd_id = {trd_id}"))
        existing_count = result.scalar()

        if existing_count > 0:
            print(f"既に {existing_count} 件のdetailが存在します。スキップします。")
            return

        # baseを計算
        result = await conn.execute(text(f"SELECT COALESCE(MAX(dtl_id), 0) FROM trade_detail WHERE trd_id = {trd_id}"))
        base = result.scalar()

        # 3つの商品を追加
        products = [
            ('0000000000004', base + 1),
            ('0000000000001', base + 2),
            ('0000000000003', base + 3),
        ]

        for code, dtl_id in products:
            await conn.execute(text(f"""
                INSERT INTO trade_detail (trd_id, dtl_id, prd_id, prd_code, prd_name, prd_price)
                SELECT {trd_id}, {dtl_id}, pm.prd_id, pm.code, pm.name, pm.price
                FROM product_master pm
                WHERE pm.code = '{code}'
            """))
            print(f"  追加: {code} (dtl_id={dtl_id})")

        # total_amtを更新
        await conn.execute(text(f"""
            UPDATE trade t
            SET t.total_amt = (
                SELECT COALESCE(SUM(td.prd_price), 0)
                FROM trade_detail td
                WHERE td.trd_id = {trd_id}
            )
            WHERE t.trd_id = {trd_id}
        """))

        # 結果を確認
        result = await conn.execute(text(f"SELECT COUNT(*) FROM trade_detail WHERE trd_id = {trd_id}"))
        detail_count = result.scalar()

        result = await conn.execute(text(f"SELECT total_amt FROM trade WHERE trd_id = {trd_id}"))
        total_amt = result.scalar()

        print(f"\n完了: {detail_count}件のdetailを追加しました")
        print(f"合計金額: {total_amt}円")

if __name__ == "__main__":
    asyncio.run(insert_trade_details())
