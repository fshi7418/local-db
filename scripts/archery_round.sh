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

# Step 1: Ask for today's date in yyyymmdd format
while true; do
    read -p "Please enter round date (yyyymmdd): " todays_date
    if is_valid_date "$todays_date"; then
        break
    else
        echo "Invalid date format. Please try again."
    fi
done

echo "You entered: $todays_date"

# Step 2: Call the Python function to get data in several archery tables

# Step 2.1: Ask the user for an integer that represents a number in the archery_riser.id column
python3 utilities.py query archery_riser
while true; do
    read -p "Please enter the ID from the 'archery_riser' table: " riser_id
    if is_valid_integer "$riser_id"; then
          echo "You selected archery_riser.id: $riser_id"
          break
    else
        echo "Invalid input. Please enter a valid integer."
    fi
done

# Step 2.2: Ask the user for an integer that represents a number in the archery_limb.id column
python3 utilities.py query archery_limb
while true; do
    read -p "Please enter the ID from the 'archery_limb' table: " limb_id
    if is_valid_integer "$limb_id"; then
          echo "You selected archery_limb.id: $limb_id"
          break
    else
        echo "Invalid input. Please enter a valid integer."
    fi
done

# Step 2.3: Ask the user for an integer that represents a number in the archery_range.id column
python3 utilities.py query archery_range
while true; do
    read -p "Please enter the ID from the 'archery_range' table: " range_id
    if is_valid_integer "$range_id"; then
          echo "You selected archery_range.id: $range_id"
          break
    else
        echo "Invalid input. Please enter a valid integer."
    fi
done

# Step 2.4: Ask the user for an integer that represents a number in the archery_arrow.id column
python3 utilities.py query archery_arrow
while true; do
    read -p "Please enter the ID from the 'archery_arrow' table: " arrow_id
    if is_valid_integer "$arrow_id"; then
          echo "You selected archery_arrow.id: $arrow_id"
          break
    else
        echo "Invalid input. Please enter a valid integer."
    fi
done

# Step 2.5: Ask the user for an integer that represents a number in the archery_sight.id column
python3 utilities.py query archery_sight
while true; do
    read -p "Please enter the ID from the 'archery_sight' table: " sight_id
    if is_valid_integer "$sight_id"; then
          echo "You selected archery_sight.id: $sight_id"
          break
    else
        echo "Invalid input. Please enter a valid integer."
    fi
done

# Step 2.6: Ask the user for an integer that represents a number in the archery_target.id column
python3 utilities.py query archery_target
while true; do
    read -p "Please enter the ID from the 'archery_target' table: " target_id
    if is_valid_integer "$target_id"; then
          echo "You selected archery_target.id: $target_id"
          break
    else
        echo "Invalid input. Please enter a valid integer."
    fi
done

# Step 2.7: Ask the user for a float that represents distance in metres
while true; do
    read -p "Please enter the distance in metres: " distance_m
    if is_valid_float "$distance_m"; then
          echo "You put distance: $distance_m"
          break
    else
        echo "Invalid input. Please enter a valid float."
    fi
done

# Step 2.8: sight, stabiliser, clicker, distance
read -r -p "sight (y/n)? " yn
if [ "$yn" == "y" ]; then
    sight="True"
else
    sight="False"
fi
read -r -p "stabliser (y/n)? " yn
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
echo "sight, stabiliser, clicker: $sight, $stabiliser, $clicker"
echo "known_distance, variable_distance: $known_distance, $variable_distance"

# Step 2.9: Ask the user for an integer that represents draw weight in pounds
while true; do
    read -p "Please enter draw weight in pounds (lb.): " draw_weight_lb
    if is_valid_integer "$draw_weight_lb"; then
          echo "You put draw weight (lb.): $draw_weight_lb"
          break
    else
        echo "Invalid input. Please enter a valid integer."
    fi
done

# Step 2.10: Ask the user for environment-related variables
while true; do
    read -p "On a scale of 1 (worst) to 10 (ideal), your mental condition was: " env_mental
    if is_valid_integer "$env_mental"; then
          echo "You put mental condition: $env_mental"
          break
    else
        echo "Invalid input. Please enter a valid integer."
    fi
done
while true; do
    read -p "On a scale of 1 (worst) to 10 (ideal), the range condition was: " env_physical
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

# Step 2.11: Ask for start and end time
while true; do
    read -p "Please enter a start time in hhmm (or press Enter to skip): " start_hhmm

    # Check if the input is either empty or exactly 4 digits
    if [[ -z "$start_hhmm" || "$start_hhmm" =~ ^[0-9]{4}$ ]]; then
        echo "start time: '$start_hhmm'"
        break
    else
        echo "Invalid input. Please enter exactly 4 digits or press Enter to skip."
    fi
done
while true; do
    read -p "Please enter a end time in hhmm (or press Enter to skip): " end_hhmm

    # Check if the input is either empty or exactly 4 digits
    if [[ -z "$end_hhmm" || "$end_hhmm" =~ ^[0-9]{4}$ ]]; then
        echo "end time: '$end_hhmm'"
        break
    else
        echo "Invalid input. Please enter exactly 4 digits or press Enter to skip."
    fi
done

# Step 2.12: Ask for scoring rule
python3 utilities.py query archery_scoring_rule
while true; do
    read -p "Please enter the ID from the 'archery_scoring_rule' table: " archery_scoring_rule_id
    if is_valid_integer "$archery_scoring_rule_id"; then
          echo "You selected archery_scoring_rule.id: $archery_scoring_rule_id"
          break
    else
        echo "Invalid input. Please enter a valid integer."
    fi
done

# Step 2.13: Ask for arrow rest
python3 utilities.py query archery_arrow_rest
while true; do
    read -p "Please enter the ID from the 'archery_arrow_rest' table: " archery_arrow_rest_id
    if is_valid_integer "$archery_arrow_rest_id"; then
          echo "You selected archery_arrow_rest.id: $archery_arrow_rest_id"
          break
    else
        echo "Invalid input. Please enter a valid integer."
    fi
done

# Step 3: Ask for user input in n rows of m inputs
echo "Please enter rows of inputs. Each row should contain integers or 'x'."
echo "Separate inputs with spaces. Press Enter after each row."
echo "If you are entering the last end, press enter, type 'done', then press enter again"

# Initialize an empty array to store the rows
rows=()

# Read input row by row
while true; do
    # Prompt the user for input
    read -p "end scores separated by space:" row

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
python3 add_archery_round.py "$riser_id" "$limb_id" "$range_id" "$arrow_id" "$sight_id" "$target_id" "$distance_m" "$sight" "$stabiliser" "$clicker" "$draw_weight_lb" "$env_mental" "$env_physical" "$hunger" "$start_hhmm" "$end_hhmm" "$input_string" "$todays_date" "$archery_scoring_rule_id" "$archery_arrow_rest_id" "$known_distance" "$variable_distance"
