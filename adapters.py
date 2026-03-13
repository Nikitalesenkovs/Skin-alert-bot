import aiohttp

API_URL = ""

async def fetch():

    async with aiohttp.ClientSession() as session:

        async with session.get(API_URL) as r:

            data = await r.json()

            items = []

            for i in data["items"]:

                items.append({
                    "id": i["id"],
                    "name": i["name"],
                    "float": i.get("float"),
                    "price": i.get("price"),
                    "collection": i.get("collection")
                })

            return items
