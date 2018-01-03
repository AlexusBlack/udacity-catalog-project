from orvData import categories

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