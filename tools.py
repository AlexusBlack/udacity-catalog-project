import datetime

from orvData import categories
from flask import session
from hashlib import md5

def get_category(category_id):
    target_category = None

    for category in categories:
        if category['id'] == category_id:
            target_category = category
            break

    return target_category

def get_item(item_id):
    target_item = None

    for category in categories:
        for item in category['items']:
            if item['id'] == item_id:
                target_item = item
                break

    return target_item

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

def get_api_key(user_id, secret_key):
    now = datetime.datetime.now()
    return md5(user_id.encode('utf-8') +
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