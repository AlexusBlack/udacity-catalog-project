import os, datetime

from flask import Flask, render_template, abort, session, request, flash, redirect, url_for
from hashlib import md5

import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery

from orvSecurity import generate_csrf_token
from orvData import categories, next_category_id, next_item_id
from orvTools import get_category, get_item

app = Flask(__name__)
app.secret_key = 'KJKxXXPKSks75g4W'
CLIENT_SECRETS_FILE = 'client_secret_701113834116-726adijgkns945m5l467eu6gu02lb18b.apps.googleusercontent.com.json'
SCOPES = ['profile']


@app.route('/', methods = ['GET'])
def index_route():
    return render_template('index.html', page={
        'title': 'Homepage',
        'has_sidebar': True
    }, user=user_info(), content={
        'categories': categories
    })

@app.route('/login', methods = ['GET'])
def login_route():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES)
    flow.redirect_uri = url_for('oauth2callback', _external=True)

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true')

    session['state'] = state

    return redirect(authorization_url)

@app.route('/logout', methods = ['GET'])
def logout_route():
    if 'credentials' in session:
        del session['credentials']
    flash('You logged out')
    return redirect(url_for('index_route'))

@app.route('/oauth2callback')
def oauth2callback():
    # Specify the state when creating the flow in the callback so that it can
    # verified in the authorization server response.
    state = session['state']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
    flow.redirect_uri = url_for('oauth2callback', _external=True)

    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    # Store credentials in the session.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    credentials = flow.credentials
    session['credentials'] = credentials_to_dict(credentials)

    # requesting use info
    service = googleapiclient.discovery.build('people', 'v1', credentials=credentials)
    result = service.people().get(resourceName='people/me', personFields='names,photos').execute()

    user_id = result['resourceName']
    user_name = result['names'][0]['displayName']
    user_photo = url_for('static', filename='images/no-profile-photo.svg')
    if len(result['photos']) > 0:
        user_photo = result['photos'][0]['url']

    session['user_id'] = user_id
    session['user_name'] = user_name
    session['user_photo'] = user_photo

    return redirect(url_for('index_route'))

@app.route('/profile', methods = ['GET'])
def profile_route():
    user = user_info()

    if not user['authorized']:
        return redirect(url_for('login_route'))

    return render_template('profile.html', page={
        'title': user['name'] + ' profile'
    }, user=user, content={
        'categories': categories,
        'api_key': get_api_key(user['id'])
    })

def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}

@app.route('/categories', methods = ['GET'])
def categories_route():
    return render_template('categories.html', page={
        'title': 'Categories'
    }, user=user_info(), content={
        'categories': categories
    })

@app.route('/category/add', methods = ['GET', 'POST'])
def category_add_route():
    if 'credentials' not in session:
        return redirect(url_for('login_route'))

    csrf = generate_csrf_token()

    if request.method == 'POST':
        if csrf != request.form['csrf_token']:
            abort(403)
        else:
            add_category()
            flash('Category added')
            return redirect(url_for('categories_route'))

    if request.method == 'GET':
        return render_template('category_edit.html', page={
            'title': 'Add category'
        }, user=user_info(), content={
            'is_edit': False,
            'csrf_token': csrf
        })

@app.route('/category/<int:category_id>/edit', methods = ['GET', 'POST'])
def category_edit_route(category_id):
    if 'credentials' not in session:
        return redirect(url_for('login_route'))

    target_category = get_category(category_id)

    if target_category is None:
        abort(404)

    csrf = generate_csrf_token()

    if request.method == 'POST':
        if csrf != request.form['csrf_token']:
            abort(403)
        else:
            update_category(category_id)
            flash('Category updated')
            return redirect(url_for('categories_route'))

    if request.method == 'GET':
        return render_template('category_edit.html', page={
            'title': 'Add category'
        }, user=user_info(), content={
            'is_edit': True,
            'csrf_token': csrf,
            'category': target_category
        })

@app.route('/category/<int:category_id>/delete', methods = ['GET', 'POST'])
def category_delete_route(category_id):
    if 'credentials' not in session:
        return redirect(url_for('login_route'))

    target_category = get_category(category_id)

    if target_category is None:
        abort(404)

    csrf = generate_csrf_token()

    if request.method == 'POST':
        if csrf != request.form['csrf_token']:
            abort(403)
        else:
            delete_category(category_id)
            flash('Category deleted')
            return redirect(url_for('categories_route'))

    if request.method == 'GET':
        return render_template('confirm.html', page={
            'title': 'Delete category'
        }, user=user_info(), content={
            'csrf_token': csrf,
            'message': 'Do you really want delete category ' + target_category['name'] + '?'
        })

@app.route('/category/<int:category_id>/add', methods = ['GET', 'POST'])
def item_add_route(category_id):
    if 'credentials' not in session:
        return redirect(url_for('login_route'))

    target_category = get_category(category_id)

    if target_category is None:
        abort(404)

    csrf = generate_csrf_token()

    if request.method == 'POST':
        if csrf != request.form['csrf_token']:
            abort(403)
        else:
            add_item(category_id)
            flash('Item added')
            return redirect(url_for('category_route', category_id=category_id))

    if request.method == 'GET':
        return render_template('item_edit.html', page={
            'title': 'Add category'
        }, user=user_info(), content={
            'is_edit': False,
            'csrf_token': csrf,
            'category': target_category
        })

@app.route('/category/<int:category_id>', methods = ['GET'])
def category_route(category_id):
    target_category = get_category(category_id)

    if target_category is None:
        abort(404)

    return render_template('category.html', page={
        'title': 'Category ' + target_category['name'],
        'has_sidebar': True
    }, user=user_info(), content={
        'categories': categories,
        'category': target_category
    })

@app.route('/item/<int:item_id>/edit', methods = ['GET', 'POST'])
def item_edit_route(item_id):
    if 'credentials' not in session:
        return redirect(url_for('login_route'))

    target_item = get_item(item_id)

    if target_item is None:
        abort(404)

    csrf = generate_csrf_token()

    if request.method == 'POST':
        if csrf != request.form['csrf_token']:
            abort(403)
        else:
            update_item(item_id)
            flash('Item updated')
            return redirect(url_for('item_route', item_id=item_id))
    
    if request.method == 'GET':
        return render_template('item_edit.html', page={
            'title': 'Edit item'
        }, user=user_info(), content={
            'is_edit': True,
            'csrf_token': csrf,
            'item': target_item
        })

@app.route('/item/<int:item_id>/delete', methods = ['GET', 'POST'])
def item_delete_route(item_id):
    if 'credentials' not in session:
        return redirect(url_for('login_route'))

    target_item = get_item(item_id)

    if target_item is None:
        abort(404)

    csrf = generate_csrf_token()

    if request.method == 'POST':
        if csrf != request.form['csrf_token']:
            abort(403)
        else:
            delete_item(item_id)
            flash('Item deleted')
            return redirect(url_for('categories_route'))

    if request.method == 'GET':
        return render_template('confirm.html', page={
            'title': 'Delete item'
        }, user=user_info(), content={
            'csrf_token': csrf,
            'message': 'Do you really want delete item ' + target_item['name'] + '?'
        })

@app.route('/item/<int:item_id>', methods = ['GET'])
def item_route(item_id):
    target_item = get_item(item_id)

    if target_item is None:
        abort(404)

    return render_template('item.html', page={
        'title': 'Item ' + target_item['name'],
        'has_sidebar': True
    }, user=user_info(), content={
        'categories': categories,
        'item': target_item
    })

def add_category():
    global next_category_id, categories
    name = request.form['name']
    
    categories.append({
        'id': next_category_id,
        'name': name,
        'items': []
    })
    next_category_id += 1

def update_category(category_id):
    global categories
    name = request.form['name']

    for index, category in enumerate(categories):
        if category['id'] == category_id:
            categories[index]['name'] = name
            break

def delete_category(category_id):
    global categories

    for index, category in enumerate(categories):
        if category['id'] == category_id:
            del categories[index]
            break

def add_item(category_id):
    global next_item_id, categories
    name = request.form['name']
    description = request.form['description']

    for index, category in enumerate(categories):
        if category['id'] == category_id:
            categories[index]['items'].append({
                'id': next_item_id,
                'name': name,
                'description': description,
                'author': user_info()['id']
            })
            break

    next_item_id += 1

def update_item(item_id):
    global categories
    name = request.form['name']
    description = request.form['description']

    done = False
    for category_index, category in enumerate(categories):
        for item_index, item in enumerate(category['items']):
            if item['id'] == item_id:
                categories[category_index]['items'][item_index]['name'] = name
                categories[category_index]['items'][item_index]['description'] = description
                done = True
                break
        if done:
            break

def delete_item(item_id):
    global categories

    done = False
    for category_index, category in enumerate(categories):
        for item_index, item in enumerate(category['items']):
            if item['id'] == item_id:
                del categories[category_index]['items'][item_index]
                done = True
                break
        if done:
            break

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

def get_api_key(user_id):
    now = datetime.datetime.now()
    return md5(user_id.encode('utf-8') + app.secret_key.encode('utf-8') + str(now.year).encode('utf-8') + str(now.month).encode('utf-8')).hexdigest()


if __name__ == '__main__':
    # for OAuth on http localhost
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    app.debug = True #False
    app.run(host='0.0.0.0', port=5000)
