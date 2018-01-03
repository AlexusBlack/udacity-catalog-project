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
    target_category=None
    print(categories)
    for category in categories:
        if category['id'] == category_id:
            target_category = category
            break
    
    if target_category == None:
        abort(404)


    return render_template('category.html', page={
        'title': 'Add category',
        'has_sidebar': True
    }, user=user, content={
        'categories': categories,
        'category_id': target_category['id'],
        'category_name': target_category['name'],
        'category_items': target_category['items']
    })


if __name__ == '__main__':
    app.debug = True #False
    app.run(host='0.0.0.0', port=5000)	