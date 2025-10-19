import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from database import async_session, ProductMaster
from sqlalchemy import select

async def test_product_search():
    async with async_session() as session:
        # Test searching by 13-digit code
        test_codes = [
            '4512345000011',  # Ballpoint pen
            '4512345000042',  # A4 paper
            '4987654000012',  # Glue stick
        ]

        print("Testing product search by 13-digit code:")
        print("=" * 60)

        for code in test_codes:
            result = await session.execute(
                select(ProductMaster).where(ProductMaster.code == code)
            )
            product = result.scalar_one_or_none()

            if product:
                print(f"SUCCESS: Code {code}")
                print(f"  Name: {product.name}")
                print(f"  Price: {product.price}")
            else:
                print(f"FAILED: Code {code} not found")
            print()

        # List all products
        print("\nAll products in database:")
        print("=" * 60)
        result = await session.execute(select(ProductMaster))
        products = result.scalars().all()

        print(f"Total products: {len(products)}\n")
        for product in products:
            print(f"{product.code} | {product.name} | {product.price}")

if __name__ == "__main__":
    asyncio.run(test_product_search())
