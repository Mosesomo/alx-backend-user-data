#!/usr/bin/env python3
'''Basic auth'''
from .auth import Auth


class BasicAuth(Auth):
    '''Basic auth inherits from auth class'''
    def extract_base64_authorization_header(
                                            self,
                                            authorization_header: str
                                           ) -> str:
        '''returns the Base64 part of the Authorization
            header for a Basic Authentication:
        '''
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        tok = authorization_header.split(" ")[-1]
        return tok
