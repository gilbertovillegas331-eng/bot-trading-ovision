from dataclasses import dataclass
from enum import Enum
from datetime import datetime


class MarketEventType(Enum):
    BOS = "BOS"
    CHOCH = "CHOCH"


@dataclass(frozen=True)
class MarketEvent:
    """
    Evento generado cuando la estructura del mercado cambia.
    """

    type: MarketEventType
    price: float
    index: int
    time: datetime
    description: str = ""