#!usr/bin/env python3
"""
this module contains user data management
"""
from typing import List
import logging
import re


PII_FIELDS = ('name', 'password', 'phone', 'ssn', 'email')


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


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """initialization method"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """this function filters values in incoming log records using
         filter_datum function"""
        return filter_datum(self.fields, self.REDACTION,
                            super(RedactingFormatter, self).format(record),
                            self.SEPARATOR)

def get_logger() -> logging.Logger:
    """this method returns a user data logger"""
    log = logging.getLogger('user_data')
    log.setLevel(logging.INFO)
    log.propagate = False
    stream_handler = logging.StreamHandler()
    formatter = logging.Formatter(RedactingFormatter(fields=PII_FIELDS))
    stream_handler.formatter(formatter)
    stream_handler.setFormatter(formatter)
    log.addHandler(stream_handler)
    return log
