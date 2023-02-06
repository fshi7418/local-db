#!/bin/bash
source ~/Environments/personal1/bin/activate
cd ~/Repos/local-db
read -p "How many rows would you like to view?" n
python3 query_transactions.py $n
deactivate
