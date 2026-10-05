from database.database import get_db


print("Testing database session...")

db = next(get_db())

print("Database session created successfully!")

db.close()

print("Database session closed successfully!")
print("KisanMitra AI Database Session is working.")