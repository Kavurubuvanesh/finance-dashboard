from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# 1. Get the DB URL from the Environment (Vercel)
# If it doesn't exist, fall back to local SQLite (Laptop)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./finance.db")

# 2. Fix the URL for SQLAlchemy (Postgres requires 'postgresql://')
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# 3. Configure the Engine
if "sqlite" in DATABASE_URL:
    # SQLite settings
    engine = create_engine(
        DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    # Postgres settings (Neon)
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()