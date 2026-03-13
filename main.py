import asyncio
import config
from filters import check_item
from notifier import send
from cache import is_seen, mark_seen

from adapters import site1


async def scan(name, adapter):

    while True:

        try:

            items = await adapter.fetch()

            for item in items:

                if is_seen(item["id"]):
                    continue

                mark_seen(item["id"])

                if check_item(item):

                    msg = (
                        f"Found item\n"
                        f"Market: {name}\n"
                        f"Name: {item['name']}\n"
                        f"Float: {item['float']}\n"
                        f"Price: {item['price']}"
                    )

                    print(msg)

                    await send(msg)

        except Exception as e:

            print(name, "error:", e)

        await asyncio.sleep(config.SCAN_INTERVAL)


async def main():

    tasks = [

        asyncio.create_task(scan("SITE1", site1)),

    ]

    await asyncio.gather(*tasks)


asyncio.run(main())
