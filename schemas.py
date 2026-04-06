from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict
from models import RoleEnum, RecordTypeEnum

# ==========================================
# User Schemas
# ==========================================
class UserCreate(BaseModel):
    username: str = Field(..., description="Unique username for the system")
    role: RoleEnum

class UserOut(BaseModel):
    id: int
    username: str
    role: RoleEnum
    status: str

    class Config:
        from_attributes = True


# ==========================================
# Financial Record Schemas
# ==========================================
class RecordCreate(BaseModel):
    amount: float = Field(gt=0, description="Amount must be strictly greater than zero")
    type: RecordTypeEnum
    category: str = Field(..., description="E.g., Salary, Rent, Software Subscriptions")
    notes: Optional[str] = None

class RecordOut(RecordCreate):
    id: int
    date: datetime
    # Notice: We do NOT include 'is_deleted' here. 
    # That is internal backend logic. The client doesn't need to see it.

    class Config:
        from_attributes = True


# ==========================================
# Dashboard Schemas
# ==========================================
class DashboardSummary(BaseModel):
    total_income: float
    total_expenses: float
    net_balance: float
    
    # THE ENTERPRISE TOUCH: Advanced Data Structures
    # This dictionary will look like: {"Rent": 1500.0, "Software": 200.0}
    expense_by_category: Dict[str, float]