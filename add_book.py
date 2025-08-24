import sys
from models import postgres_session
from models.books import Book, BookAuthor, BookLanguage, BookTranslator, BookEditor
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


def parse_ids(id_str):
    if not id_str:
        return []
    return [int(i) for i in id_str.split(",") if i.strip()]


def insert_book(
    title, subtitle, isbn, isbn13, publication_date, page_count, date_read, series_order,
    publisher_id, series_id, format_id, author_ids, language_ids, translator_ids, editor_ids,
    edition
):
    # Build the Book object
    book = Book(
        title=title,
        subtitle=subtitle or None,
        isbn=isbn or None,
        isbn13=isbn13 or None,
        publication_date=parse_date(publication_date),
        page_count=parse_int(page_count),
        date_read=parse_date(date_read),
        series_order=parse_int(series_order),
        edition=parse_int(edition),
        publisher_id=parse_int(publisher_id),
        series_id=parse_int(series_id),
        format_id=parse_int(format_id)
    )

    # Add many-to-many relationships
    if author_ids:
        book.authors = postgres_session.query(BookAuthor).filter(BookAuthor.id.in_(author_ids)).all()
    if language_ids:
        book.languages = postgres_session.query(BookLanguage).filter(BookLanguage.id.in_(language_ids)).all()
    if translator_ids:
        book.translators = postgres_session.query(BookTranslator).filter(BookTranslator.id.in_(translator_ids)).all()
    if editor_ids:
        book.editors = postgres_session.query(BookEditor).filter(BookEditor.id.in_(editor_ids)).all()

    try:
        postgres_session.add(book)
        postgres_session.commit()
        print(f"Inserted Book: {book}")
    except Exception as e:
        postgres_session.rollback()
        print(f"Error inserting Book: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 17:
        print("insert failed， arguments:")
        print(sys.argv)
        print("Usage: add_book.py <title> <subtitle> <isbn> <isbn13> <publication_date> <page_count> <date_read> <series_order> <publisher_id> <series_id> <format_id> <author_ids> <language_ids> <translator_ids> <editor_ids> <edition>")
        sys.exit(1)

    title = sys.argv[1]
    subtitle = sys.argv[2]
    isbn = sys.argv[3]
    isbn13 = sys.argv[4]
    publication_date = sys.argv[5]
    page_count = sys.argv[6]
    date_read = sys.argv[7]
    series_order = sys.argv[8]
    publisher_id = sys.argv[9]
    series_id = sys.argv[10]
    format_id = sys.argv[11]
    author_ids = parse_ids(sys.argv[12])
    language_ids = parse_ids(sys.argv[13])
    translator_ids = parse_ids(sys.argv[14])
    editor_ids = parse_ids(sys.argv[15])
    edition = sys.argv[16]

    if not title:
        print("Title is required.")
        sys.exit(1)
    if not author_ids:
        print("At least one author ID is required.")
        sys.exit(1)
    if not language_ids:
        print("At least one language ID is required.")
        sys.exit(1)

    insert_book(
        title, subtitle, isbn, isbn13, publication_date, page_count, date_read, series_order,
        publisher_id, series_id, format_id, author_ids, language_ids, translator_ids, editor_ids,
        edition
    )
