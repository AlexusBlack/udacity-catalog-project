"""
Endpoint for REST API
- /categories.json with list of all categories
- /category/<id>.json with category info plus all items in category
- /item/<id>.json item info
"""

from flask import Blueprint, abort, jsonify

from tools import get_categories, get_category, get_item

api = Blueprint('api', __name__, template_folder='templates')


@api.route('/categories.json', methods=['GET'])
def categories_api():
    """
    Lists categories
    """
    plain_list = [e.serialize() for e in get_categories()]
    return jsonify(plain_list)


@api.route('/category/<int:category_id>.json', methods=['GET'])
def category_api(category_id):
    """
    Outputs category info and items in it,
    takes category Id as argument
    """
    target_category = get_category(category_id)

    if target_category is None:
        abort(404)

    plane_object = target_category.serialize()
    # serializing category items into array
    plane_list = [e.serialize() for e in target_category.items]
    plane_object['items'] = plane_list

    return jsonify(plane_object)


@api.route('/item/<int:item_id>.json', methods=['GET'])
def item_api(item_id):
    """
    Outputs item info,
    takes item Id as argument
    """
    target_item = get_item(item_id)

    if target_item is None:
        abort(404)
    return jsonify(target_item.serialize())
