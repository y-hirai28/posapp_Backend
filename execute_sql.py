import asyncio
import aiomysql
import os
import ssl
from dotenv import load_dotenv

load_dotenv()

async def execute_sql_file(sql_file_path='table.sql'):
    # Read SQL file
    with open(sql_file_path, 'r', encoding='utf-8') as f:
        sql_content = f.read()

    # Split by statements (simple split by semicolon)
    statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]

    # Create SSL context
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    # Connect to database
    conn = await aiomysql.connect(
        host=os.getenv('DATABASE_HOST'),
        port=int(os.getenv('DATABASE_PORT', 3306)),
        user=os.getenv('DATABASE_USER'),
        password=os.getenv('DATABASE_PASSWORD'),
        db=os.getenv('DATABASE_NAME'),
        ssl=ssl_context,
        autocommit=False
    )

    try:
        async with conn.cursor() as cursor:
            for stmt in statements:
                if stmt.strip():
                    print(f"Executing: {stmt[:100]}...")
                    try:
                        await cursor.execute(stmt)
                        if stmt.strip().upper().startswith('SELECT'):
                            result = await cursor.fetchall()
                            for row in result:
                                print(row)
                    except Exception as e:
                        print(f"Error executing statement: {e}")
                        print(f"Statement: {stmt}")

            await conn.commit()
            print("All SQL statements executed successfully!")

    finally:
        conn.close()

if __name__ == "__main__":
    import sys
    sql_file = sys.argv[1] if len(sys.argv) > 1 else 'table.sql'
    asyncio.run(execute_sql_file(sql_file))
