import sqlite3

conn = sqlite3.connect("resumatch.db")
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE candidates ADD COLUMN unified_keywords TEXT")
    conn.commit()
    print("Column added successfully.")
except Exception as e:
    print(f"Note: {e}")

conn.close()