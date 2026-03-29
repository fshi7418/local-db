import sys
from models import postgres_session
from models.firearm import FirearmSight


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


def insert_firearm_sight(name_, type_, firearm_manufacturer_id_, max_magnification_):
    sight = FirearmSight(
        name=name_,
        type=type_ or None,
        firearm_manufacturer_id=firearm_manufacturer_id_,
        max_magnification=max_magnification_,
    )

    try:
        postgres_session.add(sight)
        postgres_session.commit()
        print(f"Inserted FirearmSight: {sight.id} - {sight.name}")
    except Exception as e:
        postgres_session.rollback()
        print(f"Error inserting FirearmSight: {e}")
        sys.exit(1)


if __name__ == "__main__":
    args = sys.argv

    if len(args) < 2 or not args[1]:
        print("Sight name is required.")
        sys.exit(1)

    insert_firearm_sight(
        name_=args[1],
        type_=args[2] if len(args) > 2 else None,
        firearm_manufacturer_id_=parse_int(args[3] if len(args) > 3 else None),
        max_magnification_=parse_float(args[4] if len(args) > 4 else None),
    )
