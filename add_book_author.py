import sys
from models import postgres_session
from models.books import BookAuthor
from datetime import datetime


def parse_date(date_str):
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        print(f"Invalid date format: {date_str}. Expected YYYY-MM-DD.")
        sys.exit(1)


def parse_int(val):
    if not val:
        return None
    try:
        return int(val)
    except ValueError:
        print(f"Invalid integer: {val}")
        sys.exit(1)


def insert_book_author(
    first_name_, last_name_, middle_name_, birth_year_, birth_month_, birth_day_,
    death_year_, death_month_, death_day_, nationality_
):
    author = BookAuthor(
        first_name=first_name_,
        last_name=last_name_,
        middle_name=middle_name_,
        birthday_year=birth_year_,
        birthday_month=birth_month_,
        birthday_day=birth_day_,
        death_date_year=death_year_,
        death_date_month=death_month_,
        death_date_day=death_day_,
        nationality=nationality_
    )

    try:
        postgres_session.add(author)
        postgres_session.commit()
        print(f"Inserted BookAuthor: {author}")
    except Exception as e:
        postgres_session.rollback()
        print(f"Error inserting BookAuthor: {e}")
        sys.exit(1)


if __name__ == "__main__":
    first_name = sys.argv[1]
    last_name = sys.argv[2] or None
    middle_name = sys.argv[3] or None
    birth_year = parse_int(sys.argv[4])
    birth_month = parse_int(sys.argv[5])
    birth_day = parse_int(sys.argv[6])
    death_year = parse_int(sys.argv[7])
    death_month = parse_int(sys.argv[8])
    death_day = parse_int(sys.argv[9])
    nationality = sys.argv[10] or None

    if not first_name:
        print("First name is required.")
        sys.exit(1)
    insert_book_author(
        first_name, last_name, middle_name,
        birth_year, birth_month, birth_day,
        death_year, death_month, death_day,
        nationality
    )
