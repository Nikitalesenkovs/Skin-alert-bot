import aiohttp
from config import TELEGRAM_TOKEN, CHAT_ID


async def send_telegram(message: str) -> None:
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    async with aiohttp.ClientSession() as session:
        async with session.post(
            url,
            data={"chat_id": CHAT_ID, "text": message},
            timeout=15,
        ) as resp:
            if resp.status != 200:
                text = await resp.text()
                print("[TELEGRAM ERROR]", resp.status, text)
