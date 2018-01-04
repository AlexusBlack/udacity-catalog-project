import string
import random
import datetime
import hashlib

from flask import session

def generate_csrf_token():
    if '_csrf_token' not in session:
        session['_csrf_token'] = generate_password(12)
    return session['_csrf_token']

def generate_password(size = 8, chars=string.ascii_letters + string.digits + string.punctuation):
    return ''.join(random.choice(chars) for _ in range(size))

def get_api_key(user_id, secret_key):
    now = datetime.datetime.now()
    return hashlib.md5(user_id.encode('utf-8') +
                       secret_key.encode('utf-8') +
                       str(now.year).encode('utf-8') +
                       str(now.month).encode('utf-8')).hexdigest()

def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}
