import config

def check_item(item):

    if item.get("collection") != config.TARGET_COLLECTION:
        return False

    f = item.get("float")
    if f is None:
        return False

    if not (config.FLOAT_MIN <= f <= config.FLOAT_MAX):
        return False

    if item.get("price", 999999) > config.MAX_PRICE:
        return False

    return True
