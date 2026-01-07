"""Example showing how to create a fake Apple TV server in Python code."""

import asyncio
import logging
from ipaddress import IPv4Address

from pyatv.const import Protocol
from pyatv.fake_device import FakeAppleTV

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

_LOGGER = logging.getLogger(__name__)


async def main():
    """Run a fake Apple TV server."""
    loop = asyncio.get_event_loop()
    
    # Create a fake Apple TV instance (test_mode=False for standalone server)
    fake_atv = FakeAppleTV(loop, test_mode=False)
    
    # Add MRP service (Media Remote Protocol - for Apple TV 4 and later)
    mrp_state, mrp_usecase = fake_atv.add_service(Protocol.MRP)
    _LOGGER.info("Added MRP service")
    
    # Add AirPlay service (for video streaming)
    airplay_state, airplay_usecase = fake_atv.add_service(Protocol.AirPlay)
    _LOGGER.info("Added AirPlay service")
    
    # Start the server
    await fake_atv.start()
    
    # Get the ports where services are running
    mrp_port = fake_atv.get_port(Protocol.MRP)
    airplay_port = fake_atv.get_port(Protocol.AirPlay)
    
    _LOGGER.info("Fake Apple TV server is running:")
    _LOGGER.info("  MRP service on port %d", mrp_port)
    _LOGGER.info("  AirPlay service on port %d", airplay_port)
    _LOGGER.info("")
    _LOGGER.info("You can now connect to this server using pyatv client:")
    _LOGGER.info("  atvremote -s 127.0.0.1:%d playing", mrp_port)
    _LOGGER.info("")
    _LOGGER.info("Press Ctrl+C to stop the server")
    
    try:
        # Keep the server running
        await asyncio.Event().wait()
    except KeyboardInterrupt:
        _LOGGER.info("Shutting down...")
    finally:
        await fake_atv.stop()


if __name__ == "__main__":
    asyncio.run(main())
