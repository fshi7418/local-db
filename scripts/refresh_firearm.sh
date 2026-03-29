#!/bin/bash
# shellcheck source=/dev/null
source ~/Environments/personal1/bin/activate
cd ~/Repos/local-db || exit
python3 script_modules/refresh_firearm_tables.py
deactivate
