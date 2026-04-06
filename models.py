from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Enum as SQLEnum
from datetime import datetime
import enum
from database import Base

# --- Enums ---
class RoleEnum(str, enum.Enum):
    viewer = "viewer"
    analyst = "analyst"
    admin = "admin"

class RecordTypeEnum(str, enum.Enum):
    income = "income"
    expense = "expense"

# --- Database Models ---
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    role = Column(SQLEnum(RoleEnum), default=RoleEnum.viewer)
    status = Column(String, default="active") # active or inactive

class FinancialRecord(Base):
    __tablename__ = "financial_records"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    type = Column(SQLEnum(RecordTypeEnum), nullable=False)
    category = Column(String, index=True)
    date = Column(DateTime, default=datetime.utcnow)
    notes = Column(String, nullable=True)
    
    # THE ENTERPRISE TOUCH: Soft Deletes
    # We never actually delete financial records. We just hide them.
    is_deleted = Column(Boolean, default=False, index=True)