#!/usr/bin/env python3
'''Basic auth'''
import base64
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

    def decode_base64_authorization_header(
                                           self,
                                           base64_authorization_header: str
                                          ) -> str:
        '''that returns the decoded value of a Base64 string'''
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decode = base64_authorization_header.encode('utf-8')
            decoded = base64.b64decode(decode)
            return decoded.decode("utf-8")
        except Exception:
            return None
