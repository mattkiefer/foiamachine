"""
validates stuff
"""

from decimal import Decimal
from meta import *


def validate_line(line):
    """
    takes line dict keywords
    and verifies existence
    and types of data
    """
    field_headers = get_field_headers()

    if not validate_salary_format(line):
        return False
    
    if not validate_agency_name(line):
        return False

    if not validate_name(line):
        return False

    return line
    

def validate_salary_format(line):
    salary = line['salary']

    # a salary must have a number in it
    number_present = False
    for x in range(0,10):
        if str(x) in str(salary):
            number_present = True
    if not number_present:
        return None
    # salary that converts to Decimal is legit
    try:
        line['salary'] = Decimal(salary) # if it doesn't fit, you must acquit
    except:
        # if it doesn't convert to Decimal, it may have special chars or something
        for char in ('$','.','/','hour'):
            if char in line['salary']:
                return line
        return None
    if line['salary'] == 0:
        return None
    return line


def validate_agency_name(line):
    """
    this feels redundant
    but existence of values
    should validate here
    """
    if not line['agency']:
        return False
    return line


def validate_name(line):
    """
    every record
    should have first, last name fields by
    validation time
    """
    if not line['first_name'].strip() or not line['last_name'].strip():
        return False
    return line
