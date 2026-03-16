import os
from dotenv import load_dotenv

load_dotenv()


def get_env_str(name: str, default: str = "") -> str:
    return os.getenv(name, default)


def get_env_float(name: str, default: float) -> float:
    value = os.getenv(name)
    if value is None or value == "":
        return default
    return float(value)


def get_env_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None or value == "":
        return default
    return int(value)


TARGET_COLLECTION = get_env_str("TARGET_COLLECTION", "Phoenix")
FLOAT_MIN = get_env_float("FLOAT_MIN", 0.129)
FLOAT_MAX = get_env_float("FLOAT_MAX", 0.131)
MAX_PRICE = get_env_float("MAX_PRICE", 50)
SCAN_INTERVAL = get_env_int("SCAN_INTERVAL", 5)
TELEGRAM_TOKEN = get_env_str("TELEGRAM_TOKEN", "")
CHAT_ID = get_env_str("CHAT_ID", "")
SEEN_IDS_FILE = get_env_str("SEEN_IDS_FILE", "data/seen_ids.json")
LOG_LEVEL = get_env_str("LOG_LEVEL", "INFO").upper()
