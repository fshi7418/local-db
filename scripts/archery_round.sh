#!/bin/bash
# shellcheck source=/dev/null
source ~/Environments/personal1/bin/activate
cd ~/Repos/local-db || exit

# Function to check if input is a valid date in yyyymmdd format
function is_valid_date() {
    if [[ $1 =~ ^[0-9]{8}$ ]]; then
        return 0
    else
        return 1
    fi
}

# Function to check if input is a valid integer
function is_valid_integer() {
    if [[ $1 =~ ^[0-9]+$ ]]; then
        return 0
    else
        return 1
    fi
}

# Function to check if input is a valid float
function is_valid_float() {
    if [[ $1 =~ ^[+-]?[0-9]*\.?[0-9]+$ ]]; then
        return 0
    else
        return 1
    fi
}

# Ask for today's date in yyyymmdd format
while true; do
    read -rp "Please enter round date (yyyymmdd): " todays_date
    if is_valid_date "$todays_date"; then
        break
    else
        echo "Invalid date format. Please try again."
    fi
done

echo "You entered: $todays_date"

# Ask the user for an integer that represents a number in the archery_range.id column
python3 utilities.py function display_archery_ranges
while true; do
    read -rp "Please enter the ID from the 'archery_range' table: " range_id
    if is_valid_integer "$range_id"; then
          echo "You selected archery_range.id: $range_id"
          break
    else
        echo "Invalid input. Please enter a valid integer."
    fi
done

# Ask the user for an integer that represents a number in the archery_riser.id column
python3 utilities.py function display_archery_risers
while true; do
    read -rp "Please enter the ID from the 'archery_riser' table: " riser_id
    if is_valid_integer "$riser_id"; then
          echo "You selected archery_riser.id: $riser_id"
          break
    else
        echo "Invalid input. Please enter a valid integer."
    fi
done

# Ask the user for an integer that represents a number in the archery_limb.id column
python3 utilities.py function display_archery_limbs
while true; do
    read -rp "Please enter the ID from the 'archery_limb' table: " limb_id
    if is_valid_integer "$limb_id"; then
          echo "You selected archery_limb.id: $limb_id"
          break
    else
        echo "Invalid input. Please enter a valid integer."
    fi
done

# Ask the user for an integer that represents a number in the archery_arrow.id column
python3 utilities.py function display_archery_arrows
while true; do
    read -rp "Please enter the ID from the 'archery_arrow' table: " arrow_id
    if is_valid_integer "$arrow_id"; then
          echo "You selected archery_arrow.id: $arrow_id"
          break
    else
        echo "Invalid input. Please enter a valid integer."
    fi
done

# Ask for arrow rest
python3 utilities.py function display_archery_arrow_rests
while true; do
    read -rp "Please enter the ID from the 'archery_arrow_rest' table: " archery_arrow_rest_id
    if is_valid_integer "$archery_arrow_rest_id"; then
          echo "You selected archery_arrow_rest.id: $archery_arrow_rest_id"
          break
    else
        echo "Invalid input. Please enter a valid integer."
    fi
done

# Ask the user for an integer that represents a number in the archery_sight.id column
python3 utilities.py function display_archery_sights
while true; do
    read -rp "Please enter the ID from the 'archery_sight' table: " sight_id
    if is_valid_integer "$sight_id"; then
          echo "You selected archery_sight.id: $sight_id"
          break
    else
        echo "Invalid input. Please enter a valid integer."
    fi
done

# Ask for release aid
python3 utilities.py function display_archery_release_aids
while true; do
    read -rp "Please enter the ID from the 'archery_release_aid' table: " archery_release_aid_id
    if is_valid_integer "$archery_release_aid_id"; then
          echo "You selected archery_release_aid.id: $archery_release_aid_id"
          break
    else
        echo "Invalid input. Please enter a valid integer."
    fi
done

# Ask the user for an integer that represents a number in the archery_target.id column
python3 utilities.py function display_archery_targets
while true; do
    read -rp "Please enter the ID from the 'archery_target' table: " target_id
    if is_valid_integer "$target_id"; then
          echo "You selected archery_target.id: $target_id"
          break
    else
        echo "Invalid input. Please enter a valid integer."
    fi
done

# Ask for scoring rule
python3 utilities.py query archery_scoring_rule
while true; do
    read -rp "Please enter the ID from the 'archery_scoring_rule' table: " archery_scoring_rule_id
    if is_valid_integer "$archery_scoring_rule_id"; then
          echo "You selected archery_scoring_rule.id: $archery_scoring_rule_id"
          break
    else
        echo "Invalid input. Please enter a valid integer."
    fi
done

# Ask the user for a float that represents distance in metres
while true; do
    read -rp "Please enter the distance in metres: " distance_m
    if is_valid_float "$distance_m"; then
          echo "You put distance: $distance_m"
          break
    else
        echo "Invalid input. Please enter a valid float."
    fi
done

# sight, stabiliser, clicker, distance
read -r -p "sight (y/n)? " yn
if [ "$yn" == "y" ]; then
    sight="True"
else
    sight="False"
fi
read -r -p "stabiliser (y/n)? " yn
if [ "$yn" == "y" ]; then
    stabiliser="True"
else
    stabiliser="False"
fi
read -r -p "clicker (y/n)? " yn
if [ "$yn" == "y" ]; then
    clicker="True"
else
    clicker="False"
fi
read -r -p "known distance (y/n)? " yn
if [ "$yn" == "y" ]; then
    known_distance="True"
else
    known_distance="False"
fi
read -r -p "variable distance (y/n)? " yn
if [ "$yn" == "y" ]; then
    variable_distance="True"
else
    variable_distance="False"
fi
read -r -p "was it timed (y/n)? " yn
# whether the ends were timed
if [ "$yn" == "y" ]; then
    timed="True"
else
    timed="False"
fi
if [ "$timed" == "True" ]; then
    while true; do
        read -rp "Please enter number of seconds per arrow (or press Enter to skip): " seconds_per_arrow

        # Check if the input is a floating number
        if awk "BEGIN {exit !($seconds_per_arrow > 0)}" 2>/dev/null; then
            break
        else
            echo "Invalid input. Please a non-zero positive number or press Enter to skip."
        fi
    done
else
    seconds_per_arrow=""
fi

echo "sight, stabiliser, clicker: $sight, $stabiliser, $clicker"
echo "known_distance, variable_distance: $known_distance, $variable_distance"
echo "seconds per arrow: $seconds_per_arrow"

# Ask the user for an integer that represents draw weight in pounds
while true; do
    read -rp "Please enter draw weight in pounds (lb.): " draw_weight_lb
    if is_valid_integer "$draw_weight_lb"; then
          echo "You put draw weight (lb.): $draw_weight_lb"
          break
    else
        echo "Invalid input. Please enter a valid integer."
    fi
done

# Ask the user for environment-related variables
while true; do
    read -rp "On a scale of 1 (worst) to 10 (ideal), your mental condition was: " env_mental
    if is_valid_integer "$env_mental"; then
          echo "You put mental condition: $env_mental"
          break
    else
        echo "Invalid input. Please enter a valid integer."
    fi
done
while true; do
    read -rp "On a scale of 1 (worst) to 10 (ideal), the range condition was: " env_physical
    if is_valid_integer "$env_physical"; then
          echo "You put range condition: $env_physical"
          break
    else
        echo "Invalid input. Please enter a valid integer."
    fi
done
read -r -p "were you hungry (y/n)? " yn
if [ "$yn" == "y" ]; then
    hunger="True"
else
    hunger="False"
fi

# Ask for start and end time
while true; do
    read -rp "Please enter a start time in hhmm (or press Enter to skip): " start_hhmm

    # Check if the input is either empty or exactly 4 digits
    if [[ -z "$start_hhmm" || "$start_hhmm" =~ ^[0-9]{4}$ ]]; then
        echo "start time: '$start_hhmm'"
        break
    else
        echo "Invalid input. Please enter exactly 4 digits or press Enter to skip."
    fi
done
while true; do
    read -rp "Please enter a end time in hhmm (or press Enter to skip): " end_hhmm

    # Check if the input is either empty or exactly 4 digits
    if [[ -z "$end_hhmm" || "$end_hhmm" =~ ^[0-9]{4}$ ]]; then
        echo "end time: '$end_hhmm'"
        break
    else
        echo "Invalid input. Please enter exactly 4 digits or press Enter to skip."
    fi
done

# Ask for user input in n rows of m inputs
read -rp "Did you record scores (y/n)?: " scores
if [ "$scores" == "n" ]; then
    read -rp "How many shots were there?" num_shots
    read -rp "How many ends were there?" num_ends
    python3 script_modules/add_archery_round.py "n" "$riser_id" "$limb_id" "$range_id" "$arrow_id" "$sight_id" "$target_id" "$distance_m" "$sight" "$stabiliser" "$clicker" "$draw_weight_lb" "$env_mental" "$env_physical" "$hunger" "$start_hhmm" "$end_hhmm" "$todays_date" "$archery_scoring_rule_id" "$archery_arrow_rest_id" "$known_distance" "$variable_distance" "$archery_release_aid_id" "$num_ends" "$num_shots"
else
    echo "Please enter rows of inputs. Each row should contain integers or 'x'."
    echo "Separate inputs with spaces. Press Enter after each row."
    echo "If you are entering the last end, press enter, type 'done', then press enter again"

    # Initialize an empty array to store the rows
    rows=()

    # Read input row by row
    while true; do
        # Prompt the user for input
        read -rp "end scores separated by space:" row

        # If the user presses Enter without input, break the loop
        if [[ "$row" = "done" ]]; then
            break
        fi

        # Process each element in the row
        formatted_row=""
        for element in $row; do
            # If the element is 'x' or 'X', treat it as a string and add quotes
            if [[ "$element" == "x" || "$element" == "X" ]]; then
                formatted_row+="'$element', "
            else
                # Otherwise, assume it's an integer and add it as is
                formatted_row+="$element, "
            fi
        done

        # Remove the trailing comma and space
        formatted_row=${formatted_row%, }

        # Append the formatted row to the rows array
        rows+=("[$formatted_row]")
    done

    # Join the rows into a single string representing a list of lists
    input_string=$(IFS=,; echo "[${rows[*]}]")

    # Pass the input string to the Python script
    python3 script_modules/add_archery_round.py "y" "$riser_id" "$limb_id" "$range_id" "$arrow_id" "$sight_id" "$target_id" "$distance_m" "$sight" "$stabiliser" "$clicker" "$draw_weight_lb" "$env_mental" "$env_physical" "$hunger" "$start_hhmm" "$end_hhmm" "$todays_date" "$archery_scoring_rule_id" "$archery_arrow_rest_id" "$known_distance" "$variable_distance" "$archery_release_aid_id" "$seconds_per_arrow" "$input_string"
fi



