from enum import Enum


class MarketType(str, Enum):
    FOREX = "forex"
    INDEX = "index"
    SYNTHETIC_INDEX = "synthetic_index"
    FUTURES = "futures"