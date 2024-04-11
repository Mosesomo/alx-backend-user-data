#!/usr/bin/env python3
'''Personal data'''
import re


def filter_datum(fields, redaction, message, separator):
    '''Return obfuscated log message'''
    for field in fields:
        message = re.sub(field+'=.*?'+separator,
                         field+'='+redaction+separator, message)
    return message