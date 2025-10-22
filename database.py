from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String, DECIMAL, DateTime, ForeignKey, CHAR
from sqlalchemy.orm import relationship
import os
import ssl
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "mysql+aiomysql://tech0gen10student:vY7JZNfU@rdbs-002-gen10-step3-1-oshima1.mysql.database.azure.com:3306/hirai_pos")

if "mysql" in DATABASE_URL:
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    engine = create_async_engine(
        DATABASE_URL,
        echo=True,
        connect_args={
            "ssl": ssl_context
        }
    )
else:
    engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

class ProductMaster(Base):
    __tablename__ = "product_master"

    prd_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    code = Column(CHAR(13), unique=True, index=True, nullable=False)
    name = Column(String(50), nullable=False)
    price = Column(Integer, nullable=False)

class Trade(Base):
    __tablename__ = "trade"

    trd_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    datetime = Column(DateTime, nullable=False, default=datetime.now)
    emp_cd = Column(CHAR(10), nullable=False)
    store_cd = Column(CHAR(5), nullable=False)
    pos_no = Column(CHAR(3), nullable=False)
    total_amt = Column(Integer, nullable=False, default=0)

    details = relationship("TradeDetail", back_populates="trade")

class TradeDetail(Base):
    __tablename__ = "trade_detail"

    trd_id = Column(Integer, ForeignKey("trade.trd_id"), primary_key=True)
    dtl_id = Column(Integer, primary_key=True)
    prd_id = Column(Integer, ForeignKey("product_master.prd_id"), nullable=False)
    prd_code = Column(CHAR(13), nullable=False)
    prd_name = Column(String(50), nullable=False)
    prd_price = Column(Integer, nullable=False)

    trade = relationship("Trade", back_populates="details")
    product = relationship("ProductMaster")

async def get_db():
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()