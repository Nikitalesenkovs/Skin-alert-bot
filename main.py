import asyncio
from typing import Dict, Any

from adapters.waxpeer import WaxpeerAdapter
from filters import item_matches
from notifier import send_telegram

seen_ids = set()


async def process_item(item: Dict[str, Any]) -> None:
    item_id = item["id"]

    if item_id in seen_ids:
        return

    seen_ids.add(item_id)

    if not item_matches(item):
        return

    message = (
        f"Matching item found\n"
        f"Source: {item['source']}\n"
        f"Name: {item['name']}\n"
        f"Float: {item.get('float')}\n"
        f"Price: {item.get('price')}\n"
        f"Collection: {item.get('collection')}"
    )

    print(message)
    await send_telegram(message)


async def main() -> None:
    waxpeer = WaxpeerAdapter(on_item_callback=process_item)
    await waxpeer.start()


if __name__ == "__main__":
    asyncio.run(main())
