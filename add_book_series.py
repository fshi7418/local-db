import sys
from models import postgres_session, get_est_now_clean
from models.books import BookSeries


def parse_int(val):
    if not val:
        return None
    try:
        return int(val)
    except ValueError:
        print(f"Invalid integer: {val}")
        sys.exit(1)


def insert_book_series(name_, total_books_, publisher_id_):
    series = BookSeries(
        name=name_, total_books=total_books_, publisher_id=publisher_id_, datetime_entered=get_est_now_clean()
    )

    try:
        postgres_session.add(series)
        postgres_session.commit()
        print(f"Inserted BookSeries: {series}")
    except Exception as e:
        postgres_session.rollback()
        print(f"Error inserting BookSeries: {e}")
        sys.exit(1)


if __name__ == "__main__":
    name = sys.argv[1]
    total_books = parse_int(sys.argv[2])
    publisher_id = parse_int(sys.argv[3])

    if not name:
        print("Publisher name is required.")
        sys.exit(1)
    insert_book_series(name, total_books, publisher_id)
