import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

connection = pymysql.connect(
    host=os.getenv('DATABASE_HOST'),
    port=int(os.getenv('DATABASE_PORT', 3306)),
    user=os.getenv('DATABASE_USER'),
    password=os.getenv('DATABASE_PASSWORD'),
    database=os.getenv('DATABASE_NAME'),
    ssl={'ssl_disabled': False},
    charset='utf8mb4'
)

try:
    cursor = connection.cursor()

    print("=== MySQL product_master data ===")
    cursor.execute("SELECT code, name, price FROM product_master")
    products = cursor.fetchall()

    print(f"Total products: {len(products)}\n")

    for product in products:
        code, name, price = product
        print(f"Code: {code} ({len(code)} digits) | Name: {name} | Price: {price}")

    cursor.close()

except Exception as e:
    print(f"Error: {e}")
finally:
    connection.close()
