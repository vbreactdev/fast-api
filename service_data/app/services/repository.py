from __future__ import annotations

import asyncio
from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import uuid4

from app.schemas.data import ItemCreate, ItemResponse


@dataclass
class StoredItem:
    id: str
    name: str
    description: str | None
    owner: str
    created_at: datetime

    def to_response(self) -> ItemResponse:
        return ItemResponse(
            id=self.id,
            name=self.name,
            description=self.description,
            owner=self.owner,
            created_at=self.created_at,
        )


class InMemoryItemRepository:
    def __init__(self) -> None:
        self._items: dict[str, StoredItem] = {}
        self._lock = asyncio.Lock()

    async def create_item(self, payload: ItemCreate, owner: str) -> ItemResponse:
        item = StoredItem(
            id=str(uuid4()),
            name=payload.name,
            description=payload.description,
            owner=owner,
            created_at=datetime.now(timezone.utc),
        )
        async with self._lock:
            self._items[item.id] = item
        return item.to_response()

    async def list_items(self, owner: str) -> list[ItemResponse]:
        async with self._lock:
            items = [
                item.to_response()
                for item in self._items.values()
                if item.owner == owner
            ]
        items.sort(key=lambda item: item.created_at)
        return items

    async def get_item(self, item_id: str) -> ItemResponse | None:
        async with self._lock:
            item = self._items.get(item_id)
        return None if item is None else item.to_response()

    async def delete_item(self, item_id: str, owner: str) -> bool:
        async with self._lock:
            item = self._items.get(item_id)
            if item is None or item.owner != owner:
                return False
            del self._items[item_id]
            return True
