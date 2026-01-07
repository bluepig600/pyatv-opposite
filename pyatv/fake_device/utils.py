"""Utility functions for fake device implementation."""

import asyncio
import time
from typing import Tuple

from aiohttp import ClientSession


# Simplified stub_sleep that just returns current time
# This is used for timing button presses in the fake MRP device
def stub_sleep() -> float:
    """Return current time for timing purposes."""
    return time.time()


async def simple_get(url: str) -> Tuple[bytes, int]:
    """Perform a GET-request to a specified URL."""
    async with ClientSession() as session:
        async with session.get(url) as response:
            if response.status < 200 or response.status >= 300:
                return None, response.status

            data = await response.content.read()
            return data, response.status
