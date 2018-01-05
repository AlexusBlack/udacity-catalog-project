import os

from flask import Flask, jsonify, render_template, abort, request, flash, redirect, url_for

from security import generate_csrf_token, get_api_key
from orvData import next_category_id, next_item_id
from tools import user_is_authorized, user_info

from base import Session
from item import Item
from category import Category
from auth import auth_system

app = Flask(__name__)
app.secret_key = 'KJKxXXPKSks75g4W'
app.register_blueprint(auth_system)

session = Session()

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
        return redirect(url_for('auth_system.login_route'))

    return render_template('profile.html', page={
        'title': user['name'] + ' profile'
    }, user=user, content={
        'categories': get_categories()
    })

@app.route('/categories', methods = ['GET'])
def categories_route():
    return render_template('categories.html', page={
        'title': 'Categories'
    }, user=user_info(), content={
        'categories': get_categories()
    })

@app.route('/categories.json', methods = ['GET'])
def categories_api():
    plain_list = [e.serialize() for e in get_categories()]
    return jsonify(plain_list)

@app.route('/category/add', methods = ['GET', 'POST'])
def category_add_route():
    if not user_is_authorized():
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
    if not user_is_authorized():
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
    if not user_is_authorized():
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
    if not user_is_authorized():
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
        'title': 'Category ' + target_category.name,
        'has_sidebar': True
    }, user=user_info(), content={
        'categories': get_categories(),
        'category': target_category
    })

@app.route('/category/<int:category_id>.json', methods = ['GET'])
def categoriy_api(category_id):
    target_category = get_category(category_id)

    if target_category is None:
        abort(404)

    plane_object = target_category.serialize()
    plane_list = [e.serialize() for e in target_category.items]
    plane_object['items'] = plane_list

    return jsonify(plane_object)

@app.route('/item/<int:item_id>/edit', methods = ['GET', 'POST'])
def item_edit_route(item_id):
    if not user_is_authorized():
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
    if not user_is_authorized():
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
        'title': 'Item ' + target_item.name,
        'has_sidebar': True
    }, user=user_info(), content={
        'categories': get_categories(),
        'item': target_item
    })

@app.route('/item/<int:item_id>.json', methods = ['GET'])
def item_api(item_id):
    target_item = get_item(item_id)

    if target_item is None:
        abort(404)
    return jsonify(target_item.serialize())

def get_categories():
    categories = session.query(Category).all()
    return categories

def get_category(category_id):
    target_category = session.query(Category).get(category_id)

    return target_category

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

def get_item(item_id):
    target_item = session.query(Item).get(item_id)

    return target_item

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
