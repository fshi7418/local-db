from enum import Enum


class ExpenseCat(Enum):
    DEPOSIT = 'Deposit'  # category
    SUPPLIES = 'Life & Supplies'  # category
    FOOD = 'Food'  # category
    NONESSENTIAL = 'Non-essential Expenses'  # category
    ACADEMICS = 'Textbook & Academics'  # category
    CASH = 'Cash'  # category


class ExpenseSource(Enum):
    AMEX = 'AMEX(1006)'
    BMOC = 'BMO Credit(1056)'
    BMOD = 'BMO Chequing(7334)'
    CMB = 'CMB(9076)'
    OTHER = 'Other'
    PCF = 'PC Financial(2800)'
    RBCD = 'RBC Chequing(8545)'
    RBCCO = 'RBC Credit(4682)'
    RBCC = 'RBC Credit(2262)'
    TDD = 'TD Chequing(5232)'
