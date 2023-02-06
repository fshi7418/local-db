from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import pandas as pd
import os
import sys

from expense_transactions import ExpenseTransactions
from transaction_configs import ExpenseCat, ExpenseSource

conn_string = 'postgresql://postgres:utS2022!@localhost/postgres'
engine = create_engine(conn_string)
Session = sessionmaker(bind=engine)

postgres_session = Session()


def query_first_n(n):
    if isinstance(n, int) is False:
        raise Exception(f'{n} is not an integer')
    if n < 0:
        raise Exception(f'please provide a nonnegative integer')
    first_n = postgres_session.query(
        ExpenseTransactions
    ).order_by(
        ExpenseTransactions.transaction_date.desc()
    ).limit(n).all()
    date_col_width = 10
    amount_col_width = 10
    category_col_width = 25
    source_col_width = 20
    comment_col_width = 50
    print('-' * (date_col_width + amount_col_width + category_col_width + source_col_width + comment_col_width + 4))
    print('|'.join(['Date'.ljust(date_col_width), 'Amount'.ljust(amount_col_width), 'Category'.ljust(category_col_width), 'Source'.ljust(source_col_width), 'Comment'.ljust(comment_col_width)]))
    print('-' * (date_col_width + amount_col_width + category_col_width + source_col_width + comment_col_width + 4))
    for d in first_n:
        d_row = [d.transaction_date.strftime('%Y-%m-%d'), str(d.amount).ljust(amount_col_width), str(d.category).ljust(category_col_width), d.expense_source.ljust(source_col_width), d.expense_comment]
        print('|'.join(d_row))
    postgres_session.close()


if __name__ == '__main__':
    cmd_args = sys.argv
    query_first_n(int(cmd_args[1]))
