#!/bin/bash
# shellcheck source=/dev/null
source ~/Environments/personal1/bin/activate
cd ~/Repos/local-db || exit

# --- Unit Conversion Helpers ---
# parse_length <input> -> sets barrel_length_in and barrel_length_cm
function parse_length() {
    local raw="$1"
    if [[ -z "$raw" ]]; then
        barrel_length_in=""
        barrel_length_cm=""
    elif [[ "$raw" =~ ^([0-9]+\.?[0-9]*)in$ ]]; then
        barrel_length_in="${BASH_REMATCH[1]}"
        barrel_length_cm=$(echo "scale=4; ${BASH_REMATCH[1]} * 2.54" | bc)
    elif [[ "$raw" =~ ^([0-9]+\.?[0-9]*)cm$ ]]; then
        barrel_length_cm="${BASH_REMATCH[1]}"
        barrel_length_in=$(echo "scale=4; ${BASH_REMATCH[1]} / 2.54" | bc)
    else
        echo "Invalid barrel length format. Use e.g. '29.5in' or '74.9cm'."
        exit 1
    fi
}

# parse_weight <input> -> sets weight_lb and weight_kg
function parse_weight() {
    local raw="$1"
    if [[ -z "$raw" ]]; then
        weight_lb=""
        weight_kg=""
    elif [[ "$raw" =~ ^([0-9]+\.?[0-9]*)lb$ ]]; then
        weight_lb="${BASH_REMATCH[1]}"
        weight_kg=$(echo "scale=4; ${BASH_REMATCH[1]} * 0.453592" | bc)
    elif [[ "$raw" =~ ^([0-9]+\.?[0-9]*)oz$ ]]; then
        weight_lb=$(echo "scale=4; ${BASH_REMATCH[1]} / 16" | bc)
        weight_kg=$(echo "scale=4; ${BASH_REMATCH[1]} * 0.0283495" | bc)
    elif [[ "$raw" =~ ^([0-9]+\.?[0-9]*)kg$ ]]; then
        weight_kg="${BASH_REMATCH[1]}"
        weight_lb=$(echo "scale=4; ${BASH_REMATCH[1]} / 0.453592" | bc)
    else
        echo "Invalid weight format. Use e.g. '7.5lb', '120.5oz', or '3.4kg'."
        exit 1
    fi
}

# --- Insert Firearm Manufacturer ---
function insert_firearm_manufacturer() {
    echo "Insert a new Firearm Manufacturer"
    read -p "Name: " name
    read -p "Country ISO (optional, 2-letter code): " country_iso
    read -p "Address street (optional): " address_street
    read -p "Address city (optional): " address_city
    read -p "Address province (optional): " address_province
    read -p "Address country (optional, 2-letter code): " address_country
    read -p "Postal code (optional): " postal_code
    read -p "Website (optional): " website
    read -p "Phone (optional): " phone
    read -p "Phone country code (optional): " phone_country_code

    python3 script_modules/add_firearm_manufacturer.py \
        "$name" "$country_iso" "$address_street" "$address_city" "$address_province" \
        "$address_country" "$postal_code" "$website" "$phone" "$phone_country_code"
}

# --- Insert Firearm Model ---
function insert_firearm_model() {
    echo "Insert a new Firearm Model"

    echo "Choose a Manufacturer:"
    python3 utilities.py function display_firearm_manufacturers
    read -p "Manufacturer ID: " manufacturer_id

    echo "Choose an Action:"
    python3 utilities.py function display_firearm_actions
    read -p "Action ID: " action_id

    echo "Choose a Restriction:"
    python3 utilities.py function display_firearm_restrictions
    read -p "Restriction ID: " restriction_id

    echo "Choose primary cartridge:"
    python3 utilities.py function display_firearm_cartridges
    read -p "Cartridge ID 1: " cartridge_id1

    read -p "Model name: " name
    read -p "Barrel length (e.g. '29.5in' or '74.9cm', optional): " barrel_length_raw
    parse_length "$barrel_length_raw"

    read -p "Country of origin ISO (optional, 2-letter code): " country_iso_origin

    read -p "Weight (e.g. '7.5lb', '120.5oz', or '3.4kg', optional): " weight_raw
    parse_weight "$weight_raw"

    read -p "Has rear sight? (true/false, optional): " rear_sight
    read -p "Has front sight? (true/false, optional): " front_sight
    read -p "Capacity 1 (optional): " capacity1

    echo "Additional cartridges (optional, press Enter to skip each):"
    python3 utilities.py function display_firearm_cartridges
    read -p "Cartridge ID 2 (optional): " cartridge_id2
    read -p "Capacity 2 (optional): " capacity2
    if [[ -n "$cartridge_id2" ]]; then
        python3 utilities.py function display_firearm_cartridges
        read -p "Cartridge ID 3 (optional): " cartridge_id3
        read -p "Capacity 3 (optional): " capacity3
    fi
    if [[ -n "$cartridge_id3" ]]; then
        python3 utilities.py function display_firearm_cartridges
        read -p "Cartridge ID 4 (optional): " cartridge_id4
        read -p "Capacity 4 (optional): " capacity4
    fi
    if [[ -n "$cartridge_id4" ]]; then
        python3 utilities.py function display_firearm_cartridges
        read -p "Cartridge ID 5 (optional): " cartridge_id5
        read -p "Capacity 5 (optional): " capacity5
    fi
    if [[ -n "$cartridge_id5" ]]; then
        python3 utilities.py function display_firearm_cartridges
        read -p "Cartridge ID 6 (optional): " cartridge_id6
        read -p "Capacity 6 (optional): " capacity6
    fi
    if [[ -n "$cartridge_id6" ]]; then
        python3 utilities.py function display_firearm_cartridges
        read -p "Cartridge ID 7 (optional): " cartridge_id7
        read -p "Capacity 7 (optional): " capacity7
    fi

    python3 script_modules/add_firearm_model.py \
        "$name" "$manufacturer_id" "$action_id" "$restriction_id" "$cartridge_id1" \
        "$barrel_length_in" "$barrel_length_cm" "$country_iso_origin" \
        "$weight_lb" "$weight_kg" "$rear_sight" "$front_sight" "$capacity1" \
        "$cartridge_id2" "$capacity2" "$cartridge_id3" "$capacity3" \
        "$cartridge_id4" "$capacity4" "$cartridge_id5" "$capacity5" \
        "$cartridge_id6" "$capacity6" "$cartridge_id7" "$capacity7"
}

# --- Insert Firearm Sight ---
function insert_firearm_sight() {
    echo "Insert a new Firearm Sight"

    read -p "Name: " name
    read -p "Type (optional, e.g. scope, red dot, iron): " type

    echo "Choose a Manufacturer (optional):"
    python3 utilities.py function display_firearm_manufacturers
    read -p "Manufacturer ID (optional): " manufacturer_id

    read -p "Max magnification (optional): " max_magnification

    python3 script_modules/add_firearm_sight.py "$name" "$type" "$manufacturer_id" "$max_magnification"
}

# --- Main Menu ---
echo "Firearm Database CLI"
echo "1) Insert Firearm Manufacturer"
echo "2) Insert Firearm Model"
echo "3) Insert Firearm Sight"
read -p "Choose an option: " option

case $option in
    1) insert_firearm_manufacturer ;;
    2) insert_firearm_model ;;
    3) insert_firearm_sight ;;
    *) echo "Invalid option" ;;
esac

deactivate
