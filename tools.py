from orvData import categories
from flask import session
from hashlib import md5

def user_info():
    user = {
        'authorized': False
    }
    if 'credentials' not in session:
        return user

    user['authorized'] = True
    user['id'] = session['user_id']
    user['name'] = session['user_name']
    user['photo'] = session['user_photo']

    return user

def user_is_authorized():
    return 'credentials' in session
