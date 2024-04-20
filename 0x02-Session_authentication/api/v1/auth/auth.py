#!/usr/bin/env python3
'''Authorization'''
from flask import request
from typing import List, TypeVar
from os import getenv


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
            if excluded_path[-1] == '*':
                if path.startswith(excluded_path[:-1]):
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        '''Public method'''
        if request is None:
            return None
        header = request.headers.get('Authorization')
        if header is None:
            return None
        return header

    def current_user(self, request=None) -> TypeVar('User'):
        '''public method'''
        return None

    def session_cookie(self, request=None):
        '''returns a cookie value from a request'''
        if request is None:
            return None
        session_name = getenv("SESSION_NAME", '_my_session_id')
        return request.cookies.get(session_name)
