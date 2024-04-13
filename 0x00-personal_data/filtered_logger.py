#!/usr/bin/env python3
'''Personal data'''
import re
import os
import logging
import mysql.connector
from typing import List

PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str],
                 redaction: str, message: str,
                 separator: str) -> str:
    '''Return obfuscated log message'''
    for field in fields:
        message = re.sub(field+'=.*?'+separator,
                         field+'='+redaction+separator, message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        '''filter values in incoming log records using filter_datum.'''
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.msg, self.SEPARATOR)
        return super().format(record)


def get_logger() -> logging.Logger:
    '''Return a logging.Logger object'''
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False

    handler = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    '''Return a connector to the database'''
    user = os.getenv('PERSONAL_DATA_DB_USERNAME') or 'root'
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD') or ''
    host = os.getenv('PERSONAL_DATA_DB_HOST') or 'localhost'
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')

    conn = mysql.connector.connect(
        user=user,
        password=password,
        host=host,
        database=db_name
    )

    return conn


def main():
    '''
        obtain a database connection using
        get_db and retrieve all
        rows in the users table and
        display each row under a filtered
    '''
    db = get_db()
    logger = get_logger()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM users;')
    fields = cursor.column_names
    for row in cursor:
        msg = ''.join('{}={}'.format(k, v) for k, v in zip(fields, row))
        logger.info(msg.strip())
    cursor.close()
    db.close()


if __name__ == '__main__':
    main()
