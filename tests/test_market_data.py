from models.market_data import MarketData


def test_market_data_valid():
    data = MarketData(
        symbol="EURUSD",
        timeframe="M15",
        time=1_700_000_000,
        open=1.1000,
        high=1.1050,
        low=1.0950,
        close=1.1020,
        bid=1.1019,
        ask=1.1021,
        tick_volume=100,
    )
    assert data.is_valid()


def test_market_data_rejects_invalid_high():
    data = MarketData(
        symbol="EURUSD",
        timeframe="M15",
        time=1_700_000_000,
        open=1.1000,
        high=1.0990,
        low=1.0950,
        close=1.1020,
        bid=1.1019,
        ask=1.1021,
        tick_volume=100,
    )
    assert not data.is_valid()
