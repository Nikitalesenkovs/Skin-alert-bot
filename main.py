import asyncio
from typing import Dict, Any

from adapters.waxpeer import WaxpeerAdapter
from adapters import skinport, csfloat
from filters import item_matches
from notifier import send_telegram
from config import SCAN_INTERVAL

seen_ids = set()


async def process_item(item: Dict[str, Any]) -> None:
    item_id = f"{item['source']}:{item['id']}"

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


async def scan_skinport() -> None:
    while True:
        try:
            items = await skinport.fetch()
            for item in items:
                await process_item(item)
        except Exception as e:
            print("[SKINPORT ERROR]", e)

        await asyncio.sleep(SCAN_INTERVAL)


async def scan_csfloat() -> None:
    while True:
        try:
            items = await csfloat.fetch()
            for item in items:
                await process_item(item)
        except Exception as e:
            print("[CSFLOAT ERROR]", e)

        await asyncio.sleep(SCAN_INTERVAL)


async def main() -> None:
    waxpeer = WaxpeerAdapter(on_item_callback=process_item)

    await asyncio.gather(
        waxpeer.start(),
        scan_skinport(),
        scan_csfloat(),
    )


if __name__ == "__main__":
    asyncio.run(main())
