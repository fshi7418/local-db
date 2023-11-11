from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd
import os

from models.transactions import ExpenseTransactions

doc_path = r'/home/franks/Documents'
expense_csv = os.path.join(doc_path, 'expenses.csv')

expenses_df = pd.read_csv(expense_csv, parse_dates=['Date'])

conn_string = 'postgresql://postgres:utS2022!@localhost/postgres'
engine = create_engine(conn_string)
Session = sessionmaker(bind=engine)

postgres_session = Session()

for i, r in expenses_df.iterrows():
    new_expense = dict(
        transaction_date=r['Date'],
        amount=r['Amount'],
        category=r['Category'],
        expense_source=r['Source'],
        expense_comment=r['Comment']
    )
    print(f'inserting row {i}')
    postgres_session.add(ExpenseTransactions(**new_expense))

postgres_session.commit()

