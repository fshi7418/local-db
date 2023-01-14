#!/bin/bash
source ~/Environments/personal1/bin/activate
cd ~/Repos/local-db
echo Args e.g. 20230107 9.05 FOOD PCF \"Burger King Lunch\"
read -p "Did this expense occur today (y/n)? " is_today
if [ "$is_today" = "y" ]
then
    expense_date=$(date +%Y%m%d)
else
    read -p "Please input date in yyyymmdd format: " expense_date
fi
read -p "Please enter the amount: " e_amount
cat transaction_configs.py | grep '.*=.*# category$'
read -p "Please enter the expense category e.g. FOOD " e_category
cat transaction_configs.py | grep '.*=.*[^(# category)]$'
read -p "Please enter the expense source e.g. CMB " e_source
read -p "Please enter the expense comment: " e_comment
echo $expense_date $e_amount $e_category $e_source $e_comment
python3 add_transaction.py $expense_date $e_amount $e_category $e_source "$e_comment"
deactivate
