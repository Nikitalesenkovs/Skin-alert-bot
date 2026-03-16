import json
import os
from typing import Set
from config import SEEN_IDS_FILE

seen_items: Set[str] = set()


def ensure_storage() -> None:
    directory = os.path.dirname(SEEN_IDS_FILE)
    if directory:
        os.makedirs(directory, exist_ok=True)


def load_seen_items() -> None:
    global seen_items
    ensure_storage()

    if not os.path.exists(SEEN_IDS_FILE):
        seen_items = set()
        return

    try:
        with open(SEEN_IDS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        if isinstance(data, list):
            seen_items = set(str(x) for x in data)
        else:
            seen_items = set()
    except Exception:
        seen_items = set()


def save_seen_items() -> None:
    ensure_storage()
    with open(SEEN_IDS_FILE, "w", encoding="utf-8") as f:
        json.dump(list(seen_items), f, ensure_ascii=False, indent=2)


def is_seen(item_id: str) -> bool:
    return item_id in seen_items


def mark_seen(item_id: str) -> None:
    if item_id not in seen_items:
        seen_items.add(item_id)
        save_seen_items()
