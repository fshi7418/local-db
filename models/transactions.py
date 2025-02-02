from sqlalchemy import Column, Integer, Date, Float, String
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import TIMESTAMP

from models import Base


class ExpenseTransactions(Base):
    __tablename__ = 'expense_transactions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    transaction_date = Column(Date, index=True)
    amount = Column(Float)
    category = Column(String)
    expense_budget_id = Column(Integer)
    expense_source = Column(String)
    expense_comment = Column(String)
    last_updated = Column(TIMESTAMP(timezone=True), default=func.now())


class ExpenseBudget(Base):
    __tablename__ = 'expense_budget'
    id = Column(Integer, primary_key=True, autoincrement=True)
    budget_start_date = Column(Date, index=True)
    budget_end_date = Column(Date, index=True)
    income_expense = Column(String(7))  # 'income' or 'expense'
    category = Column(String)
    subcategory = Column(String)
    frequency = Column(Integer)
    amount = Column(Float)
    last_updated = Column(TIMESTAMP(timezone=True), default=func.now())
