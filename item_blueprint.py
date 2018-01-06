"""
Item routes
"""

from flask import Blueprint, url_for, render_template, abort, flash,\
                  redirect, request

from security import generate_csrf_token
from tools import login_required, user_is_authorized, user_info, get_item,\
                  get_categories, get_category, update_item, delete_item, \
                  add_item

item = Blueprint('item', __name__, template_folder='templates')


@item.route('/item/<int:item_id>/edit', methods=['GET', 'POST'])
@login_required
def item_edit_route(item_id):
    """
    Route to edit item
    """

    target_item = get_item(item_id)

    # checking access rights
    if target_item.owner != user_info()['id']:
        flash('Only owner can edit item')
        return redirect(url_for('item.item_route', item_id=item_id))

    if target_item is None:
        abort(404)

    # some protection
    csrf = generate_csrf_token()

    if request.method == 'POST':
        if csrf != request.form['csrf_token']:
            abort(403)
        else:
            update_item(item_id)
            flash('Item updated')
            # sending user to item page after edit is done
            return redirect(url_for('item.item_route', item_id=item_id))

    if request.method == 'GET':
        return render_template('item_edit.html', page={
            'title': 'Edit item'
        }, user=user_info(), content={
            'is_edit': True,
            'csrf_token': csrf,
            'item': target_item
        })


@item.route('/item/<int:item_id>/delete', methods=['GET', 'POST'])
@login_required
def item_delete_route(item_id):
    """
    Route to delete item
    """

    target_item = get_item(item_id)

    # checking access rights
    if target_item.owner != user_info()['id']:
        flash('Only owner can delete item')
        return redirect(url_for('item.item_route', item_id=item_id))

    if target_item is None:
        abort(404)

    # some protection
    csrf = generate_csrf_token()

    if request.method == 'POST':
        if csrf != request.form['csrf_token']:
            abort(403)
        else:
            delete_item(item_id)
            flash('Item deleted')
            # sending user to categories page for he has done
            return redirect(url_for('category.categories_route'))

    if request.method == 'GET':
        return render_template('confirm.html', page={
            'title': 'Delete item'
        }, user=user_info(), content={
            'csrf_token': csrf,
            'message': 'Do you really want delete item '
                       + target_item.name + '?'
        })


@item.route('/item/<int:item_id>', methods=['GET'])
def item_route(item_id):
    """
    Route that outputs item info
    """
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


@item.route('/category/<int:category_id>/add', methods=['GET', 'POST'])
@login_required
def item_add_route(category_id):
    """
    Route to add new item
    """

    target_category = get_category(category_id)

    if target_category is None:
        abort(404)

    # adding some protection
    csrf = generate_csrf_token()

    if request.method == 'POST':
        if csrf != request.form['csrf_token']:
            abort(403)
        else:
            add_item(category_id)
            flash('Item added')
            return redirect(url_for('category.category_route',
                                    category_id=category_id))

    if request.method == 'GET':
        return render_template('item_edit.html', page={
            'title': 'Add category'
        }, user=user_info(), content={
            'is_edit': False,
            'csrf_token': csrf,
            'category': target_category
        })
