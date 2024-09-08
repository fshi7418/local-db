from sqlalchemy import Column, Integer, String, SmallInteger, DateTime
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import ForeignKey

from models import Base


class Library(Base):
    __tablename__ = 'library'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title_main = Column(String)
    title_secondary = Column(String)
    author_id = Column(Integer, ForeignKey('author.id'), index=True)
    author_additional_id = Column(JSONB)
    composition_language_id = Column(Integer, ForeignKey('language.id'), index=True)
    language1_id = Column(Integer, ForeignKey('language.id'), index=True)
    language2_id = Column(Integer, ForeignKey('language.id'))
    language3_id = Column(Integer, ForeignKey('language.id'))
    translator_id = Column(Integer, ForeignKey('author.id'))
    translator_additional_id = Column(JSONB)
    num_volume = Column(SmallInteger)
    series = Column(String)
    volume_in_series = Column(SmallInteger)
    isbn = Column(String)
    publisher_id = Column(Integer, ForeignKey('publisher.id'))
    binding_id = Column(SmallInteger, ForeignKey('binding.id'))
    num_pages = Column(Integer)
    year_published = Column(SmallInteger)
    year_published_original = Column(SmallInteger)
    year_read = Column(SmallInteger)
    month_read = Column(SmallInteger)
    day_read = Column(SmallInteger)

    datetime_entered = Column(
        DateTime, default=func.now(), server_default=func.now()
    )
    last_updated = Column(
        DateTime, default=func.now(), onupdate=func.now(), server_default=func.now(),
        server_onupdate=func.now()
    )


class Author(Base):
    __tablename__ = 'author'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    last_name = Column(String)
    first_name = Column(String)
    datetime_entered = Column(
        DateTime, default=func.now(), server_default=func.now()
    )
    last_updated = Column(
        DateTime, default=func.now(), onupdate=func.now(), server_default=func.now(),
        server_onupdate=func.now()
    )


class Language(Base):
    __tablename__ = 'language'
    id = Column(Integer, primary_key=True, autoincrement=True)
    language = Column(String, nullable=False)
    datetime_entered = Column(
        DateTime, default=func.now(), server_default=func.now()
    )
    last_updated = Column(
        DateTime, default=func.now(), onupdate=func.now(), server_default=func.now(),
        server_onupdate=func.now()
    )


class Publisher(Base):
    __tablename__ = 'publisher'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    country = Column(String)
    city = Column(String)
    datetime_entered = Column(
        DateTime, default=func.now(), server_default=func.now()
    )
    last_updated = Column(
        DateTime, default=func.now(), onupdate=func.now(), server_default=func.now(),
        server_onupdate=func.now()
    )


class Binding(Base):
    __tablename__ = 'binding'
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String, nullable=False)
