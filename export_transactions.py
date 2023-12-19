from sqlalchemy import and_
import os
import sys
import pandas as pd
import datetime

from models import postgres_session
from models.transactions import ExpenseTransactions


def export_transactions(year_start, month_start, year_end=None, month_end=None, path=None):
    if year_end is None:
        year_end = year_start
        month_end = month_start

    start_date = datetime.datetime(year_start, month_start, 1)
    if month_end == 12:
        end_date = datetime.datetime(year_end, 12, 31)
    else:
        end_date = datetime.datetime(year_end, month_end + 1, 1) - datetime.timedelta(days=1)
    print(f'querying transactions between {start_date.strftime("%Y%m%d")} to {end_date.strftime("%Y%m%d")}')
    transactions = postgres_session.query(
        ExpenseTransactions
    ).filter(
        and_(
            ExpenseTransactions.transaction_date >= start_date,
            ExpenseTransactions.transaction_date <= end_date
        )
    ).all()
    transactions_rows = []
    for t in transactions:
        t_dict = {
            'Date': t.transaction_date,
            'Amount': t.amount,
            'Category': t.category,
            'Source': t.expense_source,
            'Comment': t.expense_comment,
        }
        transactions_rows.append(t_dict)
    transactions_df = pd.DataFrame(transactions_rows)
    filename = f'{start_date.strftime("%Y%m%d")}_to_{end_date.strftime("%Y%m%d")}_transactions.xlsx'
    if path:
        export_path = os.path.join(path, filename)
    else:
        export_path = filename
    transactions_df.to_excel(export_path, index=False)
    print(f'{start_date.strftime("%Y%m%d")}_to_{end_date.strftime("%Y%m%d")}_transactions.xlsx outputted')


if __name__ == '__main__':
    cmd_args = sys.argv
    print(cmd_args)
    if len(cmd_args) == 4:
        export_transactions(int(cmd_args[1]), int(cmd_args[2]), path=cmd_args[3])
    else:
        export_transactions(int(cmd_args[1]), int(cmd_args[2]), int(cmd_args[3]), int(cmd_args[4]), path=cmd_args[5])
