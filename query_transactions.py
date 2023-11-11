from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys

from models.transactions import ExpenseTransactions

conn_string = 'postgresql://postgres:utS2022!@localhost/postgres'
engine = create_engine(conn_string)
Session = sessionmaker(bind=engine)

postgres_session = Session()


def query_first_n(n):
    if isinstance(n, int) is False:
        raise Exception(f'{n} is not an integer')
    if n < 0:
        raise Exception(f'please provide a non-negative integer')
    first_n = postgres_session.query(
        ExpenseTransactions
    ).order_by(
        ExpenseTransactions.transaction_date.desc()
    ).limit(n).all()
    id_col_width = 8
    date_col_width = 10
    amount_col_width = 10
    category_col_width = 25
    source_col_width = 20
    comment_col_width = 50
    width_list = [
        id_col_width,
        date_col_width,
        amount_col_width,
        category_col_width,
        source_col_width,
        comment_col_width,
    ]
    print('-' * (sum(width_list) + 4))
    print('|'.join([
        'ID'.ljust(id_col_width),
        'Date'.ljust(date_col_width),
        'Amount'.ljust(amount_col_width),
        'Category'.ljust(category_col_width),
        'Source'.ljust(source_col_width),
        'Comment'.ljust(comment_col_width)
    ]))
    print('-' * (sum(width_list) + 4))
    for d in first_n:
        d_row = [
            str(d.id).ljust(id_col_width),
            d.transaction_date.strftime('%Y-%m-%d'),
            str(d.amount).ljust(amount_col_width),
            str(d.category).ljust(category_col_width),
            d.expense_source.ljust(source_col_width),
            d.expense_comment
        ]
        print('|'.join(d_row))
    postgres_session.close()


if __name__ == '__main__':
    cmd_args = sys.argv
    query_first_n(int(cmd_args[1]))
