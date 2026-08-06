"""Vision Engine: observación y normalización de datos del mercado."""

from __future__ import annotations

from models.market_data import MarketData
from services.mt5_service import MT5Service


class VisionEngine:
    """Obtiene datos de MT5 y los convierte en MarketData validado."""

    def __init__(
        self,
        service: MT5Service,
        symbol: str,
        timeframe_name: str,
        timeframe_value: int,
    ) -> None:
        self.service = service
        self.symbol = symbol
        self.timeframe_name = timeframe_name
        self.timeframe_value = timeframe_value

    def get_latest_closed_candle(self) -> MarketData | None:
        # start_pos=1 evita usar la vela actual todavía en formación.
        rates = self.service.get_rates(
            symbol=self.symbol,
            timeframe=self.timeframe_value,
            count=1,
            start_pos=1,
        )
        tick = self.service.get_tick(self.symbol)

        if rates is None or len(rates) == 0 or tick is None:
            return None

        candle = rates[0]
        market_data = MarketData(
            symbol=self.symbol,
            timeframe=self.timeframe_name,
            time=int(candle["time"]),
            open=float(candle["open"]),
            high=float(candle["high"]),
            low=float(candle["low"]),
            close=float(candle["close"]),
            bid=tick["bid"],
            ask=tick["ask"],
            tick_volume=int(candle["tick_volume"]),
        )

        return market_data if market_data.is_valid() else None
