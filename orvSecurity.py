from flask import session
import string, random

def generate_csrf_token():
    if '_csrf_token' not in session:
        session['_csrf_token'] = generate_password(12)
    return session['_csrf_token']

def generate_password(size = 8, chars=string.ascii_letters + string.digits + string.punctuation):
    return ''.join(random.choice(chars) for _ in range(size))
