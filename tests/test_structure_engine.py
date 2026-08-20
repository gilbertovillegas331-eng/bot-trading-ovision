from models.structure import Trend, StructureType

from engines.structure.structure_engine import (
    StructureEngine,
    StructureAnalysis,
)


def test_structure_engine_returns_analysis():

    engine = StructureEngine()

    result = engine.analyze(
        Trend.BULLISH,
        StructureType.HH,
    )

    assert isinstance(result, StructureAnalysis)
    assert result.trend == Trend.BULLISH
    assert result.structure == StructureType.HH