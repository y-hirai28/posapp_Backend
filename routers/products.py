from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from database import get_db, ProductMaster
from schemas.product import Product, ProductCreate

router = APIRouter()

@router.post("/", response_model=Product)
async def create_product(product: ProductCreate, db: AsyncSession = Depends(get_db)):
    db_product = ProductMaster(**product.dict())
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product

@router.get("/", response_model=List[Product])
async def get_products(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ProductMaster))
    products = result.scalars().all()
    return products

@router.get("/{product_code}", response_model=Product)
async def get_product_by_code(product_code: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ProductMaster).where(ProductMaster.code == product_code))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{product_id}", response_model=Product)
async def update_product(product_id: int, product: ProductCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ProductMaster).where(ProductMaster.prd_id == product_id))
    db_product = result.scalar_one_or_none()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    for key, value in product.dict().items():
        setattr(db_product, key, value)

    await db.commit()
    await db.refresh(db_product)
    return db_product

@router.delete("/{product_id}")
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ProductMaster).where(ProductMaster.prd_id == product_id))
    db_product = result.scalar_one_or_none()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    await db.delete(db_product)
    await db.commit()
    return {"message": "Product deleted successfully"}