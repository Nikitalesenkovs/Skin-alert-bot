import asyncio
import logging
from typing import Dict, Any

from adapters.waxpeer import WaxpeerAdapter
from adapters import skinport, csfloat
from filters import item_matches
from notifier import send_telegram
from config import SCAN_INTERVAL, LOG_LEVEL, FLOAT_MIN, FLOAT_MAX, TARGET_COLLECTION, MAX_PRICE
from cache import is_seen, mark_seen, load_seen_items

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger(__name__)


async def process_item(item: Dict[str, Any]) -> None:
    item_id = f"{item['source']}:{item['id']}"

    if is_seen(item_id):
        return

    if not item_matches(item):
        return

    mark_seen(item_id)

    message = (
        f"Matching item found\n"
        f"Source: {item['source']}\n"
        f"Name: {item['name']}\n"
        f"Float: {item.get('float')}\n"
        f"Price: {item.get('price')}\n"
        f"Collection: {item.get('collection')}"
    )

    logger.info("Matched item: %s", message.replace("\n", " | "))
    await send_telegram(message)


async def scan_skinport() -> None:
    while True:
        try:
            items = await skinport.fetch()
            for item in items:
                await process_item(item)
        except Exception as e:
            logger.exception("Skinport scan error: %s", e)

        await asyncio.sleep(SCAN_INTERVAL)


async def scan_csfloat() -> None:
    while True:
        try:
            items = await csfloat.fetch(
                min_float=FLOAT_MIN,
                max_float=FLOAT_MAX,
                collection=TARGET_COLLECTION,
                max_price=int(MAX_PRICE * 100),
                limit=50,
                sort_by="most_recent",
            )
            for item in items:
                await process_item(item)
        except Exception as e:
            logger.exception("CSFloat scan error: %s", e)

        await asyncio.sleep(SCAN_INTERVAL)


async def main() -> None:
    load_seen_items()
    waxpeer = WaxpeerAdapter(on_item_callback=process_item)

    await asyncio.gather(
        waxpeer.start(),
        scan_skinport(),
        scan_csfloat(),
    )


if __name__ == "__main__":
    asyncio.run(main())
