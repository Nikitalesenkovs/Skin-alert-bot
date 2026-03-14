import aiohttp
from typing import Any, Dict, List, Optional

API_URL = "https://api.skinport.com/v1/items"


async def fetch() -> List[Dict[str, Any]]:
    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL, timeout=15) as response:
            response.raise_for_status()
            data = await response.json()

    items: List[Dict[str, Any]] = []

    if isinstance(data, list):
        source_items = data
    elif isinstance(data, dict):
        source_items = data.get("items") or data.get("data") or []
    else:
        source_items = []

    for item in source_items:
        normalized = normalize_item(item)
        if normalized:
            items.append(normalized)

    return items


def normalize_item(item: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    item_id = item.get("id") or item.get("item_id") or item.get("market_hash_name")
    name = item.get("market_hash_name") or item.get("name")
    price = item.get("price") or item.get("suggested_price")
    float_value = item.get("float") or item.get("float_value") or item.get("wear")
    collection = item.get("collection")

    if item_id is None or name is None:
        return None

    try:
        if price is not None:
            price = float(price)
    except (ValueError, TypeError):
        price = None

    try:
        if float_value is not None:
            float_value = float(float_value)
    except (ValueError, TypeError):
        float_value = None

    return {
        "id": str(item_id),
        "name": name,
        "price": price,
        "float": float_value,
        "collection": collection,
        "source": "skinport",
        "raw": item,
    }
