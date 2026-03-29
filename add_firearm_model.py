import sys
from models import postgres_session
from models.firearm import FirearmModel


def parse_int(val):
    if not val:
        return None
    try:
        return int(val)
    except ValueError:
        print(f"Invalid integer: {val}")
        sys.exit(1)


def parse_float(val):
    if not val:
        return None
    try:
        return float(val)
    except ValueError:
        print(f"Invalid float: {val}")
        sys.exit(1)


def parse_bool(val):
    if not val:
        return None
    return val.strip().lower() in ('1', 'true', 'yes', 'y')


def insert_firearm_model(
    firearm_manufacturer_id_, name_, firearm_action_id_, firearm_restriction_id_,
    firearm_cartridge_id1_, barrel_length_in_, barrel_length_cm_, country_iso_origin_,
    weight_lb_, weight_kg_, rear_sight_, front_sight_, capacity1_,
    firearm_cartridge_id2_, capacity2_, firearm_cartridge_id3_, capacity3_,
    firearm_cartridge_id4_, capacity4_, firearm_cartridge_id5_, capacity5_,
    firearm_cartridge_id6_, capacity6_, firearm_cartridge_id7_, capacity7_,
):
    model = FirearmModel(
        firearm_manufacturer_id=firearm_manufacturer_id_,
        name=name_,
        firearm_action_id=firearm_action_id_,
        firearm_restriction_id=firearm_restriction_id_,
        firearm_cartridge_id1=firearm_cartridge_id1_,
        barrel_length_in=barrel_length_in_,
        barrel_length_cm=barrel_length_cm_,
        country_iso_origin=country_iso_origin_ or None,
        weight_lb=weight_lb_,
        weight_kg=weight_kg_,
        rear_sight=rear_sight_,
        front_sight=front_sight_,
        capacity1=capacity1_,
        firearm_cartridge_id2=firearm_cartridge_id2_,
        capacity2=capacity2_,
        firearm_cartridge_id3=firearm_cartridge_id3_,
        capacity3=capacity3_,
        firearm_cartridge_id4=firearm_cartridge_id4_,
        capacity4=capacity4_,
        firearm_cartridge_id5=firearm_cartridge_id5_,
        capacity5=capacity5_,
        firearm_cartridge_id6=firearm_cartridge_id6_,
        capacity6=capacity6_,
        firearm_cartridge_id7=firearm_cartridge_id7_,
        capacity7=capacity7_,
    )

    try:
        postgres_session.add(model)
        postgres_session.commit()
        print(f"Inserted FirearmModel: {model.id} - {model.name}")
    except Exception as e:
        postgres_session.rollback()
        print(f"Error inserting FirearmModel: {e}")
        sys.exit(1)


if __name__ == "__main__":
    args = sys.argv

    if len(args) < 6:
        print("Usage: add_firearm_model.py <name> <manufacturer_id> <action_id> <restriction_id> <cartridge_id1> ...")
        sys.exit(1)

    insert_firearm_model(
        name_=args[1],
        firearm_manufacturer_id_=parse_int(args[2]),
        firearm_action_id_=parse_int(args[3]),
        firearm_restriction_id_=parse_int(args[4]),
        firearm_cartridge_id1_=parse_int(args[5]),
        barrel_length_in_=parse_float(args[6] if len(args) > 6 else None),
        barrel_length_cm_=parse_float(args[7] if len(args) > 7 else None),
        country_iso_origin_=args[8] if len(args) > 8 else None,
        weight_lb_=parse_float(args[9] if len(args) > 9 else None),
        weight_kg_=parse_float(args[10] if len(args) > 10 else None),
        rear_sight_=parse_bool(args[11] if len(args) > 11 else None),
        front_sight_=parse_bool(args[12] if len(args) > 12 else None),
        capacity1_=parse_int(args[13] if len(args) > 13 else None),
        firearm_cartridge_id2_=parse_int(args[14] if len(args) > 14 else None),
        capacity2_=parse_int(args[15] if len(args) > 15 else None),
        firearm_cartridge_id3_=parse_int(args[16] if len(args) > 16 else None),
        capacity3_=parse_int(args[17] if len(args) > 17 else None),
        firearm_cartridge_id4_=parse_int(args[18] if len(args) > 18 else None),
        capacity4_=parse_int(args[19] if len(args) > 19 else None),
        firearm_cartridge_id5_=parse_int(args[20] if len(args) > 20 else None),
        capacity5_=parse_int(args[21] if len(args) > 21 else None),
        firearm_cartridge_id6_=parse_int(args[22] if len(args) > 22 else None),
        capacity6_=parse_int(args[23] if len(args) > 23 else None),
        firearm_cartridge_id7_=parse_int(args[24] if len(args) > 24 else None),
        capacity7_=parse_int(args[25] if len(args) > 25 else None),
    )
