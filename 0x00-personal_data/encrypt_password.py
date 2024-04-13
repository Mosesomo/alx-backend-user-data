#!/usr/bin/env python3
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


def is_valid(hash_password: bytes, password: str) -> bool:
    ''' returns a boolean.'''
    if bcrypt.checkpw(password.encode(), hash_password):
        return True
    else:
        return False
