#!/bin/bash
# shellcheck source=/dev/null
source ~/Environments/personal1/bin/activate
cd ~/Repos/local-db || exit
read -r -p "How many rows would you like to view?" n
python3 query_transactions.py "$n"
deactivate
