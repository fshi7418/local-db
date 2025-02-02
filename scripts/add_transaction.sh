#!/bin/bash
# shellcheck source=/dev/null
source ~/Environments/personal1/bin/activate
cd ~/Repos/local-db || exit
echo Args e.g. 20230107 9.05 FOOD PCF \"Burger King Lunch\"
read -r -p "Did this expense occur today (y/n)? " is_today
if [ "$is_today" = "y" ]
then
    expense_date=$(date +%Y%m%d)
else
    read -r -p "Please input date in yyyymmdd format: " expense_date
fi
read -r -p "Please enter the amount: " e_amount
< transaction_configs.py grep '.*=.*# category$'
read -r -p "Please enter the expense category e.g. FOOD " e_category
< transaction_configs.py grep '.*=.*[^(# category)]$'
read -r -p "Please enter the expense source e.g. CMB " e_source
python3 utilities.py query expense_budget
read -r -p "Please enter budget id if applicable: " e_budget_id
read -r -p "Please enter the expense comment: " e_comment
echo "$expense_date" "$e_amount" "$e_category" "$e_source" "$e_comment" "$e_budget_id"
python3 add_transaction.py "$expense_date" "$e_amount" "$e_category" "$e_source" "$e_comment" "$e_budget_id"
deactivate
