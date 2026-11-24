
from datetime import date
from pydantic import BaseModel, Field


class ExpenseCreate(BaseModel):
    farm_id: int
    category: str = Field(min_length=2, max_length=100)
    amount: float = Field(gt=0)
    description: str | None = None
    expense_date: date


class ExpenseUpdate(BaseModel):
    category: str | None = Field(default=None, min_length=2, max_length=100)
    amount: float | None = Field(default=None, gt=0)
    description: str | None = None
    expense_date: date | None = None


class ExpenseResponse(BaseModel):
    id: int
    farm_id: int
    category: str
    amount: float
    description: str | None = None
    expense_date: date

    class Config:
        from_attributes = True
