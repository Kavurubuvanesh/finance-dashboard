from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from typing import List, Annotated
from sqlalchemy.orm import Session
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from db import models, database
import schemas
import pandas as pd  # <--- NEW
import io  # <--- NEW

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://localhost:5176",  # Added your port just in case
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=database.engine)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


# --- EXISTING ENDPOINTS ---

@app.post("/transactions/", response_model=schemas.TransactionModel)
async def create_transaction(transaction: schemas.TransactionCreate, db: db_dependency):
    db_transaction = models.Transaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


@app.get("/transactions/", response_model=List[schemas.TransactionModel])
async def read_transactions(db: db_dependency, skip: int = 0, limit: int = 100):
    transactions = db.query(models.Transaction).offset(skip).limit(limit).all()
    return transactions


# --- NEW AUTOMATION ENDPOINT ---

# SWAP THE ORDER: db first, file second
@app.post("/transactions/upload")
async def upload_transactions(db: db_dependency, file: UploadFile = File(...)):
    # 1. Read the file content
    contents = await file.read()

    # 2. Convert bytes to a Pandas DataFrame
    df = pd.read_csv(io.BytesIO(contents))

    # 3. Iterate and save
    transactions_added = 0

    for index, row in df.iterrows():
        try:
            transaction = models.Transaction(
                amount=float(row['amount']),
                category=row['category'],
                description=row.get('description', ''),
                is_income=bool(row['is_income']),
                date=str(row['date'])
            )
            db.add(transaction)
            transactions_added += 1
        except Exception as e:
            print(f"Error skipping row {index}: {e}")
            continue

    db.commit()
    return {"message": f"Successfully uploaded {transactions_added} transactions"}