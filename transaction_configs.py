from enum import Enum


class ExpenseCat(Enum):
    DEPOSIT = 'Deposit'  # category
    SUPPLIES = 'Life & Supplies'  # category
    FOOD = 'Food'  # category
    NONESSENTIAL = 'Non-essential Expenses'  # category
    ACADEMICS = 'Textbook & Academics'  # category
    CASH = 'Cash'  # category


class ExpenseSource(Enum):
    DEPOSIT = 'Deposit'
    RBCD = 'RBC Chequing'
    BMOD = 'BMO Chequing'
    RBCCO = 'RBC Credit(0397)'
    CMB = 'CMB(9076)'
    RBCC = 'RBC Credit(0148)'
    PCF = 'PC Financial(2800)'
    OTHER = 'Other'
    BMOC = 'BMO Credit(2527)'
