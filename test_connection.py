import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

try:
    connection = pymysql.connect(
        host='rdbs-002-gen10-step3-1-oshima1.mysql.database.azure.com',
        port=3306,
        user='tech0gen10student',
        password='vY7JZNfU',
        database='hirai_pos',
        ssl={'ssl_disabled': False},
        charset='utf8mb4'
    )
    
    print("MySQL接続成功!")
    
    cursor = connection.cursor()
    cursor.execute("SELECT VERSION()")
    version = cursor.fetchone()
    print(f"MySQL バージョン: {version[0]}")
    
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    print(f"テーブル数: {len(tables)}")
    
    cursor.close()
    connection.close()
    
except Exception as e:
    print(f"MySQL接続失敗: {e}")