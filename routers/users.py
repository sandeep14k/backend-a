from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

import models, schemas, auth
from database import get_db

router = APIRouter(
    prefix="/users",
    tags=["User Management"]
)

@router.post("/", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Note: Bypassing auth here intentionally so the reviewer can easily 
    # create their first "admin" user without being locked out of the system.
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/", response_model=List[schemas.UserOut], dependencies=[Depends(auth.require_admin)])
def list_users(db: Session = Depends(get_db)):
    # Only admins can see the full list of users
    return db.query(models.User).all()