import os

from flask import Flask, render_template, abort, session, request, flash, redirect, url_for

from orvSecurity import generate_csrf_token
from orvData import categories, next_category_id, next_item_id
from tools import *

from auth import auth_system

app = Flask(__name__)
app.secret_key = 'KJKxXXPKSks75g4W'
app.register_blueprint(auth_system)

@app.route('/', methods = ['GET'])
def index_route():
    return render_template('index.html', page={
        'title': 'Homepage',
        'has_sidebar': True
    }, user=user_info(), content={
        'categories': categories
    })

@app.route('/profile', methods = ['GET'])
def profile_route():
    user = user_info()

    if not user['authorized']:
        return redirect(url_for('auth_system.login_route'))

    return render_template('profile.html', page={
        'title': user['name'] + ' profile'
    }, user=user, content={
        'categories': categories,
        'api_key': get_api_key(user['id'], app.secret_key)
    })

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
        return redirect(url_for('auth_system.login_route'))

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
        return redirect(url_for('auth_system.login_route'))

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
        return redirect(url_for('auth_system.login_route'))

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
        return redirect(url_for('auth_system.login_route'))

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
        return redirect(url_for('auth_system.login_route'))

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
        return redirect(url_for('auth_system.login_route'))

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

if __name__ == '__main__':
    # for OAuth on http localhost
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    app.debug = True #False
    app.run(host='0.0.0.0', port=5000)
