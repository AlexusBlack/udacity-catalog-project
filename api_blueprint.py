from flask import Blueprint, abort, jsonify

from tools import get_categories, get_category, get_item

api = Blueprint('api', __name__, template_folder='templates')

@api.route('/categories.json', methods = ['GET'])
def categories_api():
    plain_list = [e.serialize() for e in get_categories()]
    return jsonify(plain_list)

@api.route('/category/<int:category_id>.json', methods = ['GET'])
def categoriy_api(category_id):
    target_category = get_category(category_id)

    if target_category is None:
        abort(404)

    plane_object = target_category.serialize()
    plane_list = [e.serialize() for e in target_category.items]
    plane_object['items'] = plane_list

    return jsonify(plane_object)

@api.route('/item/<int:item_id>.json', methods = ['GET'])
def item_api(item_id):
    target_item = get_item(item_id)

    if target_item is None:
        abort(404)
    return jsonify(target_item.serialize())
