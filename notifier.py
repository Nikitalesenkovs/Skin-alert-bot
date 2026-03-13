import aiohttp
import config

async def send(msg):

    url = f""

    async with aiohttp.ClientSession() as session:
        await session.post(url, data={
            "chat_id": config.CHAT_ID,
            "text": msg
        })
