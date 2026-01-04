from sqlalchemy import Column, Integer, String, Float, Boolean
from .database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    description = Column(String, nullable=True)
    is_income = Column(Boolean, default=False)
    date = Column(String, nullable=False)
    # Note: We use String for date in SQLite for simplicity,
    # but in Postgres, we would use proper Date types.