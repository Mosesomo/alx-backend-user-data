#!/usr/bin/env python3
'''session authentication'''
import uuid
from .auth import Auth
from models.user import User


class SessionAuth(Auth):
    '''sessiona authorization that inherits from authorization'''
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        '''method that creates a session id for a user'''
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self,
                               session_id: str = None) -> str:
        '''returns the user id  based on a session id'''
        if session_id is None:
            return None
        if not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        '''returns a User instance based on a cookie value:'''
        session_id = self.session_cookie(request)
        if session_id is None:
            return None
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return None
        user = User.get(user_id)
        return user

    def destroy_session(self, request=None):
        '''logout user'''
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return False
        if session_id in self.user_id_by_session_id:
            del self.user_id_by_session_id[session_id]
            return True
        return False
