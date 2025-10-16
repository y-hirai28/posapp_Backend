import asyncio
from database import async_session
from sqlalchemy import text

async def check_products():
    async with async_session() as session:
        result = await session.execute(text('SELECT code, name FROM product_master'))
        products = result.fetchall()
        print('\n現在のデータベース内の商品コード:')
        for p in products:
            print(f'{p[0]} - {p[1]}')

if __name__ == "__main__":
    asyncio.run(check_products())
