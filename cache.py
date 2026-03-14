seen_items = set()


def is_seen(item_id: str) -> bool:
    return item_id in seen_items


def mark_seen(item_id: str) -> None:
    seen_items.add(item_id)
