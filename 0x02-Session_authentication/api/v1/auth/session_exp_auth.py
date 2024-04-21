#!/usr/bin/env python3
'''expiration date'''
import datetime
from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import datetime


class SessionExpAuth(SessionAuth):
    '''session expiration auth'''
    def __init__(self):
        '''instantiation'''
        self.session_duration = int(getenv("SESSION_DURATION", 0))

    def create_session(self, user_id: str = None):
        '''creating session id'''
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dictionary = {
            'user_id': user_id,
            'create_at': datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id: str = None):
        '''session_id'''
        if session_id is None:
            return None
        if session_id not in self.user_id_by_session_id:
            return None
        session_dict = self.user_id_by_session_id[session_id]
        if self.session_duration <= 0:
            return session_dict.get('user_id')
        created_at = session_dict.get('created_at')
        if created_at not in session_dict:
            return None
        created_at_session = created_at + datetime.timedelta(
            seconds=self.session_duration
        )
        if created_at_session < datetime.now():
            return None
        return session_dict.get('user_id')
