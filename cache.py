seen_items = set()

def is_seen(item_id):
    return item_id in seen_items

def mark_seen(item_id):
    seen_items.add(item_id)
