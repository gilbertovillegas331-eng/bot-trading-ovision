"""Pruebas contractuales del clasificador de estructura."""
import pytest

from engines.structure.structure_classifier import StructureClassifier
from models.structure import StructureType, Swing, SwingType


def test_classifies_higher_high() -> None:
    classifier = StructureClassifier()

    previous = Swing(
        kind=SwingType.HIGH,
        index=1,
        price=100.0,
        time=1,
    )
    current = Swing(
        kind=SwingType.HIGH,
        index=2,
        price=110.0,
        time=2,
    )

    assert classifier.classify(previous, current) is StructureType.HH


def test_classifies_higher_low() -> None:
    classifier = StructureClassifier()

    previous = Swing(
        kind=SwingType.LOW,
        index=1,
        price=100.0,
        time=1,
    )
    current = Swing(
        kind=SwingType.LOW,
        index=2,
        price=110.0,
        time=2,
    )

    assert classifier.classify(previous, current) is StructureType.HL


def test_classifies_lower_high() -> None:
    classifier = StructureClassifier()

    previous = Swing(
        kind=SwingType.HIGH,
        index=1,
        price=110.0,
        time=1,
    )
    current = Swing(
        kind=SwingType.HIGH,
        index=2,
        price=100.0,
        time=2,
    )

    assert classifier.classify(previous, current) is StructureType.LH


def test_classifies_lower_low() -> None:
    classifier = StructureClassifier()

    previous = Swing(
        kind=SwingType.LOW,
        index=1,
        price=110.0,
        time=1,
    )
    current = Swing(
        kind=SwingType.LOW,
        index=2,
        price=100.0,
        time=2,
    )

    assert classifier.classify(previous, current) is StructureType.LL
def test_rejects_swings_of_different_kind() -> None:
    classifier = StructureClassifier()

    previous = Swing(
        kind=SwingType.HIGH,
        index=1,
        price=100.0,
        time=1,
    )
    current = Swing(
        kind=SwingType.LOW,
        index=2,
        price=90.0,
        time=2,
    )

    with pytest.raises(ValueError, match="same kind"):
        classifier.classify(previous, current)


def test_rejects_equal_prices() -> None:
    classifier = StructureClassifier()

    previous = Swing(
        kind=SwingType.HIGH,
        index=1,
        price=100.0,
        time=1,
    )
    current = Swing(
        kind=SwingType.HIGH,
        index=2,
        price=100.0,
        time=2,
    )

    with pytest.raises(ValueError, match="Equal prices"):
        classifier.classify(previous, current)