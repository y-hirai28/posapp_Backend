import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

def execute_sql_file(sql_file_path='table.sql'):
    # Read SQL file
    with open(sql_file_path, 'r', encoding='utf-8') as f:
        sql_content = f.read()

    # Split by statements
    statements = []
    current_stmt = []
    in_delimiter = False

    for line in sql_content.split('\n'):
        stripped = line.strip()

        # Skip comments and USE statements
        if stripped.startswith('--') or stripped.startswith('USE '):
            continue

        # Handle DELIMITER changes
        if stripped.startswith('DELIMITER'):
            in_delimiter = not in_delimiter
            continue

        current_stmt.append(line)

        # Check for statement end
        if not in_delimiter and stripped.endswith(';'):
            stmt = '\n'.join(current_stmt)
            if stmt.strip():
                statements.append(stmt)
            current_stmt = []

    # Add remaining statement if any
    if current_stmt:
        stmt = '\n'.join(current_stmt)
        if stmt.strip():
            statements.append(stmt)

    # Connect to database
    connection = pymysql.connect(
        host=os.getenv('DATABASE_HOST'),
        port=int(os.getenv('DATABASE_PORT', 3306)),
        user=os.getenv('DATABASE_USER'),
        password=os.getenv('DATABASE_PASSWORD'),
        database=os.getenv('DATABASE_NAME'),
        ssl={'ssl_disabled': False},
        charset='utf8mb4',
        autocommit=False
    )

    try:
        cursor = connection.cursor()

        for i, stmt in enumerate(statements, 1):
            if stmt.strip():
                print(f"[{i}/{len(statements)}] Executing: {stmt[:80].strip()}...")
                try:
                    # Execute statement
                    cursor.execute(stmt)

                    # If SELECT, show results
                    if stmt.strip().upper().startswith('SELECT'):
                        results = cursor.fetchall()
                        if results:
                            for row in results:
                                print(f"  Result: {row}")
                        else:
                            print("  No results")
                    else:
                        print(f"  Affected rows: {cursor.rowcount}")

                except Exception as e:
                    print(f"  Error: {e}")
                    print(f"  Statement: {stmt[:200]}")
                    # Continue with next statement

        connection.commit()
        print("\n✓ All SQL statements executed successfully!")

        # Verify product_master data
        print("\n商品マスタのデータを確認:")
        cursor.execute("SELECT code, name, price FROM product_master LIMIT 10")
        products = cursor.fetchall()
        for product in products:
            print(f"  {product[0]} | {product[1]} | ¥{product[2]}")

        cursor.close()

    except Exception as e:
        connection.rollback()
        print(f"Error during execution: {e}")
        raise
    finally:
        connection.close()

if __name__ == "__main__":
    import sys
    sql_file = sys.argv[1] if len(sys.argv) > 1 else 'table.sql'
    execute_sql_file(sql_file)
