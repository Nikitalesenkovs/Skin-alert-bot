import asyncio
import socketio
from typing import Any, Callable, Dict, Optional


class WaxpeerAdapter:
    def __init__(
        self,
        on_item_callback: Callable[[Dict[str, Any]], Any],
        api_key: Optional[str] = None,
    ):
        self.on_item_callback = on_item_callback
        self.api_key = api_key
        self.sio = socketio.AsyncClient(
            reconnection=True,
            reconnection_attempts=0,
            reconnection_delay=1,
            reconnection_delay_max=5,
            logger=False,
            engineio_logger=False,
        )
        self._register_handlers()

    def _register_handlers(self) -> None:
        @self.sio.event
        async def connect():
            print("[WAXPEER] Connected")

        @self.sio.event
        async def disconnect():
            print("[WAXPEER] Disconnected")

        @self.sio.event
        async def connect_error(data):
            print("[WAXPEER] Connection error:", data)

        @self.sio.on("new-items")
        async def on_new_items(data):
            await self._handle_items(data)

        @self.sio.on("items")
        async def on_items(data):
            await self._handle_items(data)

    async def _handle_items(self, data: Any) -> None:
        items = []

        if isinstance(data, list):
            items = data
        elif isinstance(data, dict):
            if isinstance(data.get("items"), list):
                items = data["items"]
            elif isinstance(data.get("data"), list):
                items = data["data"]

        for raw_item in items:
            normalized = self._normalize_item(raw_item)
            if normalized:
                await self.on_item_callback(normalized)

    def _normalize_item(self, item: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        item_id = item.get("id") or item.get("item_id")
        name = item.get("name") or item.get("itemName") or item.get("market_hash_name")
        price = item.get("price")
        float_value = item.get("float") or item.get("float_value") or item.get("wear")
        collection = item.get("collection")

        if item_id is None or name is None:
            return None

        try:
            if price is not None:
                price = float(price)
        except (ValueError, TypeError):
            price = None

        try:
            if float_value is not None:
                float_value = float(float_value)
        except (ValueError, TypeError):
            float_value = None

        return {
            "id": str(item_id),
            "name": name,
            "price": price,
            "float": float_value,
            "collection": collection,
            "source": "waxpeer",
            "raw": item,
        }

    async def start(self) -> None:
        await self.sio.connect(
            "https://socket.waxpeer.com",
            transports=["websocket", "polling"],
        )
        await self.sio.wait()

    async def stop(self) -> None:
        if self.sio.connected:
            await self.sio.disconnect()
