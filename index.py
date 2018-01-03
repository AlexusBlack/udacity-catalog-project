from flask import Flask, render_template, abort

app = Flask(__name__) 

user = {
    'authorized': True,
    'name': 'Alex Chernov'
}

categories = [
    {
        'id': 0,
        'name': 'Characters',
        'items': [
            {
                'id': 0,
                'name': 'Captain Ed Mercer',
                'description': """
Ed Mercer is the Human captain of the USS Orville.
He is portrayed by Seth MacFarlane.""",
                'author': 0
            },
            {
                'id': 1,
                'name': 'Commander Kelly Grayson',
                'description': """
Kelly Grayson is a Commander and First Officer of the USS Orville.""",
                'author': 0
            },
            {
                'id': 2,
                'name': 'Lt. Commander Bortus',
                'description': """
Bortus is a Moclan crew member of the The Orville. 
He comes from a single gender species with cultural and behavioral attitudes that are quite different from other species that are members of the Planetary Union. 
For this reason, Captain Mercer and the rest of The Orville's crew aren't quite sure how to communicate with him.
He has a mate named Klyden who lives onboard the ship alongside him, with their son Topa.""",
                'author': 0
            }
        ]
    },
    {
        'id': 1,
        'name': 'Planets',
        'items': []
    },
    {
        'id': 2,
        'name': 'Space Ships',
        'items': []
    },
    {
        'id': 3,
        'name': 'Races',
        'items': []
    },
    {
        'id': 4,
        'name': 'Factions',
        'items': []
    },
    {
        'id': 5,
        'name': 'Technologies',
        'items': []
    }
]

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
    return render_template('category_edit.html', page={
        'title': 'Add category'
    }, user=user, content={
        'is_edit': False
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


if __name__ == '__main__':
    app.debug = True #False
    app.run(host='0.0.0.0', port=5000)	