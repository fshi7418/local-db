import os
import pandas as pd
from sqlalchemy import null

from models import postgres_session
from models.archery_scores import Rounds, Ends, Shots

doc_path = r'/home/franks/Documents/Archery'
archery_xlsx = os.path.join(doc_path, 'Scores.xlsx')

rounds = pd.read_excel(archery_xlsx, sheet_name='Rounds', parse_dates=['date'])
ends = pd.read_excel(archery_xlsx, sheet_name='Ends')
shots = pd.read_excel(archery_xlsx, sheet_name='Shots')

rounds_counter = 0
for r, r_dict in rounds.iterrows():
    r_id = r_dict['id']
    r_ends_df = ends.loc[ends['rounds_id'] == r_id, ]
    r_ends = []
    for rr, rr_dict in r_ends_df.iterrows():
        rr_id = rr_dict['id']
        rr_shots_df = shots.loc[shots['ends_id'] == rr_id]
        rr_shots = []
        for rrr, rrr_dict in rr_shots_df.iterrows():
            rrr_dict_actual = dict(rrr_dict)
            if pd.isna(rrr_dict_actual['is_x']):
                rrr_dict_actual['is_x'] = None
            rr_shots.append(Shots(
                **rrr_dict_actual
            ))
        r_ends.append(Ends(
            id=rr_dict['id'],
            rounds_id=r_id,
            end=rr_dict['end'],
            score_total=rr_dict['score_total'],
            num_shots=rr_dict['num_shots'],
            shots_ordered=rr_dict['shots_ordered'],
            shots=rr_shots
        ))
    postgres_session.add(Rounds(
        id=r_id,
        round_date=r_dict['date'].date(),
        distance_m=r_dict['distance_m'],
        target_size_cm=r_dict['target_size_cm'],
        sight=r_dict['sight'],
        clicker=r_dict['clicker'],
        stabliser=r_dict['stabliser'],
        bow=r_dict['bow'],
        arrow_stiffness=null() if pd.isna(r_dict['arrow_stiffness']) else r_dict['arrow_stiffness'],
        bow_weight_lb=r_dict['bow_weight_lb'],
        bow_length_in=r_dict['bow_length_in'],
        total_score=r_dict['total_score'],
        num_x=r_dict['num_x'],
        num_10=r_dict['num_10'],
        num_9=r_dict['num_9'],
        stdev_ends=r_dict['stdev_ends'],
        stdev_shots=r_dict['stdev_shots'],
        num_shots=r_dict['num_shots'],
        location=r_dict['location'],
        mental_status=r_dict['mental_status'],
        conditions=r_dict['conditions'],
        hunger=r_dict['hunger'],
        days_since_last_practice=r_dict['days_since_last_practice'],
        ends=r_ends,
    ))
    rounds_counter += 1

print(f'logging {rounds_counter} rounds')
postgres_session.commit()
