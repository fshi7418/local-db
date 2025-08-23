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


def insert_book_author(first_name, last_name, middle_name, birth_date, death_date, nationality):
    author = BookAuthor(
        first_name=first_name,
        last_name=last_name,
        middle_name=middle_name,
        birth_date=birth_date,
        death_date=death_date,
        nationality=nationality
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
    if len(sys.argv) != 7:
        print("Usage: add_book_author.py <first_name> <last_name> <middle_name> <birth_date> <death_date> <nationality>")
        sys.exit(1)

    first_name = sys.argv[1]
    last_name = sys.argv[2] or None
    middle_name = sys.argv[3] or None
    birth_date = parse_date(sys.argv[4])
    death_date = parse_date(sys.argv[5])
    nationality = sys.argv[6] or None

    if not first_name:
        print("First name is required.")
        sys.exit(1)
    insert_book_author(first_name, last_name, middle_name, birth_date, death_date, nationality)
