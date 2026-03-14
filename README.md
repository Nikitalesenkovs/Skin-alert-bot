# Skin-alert-bot
# CS2 Skin Float Scanner

A lightweight asynchronous Python scanner that monitors CS2 skin marketplaces and detects listings that match specific parameters such as **float value**, **collection**, and **price**.

## Features

* Asynchronous scanning for faster monitoring
* Support for multiple marketplaces via adapters
* Filters for collection, float range, and price
* Telegram notifications for matched items
* Duplicate detection to avoid repeated alerts
* Easy to extend with new marketplaces

## Project Structure

```
Skin-alert-bot/
├── adapters/
│   ├── __init__.py
│   ├── csfloat.py
│   ├── skinport.py
│   └── waxpeer.py
├── cache.py
├── config.py
├── filters.py
├── main.py
├── notifier.py
├── requirements.txt
└── README.md
```

## Requirements

* Python 3.9+
* aiohttp

Install dependencies:

```
pip install aiohttp
```

## Configuration

Edit **config.py** and set your parameters:

```
TARGET_COLLECTION = "Phoenix"

FLOAT_MIN = 0.12
FLOAT_MAX = 0.14

MAX_PRICE = 50
SCAN_INTERVAL = 2

TELEGRAM_TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"
```

## Running the Scanner

```
python main.py
```

The scanner will continuously check marketplaces and send alerts when matching items appear.

## Adding a New Marketplace

Create a new adapter inside the **adapters/** folder and implement a `fetch()` function that returns normalized item data.

## Notes

* This tool only monitors publicly available data.
* Make sure your usage complies with the terms of the marketplaces you monitor.

## License

MIT
