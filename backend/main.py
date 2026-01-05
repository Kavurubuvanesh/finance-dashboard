import sys
import os

# --- PATH HACK FOR VERCEL ---
# Get the directory where this file (main.py) lives
current_dir = os.path.dirname(os.path.abspath(__file__))
# Get the parent directory (root)
parent_dir = os.path.dirname(current_dir)

# Force add both to Python's search path
sys.path.append(current_dir)
sys.path.append(parent_dir)
# ---------------------------

from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from typing import List, Annotated
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import io

# --- ROBUST IMPORTS ---
# We try importing with the 'backend.' prefix (Cloud/Root style)
# If that fails, we try local style.
try:
    from backend.db import models, database
    from backend import schemas
except ImportError:
    # Fallback for local testing
    from db import models, database
    import schemas
# ----------------------

# Detect Vercel
is_vercel = os.getenv("VERCEL")
app = FastAPI(root_path="/api" if is_vercel else "")

# CORS
origins = ["*"]  # Allow everything for now
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
    count = 0
    for index, row in df.iterrows():
        try:
            # Flexible boolean conversion
            is_inc = str(row['is_income']).lower() in ['true', '1', 'yes']

            t = models.Transaction(
                amount=float(row['amount']),
                category=str(row['category']),
                description=str(row.get('description', '')),
                is_income=is_inc,
                date=str(row['date'])
            )
            db.add(t)
            count += 1
        except Exception:
            continue
    db.commit()
    return {"message": f"Uploaded {count} transactions"}