#!/bin/bash
# shellcheck source=/dev/null
source ~/Environments/personal1/bin/activate
cd ~/Repos/local-db || exit

today=$(date +%Y%m%d)
read -p "Is today the visit date? ($today) (y/n): " is_today
if [ "$is_today" = "y" ]; then
    visit_date=$today
else
    read -p "Visit date (yyyymmdd): " visit_date
fi

echo "Choose a range:"
python3 utilities.py function display_firearm_ranges
read -p "Firearm range ID: " firearm_range_id

read -p "Start time (HHMM, optional): " time_start
read -p "End time (HHMM, optional): " time_end

visit_id=$(python3 script_modules/add_firearm_visit.py "$visit_date" "$firearm_range_id" "$time_start" "$time_end")
echo "Inserted FirearmVisit with ID: $visit_id"

read -p "Do you want to add information for each end (y/n)? " add_ends
if [ "$add_ends" != "y" ]; then
    deactivate
    exit 0
fi

echo "Please start entering information per end. If finished, type 'end'."

end_i=1
ends_json="["

while true; do
    echo ""
    echo "End $end_i"

    # Step 4: Display firearm models and ask for model ID
    python3 utilities.py function display_firearm_models
    read -p "Firearm model ID: " firearm_model_id

    # Step 6: Ammunition or cartridge
    read -p "Do you know the ammunition for this end (y/n)? " knows_ammo
    if [ "$knows_ammo" = "y" ]; then
        python3 utilities.py function display_firearm_ammunition
        read -p "Firearm ammunition ID: " firearm_ammunition_id
        firearm_cartridge_id=$(python3 -c "
from models import postgres_session
from models.firearm import FirearmAmmunition
a = postgres_session.query(FirearmAmmunition).filter_by(id=$firearm_ammunition_id).first()
print(a.firearm_cartridge_id if a and a.firearm_cartridge_id else '')
")
    else
        python3 utilities.py function display_firearm_cartridges
        read -p "Firearm cartridge ID: " firearm_cartridge_id
        firearm_ammunition_id=""
    fi

    # Step 7: Quantity
    read -p "Quantity (optional): " quantity

    # Step 8: Distance
    read -p "Distance unit (yd/m): " distance_unit
    if [ "$distance_unit" = "yd" ]; then
        read -p "Distance in yards (optional): " distance_input
        if [ -z "$distance_input" ]; then
            distance_m=""
        else
            distance_m=$(echo "$distance_input * 0.9144" | bc -l)
        fi
    else
        read -p "Distance in metres (optional): " distance_m
    fi

    # Step 9: Target
    python3 utilities.py function display_firearm_targets
    read -p "Firearm target ID (optional): " firearm_target_id

    # Step 10: Shots scored
    read -p "Shots scored (optional): " shots_scored

    # Step 11: Points of stabilisation
    read -p "Points of stabilisation (optional): " points_of_stabilisation

    # Step 12: Supporting hands
    read -p "Supporting hands (optional): " supporting_hands

    # Step 13: Firearm sight
    python3 utilities.py function display_firearm_sights
    read -p "Firearm sight ID (optional): " firearm_sight_id

    # Step 14: Stance
    read -p "Stance (standing/benchrest/from_cover/retention/sitting/walking): " stance

    # Trap round
    read -p "Is this a trap round? (y/n): " is_trap
    trap_round_json="null"
    if [ "$is_trap" = "y" ]; then
        read -p "Distance unit (yd/m): " trap_distance_unit
        if [ "$trap_distance_unit" = "yd" ]; then
            read -p "Distance in yards: " trap_distance_yard
            if [ -z "$trap_distance_yard" ]; then
                trap_distance_m=""
            else
                trap_distance_m=$(echo "$trap_distance_yard * 0.9144" | bc -l)
            fi
        else
            read -p "Distance in metres: " trap_distance_m
            if [ -z "$trap_distance_m" ]; then
                trap_distance_yard=""
            else
                trap_distance_yard=$(echo "$trap_distance_m * 1.09361" | bc -l)
            fi
        fi
        while true; do
            read -p "Discipline (olympic/ata): " trap_style_input
            if [ "$trap_style_input" = "olympic" ]; then
                trap_style="Olympic"
                break
            elif [ "$trap_style_input" = "ata" ]; then
                trap_style="American"
                break
            else
                echo "Invalid style. Please enter 'olympic' or 'ata'."
            fi
        done
        read -p "Number of breaks (optional): " trap_num_break
        read -p "Starting station (optional): " trap_starting_station
        python3 utilities.py function display_shotgun_choke
        read -p "Shotgun choke ID (optional): " trap_shotgun_choke_id
        read -p "Do you know the number of breaks by station? (y/n): " knows_station_breaks
        trap_shots_json="null"
        if [ "$knows_station_breaks" = "y" ]; then
            trap_shots_json="["
            first_shot=true
            for station in 1 2 3 4 5; do
                read -p "Breaks at station $station (optional): " station_breaks
                if [ -n "$station_breaks" ]; then
                    if [ "$first_shot" = "true" ]; then
                        first_shot=false
                    else
                        trap_shots_json+=","
                    fi
                    trap_shots_json+="{\"station\":$station,\"num_break\":$station_breaks}"
                fi
            done
            trap_shots_json+="]"
        fi
        trap_round_json="{\"distance_yard\":\"$trap_distance_yard\",\"distance_m\":\"$trap_distance_m\",\"discipline\":\"$trap_style\",\"num_break\":\"$trap_num_break\",\"starting_station\":\"$trap_starting_station\",\"shotgun_choke_id\":\"$trap_shotgun_choke_id\",\"trap_shots\":$trap_shots_json}"
    fi

    # Build JSON for this end
    if [ $end_i -gt 1 ]; then
        ends_json+=","
    fi
    ends_json+="{\"firearm_model_id\":\"$firearm_model_id\",\"firearm_cartridge_id\":\"$firearm_cartridge_id\",\"firearm_ammunition_id\":\"$firearm_ammunition_id\",\"quantity\":\"$quantity\",\"distance_m\":\"$distance_m\",\"firearm_target_id\":\"$firearm_target_id\",\"shots_scored\":\"$shots_scored\",\"points_of_stabilisation\":\"$points_of_stabilisation\",\"supporting_hands\":\"$supporting_hands\",\"firearm_sight_id\":\"$firearm_sight_id\",\"stance\":\"$stance\",\"trap_round\":$trap_round_json}"

    end_i=$((end_i + 1))

    # Step 16: Ask if there is another end
    read -p "Add another end? (press Enter to continue, type 'end' to finish): " more_ends
    if [ "$more_ends" = "end" ]; then
        break
    fi
done

ends_json+="]"

# Step 17: Insert all ends
python3 script_modules/insert_firearm_ends.py "$visit_id" "$ends_json"

deactivate
