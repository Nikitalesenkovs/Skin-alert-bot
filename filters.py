from typing import Dict, Any

TARGET_COLLECTION = "Phoenix"
FLOAT_MIN = 0.129
FLOAT_MAX = 0.131


def item_matches(item: Dict[str, Any]) -> bool:
    collection = item.get("collection")
    float_value = item.get("float")

    if collection != TARGET_COLLECTION:
        return False

    if float_value is None:
        return False

    if not (FLOAT_MIN <= float_value <= FLOAT_MAX):
        return False

    return True
