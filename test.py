import sqlite3

# Connect to the database
conn = sqlite3.connect("arxiv_papers.db")
cursor = conn.cursor()

# List all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables in database:", tables)

# For each table, list columns
for table_name, in tables:
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = cursor.fetchall()
    print(f"\nColumns in table '{table_name}':")
    for col in columns:
        # col[1] is the column name, col[2] is the type
        print(f"  {col[1]} ({col[2]})")

conn.close()
