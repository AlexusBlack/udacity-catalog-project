import flask
from hashlib import md5

from item import Item
from category import Category
from base import session

def user_info():
    user = {
        'authorized': False
    }
    if 'credentials' not in flask.session:
        return user

    user['authorized'] = True
    user['id'] = flask.session['user_id']
    user['name'] = flask.session['user_name']
    user['photo'] = flask.session['user_photo']

    return user

def user_is_authorized():
    return 'credentials' in flask.session

def get_categories():
    categories = session.query(Category).all()
    return categories

def get_category(category_id):
    target_category = session.query(Category).get(category_id)

    return target_category

def add_category():
    name = flask.request.form['name']
    new_category = Category(name)

    session.add(new_category)
    session.commit()

def update_category(category_id):
    name = flask.request.form['name']
    category_to_update = session.query(Category).get(category_id)
    category_to_update.name = name

    session.add(category_to_update)
    session.commit()

def delete_category(category_id):
    session.query(Category).filter(Category.id == category_id).delete()
    session.commit()

def get_item(item_id):
    target_item = session.query(Item).get(item_id)
    return target_item

def add_item(category_id):
    name = flask.request.form['name']
    description = flask.request.form['description']
    new_item = Item(name, description)
    new_item.category_id = category_id

    session.add(new_item)
    session.commit()

def update_item(item_id):
    name = flask.request.form['name']
    description = flask.request.form['description']

    item_to_update = session.query(Item).get(item_id)
    item_to_update.name = name
    item_to_update.description = description

    session.add(item_to_update)
    session.commit()

def delete_item(item_id):
    session.query(Item).filter(Item.id == item_id).delete()
    session.commit()