from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from database.database import get_db
from models.expense import Expense
from models.farm import Farm
from models.user import User
from api.auth import get_current_user
from schemas.expense import ExpenseCreate, ExpenseUpdate, ExpenseResponse

router = APIRouter(
    prefix="/api/v1/expenses",
    tags=["Farm Expenses"]
)


@router.post("/", response_model=ExpenseResponse)
def create_expense(
    expense: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    farm = db.query(Farm).filter(
        Farm.id == expense.farm_id,
        Farm.user_id == current_user.id
    ).first()

    if not farm:
        raise HTTPException(status_code=404, detail="Farm not found")

    new_expense = Expense(**expense.model_dump())

    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    return new_expense


@router.get("/", response_model=list[ExpenseResponse])
def get_expenses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Expense).join(
        Farm, Expense.farm_id == Farm.id
    ).filter(
        Farm.user_id == current_user.id
    ).order_by(Expense.expense_date.desc()).all()


@router.put("/{expense_id}", response_model=ExpenseResponse)
def update_expense(
    expense_id: int,
    expense: ExpenseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    existing = db.query(Expense).join(
        Farm, Expense.farm_id == Farm.id
    ).filter(
        Expense.id == expense_id,
        Farm.user_id == current_user.id
    ).first()

    if not existing:
        raise HTTPException(status_code=404, detail="Expense not found")

    for key, value in expense.model_dump(exclude_unset=True).items():
        setattr(existing, key, value)

    db.commit()
    db.refresh(existing)

    return existing


@router.delete("/{expense_id}")
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    existing = db.query(Expense).join(
        Farm, Expense.farm_id == Farm.id
    ).filter(
        Expense.id == expense_id,
        Farm.user_id == current_user.id
    ).first()

    if not existing:
        raise HTTPException(status_code=404, detail="Expense not found")

    db.delete(existing)
    db.commit()

    return {"message": "Expense deleted successfully"}
@router.get("/summary")
def get_expense_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = db.query(
        func.count(Expense.id),
        func.coalesce(func.sum(Expense.amount), 0)
    ).join(
        Farm, Expense.farm_id == Farm.id
    ).filter(
        Farm.user_id == current_user.id
    ).first()

    return {
        "status": "success",
        "total_expenses": result[0],
        "total_amount": result[1]
    }