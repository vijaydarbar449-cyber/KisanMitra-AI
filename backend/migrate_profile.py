import sqlite3

DATABASE = "kisanmitra.db"

conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()

columns = [
    ("main_crop", "TEXT"),
    ("land_area", "TEXT"),
    ("irrigation_type", "TEXT"),
    ("mobile", "TEXT"),
]

for column_name, column_type in columns:
    try:
        cursor.execute(
            f"ALTER TABLE users ADD COLUMN {column_name} {column_type}"
        )
        print(f"Added column: {column_name}")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e).lower():
            print(f"Already exists: {column_name}")
        else:
            print(f"Error with {column_name}: {e}")

conn.commit()
conn.close()

print("Database migration completed successfully!")