import sys
from models import postgres_session
from models.firearm import FirearmVisit


def insert_firearm_visit(visit_date_, firearm_range_id_, time_start_, time_end_):
    visit = FirearmVisit(
        visit_date=visit_date_,
        firearm_range_id=int(firearm_range_id_),
        time_start=time_start_ or None,
        time_end=time_end_ or None,
    )

    try:
        postgres_session.add(visit)
        postgres_session.commit()
        print(visit.id)
    except Exception as e:
        postgres_session.rollback()
        print(f"Error inserting FirearmVisit: {e}")
        sys.exit(1)


if __name__ == "__main__":
    insert_firearm_visit(
        visit_date_=sys.argv[1],
        firearm_range_id_=sys.argv[2],
        time_start_=sys.argv[3] if len(sys.argv) > 3 else None,
        time_end_=sys.argv[4] if len(sys.argv) > 4 else None,
    )
