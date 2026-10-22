# models/signal_models.py
from dataclasses import dataclass, field
from typing import List
from datetime import datetime

@dataclass
class Confluence:
    factor: str        # Ej: "FVG Alcista", "Barrido de Liquidez", "Sesgo 4H"
    description: str   # Explicación educativa de qué es y por qué importa
    weight: int        # Peso en la decisión final (ej. 1 o 2)

@dataclass
class TradeSignal:
    symbol: str
    direction: str     # "LONG" o "SHORT"
    entry_price: float
    stop_loss: float
    take_profit: float
    risk_percent: float
    timestamp: datetime
    confluences: List[Confluence] = field(default_factory=list)
    
    @property
    def total_score(self) -> int:
        return sum(c.weight for c in self.confluences)

    def build_explanation(self) -> str:
        """Genera el texto educativo de por qué se tomó la entrada."""
        if not self.confluences:
            return "Sin confluencias suficientes."
            
        lines = [
            f"🎯 SEÑAL OVISION: {self.direction} {self.symbol}",
            f"⏰ Hora: {self.timestamp.strftime('%Y-%m-%d %H:%M')}",
            f"💰 Entrada: {self.entry_price} | SL: {self.stop_loss} | TP: {self.take_profit}",
            f"📊 Riesgo: {self.risk_percent}% de la cuenta",
            "\n📚 MOTIVO EDUCATIVO (¿Por qué entramos?):"
        ]
        for i, conf in enumerate(self.confluences, 1):
            lines.append(f"  {i}. {conf.factor}: {conf.description}")
        
        lines.append(f"\n✅ Puntaje de Confluencia: {self.total_score} (Mínimo requerido: 3)")
        return "\n".join(lines)