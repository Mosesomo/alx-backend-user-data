#!/usr/bin/env python3
'''Authorization'''
from flask import request
from typing import List, TypeVar


class Auth:
    '''Auth class'''
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        '''public method'''
        if path is None:
            return True
        if excluded_paths is None or excluded_paths == []:
            return True
        if path in excluded_paths:
            return False
        if path.endswith('/'):
            path += '/'
        for excluded_path in excluded_paths:
            if path == excluded_path.rstrip('/'):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        '''Public method'''
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        '''public method'''
        return None
