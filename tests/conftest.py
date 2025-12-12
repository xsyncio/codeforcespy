"""Pytest configuration and fixtures."""

import pytest
import respx


@pytest.fixture
def respx_mock():
    """Fixture for mocking HTTP requests using respx."""
    with respx.mock(base_url="https://codeforces.com/api") as mock:
        yield mock
