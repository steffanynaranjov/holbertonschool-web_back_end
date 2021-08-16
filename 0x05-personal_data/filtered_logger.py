#!/usr/bin/env python3
"""3. Connect to secure database"""
from typing import List
import re
import logging
import os
import mysql.connector


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Returns the log message obfuscated
    Arguments:
    fields: a list of strings representing all fields to obfuscate
    redaction: a string representing by what the field will be obfuscated
    message: a string representing the log line
    separator: a string representing by which character is separating all
    fields in the log line (message)
    re.sub(pattern, repl, string)
    """

    for info in fields:
        pattern = info + "=.+?(?=abc)*\\" + ";"
        message = re.sub(pattern, info + "=" + redaction + separator, message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Constructor"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """filter values in incoming log records using filter_datum"""
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)


def get_logger() -> logging.Logger:
    """Returns a logging.Logger object."""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(RedactingFormatter(PII_FIELDS)))
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Returns a connector to the database"""
    psw = os.environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    username = os.environ.get('PERSONAL_DATA_DB_USERNAME', "root")
    host = os.environ.get('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.environ.get('PERSONAL_DATA_DB_NAME')
    my_connection = mysql.connector.connect(
        host=host,
        database=db_name,
        user=username,
        password=psw)
    return my_connection


if __name__ == '__main__':
    connection = get_db()
    cursor = connection.cursor(dictionary=True)
    query = ("SELECT * FROM users")
    cursor.execute(query)
    for row in cursor:
        string = ""
        for key in row:
            string += "{}={}; ".format(key, row[key])
        print(string)
    cursor.close()
    connection.close()
