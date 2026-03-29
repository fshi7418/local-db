import sys
from models import postgres_session
from models.books import BookEditor

def insert_book_editor(first_name, last_name, middle_name):
    editor = BookEditor(
        first_name=first_name,
        last_name=last_name or None,
        middle_name=middle_name or None
    )

    try:
        postgres_session.add(editor)
        postgres_session.commit()
        print(f"Inserted BookEditor: {editor}")
    except Exception as e:
        postgres_session.rollback()
        print(f"Error inserting BookEditor: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: add_book_editor.py <first_name> <last_name> <middle_name>")
        sys.exit(1)

    first_name = sys.argv[1]
    last_name = sys.argv[2]
    middle_name = sys.argv[3]

    if not first_name:
        print("First name is required.")
        sys.exit(1)
    insert_book_editor(first_name, last_name, middle_name)
