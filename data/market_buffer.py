from __future__ import annotations

from collections import deque
from typing import Any

from domain.market_stream import MarketStreamKey


class MarketBuffer:
    def __init__(self, capacity: int) -> None:
        if isinstance(capacity, bool):
            raise TypeError("capacity must be an integer")

        if not isinstance(capacity, int):
            raise TypeError("capacity must be an integer")

        if capacity <= 0:
            raise ValueError("capacity must be greater than zero")

        self.capacity = capacity
        self._streams: dict[
            MarketStreamKey,
            deque[Any],
        ] = {}

    def append(
        self,
        key: MarketStreamKey,
        item: Any,
    ) -> None:
        if not isinstance(key, MarketStreamKey):
            raise TypeError(
                "key must be a MarketStreamKey"
            )

        if key not in self._streams:
            self._streams[key] = deque(
                maxlen=self.capacity
            )

        self._streams[key].append(item)

    def snapshot(
        self,
        key: MarketStreamKey,
    ) -> tuple[Any, ...]:
        stream = self._streams.get(key)

        if stream is None:
            return ()

        return tuple(stream)

    def latest(
        self,
        key: MarketStreamKey,
    ) -> Any | None:
        stream = self._streams.get(key)

        if not stream:
            return None

        return stream[-1]

    def clear(
        self,
        key: MarketStreamKey | None = None,
    ) -> None:
        if key is None:
            self._streams.clear()
            return

        if not isinstance(key, MarketStreamKey):
            raise TypeError(
                "key must be a MarketStreamKey or None"
            )

        self._streams.pop(key, None)