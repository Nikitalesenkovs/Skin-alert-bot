import aiohttp

BOT_TOKEN = "tut nuzhen token"
CHAT_ID = "i tut nuzhen token"


async def send_telegram(message: str) -> None:
    url = f"https://api.telegram.org/bot{token bota}/sendMessage"

    async with aiohttp.ClientSession() as session:
        async with session.post(
            url,
            data={"chat_id": CHAT_ID, "text": message},
            timeout=15,
        ) as resp:
            if resp.status != 200:
                text = await resp.text()
                print("[TELEGRAM ERROR]", resp.status, text)
