from models.structure import StructureAnalysis
from engines.structure.structure_engine import StructureEngine


def test_structure_engine_returns_analysis():

    engine = StructureEngine()

    candles = []

    result = engine.analyze(candles)

    assert isinstance(result, StructureAnalysis)