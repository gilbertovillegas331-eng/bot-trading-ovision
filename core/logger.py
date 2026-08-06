"""Sistema centralizado de registros de OVISION."""

from __future__ import annotations

import logging
from pathlib import Path


class OviLogger:
    """Crea y expone un logger configurado para OVISION."""

    def __init__(
        self,
        folder: str = "logs",
        filename: str = "ovision.log",
        level: str = "INFO",
    ) -> None:
        log_dir = Path(folder)
        log_dir.mkdir(parents=True, exist_ok=True)

        self._logger = logging.getLogger("ovision")
        self._logger.setLevel(getattr(logging, level.upper(), logging.INFO))
        self._logger.propagate = False

        if not self._logger.handlers:
            formatter = logging.Formatter(
                "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
            )

            file_handler = logging.FileHandler(
                log_dir / filename,
                encoding="utf-8",
            )
            file_handler.setFormatter(formatter)

            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)

            self._logger.addHandler(file_handler)
            self._logger.addHandler(console_handler)

    @property
    def logger(self) -> logging.Logger:
        return self._logger
