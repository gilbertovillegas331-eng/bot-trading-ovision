from datetime import datetime, timezone

import pytest


@pytest.fixture
def utc_time():
    return datetime(2026, 1, 1, 12, 0, tzinfo=timezone.utc)


@pytest.fixture
def sample_ohlc():
    return {
        "open": 1.1000,
        "high": 1.1050,
        "low": 1.0950,
        "close": 1.1020,
    }


@pytest.fixture
def sample_tick():
    return {
        "bid": 1.1019,
        "ask": 1.1021,
        "last": 1.1020,
    }