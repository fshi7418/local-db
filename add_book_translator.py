import sys
from models import postgres_session
from models.books import BookTranslator


def insert_book_translator(first_name, last_name, middle_name):
    translator = BookTranslator(
        first_name=first_name,
        last_name=last_name,
        middle_name=middle_name
    )

    try:
        postgres_session.add(translator)
        postgres_session.commit()
        print(f"Inserted BookTranslator: {translator}")
    except Exception as e:
        postgres_session.rollback()
        print(f"Error inserting BookTranslator: {e}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: add_book_translator.py <first_name> <last_name> <middle_name>")
        sys.exit(1)

    first_name = sys.argv[1]
    last_name = sys.argv[2] or None
    middle_name = sys.argv[3] or None

    if not first_name:
        print("First name is required.")
        sys.exit(1)
    insert_book_translator(first_name, last_name, middle_name)
