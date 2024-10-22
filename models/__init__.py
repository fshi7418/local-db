import json
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db_name = 'postgres'

with open('configs.json', 'rb') as config_file:
    configs = json.load(config_file)
local_postgres = configs.get('database', dict()).get(db_name, dict())
username = local_postgres.get('username', '')
password = local_postgres.get('password', '')

Base = declarative_base()
conn_string = f'postgresql://{username}:{password}@localhost/{db_name}'
engine = create_engine(conn_string)
Session = sessionmaker(bind=engine)

postgres_session = Session()

