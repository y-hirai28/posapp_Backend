import asyncio
import sys
from sqlalchemy import text
from database import engine

# Windows環境でのaiomysql対応
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

async def check_database():
    try:
        async with engine.connect() as conn:
            print("[OK] データベース接続成功\n")

            # テーブル一覧を取得
            result = await conn.execute(text("SHOW TABLES"))
            tables = result.fetchall()
            print(f"テーブル一覧 ({len(tables)}件):")
            for table in tables:
                print(f"  - {table[0]}")
            print()

            # product_masterの確認
            try:
                result = await conn.execute(text("SELECT COUNT(*) FROM product_master"))
                count = result.scalar()
                print(f"product_master: {count}件のデータ")

                result = await conn.execute(text("SELECT * FROM product_master LIMIT 5"))
                rows = result.fetchall()
                for row in rows:
                    print(f"  {row}")
                print()
            except Exception as e:
                print(f"[WARNING] product_masterテーブルが存在しないか、エラー: {e}\n")

            # tradeの確認
            try:
                result = await conn.execute(text("SELECT COUNT(*) FROM trade"))
                count = result.scalar()
                print(f"trade: {count}件のデータ")

                result = await conn.execute(text("SELECT * FROM trade LIMIT 5"))
                rows = result.fetchall()
                for row in rows:
                    print(f"  {row}")
                print()
            except Exception as e:
                print(f"[WARNING] tradeテーブルが存在しないか、エラー: {e}\n")

            # trade_detailの確認
            try:
                result = await conn.execute(text("SELECT COUNT(*) FROM trade_detail"))
                count = result.scalar()
                print(f"trade_detail: {count}件のデータ")

                result = await conn.execute(text("SELECT * FROM trade_detail LIMIT 5"))
                rows = result.fetchall()
                for row in rows:
                    print(f"  {row}")
                print()
            except Exception as e:
                print(f"[WARNING] trade_detailテーブルが存在しないか、エラー: {e}\n")

    except Exception as e:
        print(f"[ERROR] データベース接続エラー: {e}")

if __name__ == "__main__":
    asyncio.run(check_database())
