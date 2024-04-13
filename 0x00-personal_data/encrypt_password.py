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


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Check whether a password is valid
    Args:
        hashed_password (bytes): hashed password
        password (str): password in string
    Return:
        bool
    """
    return bcrypt.checkpw(password.encode(), hashed_password)
