import sys
from models import postgres_session
from models.firearm import FirearmManufacturer


def insert_firearm_manufacturer(
    name_, country_iso_, address_street_, address_city_, address_province_,
    address_country_, postal_code_, website_, phone_, phone_country_code_
):
    manufacturer = FirearmManufacturer(
        name=name_,
        country_iso=country_iso_ or None,
        address_street=address_street_ or None,
        address_city=address_city_ or None,
        address_province=address_province_ or None,
        address_country=address_country_ or None,
        postal_code=postal_code_ or None,
        website=website_ or None,
        phone=phone_ or None,
        phone_country_code=phone_country_code_ or None,
    )

    try:
        postgres_session.add(manufacturer)
        postgres_session.commit()
        print(f"Inserted FirearmManufacturer: {manufacturer.id} - {manufacturer.name}")
    except Exception as e:
        postgres_session.rollback()
        print(f"Error inserting FirearmManufacturer: {e}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2 or not sys.argv[1]:
        print("Manufacturer name is required.")
        sys.exit(1)

    insert_firearm_manufacturer(
        name_=sys.argv[1],
        country_iso_=sys.argv[2] if len(sys.argv) > 2 else None,
        address_street_=sys.argv[3] if len(sys.argv) > 3 else None,
        address_city_=sys.argv[4] if len(sys.argv) > 4 else None,
        address_province_=sys.argv[5] if len(sys.argv) > 5 else None,
        address_country_=sys.argv[6] if len(sys.argv) > 6 else None,
        postal_code_=sys.argv[7] if len(sys.argv) > 7 else None,
        website_=sys.argv[8] if len(sys.argv) > 8 else None,
        phone_=sys.argv[9] if len(sys.argv) > 9 else None,
        phone_country_code_=sys.argv[10] if len(sys.argv) > 10 else None,
    )
