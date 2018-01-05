import os
import sys

from flask import Flask, render_template, redirect, url_for
from tools import user_is_authorized, user_info, get_categories

from auth_blueprint import auth
from category_blueprint import category
from item_blueprint import item
from api_blueprint import api

app = Flask(__name__)
app.secret_key = 'This is placeholder for secret key and must be replaced'
app.register_blueprint(auth)
app.register_blueprint(category)
app.register_blueprint(item)
app.register_blueprint(api)

@app.route('/', methods = ['GET'])
def index_route():
    return render_template('index.html', page={
        'title': 'Homepage',
        'has_sidebar': True
    }, user=user_info(), content={
        'categories': get_categories()
    })

@app.route('/profile', methods = ['GET'])
def profile_route():
    user = user_info()

    if not user_is_authorized():
        return redirect(url_for('auth.login_route'))

    return render_template('profile.html', page={
        'title': user['name'] + ' profile'
    }, user=user, content={
        'categories': get_categories()
    })

if __name__ == '__main__':
    args_number = len(sys.argv)
    if args_number > 0 and '--production' not in sys.argv:
        print('WARNING: running in debug mode\nadd `--production` flag to run in production mode')
        # for OAuth on http localhost
        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
        app.debug = True
    else:
        app.debug = False
    app.run(host='0.0.0.0', port=5000)
