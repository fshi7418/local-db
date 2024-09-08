#!/bin/bash
# shellcheck source=/dev/null
source ~/Environments/personal1/bin/activate
cd ~/Repos/local-db/cli || exit
echo Please put in author name to detect existence. Not case-sensitive
read -r -p "What is the author name? " author_name
#python3 add_transaction.py
deactivate
