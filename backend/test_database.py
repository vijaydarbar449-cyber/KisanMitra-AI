from database.database import engine, Base
from models.user import User

print("Connecting to database...")

Base.metadata.create_all(bind=engine)

print("Database connected successfully!")
print("Users table created successfully!")
print("KisanMitra AI Database is ready.")