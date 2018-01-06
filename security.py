"""
Small library of various useful for security functions
"""

import string
import random

from flask import session


def generate_csrf_token():
    """
    Under glorious name of csrf token we are hiding simple
    12 caracters password
    """
    if '_csrf_token' not in session:
        session['_csrf_token'] = generate_password(12)
    return session['_csrf_token']


def generate_password(size=8, chars=string.ascii_letters
                      + string.digits + string.punctuation):
    """
    Generating passord of specified length
    """
    return ''.join(random.choice(chars) for _ in range(size))


def credentials_to_dict(credentials):
    """
    Converting Google credentials into serializable object,
    so we can save it to session
    """
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}
