import os
import sys
import ast
import pandas as pd
from sqlalchemy import null

from models import postgres_session
# Import the necessary models
from models.archery import ArcheryRange, ArcheryTarget, ArcheryBowType, ArcheryManufacturer, ArcheryLimb, \
    ArcheryRiser, ArcheryArrow, Shots, Ends, Rounds


if __name__ == '__main__':
    import sys
    import ast

    # Get the input string from the command-line argument
    input_string = sys.argv[1]

    # Convert the input string to a Python list of lists
    input_list = ast.literal_eval(input_string)

    # Print the list of lists to verify
    print("Input as list of lists:", input_list)
