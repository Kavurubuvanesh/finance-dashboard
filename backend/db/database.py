from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Defines the Database URL
# For SQLite, creates a file named "finance.db" in backend folder.
SQLALCHEMY_DATABASE_URL = "sqlite:///./finance.db"

# Creates the Engine
# connect_args={"check_same_thread": False} is needed ONLY for SQLite.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Creates a SessionLocal class
# Each instance of this class will be a database session.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Creates a Base class
# Later, we will inherit from this class to create each of our database models.
Base = declarative_base()

# Dependency
# This is a helper function to get a database session in our endpoints.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()