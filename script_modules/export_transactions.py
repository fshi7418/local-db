import os
import sys
import pandas as pd
import datetime

import utilities
from models import postgres_session


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
    txt = f'''
        select 
            t.transaction_date, t.amount, t.category, t.expense_source, t.expense_comment,
            b.subcategory as budget_subcategory
        from expense_transactions t
        left join expense_budget b on t.expense_budget_id = b.id
        where true
        and transaction_date >= '{start_date.strftime("%Y-%m-%d")}'
        and transaction_date <= '{end_date.strftime("%Y-%m-%d")}'
        order by transaction_date asc, t.id asc
    '''
    print(txt)
    cols, rows = utilities.execute_any_q_text(postgres_session.bind, txt)
    transactions = [
        {c: r[i] for i, c in enumerate(cols)} for r in rows
    ]

    transaction_rows = []
    for t in transactions:
        t_dict = {
            'Date': t['transaction_date'],
            'Amount': t['amount'],
            'Category': t['category'],
            'Source': t['expense_source'],
            'Comment': t['expense_comment'],
            'Subcategory': t['budget_subcategory'],
        }
        transaction_rows.append(t_dict)
    transactions_df = pd.DataFrame(transaction_rows)
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
