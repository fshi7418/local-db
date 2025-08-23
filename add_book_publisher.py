import sys
from models import postgres_session
from models.books import BookPublisher

def insert_book_publisher(name):
    publisher = BookPublisher(
        name=name
    )

    try:
        postgres_session.add(publisher)
        postgres_session.commit()
        print(f"Inserted BookPublisher: {publisher}")
    except Exception as e:
        postgres_session.rollback()
        print(f"Error inserting BookPublisher: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: add_book_publisher.py <publisher_name>")
        sys.exit(1)

    name = sys.argv[1]

    if not name:
        print("Publisher name is required.")
        sys.exit(1)
    insert_book_publisher(name)
