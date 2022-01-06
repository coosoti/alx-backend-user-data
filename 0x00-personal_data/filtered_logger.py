#!usr/bin/env python3
"""
this module contains user data management
"""
from typing import List
import re


def filter_datum(fields: List, redaction: str, message: str, separator: str):
    """
    this function returns the log message obfuscated - the function uses
    a regex to replace occurences of certain field values
    Arguments:
        fields: list of strings representing all fields to obfuscate
        redaction: string representing by what the field will be obfuscated
        message: a string representing the log line
        separator a string representing by which character is
                   separating all fields in the log line (message)
    Returns:
        the log message obfuscated
    """
    for field in fields:
        pattern = "{}=.*?{}".format(field, separator)
        replace = "{}={}{}".format(field, redaction, separator)
        message = re.sub(pattern, replace, message)
    return message
