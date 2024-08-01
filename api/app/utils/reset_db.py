import os
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy_utils import database_exists, create_database, drop_database
from sqlalchemy.orm import declarative_base
from alembic import command
from alembic.config import Config

Base = declarative_base()


# Database connection string
DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/postgres"

def reset_database():
    try:
        # Create engine to connect to default database
        default_engine = create_engine(DATABASE_URL)
        
        with default_engine.connect() as connection:
            connection.execute(text("COMMIT"))  # Close any open transactions
            
            # Check if the database exists
            exists = connection.execute(text(f"SELECT 1 FROM pg_database WHERE datname='{DB_NAME}'")).fetchone()
            
            if not exists:
                print(f"Creating new database: {DB_NAME}")
                connection.execute(text(f"CREATE DATABASE {DB_NAME}"))
            else:
                print(f"Database {DB_NAME} already exists")

        # Create engine for the specific database
        engine = create_engine(DATABASE_URL)
        print(f"Connecting to database: {DATABASE_URL}")

        # Create all tables
        print("Creating tables...")
        Base.metadata.create_all(engine)

        # Run Alembic migrations
        print("Running migrations...")
        alembic_cfg = Config("alembic.ini")
        command.upgrade(alembic_cfg, "head")

        print("Database setup/reset successful!")
        return True

    except SQLAlchemyError as e:
        print(f"An error occurred: {str(e)}")
        return False

if __name__ == "__main__":
    reset_database()