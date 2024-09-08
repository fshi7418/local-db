from sqlalchemy import create_engine, null
from sqlalchemy.orm import sessionmaker
import pandas as pd
import datetime
import os
import json

from models.books import Library, Author, Publisher, Language

with open('../configs.json', 'rb') as f:
    configs = json.load(f)
f.close()
db_username = configs['database']['postgres']['username']
db_password = configs['database']['postgres']['password']
conn_string = f'postgresql://{db_username}:{db_password}@localhost/postgres'
engine = create_engine(conn_string)
Session = sessionmaker(bind=engine)
postgres_session = Session()

# read the file
doc_path = r'/home/franks/Documents/Random Projects/'
books_file = os.path.join(doc_path, 'owned books.xlsx')
library_df = pd.read_excel(books_file, sheet_name='library')
author_df = pd.read_excel(books_file, sheet_name='author')
publisher_df = pd.read_excel(books_file, sheet_name='publisher')
language_df = pd.read_excel(books_file, sheet_name='language')

# process


def string_to_list(s):
    if s is None:
        return s
    # Remove the square brackets and split the string by commas
    s = s.strip('[]')
    # Convert the split strings into integers and return as a list
    return [int(x) for x in s.split(',') if x]


def nan_to_none(n):
    if pd.isna(n):
        return None
    return n


def extract_isbn(s):
    # Check if the string starts with '=' and has quotes
    if s.startswith('=') and '"' in s:
        # Find the positions of the quotes
        start = s.find('"') + 1
        end = s.rfind('"')
        # Extract and return the content between the quotes
        if s[start:end] == '':
            return null()
        return s[start:end]
    return null()  # Return None if the format is incorrect


for i, r in library_df.iterrows():
    r_additional_authors = null()
    if nan_to_none(r['author_additional_id']) is not None:
        r_additional_authors = string_to_list(r['author_additional_id'])
    r_additional_translators = null()
    if nan_to_none(r['translator_additional_id']) is not None:
        r_additional_translators = string_to_list(r['translator_additional_id'])
    year_read = None
    month_read = None
    day_read = None
    date_read_str = nan_to_none(r['date_read'])
    if date_read_str is not None:
        date_read = datetime.datetime.strptime(date_read_str, '%Y/%m/%d')
        year_read = date_read.year
        month_read = date_read.month
        day_read = date_read.day
    new_d = dict(
        title_main=r['title_main'],
        title_secondary=nan_to_none(r['title_secondary']),
        author_id=r['author_id'],
        author_additional_id=r_additional_authors,
        composition_language_id=r['composition_language_id'],
        language1_id=r['language1_id'],
        language2_id=nan_to_none(r['language2_id']),
        language3_id=nan_to_none(r['language3_id']),
        translator_id=nan_to_none(r['translator_id']),
        translator_additional_id=r_additional_translators,
        num_volume=nan_to_none(r['num_volume']),
        series=nan_to_none(r['series']),
        volume_in_series=nan_to_none(r['volume_in_series']),
        isbn=extract_isbn(r['isbn']),
        publisher_id=r['publisher_id'],
        binding_id=r['binding_id'],
        num_pages=r['num_pages'],
        year_published=r['year_published'],
        year_published_original=nan_to_none(r['year_published_original']),
        year_read=year_read,
        month_read=month_read,
        day_read=day_read,
    )
    print(f'inserting row {i}')
    postgres_session.add(Library(**new_d))

postgres_session.commit()

