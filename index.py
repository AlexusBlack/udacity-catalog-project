from flask import Flask, render_template, abort, session
from orvSecurity import generate_csrf_token
from orvData import user, categories
from orvTools import get_category, get_item

app = Flask(__name__) 
app.secret_key = 'KJKxXXPKSks75g4W'

@app.route('/', methods = ['GET'])
def index_route():
    return render_template('index.html', page={
        'title': 'Homepage',
        'has_sidebar': True
    }, user=user, content={
        'categories': categories
    })

@app.route('/categories', methods = ['GET'])
def categories_route():
    return render_template('categories.html', page={
        'title': 'Categories'
    }, user=user, content={
        'categories': categories
    })

@app.route('/category/add', methods = ['GET'])
def category_add_route():
    csrf = generate_csrf_token()
    return render_template('category_edit.html', page={
        'title': 'Add category'
    }, user=user, content={
        'is_edit': False,
        'csrf_token': csrf
    })

@app.route('/category/<int:category_id>/edit', methods = ['GET'])
def category_edit_route(category_id):
    target_category = get_category(category_id)

    if target_category is None:
        abort(404)

    csrf = generate_csrf_token()
    
    return render_template('category_edit.html', page={
        'title': 'Add category'
    }, user=user, content={
        'is_edit': True,
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
    }, user=user, content={
        'categories': categories,
        'category': target_category
    })

@app.route('/item/<int:item_id>', methods = ['GET'])
def item_route(item_id):
    target_item = get_item(item_id)

    if target_item is None:
        abort(404)

    return render_template('item.html', page={
        'title': 'Item ' + target_item['name'],
        'has_sidebar': True
    }, user=user, content={
        'categories': categories,
        'item': target_item
    })

if __name__ == '__main__':
    app.debug = True #False
    app.run(host='0.0.0.0', port=5000)	