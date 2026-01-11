"""Tests for main module."""

import logging

from src.main import setup_logging


def test_setup_logging_creates_logger() -> None:
    """Test that the module logger can be retrieved after setup."""
    setup_logging(debug=False)
    logger = logging.getLogger("src.main")
    assert logger is not None
