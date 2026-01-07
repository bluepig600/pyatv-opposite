"""Representation of a fake device supporting multiple protocol."""

# Re-export everything from pyatv.fake_device for backward compatibility in tests
from pyatv.fake_device import (
    FACTORIES,
    FakeAppleTV,
    FakeService,
)

__all__ = ["FACTORIES", "FakeAppleTV", "FakeService"]

