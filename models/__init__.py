import json
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

with open('configs.json', 'rb') as config_file:
    configs = json.load(config_file)
# local_postgres = configs.get('database', dict()).get('postgres', dict())
local_postgres = configs.get('database', dict()).get('franks', dict())
username = local_postgres.get('username', '')
password = local_postgres.get('password', '')

Base = declarative_base()
conn_string = f'postgresql://{username}:{password}@localhost/franks'
engine = create_engine(conn_string)
Session = sessionmaker(bind=engine)

postgres_session = Session()

