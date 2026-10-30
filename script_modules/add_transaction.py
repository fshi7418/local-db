from models import postgres_session
from models.transactions import ExpenseTransactions, ExpenseSource
from transaction_configs import ExpenseCat


def add_expense(e_date, e_amount, e_category_str, e_source_id, e_comment, e_budget_id):

    try:
        category_obj = getattr(ExpenseCat, e_category_str)
    except AttributeError:
        print(f'{e_category_str} is not recognised, please try again')
        return

    source_obj = postgres_session.get(ExpenseSource, int(e_source_id))
    if source_obj is None:
        print(f'expense_source id {e_source_id} is not recognised, please try again')
        return

    if e_budget_id == '':
        e_budget_id = None
    new_expense = dict(
        transaction_date=e_date,
        amount=e_amount,
        category=category_obj.value,
        expense_source_id=source_obj.id,
        expense_comment=e_comment,
        expense_budget_id=e_budget_id,
    )
    print('adding record...')
    postgres_session.add(ExpenseTransactions(**new_expense))

    print('committing to db...')
    postgres_session.commit()
    postgres_session.close()
