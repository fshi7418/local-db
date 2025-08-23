import json
import pytz
import datetime as dt
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

db_name = 'postgres'

with open('configs.json', 'rb') as config_file:
    configs = json.load(config_file)
local_postgres = configs.get('database', dict()).get(db_name, dict())
username = local_postgres.get('username', '')
password = local_postgres.get('password', '')

conn_string = f'postgresql://{username}:{password}@localhost/{db_name}'
engine = create_engine(conn_string)
Session = sessionmaker(bind=engine)

postgres_session = Session()


# for data migration purposes
db_name2 = 'franks'

with open('configs.json', 'rb') as config_file:
    configs = json.load(config_file)
local_postgres2 = configs.get('database', dict()).get(db_name2, dict())
username2 = local_postgres.get('username', '')
password2 = local_postgres.get('password', '')

conn_string2 = f'postgresql://{username2}:{password2}@localhost/{db_name2}'
engine2 = create_engine(conn_string)
Session2 = sessionmaker(bind=engine)

postgres_session2 = Session2()


def get_est_now_clean():
    eastern = pytz.timezone('US/Eastern')
    eastern_time_aware = dt.datetime.now(eastern)
    eastern_time_naive = eastern_time_aware.replace(tzinfo=None)
    return eastern_time_naive
