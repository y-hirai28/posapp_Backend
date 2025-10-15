import asyncio
from database import engine, Base, ProductMaster, async_session

async def init_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        # 13桁JANコード形式のサンプルデータ
        sample_products = [
            # 文具カテゴリー: 45xxxxx
            ProductMaster(code='4512345000011', name='ボールペン(黒・0.5mm)', price=120),
            ProductMaster(code='4512345000028', name='シャープペンシル(0.5mm)', price=180),
            ProductMaster(code='4512345000035', name='消しゴム(小)', price=80),
            ProductMaster(code='4512345000042', name='はさみ(事務用)', price=350),

            # オフィス用品: 49xxxxx
            ProductMaster(code='4987654000012', name='A4コピー用紙(500枚)', price=480),
            ProductMaster(code='4987654000029', name='スティックのり', price=150),
            ProductMaster(code='4987654000036', name='ホッチキス(中型)', price=520),
            ProductMaster(code='4987654000043', name='ホッチキス針(1000本入り)', price=250),

            # 家具カテゴリー: 46xxxxx
            ProductMaster(code='4611111000016', name='デスクチェア(メッシュ)', price=6980),
            ProductMaster(code='4611111000023', name='折りたたみ会議テーブル(180cm)', price=4980),
            ProductMaster(code='4611111000030', name='オフィスデスク(シンプルタイプ)', price=8500),
            ProductMaster(code='4611111000047', name='スチール書庫(3段)', price=12800),
            ProductMaster(code='4611111000054', name='卓上LEDライト(USB電源)', price=1980),
        ]

        for product in sample_products:
            session.add(product)

        await session.commit()
        print("サンプルデータを追加しました")

if __name__ == "__main__":
    asyncio.run(init_database())