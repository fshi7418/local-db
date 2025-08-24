from sqlalchemy import Column, Integer, String, DateTime, Table, Date, SmallInteger
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

from models import Base, get_est_now_clean

# Association tables for many-to-many relationships
book_to_book_author = Table(
    'book_to_book_author',
    Base.metadata,
    Column('book_id', Integer, ForeignKey('book.id'), primary_key=True),
    Column('book_author_id', Integer, ForeignKey('book_author.id'), primary_key=True)
)

book_to_book_language = Table(
    'book_to_book_language',
    Base.metadata,
    Column('book_id', Integer, ForeignKey('book.id'), primary_key=True),
    Column('book_language_id', Integer, ForeignKey('book_language.id'), primary_key=True)
)

book_to_book_translator = Table(
    'book_to_book_translator',
    Base.metadata,
    Column('book_id', Integer, ForeignKey('book.id'), primary_key=True),
    Column('book_translator_id', Integer, ForeignKey('book_translator.id'), primary_key=True)
)

book_to_book_editor = Table(
    'book_to_book_editor',
    Base.metadata,
    Column('book_id', Integer, ForeignKey('book.id'), primary_key=True),
    Column('book_editor_id', Integer, ForeignKey('book_editor.id'), primary_key=True)
)


class BookFormat(Base):
    __tablename__ = 'book_format'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)


class BookAuthor(Base):
    __tablename__ = 'book_author'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100))
    middle_name = Column(String(100))
    birth_date = Column(Date)
    death_date = Column(Date)
    nationality = Column(String(100))

    datetime_entered = Column(DateTime, default=get_est_now_clean())

    # Relationships
    books = relationship('Book', secondary=book_to_book_author, back_populates='authors')

    def __repr__(self):
        return f"<BookAuthor(id={self.id}, name='{self.first_name} {self.last_name}')>"


class BookTranslator(Base):
    __tablename__ = 'book_translator'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100))
    middle_name = Column(String(100))

    datetime_entered = Column(DateTime, default=get_est_now_clean())

    # Relationships
    translated_books = relationship('Book', secondary=book_to_book_translator, back_populates='translators')

    def __repr__(self):
        return f"<BookTranslator(id={self.id}, name='{self.first_name} {self.last_name}')>"


class BookLanguage(Base):
    __tablename__ = 'book_language'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    code = Column(String(10), unique=True)  # ISO language code

    datetime_entered = Column(DateTime, default=get_est_now_clean())

    # Relationships
    books = relationship('Book', secondary=book_to_book_language, back_populates='languages')

    def __repr__(self):
        return f"<BookLanguage(id={self.id}, name='{self.name}')>"


class BookPublisher(Base):
    __tablename__ = 'book_publisher'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)

    datetime_entered = Column(DateTime, default=get_est_now_clean())

    def __repr__(self):
        return f"<BookPublisher(id={self.id}, name='{self.name}')>"


class BookSeries(Base):
    __tablename__ = 'book_series'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    total_books = Column(Integer)  # Total books planned in the series
    publisher_id = Column(Integer, ForeignKey('book_publisher.id'))

    datetime_entered = Column(DateTime, default=get_est_now_clean())

    # Relationships
    books = relationship('Book', back_populates='series')

    def __repr__(self):
        return f"<BookSeries(id={self.id}, name='{self.name}')>"


class BookEditor(Base):
    __tablename__ = 'book_editor'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100))
    middle_name = Column(String(100))

    datetime_entered = Column(DateTime, default=get_est_now_clean())

    # Relationships
    edited_books = relationship('Book', secondary=book_to_book_editor, back_populates='editors')

    def __repr__(self):
        return f"<BookEditor(id={self.id}, name='{self.first_name} {self.last_name}')>"


class Book(Base):
    __tablename__ = 'book'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(300), nullable=False)
    subtitle = Column(String(300))
    isbn = Column(String(20))
    isbn13 = Column(String(15))
    publication_year = Column(SmallInteger)
    publication_month = Column(SmallInteger)
    publication_day = Column(SmallInteger)
    page_count = Column(Integer)
    date_read = Column(Date)
    datetime_entered = Column(DateTime, default=get_est_now_clean())
    series_order = Column(Integer)  # Order in the series
    edition = Column(Integer)

    # Foreign keys
    publisher_id = Column(Integer, ForeignKey('book_publisher.id'))
    series_id = Column(Integer, ForeignKey('book_series.id'))
    format_id = Column(Integer, ForeignKey('book_format.id'))

    # Relationships
    authors = relationship('BookAuthor', secondary=book_to_book_author, back_populates='books')
    languages = relationship('BookLanguage', secondary=book_to_book_language, back_populates='books')
    translators = relationship('BookTranslator', secondary=book_to_book_translator, back_populates='translated_books')
    editors = relationship('BookEditor', secondary=book_to_book_editor, back_populates='edited_books')
    series = relationship('BookSeries', back_populates='books')

    def __repr__(self):
        return f"<Book(id={self.id}, title='{self.title}')>"
