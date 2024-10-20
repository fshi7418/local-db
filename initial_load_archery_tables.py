import os
import pandas as pd
from sqlalchemy import null

from models import postgres_session
# Import the necessary models
from models.archery import ArcheryRange, ArcheryTarget, ArcheryBowType, ArcheryManufacturer, ArcheryLimb, \
    ArcheryRiser, ArcheryArrow, Shots, Ends, Rounds

# Delete data from all imported tables
tables_to_clear = [Shots, Ends, Rounds, ArcheryLimb, ArcheryRiser, ArcheryArrow,
                   ArcheryRange, ArcheryTarget, ArcheryBowType, ArcheryManufacturer]

for table in tables_to_clear:
    postgres_session.query(table).delete()

postgres_session.commit()
print("All data has been deleted from the imported tables.")

# import
print("Importing...")
doc_path = r'/home/franks/Documents/Archery'
archery_xlsx = os.path.join(doc_path, 'Scores.xlsx')

rounds = pd.read_excel(archery_xlsx, sheet_name='Rounds', parse_dates=['date'], dtype={'start_time': str, 'end_time': str})
ends = pd.read_excel(archery_xlsx, sheet_name='Ends')
shots = pd.read_excel(archery_xlsx, sheet_name='Shots')
# Read additional sheets from the Excel file
ranges = pd.read_excel(archery_xlsx, sheet_name='Ranges')
targets = pd.read_excel(archery_xlsx, sheet_name='Targets')
bow_types = pd.read_excel(archery_xlsx, sheet_name='Bow Types')
manufacturers = pd.read_excel(archery_xlsx, sheet_name='Manufacturers')
limbs = pd.read_excel(archery_xlsx, sheet_name='Limbs')
risers = pd.read_excel(archery_xlsx, sheet_name='Risers')
arrows = pd.read_excel(archery_xlsx, sheet_name='Arrows')


# Function to handle null values
def handle_null(value):
    return null() if pd.isna(value) else value


# Load data into static tables
for _, row in ranges.iterrows():
    postgres_session.add(ArcheryRange(**{k: handle_null(v) for k, v in row.to_dict().items()}))

for _, row in targets.iterrows():
    postgres_session.add(ArcheryTarget(**{k: handle_null(v) for k, v in row.to_dict().items()}))

for _, row in manufacturers.iterrows():
    postgres_session.add(ArcheryManufacturer(**{k: handle_null(v) for k, v in row.to_dict().items()}))

postgres_session.commit()

for _, row in bow_types.iterrows():
    postgres_session.add(ArcheryBowType(**{k: handle_null(v) for k, v in row.to_dict().items()}))

for _, row in limbs.iterrows():
    postgres_session.add(ArcheryLimb(**{k: handle_null(v) for k, v in row.to_dict().items()}))

for _, row in risers.iterrows():
    postgres_session.add(ArcheryRiser(**{k: handle_null(v) for k, v in row.to_dict().items()}))

for _, row in arrows.iterrows():
    postgres_session.add(ArcheryArrow(**{k: handle_null(v) for k, v in row.to_dict().items()}))

postgres_session.commit()

# Parse and load Rounds data
for _, row in rounds.iterrows():
    # Filter out columns that are outside the main dataframe
    valid_columns = [col for col in row.index if not pd.isna(row[col])]
    round_data = {col: handle_null(row[col]) for col in valid_columns if col in Rounds.__table__.columns.keys()}
    postgres_session.add(Rounds(**round_data))

# Parse and load Ends data
for _, row in ends.iterrows():
    # Filter out columns that are outside the main dataframe
    valid_columns = [col for col in row.index if not pd.isna(row[col])]
    end_data = {col: handle_null(row[col]) for col in valid_columns if col in Ends.__table__.columns.keys()}
    postgres_session.add(Ends(**end_data))

# Parse and load Shots data
for _, row in shots.iterrows():
    # Filter out columns that are outside the main dataframe
    valid_columns = [col for col in row.index if not pd.isna(row[col])]
    shot_data = {col: handle_null(row[col]) for col in valid_columns if col in Shots.__table__.columns.keys()}
    postgres_session.add(Shots(**shot_data))

postgres_session.commit()
