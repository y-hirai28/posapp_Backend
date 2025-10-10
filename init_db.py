import asyncio
from database import engine, Base, ProductMaster, async_session

async def init_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        # SQLファイルに合わせたサンプルデータ
        sample_products = [
            ProductMaster(code='0000000000001', name='ボールペン(黒・0.5mm)', price=120),
            ProductMaster(code='0000000000002', name='シャープペンシル(0.5mm)', price=180),
            ProductMaster(code='0000000000003', name='消しゴム(小)', price=80),
            ProductMaster(code='0000000000004', name='A4コピー用紙(500枚)', price=480),
            ProductMaster(code='0000000000005', name='スティックのり', price=150),
            ProductMaster(code='0000000000006', name='ホッチキス(中型)', price=520),
            ProductMaster(code='0000000000007', name='ホッチキス針(1000本入り)', price=250),
            ProductMaster(code='0000000000008', name='はさみ(事務用)', price=350),
            ProductMaster(code='0000000000009', name='デスクチェア(メッシュ)', price=6980),
            ProductMaster(code='0000000000010', name='折りたたみ会議テーブル(180cm)', price=4980),
            ProductMaster(code='0000000000011', name='オフィスデスク(シンプルタイプ)', price=8500),
            ProductMaster(code='0000000000012', name='スチール書庫(3段)', price=12800),
            ProductMaster(code='0000000000013', name='卓上LEDライト(USB電源)', price=1980),
        ]

        for product in sample_products:
            session.add(product)

        await session.commit()
        print("サンプルデータを追加しました")

if __name__ == "__main__":
    asyncio.run(init_database())