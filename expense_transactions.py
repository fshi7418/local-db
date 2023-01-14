from sqlalchemy import Column, Integer, Date, Float, String, create_engine
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ExpenseTransactions(Base):
    __tablename__ = 'expense_transactions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    transaction_date = Column(Date, index=True)
    amount = Column(Float)
    category = Column(String)
    expense_source = Column(String)
    expense_comment = Column(String)
    last_updated = Column(TIMESTAMP(timezone=True), default=func.now())


