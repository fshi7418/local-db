#!/bin/bash
# shellcheck source=/dev/null
source ~/Environments/personal1/bin/activate
current_dir=$(pwd)
cd ~/Repos/local-db
read -r -p "Year of start date? " year_start
read -r -p "Month of start date? " month_start
read -r -p "Is there an end year and end month (y/n)? " end_date
if [ "$end_date" = "y" ]
then
    read -r -p "Year of end date? " year_end
    read -r -p "Month of end date? " month_end
    python3 ~/Repos/local-db/export_transactions.py "$year_start" "$month_start" "$year_end" "$month_end" "$current_dir"
else
    python3 ~/Repos/local-db/export_transactions.py "$year_start" "$month_start" "$current_dir"
fi
deactivate
