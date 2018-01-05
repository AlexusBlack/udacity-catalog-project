from flask import Blueprint, url_for, render_template, abort, flash, redirect, request

from security import generate_csrf_token
from tools import user_is_authorized, user_info, get_categories, get_category, add_category, update_category, delete_category

category = Blueprint('category', __name__, template_folder='templates')

@category.route('/categories', methods = ['GET'])
def categories_route():
    return render_template('categories.html', page={
        'title': 'Categories'
    }, user=user_info(), content={
        'categories': get_categories()
    })

@category.route('/category/add', methods = ['GET', 'POST'])
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
            return redirect(url_for('category.categories_route'))

    if request.method == 'GET':
        return render_template('category_edit.html', page={
            'title': 'Add category'
        }, user=user_info(), content={
            'is_edit': False,
            'csrf_token': csrf
        })

@category.route('/category/<int:category_id>/edit', methods = ['GET', 'POST'])
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
            return redirect(url_for('category.categories_route'))

    if request.method == 'GET':
        return render_template('category_edit.html', page={
            'title': 'Add category'
        }, user=user_info(), content={
            'is_edit': True,
            'csrf_token': csrf,
            'category': target_category
        })

@category.route('/category/<int:category_id>/delete', methods = ['GET', 'POST'])
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
            return redirect(url_for('category.categories_route'))

    if request.method == 'GET':
        return render_template('confirm.html', page={
            'title': 'Delete category'
        }, user=user_info(), content={
            'csrf_token': csrf,
            'message': 'Do you really want delete category ' + target_category.name + '?'
        })

@category.route('/category/<int:category_id>', methods = ['GET'])
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
