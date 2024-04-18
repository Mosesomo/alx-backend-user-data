#!/usr/bin/env python3
'''Basic auth'''
import base64
from .auth import Auth
from typing import TypeVar
from models.user import User


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

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        ''' returns the user email
            and password from the Base64 decoded value.
        '''
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        email = decoded_base64_authorization_header.split(':')[0]
        password = decoded_base64_authorization_header[len(email) + 1:]
        return (email, password)

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        '''returns the User instance
            based on his email and password.
        '''
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({'email': user_email})
            if not users or users == []:
                return None
            for user in users:
                if user.is_valid_password(user_pwd):
                    return user
            return None
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        ''' overloads Auth and retrieves
            the User instance for a request
        '''
        auth_header = self.authorization_header(request)
        if auth_header:
            token = self.extract_base64_authorization_header(auth_header)
            if token:
                decode = self.decode_base64_authorization_header(token)
                if decode:
                    email, pwd = self.extract_user_credentials(decode)
                    if email:
                        return self.user_object_from_credentials(email, pwd)
        return
