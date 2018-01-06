"""
Set of tools that provides us additional abstration layer on top of database
and other useful functions
"""

from functools import wraps
import flask

from item import Item
from category import Category
from base import session

def login_required(func):
    """
    Login decorator (middleware)
    that protects route from unauthorized access
    """
    print('wrapping')
    @wraps(func)
    def check_login(*args, **kwargs):
        """
        Checks if user logged in before executing function
        if not logged redirects to login page
        """
        print('checking auth')
        if user_is_authorized():
            return func(*args, **kwargs)
        else:
            return flask.redirect(flask.url_for('auth.login_route'))
    return check_login

def user_info():
    """
    General use user information
    """
    user = {
        'authorized': False
    }
    if not user_is_authorized():
        return user

    user['authorized'] = True
    user['id'] = flask.session['user_id']
    user['name'] = flask.session['user_name']
    user['photo'] = flask.session['user_photo']

    return user

def user_is_authorized():
    """
    Simple check if user is authorized
    """
    return 'credentials' in flask.session

def get_categories():
    """
    Getting categories list out of DB
    """
    categories = session.query(Category).all()
    return categories

def get_category(category_id):
    """
    Getting single category out of DB by id
    """
    target_category = session.query(Category).get(category_id)

    return target_category

def add_category():
    """
    Adding new category to DB with fields from request form
    * better replace with arguments, to make method more independent
    """
    name = flask.request.form['name']
    new_category = Category(name)

    session.add(new_category)
    session.commit()

def update_category(category_id):
    """
    Updating category in DB with fields from request form
    * better replace with arguments, to make method more independent
    """
    name = flask.request.form['name']
    category_to_update = session.query(Category).get(category_id)
    category_to_update.name = name

    session.add(category_to_update)
    session.commit()

def delete_category(category_id):
    """
    Deleting category by id
    """
    category_to_delete = session.query(Category).filter(Category.id == category_id).first()
    session.delete(category_to_delete)
    session.commit()

def get_item(item_id):
    """
    Retrieving item from DB by id
    """
    target_item = session.query(Item).get(item_id)
    return target_item

def add_item(category_id):
    """
    Adding item to DB with fields from request form
    * better replace with arguments, to make method more independent
    """
    name = flask.request.form['name']
    description = flask.request.form['description']
    new_item = Item(name, description)
    new_item.category_id = category_id

    session.add(new_item)
    session.commit()

def update_item(item_id):
    """
    Updating item in DB with fields from request form
    * better replace with arguments, to make method more independent
    """
    name = flask.request.form['name']
    description = flask.request.form['description']

    item_to_update = session.query(Item).get(item_id)
    item_to_update.name = name
    item_to_update.description = description

    session.add(item_to_update)
    session.commit()

def delete_item(item_id):
    """
    Deleting item in DB by id
    """
    session.query(Item).filter(Item.id == item_id).delete()
    session.commit()