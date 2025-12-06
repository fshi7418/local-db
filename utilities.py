import sys

from models import postgres_session
# Import the necessary models
from models.transactions import ExpenseBudget
from models.archery import ArcheryRange, ArcheryTarget, ArcheryBowType, ArcheryManufacturer, ArcheryLimb, \
    ArcheryRiser, ArcheryArrow, Shots, Ends, Rounds, ArcherySight, ArcheryScoringRule, ArcheryArrowRest, \
    ArcheryReleaseAid
from models.books import BookPublisher, BookAuthor, BookTranslator, BookLanguage, BookSeries, BookEditor, BookFormat, Book

str_to_model = {
    'archery_range': ArcheryRange,
    'archery_target': ArcheryTarget,
    'archery_bow_type': ArcheryBowType,
    'archery_manufacturer': ArcheryManufacturer,
    'archery_limb': ArcheryLimb,
    'archery_riser': ArcheryRiser,
    'archery_release_aid': ArcheryReleaseAid,
    'archery_arrow': ArcheryArrow,
    'archery_arrow_rest': ArcheryArrowRest,
    'archery_scoring_rule': ArcheryScoringRule,
    'archery_sight': ArcherySight,
    'book_publisher': BookPublisher,
    'book_author': BookAuthor,
    'book_editor': BookEditor,
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
    :return: list of str, representing the column names, and list of tuples containing the results.
    """
    # Connect to the database
    connection = db_engine.raw_connection()
    cursor = connection.cursor()
    column_names = []
    results = []
    try:
        # Execute the query
        cursor.execute(q_stmt)
        # Fetch all results
        results = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()
        return column_names, results


def display_table_rows_given_columns(column_names, rows):
    if not rows:
        print("No records found.")
        return

    # transform result into list of dict
    r_records = [{
        c: r[i] for i, c in enumerate(column_names)
    } for r in rows]

    # get the appropriate string length to left-justify to make the cmd print output readable
    max_str_len_by_col_name = {cn: len(cn) for cn in column_names}
    for row in r_records:
        for col, val in row.items():
            val = str(val)
            if len(val) > max_str_len_by_col_name[col]:
                max_str_len_by_col_name[col] = len(val)

    # construct what is actually printed
    column_names_printed = [cn.ljust(max_str_len_by_col_name[cn]) for cn in column_names]

    # Print header
    header = "|".join(column_names_printed)
    print(header)
    print("-" * len(header))
    row_data = []
    for row in r_records:
        for col, val in row.items():
            row_data.append(str(val).ljust(max_str_len_by_col_name[col]))
        print('|'.join(row_data))
        row_data = []


def display_table_rows(model_, rows):
    if not rows:
        print("No records found.")
        return

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


def query_and_display_stmt(db_session, q):
    cols, rs = execute_any_q_text(db_session, q)
    display_table_rows_given_columns(cols, rs)


def display_expense_categories(db_session, year):
    query_and_display_stmt(db_session.bind, f'''
        select budget_start_date, budget_end_date, income_expense, category, subcategory, id
        from expense_budget
        where true
        and budget_start_date = '{year}-01-01'
        and budget_end_date = '{year}-12-31'
        order by income_expense, category, subcategory
    ''')


def display_archery_risers(db_session):
    q = f'''
        select 
            r.id as riser_id, t.name as bow_type, m.name as manufacturer, r.name as riser_name, r.length_in, 
            r.rh_lh, r.letoff_pct
        from archery_riser r
        left join archery_manufacturer m on m.id = r.archery_manufacturer_id
        left join archery_bow_type t on t.id = r.archery_bow_type_id
        order by t.name, m.name, r.name
    '''
    query_and_display_stmt(db_session.bind, q)


def display_archery_limbs(db_session):
    q = f'''
        select 
            l.id as limb_id, m.name as manufacturer, l.name as limb, l.total_length_in, l.draw_weight_lb_min, 
            l.draw_weight_lb_max, t.name
        from archery_limb l
        left join archery_manufacturer m on m.id = l.archery_manufacturer_id
        left join archery_bow_type t on t.id = l.archery_bow_type_id
        order by t.name, m.name, l.total_length_in, l.draw_weight_lb_max
    '''
    query_and_display_stmt(db_session.bind, q)


def display_archery_ranges(db_session):
    q = f'''
        select 
            id, name, country_iso, address_province, address_city, address_street, outdoor
        from archery_range 
        order by country_iso, address_province, address_city, name
    '''
    query_and_display_stmt(db_session.bind, q)


def display_archery_arrows(db_session):
    q = f'''
        select 
            a.id as arrow_id, m.name as manufacturer, a.name as arrow, shaft_length_in, spine, size_mm, fletching
        from archery_arrow a
        left join archery_manufacturer m on a.archery_manufacturer_id = m.id
        order by m.name, fletching, shaft_length_in, size_mm, spine, a.name
    '''
    query_and_display_stmt(db_session.bind, q)


def display_archery_sights(db_session):
    q = f'''
        select 
            s.id as sight_id, m.name as manufacturer, s.name as sight, s.magnification
        from archery_sight s
        left join archery_manufacturer m on s.archery_manufacturer_id = m.id
        order by m.name, s.name, s.magnification
    '''
    query_and_display_stmt(db_session.bind, q)


def display_archery_targets(db_session):
    q = f'''
        select * from archery_target order by id
    '''
    query_and_display_stmt(db_session.bind, q)


def display_archery_arrow_rests(db_session):
    q = f'''
        select 
            r.id as rest_id, m.name as manufacturer, r.name as rest_name, r.description as rest_desc, r.arrow_rest_type
        from archery_arrow_rest r
        left join archery_manufacturer m on r.archery_manufacturer_id = m.id
        order by r.arrow_rest_type, m.name, r.name
    '''
    query_and_display_stmt(db_session.bind, q)


def display_archery_release_aids(db_session):
    q = f'''
        select 
            r.id as release_aid_id, m.name as manufacturer, r.name as release_aid_name
        from archery_release_aid r
        left join archery_manufacturer m on r.archery_manufacturer_id = m.id
        order by m.name, r.name
    '''
    query_and_display_stmt(db_session.bind, q)


def display_book_publishers(db_session):
    q = f'''
        select id, name, datetime_entered
        from book_publisher
        order by name collate "zh-Hans-CN-x-icu"
    '''
    query_and_display_stmt(db_session.bind, q)


def display_book_authors(db_session):
    q = f'''
        select id, last_name, first_name, middle_name, nationality, datetime_entered
        from book_author
        order by last_name collate "zh-Hans-CN-x-icu", first_name collate "zh-Hans-CN-x-icu";
    '''
    query_and_display_stmt(db_session.bind, q)


def display_book_translators(db_session):
    q = f'''
        select
            id, last_name, first_name, middle_name, datetime_entered
        from book_translator
        order by last_name collate "zh-Hans-CN-x-icu", first_name collate "zh-Hans-CN-x-icu";
    '''
    query_and_display_stmt(db_session.bind, q)


def display_book_editors(db_session):
    q = f'''
        select
            id, last_name, first_name, middle_name, datetime_entered
        from book_editor
        order by last_name collate "zh-Hans-CN-x-icu", first_name collate "zh-Hans-CN-x-icu";
    '''
    query_and_display_stmt(db_session.bind, q)


def display_book_language(db_session):
    q = f'''
        select
            id, name, code, datetime_entered
        from book_language
        order by name;
    '''
    query_and_display_stmt(db_session.bind, q)


def display_book_series(db_session):
    q = f'''
        select s.id as series_id, s.name as series_name, s.total_books, p.name as publisher_name, p.id as publisher_id
        from book_series s, book_publisher p
        where true
        and s.publisher_id = p.id
        order by p.name collate "zh-Hans-CN-x-icu"
    '''
    query_and_display_stmt(db_session.bind, q)


def display_book_format(db_session):
    q = f'''
        select * from book_format order by id
    '''
    query_and_display_stmt(db_session.bind, q)


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
    elif cmd_type == 'function':
        function_name = cmd_args[2]
        if function_name == 'expense_categories':
            year_int = int(cmd_args[3])
            display_expense_categories(postgres_session, year_int)
        elif function_name == 'display_archery_risers':
            display_archery_risers(postgres_session)
        elif function_name == 'display_archery_limbs':
            display_archery_limbs(postgres_session)
        elif function_name == 'display_archery_ranges':
            display_archery_ranges(postgres_session)
        elif function_name == 'display_archery_arrows':
            display_archery_arrows(postgres_session)
        elif function_name == 'display_archery_sights':
            display_archery_sights(postgres_session)
        elif function_name == 'display_archery_targets':
            display_archery_targets(postgres_session)
        elif function_name == 'display_archery_arrow_rests':
            display_archery_arrow_rests(postgres_session)
        elif function_name == 'display_archery_release_aids':
            display_archery_release_aids(postgres_session)
        elif function_name == 'display_book_publishers':
            display_book_publishers(postgres_session)
        elif function_name == 'display_book_authors':
            display_book_authors(postgres_session)
        elif function_name == 'display_book_translators':
            display_book_translators(postgres_session)
        elif function_name == 'display_book_editors':
            display_book_editors(postgres_session)
        elif function_name == 'display_book_language':
            display_book_language(postgres_session)
        elif function_name == 'display_book_series':
            display_book_series(postgres_session)
        elif function_name == 'display_book_format':
            display_book_format(postgres_session)
        else:
            raise NotImplementedError(f'{function_name} not implemented')
    else:
        raise NotImplementedError(f'{cmd_type} is not implemented')

    # r = execute_any_q_text(postgres_session.bind, 'select max(date) from archery_round')
    # print(r)
