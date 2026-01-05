import sys
import os
from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from typing import List, Annotated
from sqlalchemy.orm import Session
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import io

# --- BULLETPROOF IMPORT BLOCK ---
# This handles the difference between "Local Laptop" and "Vercel Cloud"
try:
    # Try the local way first (when running from backend/ folder)
    from db import models, database
    import schemas
except ImportError:
    # If that fails, try the Vercel way (absolute path from root)
    from backend.db import models, database
    from backend import schemas
# --------------------------------

# --- VERCEL ROUTING FIX ---
# Detect if running on Vercel
is_vercel = os.getenv("VERCEL")
app = FastAPI(root_path="/api" if is_vercel else "")

# --- CORS CONFIGURATION ---
origins = [
    "http://localhost:5173",
    "https://finance-dashboard.vercel.app",
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create Tables
models.Base.metadata.create_all(bind=database.engine)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


# --- ENDPOINTS ---

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


@app.post("/transactions/upload")
async def upload_transactions(db: db_dependency, file: UploadFile = File(...)):
    contents = await file.read()
    df = pd.read_csv(io.BytesIO(contents))
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
            continue

    db.commit()
    return {"message": f"Successfully uploaded {transactions_added} transactions"}