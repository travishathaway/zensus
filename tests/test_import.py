"""Test Zensus Collector."""

import zensus_collector


def test_import() -> None:
    """Test that the app can be imported."""
    assert isinstance(zensus_collector.__name__, str)
