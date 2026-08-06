"""OVI CORE: coordinador principal de OVISION."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from core.logger import OviLogger


class OviCore:
    """Coordina el arranque y el estado general del sistema."""

    def __init__(self, settings_path: str = "config/settings.json") -> None:
        self.settings_path = Path(settings_path)
        self.settings: dict[str, Any] = {}
        self.system_ready = False
        self.log = None

    def load_settings(self) -> None:
        if not self.settings_path.exists():
            raise FileNotFoundError(
                f"No existe el archivo de configuración: {self.settings_path}"
            )

        with self.settings_path.open("r", encoding="utf-8") as file:
            self.settings = json.load(file)

    def start_logger(self) -> None:
        logging_settings = self.settings.get("logging", {})
        self.log = OviLogger(
            folder=logging_settings.get("folder", "logs"),
            filename=logging_settings.get("file", "ovision.log"),
            level=logging_settings.get("level", "INFO"),
        ).logger

    def start(self) -> bool:
        try:
            self.load_settings()
            print("[OK] Configuración cargada")

            self.start_logger()
            self.log.info("OVISION inició el proceso de arranque")
            print("[OK] Logger iniciado")

            project = self.settings.get("project", {})
            self.log.info(
                "Proyecto=%s | Versión=%s",
                project.get("name", "OVISION"),
                project.get("version", "desconocida"),
            )

            self.system_ready = True
            print("[OK] OVI CORE iniciado")
            print("[OK] Sistema listo")
            print("Esperando conexión con MetaTrader 5...")
            self.log.info("OVI CORE listo")
            return True

        except (OSError, json.JSONDecodeError, ValueError) as exc:
            print(f"[ERROR] No fue posible iniciar OVISION: {exc}")
            if self.log:
                self.log.exception("Fallo durante el arranque")
            return False
