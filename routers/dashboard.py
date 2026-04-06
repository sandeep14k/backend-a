from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Dict

import models, schemas, auth
from database import get_db

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard Analytics"]
)

@router.get("/summary", response_model=schemas.DashboardSummary, dependencies=[Depends(auth.require_analyst_or_admin)])
def get_dashboard_summary(db: Session = Depends(get_db)):
    # 1. Calculate Total Income (excluding soft deletes)
    total_income = db.query(func.sum(models.FinancialRecord.amount)).filter(
        models.FinancialRecord.type == models.RecordTypeEnum.income,
        models.FinancialRecord.is_deleted == False
    ).scalar() or 0.0

    # 2. Calculate Total Expenses (excluding soft deletes)
    total_expenses = db.query(func.sum(models.FinancialRecord.amount)).filter(
        models.FinancialRecord.type == models.RecordTypeEnum.expense,
        models.FinancialRecord.is_deleted == False
    ).scalar() or 0.0

    # 3. THE ENTERPRISE TOUCH: Category-wise Expense Grouping
    # This generates a single SQL query like: 
    # SELECT category, SUM(amount) FROM records WHERE type='expense' GROUP BY category
    category_totals = db.query(
        models.FinancialRecord.category,
        func.sum(models.FinancialRecord.amount).label("total")
    ).filter(
        models.FinancialRecord.type == models.RecordTypeEnum.expense,
        models.FinancialRecord.is_deleted == False
    ).group_by(models.FinancialRecord.category).all()

    # Convert the SQLAlchemy result into a standard Python dictionary
    expense_dict: Dict[str, float] = {cat: total for cat, total in category_totals}

    return schemas.DashboardSummary(
        total_income=total_income,
        total_expenses=total_expenses,
        net_balance=total_income - total_expenses,
        expense_by_category=expense_dict
    )