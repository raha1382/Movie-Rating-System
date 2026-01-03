from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import os

# Get database URL from environment variable (.env)
# Fallback to hardcoded URL if env variable is not set
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:123456@localhost:5432/movie_db"
)

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

try:
    # Try to connect to the database
    with engine.connect() as connection:
        # Execute a simple query to test the connection
        result = connection.execute(text("SELECT 1"))

        print("✅ Database connection successful")
        print("Result:", result.scalar())

except SQLAlchemyError as e:
    # Catch and print any connection-related errors
    print("❌ Database connection failed")
    print(e)