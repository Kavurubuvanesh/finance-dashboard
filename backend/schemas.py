from pydantic import BaseModel

# Base schema with shared attributes
class TransactionBase(BaseModel):
    amount: float
    category: str
    description: str | None = None
    is_income: bool = False
    date: str

# Schema for CREATING a transaction (Input)
class TransactionCreate(TransactionBase):
    pass

# Schema for READING a transaction (Output)
# We include the 'id' here because the database generates it,
# but the user doesn't provide it when creating.
class TransactionModel(TransactionBase):
    id: int

    class Config:
        from_attributes = True