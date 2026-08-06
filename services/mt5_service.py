"""Servicio de integración entre OVISION y MetaTrader 5."""

from __future__ import annotations

from typing import Any

try:
    import MetaTrader5 as mt5
except ImportError:  # Permite ejecutar pruebas sin MT5 instalado.
    mt5 = None


class MT5Service:
    """Encapsula la conexión y lectura básica de MetaTrader 5."""

    def __init__(self) -> None:
        self.connected = False

    def connect(
        self,
        terminal_path: str = "",
        login: int | None = None,
        password: str = "",
        server: str = "",
    ) -> bool:
        if mt5 is None:
            raise RuntimeError(
                "El paquete MetaTrader5 no está instalado. "
                "Ejecute: pip install MetaTrader5"
            )

        kwargs: dict[str, Any] = {}
        if terminal_path:
            kwargs["path"] = terminal_path
        if login:
            kwargs["login"] = int(login)
        if password:
            kwargs["password"] = password
        if server:
            kwargs["server"] = server

        self.connected = bool(mt5.initialize(**kwargs))
        if not self.connected:
            error = mt5.last_error()
            raise ConnectionError(f"No fue posible conectar con MT5: {error}")

        return True

    def disconnect(self) -> None:
        if mt5 is not None and self.connected:
            mt5.shutdown()
        self.connected = False

    def get_tick(self, symbol: str) -> dict[str, float] | None:
        self._require_connection()
        tick = mt5.symbol_info_tick(symbol)
        if tick is None:
            return None
        return {"bid": float(tick.bid), "ask": float(tick.ask)}

    def get_rates(
        self,
        symbol: str,
        timeframe: int,
        count: int = 200,
        start_pos: int = 0,
    ):
        self._require_connection()
        return mt5.copy_rates_from_pos(symbol, timeframe, start_pos, count)

    def _require_connection(self) -> None:
        if not self.connected:
            raise RuntimeError("MetaTrader 5 no está conectado")
