from typing import Dict, Any
from config import TARGET_COLLECTION, FLOAT_MIN, FLOAT_MAX, MAX_PRICE


def item_matches(item: Dict[str, Any]) -> bool:
    collection = item.get("collection")
    float_value = item.get("float")
    price = item.get("price")

    if collection != TARGET_COLLECTION:
        return False

    if float_value is None:
        return False

    if not (FLOAT_MIN <= float_value <= FLOAT_MAX):
        return False

    if price is not None and price > MAX_PRICE:
        return False

    return True
