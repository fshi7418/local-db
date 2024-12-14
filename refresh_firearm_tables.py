import os
import pandas as pd
from sqlalchemy import null

from models import postgres_session
# Import the necessary models
from models.firearm import FirearmTrade, FirearmManufacturer, FirearmModel, FirearmAction, FirearmRestriction, \
    FirearmCartridge, FirearmDealer, FirearmVisit, FirearmEnd, FirearmShot, FirearmRange, FirearmTarget, FirearmSight, \
    FirearmAmmunition

# Delete data from all imported tables
tables_to_clear = [
    FirearmVisit, FirearmEnd, FirearmShot, FirearmTrade, FirearmModel, FirearmSight, FirearmAmmunition,
    FirearmManufacturer, FirearmAction, FirearmRestriction, FirearmCartridge, FirearmDealer, FirearmRange, FirearmTarget
]

for table in tables_to_clear:
    postgres_session.query(table).delete()

postgres_session.commit()
print("All data has been deleted from the imported tables.")

# import
print("Importing...")
doc_path = r'/home/franks/Documents/Firearms'
firearm_ods = os.path.join(doc_path, 'Data.ods')

firearm_manufacturer = pd.read_excel(
    firearm_ods, sheet_name='manufacturer', dtype={'phone': str, 'postal_code': str}, engine='odf'
)
firearm_model = pd.read_excel(firearm_ods, sheet_name='model', engine='odf')
firearm_sight = pd.read_excel(firearm_ods, sheet_name='sight', engine='odf')
firearm_ammunition = pd.read_excel(firearm_ods, sheet_name='ammunition', engine='odf')
firearm_action = pd.read_excel(firearm_ods, sheet_name='action', engine='odf')
firearm_restriction = pd.read_excel(firearm_ods, sheet_name='restriction', engine='odf')
firearm_cartridge = pd.read_excel(firearm_ods, sheet_name='cartridge', engine='odf')
firearm_dealer = pd.read_excel(firearm_ods, sheet_name='dealer', engine='odf', dtype={'postal_code': str})
firearm_range = pd.read_excel(firearm_ods, sheet_name='range', engine='odf', dtype={'postal_code': str})
firearm_target = pd.read_excel(firearm_ods, sheet_name='target', engine='odf')

firearm_trade = pd.read_excel(firearm_ods, sheet_name='trade', engine='odf')
firearm_visit = pd.read_excel(
    firearm_ods, sheet_name='visit', engine='odf', dtype={
        'time_start': str, 'time_end': str
    }
)
firearm_end = pd.read_excel(firearm_ods, sheet_name='end', engine='odf')
firearm_shot = pd.read_excel(firearm_ods, sheet_name='shot', engine='odf')


# Function to handle null values
def handle_null(value):
    return null() if pd.isna(value) else value


# Load data into static tables
for _, row in firearm_manufacturer.iterrows():
    postgres_session.add(FirearmManufacturer(**{k: handle_null(v) for k, v in row.to_dict().items()}))

for _, row in firearm_dealer.iterrows():
    postgres_session.add(FirearmDealer(**{k: handle_null(v) for k, v in row.to_dict().items()}))

for _, row in firearm_action.iterrows():
    postgres_session.add(FirearmAction(**{k: handle_null(v) for k, v in row.to_dict().items()}))

for _, row in firearm_cartridge.iterrows():
    postgres_session.add(FirearmCartridge(**{k: handle_null(v) for k, v in row.to_dict().items()}))

for _, row in firearm_restriction.iterrows():
    postgres_session.add(FirearmRestriction(**{k: handle_null(v) for k, v in row.to_dict().items()}))

for _, row in firearm_range.iterrows():
    postgres_session.add(FirearmRange(**{k: handle_null(v) for k, v in row.to_dict().items()}))

for _, row in firearm_target.iterrows():
    postgres_session.add(FirearmTarget(**{k: handle_null(v) for k, v in row.to_dict().items()}))

postgres_session.commit()

for _, row in firearm_model.iterrows():
    postgres_session.add(FirearmModel(**{k: handle_null(v) for k, v in row.to_dict().items()}))
for _, row in firearm_sight.iterrows():
    postgres_session.add(FirearmSight(**{k: handle_null(v) for k, v in row.to_dict().items()}))
for _, row in firearm_ammunition.iterrows():
    postgres_session.add(FirearmAmmunition(**{k: handle_null(v) for k, v in row.to_dict().items()}))

postgres_session.commit()

for _, row in firearm_trade.iterrows():
    postgres_session.add(FirearmTrade(**{k: handle_null(v) for k, v in row.to_dict().items()}))

for _, row in firearm_visit.iterrows():
    postgres_session.add(FirearmVisit(**{k: handle_null(v) for k, v in row.to_dict().items()}))

for _, row in firearm_end.iterrows():
    postgres_session.add(FirearmEnd(**{k: handle_null(v) for k, v in row.to_dict().items()}))

for _, row in firearm_shot.iterrows():
    postgres_session.add(FirearmShot(**{k: handle_null(v) for k, v in row.to_dict().items()}))

postgres_session.commit()
