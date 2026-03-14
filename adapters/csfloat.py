import aiohttp
from typing import Any, Dict, List, Optional

API_URL = "https://csfloat.com/api/v1/listings"


async def fetch(
    min_float: Optional[float] = None,
    max_float: Optional[float] = None,
    collection: Optional[str] = None,
    max_price: Optional[int] = None,
    limit: int = 50,
    sort_by: str = "most_recent",
) -> List[Dict[str, Any]]:
    params: Dict[str, Any] = {
        "limit": min(limit, 50),
        "sort_by": sort_by,
    }

    if min_float is not None:
        params["min_float"] = min_float

    if max_float is not None:
        params["max_float"] = max_float

    if collection:
        params["collection"] = collection

    if max_price is not None:
        params["max_price"] = max_price

    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL, params=params, timeout=15) as response:
            response.raise_for_status()
            data = await response.json()

    items: List[Dict[str, Any]] = []

    if isinstance(data, list):
        source_items = data
    elif isinstance(data, dict):
        source_items = data.get("data") or data.get("items") or []
    else:
        source_items = []

    for item in source_items:
        normalized = normalize_item(item)
        if normalized:
            items.append(normalized)

    return items


def normalize_item(item: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    listing_id = item.get("id")
    listing_price = item.get("price")
    inner_item = item.get("item", {})

    name = inner_item.get("market_hash_name") or inner_item.get("item_name")
    float_value = inner_item.get("float_value")
    collection = inner_item.get("collection")

    if listing_id is None or name is None:
        return None

    try:
        if listing_price is not None:
            listing_price = float(listing_price) / 100
    except (ValueError, TypeError):
        listing_price = None

    try:
        if float_value is not None:
            float_value = float(float_value)
    except (ValueError, TypeError):
        float_value = None

    return {
        "id": str(listing_id),
        "name": name,
        "price": listing_price,
        "float": float_value,
        "collection": collection,
        "source": "csfloat",
        "raw": item,
    }
