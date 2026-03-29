import sys

from models import postgres_session
from models.transactions import ExpenseTransactions
from transaction_configs import ExpenseCat, ExpenseSource


def add_expense(e_date, e_amount, e_category_str, e_source_str, e_comment, e_budget_id):

    try:
        category_obj = getattr(ExpenseCat, e_category_str)
    except AttributeError:
        print(f'{e_category_str} is not recognised, please try again')
        return

    try:
        source_obj = getattr(ExpenseSource, e_source_str)
    except AttributeError:
        print(f'{e_source_str} is not recognised, please try again')
        return

    if e_budget_id == '':
        e_budget_id = None
    new_expense = dict(
        transaction_date=e_date,
        amount=e_amount,
        category=category_obj.value,
        expense_source=source_obj.value,
        expense_comment=e_comment,
        expense_budget_id=e_budget_id,
    )
    print('adding record...')
    postgres_session.add(ExpenseTransactions(**new_expense))

    print('committing to db...')
    postgres_session.commit()
    postgres_session.close()


if __name__ == '__main__':
    cmd_args = sys.argv
    add_expense(cmd_args[1], cmd_args[2], cmd_args[3], cmd_args[4], cmd_args[5], cmd_args[6])
