from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError # <-- NEW IMPORT
from typing import List

import models, schemas, auth
from database import get_db

router = APIRouter(
    prefix="/users",
    tags=["User Management"]
)

@router.post("/", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    
    try:
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        # THE ENTERPRISE TOUCH: Catch the unique constraint failure
        db.rollback() # Roll back the failed transaction
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="That username is already taken. Please choose another."
        )

@router.get("/", response_model=List[schemas.UserOut], dependencies=[Depends(auth.require_admin)])
def list_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()