import sys
import json
from models import postgres_session
from models.firearm import FirearmEnd


def int_or_none(val):
    if val is None or val == '':
        return None
    return int(val)


def float_or_none(val):
    if val is None or val == '':
        return None
    return float(val)


def str_or_none(val):
    if val is None or val == '':
        return None
    return val


def insert_firearm_ends(visit_id_, ends_json_str):
    ends_data = json.loads(ends_json_str)
    end_objects = []
    for end in ends_data:
        end_objects.append(FirearmEnd(
            firearm_visit_id=int(visit_id_),
            firearm_model_id=int_or_none(end.get('firearm_model_id')),
            firearm_cartridge_id=int_or_none(end.get('firearm_cartridge_id')),
            firearm_ammunition_id=int_or_none(end.get('firearm_ammunition_id')),
            quantity=int_or_none(end.get('quantity')),
            distance_m=float_or_none(end.get('distance_m')),
            firearm_target_id=int_or_none(end.get('firearm_target_id')),
            shots_scored=int_or_none(end.get('shots_scored')),
            points_of_stabilisation=int_or_none(end.get('points_of_stabilisation')),
            supporting_hands=int_or_none(end.get('supporting_hands')),
            firearm_sight_id=int_or_none(end.get('firearm_sight_id')),
            stance=str_or_none(end.get('stance')),
        ))
    try:
        postgres_session.add_all(end_objects)
        postgres_session.commit()
        print(f"Inserted {len(end_objects)} end(s) for visit {visit_id_}")
    except Exception as e:
        postgres_session.rollback()
        print(f"Error inserting FirearmEnd(s): {e}")
        sys.exit(1)


if __name__ == "__main__":
    insert_firearm_ends(
        visit_id_=sys.argv[1],
        ends_json_str=sys.argv[2],
    )
