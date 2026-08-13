from datetime import datetime, timezone

import pytest

from domain.instrument import (
    InstrumentCapabilities,
    InstrumentId,
    InstrumentSpec,
    VolumeType,
)
from domain.market_type import MarketType


def test_instrument_id_normalizes_whitespace():
    instrument_id = InstrumentId("  EURUSD  ")

    assert instrument_id.value == "EURUSD"


def test_instrument_id_rejects_empty_value():
    with pytest.raises(ValueError):
        InstrumentId("")


def test_instrument_id_rejects_whitespace_only():
    with pytest.raises(ValueError):
        InstrumentId("   ")


def test_instrument_id_is_hashable():
    values = {
        InstrumentId("EURUSD"),
        InstrumentId("EURUSD"),
    }

    assert len(values) == 1


def test_volume_type_has_stable_values():
    assert VolumeType.NONE.value == "none"
    assert VolumeType.TICK.value == "tick"
    assert VolumeType.REAL.value == "real"
    assert VolumeType.CONTRACTS.value == "contracts"


def test_capabilities_default_to_false():
    capabilities = InstrumentCapabilities()

    assert capabilities.bid_ask is False
    assert capabilities.last_price is False
    assert capabilities.tick_volume is False
    assert capabilities.real_volume is False
    assert capabilities.open_interest is False
    assert capabilities.market_depth is False
    assert capabilities.trade_prints is False
    assert capabilities.execution is False


def test_capabilities_are_independent():
    capabilities = InstrumentCapabilities(
        bid_ask=True,
        tick_volume=True,
        execution=True,
    )

    assert capabilities.bid_ask is True
    assert capabilities.tick_volume is True
    assert capabilities.real_volume is False
    assert capabilities.execution is True


def test_forex_instrument_spec():
    spec = InstrumentSpec(
        instrument_id=InstrumentId("EURUSD"),
        market_type=MarketType.FOREX,
        tick_size=0.00001,
        digits=5,
        capabilities=InstrumentCapabilities(
            bid_ask=True,
            tick_volume=True,
            execution=True,
        ),
        contract_size=100_000,
        base_currency="EUR",
        quote_currency="USD",
        provider_symbol="EURUSD.a",
    )

    assert spec.instrument_id == InstrumentId("EURUSD")
    assert spec.market_type is MarketType.FOREX
    assert spec.tick_size == 0.00001
    assert spec.provider_symbol == "EURUSD.a"


def test_futures_instrument_spec():
    expiry = datetime(
        2026,
        12,
        18,
        tzinfo=timezone.utc,
    )

    spec = InstrumentSpec(
        instrument_id=InstrumentId("NQ"),
        market_type=MarketType.FUTURES,
        tick_size=0.25,
        tick_value=5.0,
        digits=2,
        capabilities=InstrumentCapabilities(
            bid_ask=True,
            last_price=True,
            real_volume=True,
            open_interest=True,
            execution=True,
        ),
        exchange="CME",
        timezone="America/Chicago",
        provider_symbol="NQZ26",
        expiry=expiry,
    )

    assert spec.tick_value == 5.0
    assert spec.exchange == "CME"
    assert spec.expiry == expiry
    assert spec.capabilities.open_interest is True


def test_synthetic_does_not_require_forex_fields():
    spec = InstrumentSpec(
        instrument_id=InstrumentId("VOLATILITY_75"),
        market_type=MarketType.SYNTHETIC_INDEX,
        tick_size=0.01,
        digits=2,
        capabilities=InstrumentCapabilities(
            bid_ask=True,
            execution=True,
        ),
    )

    assert spec.base_currency is None
    assert spec.quote_currency is None


def test_futures_market_does_not_imply_real_volume():
    spec = InstrumentSpec(
        instrument_id=InstrumentId("NQ"),
        market_type=MarketType.FUTURES,
        tick_size=0.25,
        digits=2,
        capabilities=InstrumentCapabilities(),
    )

    assert spec.capabilities.real_volume is False


@pytest.mark.parametrize(
    "tick_size",
    [
        0,
        -0.01,
        float("nan"),
        float("inf"),
        float("-inf"),
    ],
)
def test_instrument_spec_rejects_invalid_tick_size(tick_size):
    with pytest.raises(ValueError):
        InstrumentSpec(
            instrument_id=InstrumentId("EURUSD"),
            market_type=MarketType.FOREX,
            tick_size=tick_size,
            digits=5,
            capabilities=InstrumentCapabilities(),
        )


@pytest.mark.parametrize("digits", [-1, -5])
def test_instrument_spec_rejects_negative_digits(digits):
    with pytest.raises(ValueError):
        InstrumentSpec(
            instrument_id=InstrumentId("EURUSD"),
            market_type=MarketType.FOREX,
            tick_size=0.00001,
            digits=digits,
            capabilities=InstrumentCapabilities(),
        )