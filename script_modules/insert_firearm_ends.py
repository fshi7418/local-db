import sys
import json
from models import postgres_session
from models.firearm import FirearmEnd, TrapRound, TrapShot


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
    try:
        for end in ends_data:
            end_obj = FirearmEnd(
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
            )
            postgres_session.add(end_obj)
            postgres_session.flush()

            trap_data = end.get('trap_round')
            if trap_data and isinstance(trap_data, dict):
                trap_round_obj = TrapRound(
                    firearm_end_id=end_obj.id,
                    distance_yard=float_or_none(trap_data.get('distance_yard')),
                    distance_m=float_or_none(trap_data.get('distance_m')),
                    discipline=str_or_none(trap_data.get('discipline')),
                    num_break=int_or_none(trap_data.get('num_break')),
                    starting_station=int_or_none(trap_data.get('starting_station')),
                    shotgun_choke_id=int_or_none(trap_data.get('shotgun_choke_id')),
                )
                postgres_session.add(trap_round_obj)
                postgres_session.flush()

                trap_shots = trap_data.get('trap_shots')
                if trap_shots and isinstance(trap_shots, list):
                    for shot in trap_shots:
                        postgres_session.add(TrapShot(
                            trap_round_id=trap_round_obj.id,
                            station=int(shot['station']),
                            num_break=int(shot['num_break']),
                        ))

        postgres_session.commit()
        print(f"Inserted {len(ends_data)} end(s) for visit {visit_id_}")
    except Exception as e:
        postgres_session.rollback()
        print(f"Error inserting end(s): {e}")
        sys.exit(1)


if __name__ == "__main__":
    insert_firearm_ends(
        visit_id_=sys.argv[1],
        ends_json_str=sys.argv[2],
    )
