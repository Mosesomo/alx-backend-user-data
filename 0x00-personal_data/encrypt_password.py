#!/usr/bin/en python3
'''Encrypting password'''
import bcrypt
from bcrypt import hashpw


def hash_password(password: str) -> bytes:
    '''returns a salted, hashed password,
        which is a byte string
    '''
    pwd = password.encode()
    hashed = hashpw(pwd, bcrypt.gensalt())
    return hashed
