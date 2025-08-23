import sys

from models import postgres_session
# Import the necessary models
from models.transactions import ExpenseBudget
from models.archery import ArcheryRange, ArcheryTarget, ArcheryBowType, ArcheryManufacturer, ArcheryLimb, \
    ArcheryRiser, ArcheryArrow, Shots, Ends, Rounds, ArcherySight, ArcheryScoringRule, ArcheryArrowRest
from models.books import BookPublisher, BookAuthor, BookTranslator, BookLanguage, BookSeries, BookFormat, Book

str_to_model = {
    'archery_range': ArcheryRange,
    'archery_target': ArcheryTarget,
    'archery_bow_type': ArcheryBowType,
    'archery_manufacturer': ArcheryManufacturer,
    'archery_limb': ArcheryLimb,
    'archery_riser': ArcheryRiser,
    'archery_arrow': ArcheryArrow,
    'archery_arrow_rest': ArcheryArrowRest,
    'archery_scoring_rule': ArcheryScoringRule,
    'archery_sight': ArcherySight,
    'book_publisher': BookPublisher,
    'book_author': BookAuthor,
    'book_translator': BookTranslator,
    'book_language': BookLanguage,
    'book_series': BookSeries,
    'book_format': BookFormat,
    'book': Book,
    'shots': Shots,
    'ends': Ends,
    'rounds': Rounds,
    'expense_budget': ExpenseBudget
}


def execute_any_q_text(db_engine, q_stmt):
    """
    Executes a SQL query and returns the results.

    :param db_engine: Path to the SQLite database file.
    :param q_stmt: SQL query string.
    :return: List of tuples containing the results.
    """
    # Connect to the database
    connection = db_engine.raw_connection()
    cursor = connection.cursor()
    results = []
    try:
        # Execute the query
        cursor.execute(q_stmt)
        # Fetch all results
        results = cursor.fetchall()

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()
        return results


def display_table_rows(model_, rows):
    if not rows:
        print("No records found.")
        return

    # Get column names
    column_names = model_.__table__.columns.keys()

    # get the appropriate string length to left-justify to make the cmd print output readable
    max_str_len_by_col_name = {cn: len(cn) for cn in column_names}
    for row in rows:
        for col in column_names:
            data_rc = str(getattr(row, col))
            if len(data_rc) > max_str_len_by_col_name[col]:
                max_str_len_by_col_name[col] = len(data_rc)

    # construct what is actually printed
    column_names_printed = [cn.ljust(max_str_len_by_col_name[cn]) for cn in column_names]

    # Print header
    header = "|".join(column_names_printed)
    print(header)
    print("-" * len(header))
    row_data = []
    for row in rows:
        for col in column_names:
            row_data.append(str(getattr(row, col)).ljust(max_str_len_by_col_name[col]))
        print('|'.join(row_data))
        row_data = []


def display_and_return_table_rows(model_, session):
    ret = []
    rows = []
    try:
        # Query all rows from the table
        rows = session.query(model_).all()

        # construct return value
        column_names = model_.__table__.columns.keys()
        ret = [[getattr(row, col) for col in column_names] for row in rows]

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        display_table_rows(model_, rows)
        return ret


if __name__ == '__main__':
    cmd_args = sys.argv
    cmd_type = cmd_args[1]
    if cmd_type == 'query':
        if len(cmd_args) < 3:
            raise ValueError('need to provide table being queried')
        table_name = cmd_args[2]
        model = str_to_model.get(table_name)
        if model is None:
            raise KeyError(f'{table_name} does not exist')
        display_and_return_table_rows(model, postgres_session)
    else:
        raise NotImplementedError(f'{cmd_type} is not implemented')

    # r = execute_any_q_text(postgres_session.bind, 'select max(date) from archery_round')
    # print(r)
