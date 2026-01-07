"""Advanced example showing how to customize and monitor a fake Apple TV server."""

import asyncio
import logging
from ipaddress import IPv4Address

from pyatv.const import Protocol, DeviceState, MediaType
from pyatv.fake_device import FakeAppleTV

# Configure logging to see what's happening
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

_LOGGER = logging.getLogger(__name__)


async def main():
    """Run a fake Apple TV server with custom state."""
    loop = asyncio.get_event_loop()
    
    # Create a fake Apple TV instance
    fake_atv = FakeAppleTV(loop, test_mode=False)
    
    # Add MRP service (Media Remote Protocol)
    mrp_state, mrp_usecase = fake_atv.add_service(Protocol.MRP)
    _LOGGER.info("Added MRP service")
    
    # Set up initial playing state with video
    mrp_usecase.example_video(
        title="Big Buck Bunny",
        total_time=596,  # Duration in seconds
        position=0,
    )
    _LOGGER.info("Set initial media state with 'Big Buck Bunny'")
    
    # Start the server
    await fake_atv.start()
    
    mrp_port = fake_atv.get_port(Protocol.MRP)
    
    _LOGGER.info("=" * 60)
    _LOGGER.info("Fake Apple TV server is running!")
    _LOGGER.info("=" * 60)
    _LOGGER.info("  MRP service on port %d", mrp_port)
    _LOGGER.info("")
    _LOGGER.info("You can now connect using:")
    _LOGGER.info("  atvremote -s 127.0.0.1:%d playing", mrp_port)
    _LOGGER.info("  atvremote -s 127.0.0.1:%d play", mrp_port)
    _LOGGER.info("  atvremote -s 127.0.0.1:%d pause", mrp_port)
    _LOGGER.info("=" * 60)
    _LOGGER.info("")
    _LOGGER.info("The server will respond to remote control commands!")
    _LOGGER.info("Press Ctrl+C to stop the server")
    _LOGGER.info("")
    
    try:
        # Monitor commands received
        last_command_count = 0
        while True:
            await asyncio.sleep(5)
            
            # You can check the state to see what commands were received
            # (In a real implementation, you might want to add callbacks)
            if hasattr(mrp_state, "command_count"):
                if mrp_state.command_count > last_command_count:
                    _LOGGER.info(
                        "Received %d commands so far", mrp_state.command_count
                    )
                    last_command_count = mrp_state.command_count
                    
    except KeyboardInterrupt:
        _LOGGER.info("Shutting down...")
    finally:
        await fake_atv.stop()


if __name__ == "__main__":
    asyncio.run(main())
