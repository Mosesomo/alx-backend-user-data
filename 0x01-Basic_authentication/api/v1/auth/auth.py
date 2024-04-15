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
        if not excluded_paths or excluded_paths is None:
            return True
        for excluded_path in excluded_paths:
            if path == excluded_path:
                return False
        if not path.endswith('/'):
            path += '/'
        return True

    def authorization_header(self, request=None) -> str:
        '''Public method'''
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        '''public method'''
        return None
