from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

import models, schemas, auth
from database import get_db

# Create an APIRouter instance for the records domain
router = APIRouter(
    prefix="/records",
    tags=["Financial Records"]
)

@router.post("/", response_model=schemas.RecordOut, status_code=status.HTTP_201_CREATED, dependencies=[Depends(auth.require_admin)])
def create_record(record: schemas.RecordCreate, db: Session = Depends(get_db)):
    db_record = models.FinancialRecord(**record.model_dump())
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

@router.get("/", response_model=List[schemas.RecordOut], dependencies=[Depends(auth.require_analyst_or_admin)])
def get_records(
    type: Optional[models.RecordTypeEnum] = None, 
    category: Optional[str] = None, 
    start_date: Optional[datetime] = Query(None, description="Filter records from this date"),
    end_date: Optional[datetime] = Query(None, description="Filter records up to this date"),
    skip: int = Query(0, ge=0, description="Pagination offset"),
    limit: int = Query(100, ge=1, le=100, description="Pagination limit (max 100)"),
    db: Session = Depends(get_db)
):
    # 1. Base Query: ALWAYS exclude soft-deleted records
    query = db.query(models.FinancialRecord).filter(models.FinancialRecord.is_deleted == False)
    
    # 2. Apply dynamic filters
    if type:
        query = query.filter(models.FinancialRecord.type == type)
    if category:
        query = query.filter(models.FinancialRecord.category == category)
    if start_date:
        query = query.filter(models.FinancialRecord.date >= start_date)
    if end_date:
        query = query.filter(models.FinancialRecord.date <= end_date)
        
    # 3. Apply pagination and fetch results
    return query.offset(skip).limit(limit).all()

@router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(auth.require_admin)])
def delete_record(record_id: int, db: Session = Depends(get_db)):
    # Look for the record, ensuring it hasn't already been deleted
    record = db.query(models.FinancialRecord).filter(
        models.FinancialRecord.id == record_id,
        models.FinancialRecord.is_deleted == False
    ).first()
    
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")
    
    # THE ENTERPRISE TOUCH: Soft Delete
    record.is_deleted = True
    db.commit()
    
    # Returning nothing is standard practice for a 204 No Content response
    return