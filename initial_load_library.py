from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd
import os
import json

from models.transactions import ExpenseTransactions
from models.credentials import Credentials

with open('configs.json', 'rb') as f:
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
books_df = pd.read_excel(books_file)

# process


for i, r in books_df.iterrows():
    r_extra_info = r['extra_info']
    if pd.isna(r_extra_info):
        r_extra_info = None
    if r_extra_info and r_extra_info.lower() in ['nan', 'null']:
        r_extra_info = None
    if r_extra_info is not None:
        r_extra_info = json.loads(r_extra_info)

    r_notes = r['notes']
    if pd.isna(r_notes):
        r_notes = None
    new_expense = dict(
        name=r['name'],
        login=r['login'],
        password=r['password'],
        website=r['website'],
        category=r['category'],
        importance=r['importance'],
        extra_info=r_extra_info,
        last_updated=r['last_updated'],
        notes=r_notes
    )
    print(f'inserting row {i}')
    postgres_session.add(Credentials(**new_expense))

postgres_session.commit()

