import aiohttp
import logging
from config import TELEGRAM_TOKEN, CHAT_ID

logger = logging.getLogger(__name__)


async def send_telegram(message: str) -> None:
    if not TELEGRAM_TOKEN or not CHAT_ID:
        logger.warning("Telegram credentials are not configured")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    async with aiohttp.ClientSession() as session:
        async with session.post(
            url,
            data={"chat_id": CHAT_ID, "text": message},
            timeout=15,
        ) as resp:
            if resp.status != 200:
                text = await resp.text()
                logger.error("Telegram error %s: %s", resp.status, text)
