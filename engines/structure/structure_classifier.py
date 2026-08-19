"""Clasificación determinista de estructura HH, HL, LH y LL."""

from __future__ import annotations

from models.structure import StructureType, Swing, SwingType


class StructureClassifier:
    """Clasifica un swing respecto al swing previo comparable."""

    def classify(self, previous: Swing, current: Swing) -> StructureType:
        if previous.kind is not current.kind:
            raise ValueError(
                "Structure comparison requires swings of the same kind."
            )

        if previous.price == current.price:
            raise ValueError(
                "Equal prices do not define HH, HL, LH or LL."
            )

        if current.kind is SwingType.HIGH:
            if current.price > previous.price:
                return StructureType.HH
            return StructureType.LH

        if current.price > previous.price:
            return StructureType.HL

        return StructureType.LL