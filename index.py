from flask import Flask, render_template

app = Flask(__name__) 

user = {
    'authorized': True,
    'name': 'Alex Chernov'
}

categories = (
    {
        'id': 0,
        'name': 'Characters'
    },
    {
        'id': 1,
        'name': 'Planets'
    },
    {
        'id': 2,
        'name': 'Space Ships'
    },
    {
        'id': 3,
        'name': 'Races'
    },
    {
        'id': 4,
        'name': 'Factions'
    },
    {
        'id': 5,
        'name': 'Technologies'
    }
)

@app.route('/', methods = ['GET'])
def index_route():
    return render_template('index.html', page={
        'title': 'Homepage',
        'has_sidebar': True
    }, user=user, content={
        'categories': categories
    })

# @app.route('/categories', methods = ['GET'])
# def categories_route():
#     return render_template('index.html', page={
#         'title': 'Categories'
#     }, user=user, content={
#         'categories': categories
#     })


if __name__ == '__main__':
    app.debug = True #False
    app.run(host='0.0.0.0', port=5000)	