#!/usr/bin/env python3
"""Example: Using atvproxy to capture button presses from Apple TV Remote app.

This example shows how to programmatically run the atvproxy MRP server
to capture button presses from the Apple TV Remote app.

Note: In most cases, you'll want to use the command-line tool instead:
    atvproxy mrp <credentials> <apple_tv_ip>

This example is useful if you want to integrate button capture into
your own Python application.
"""

import asyncio
import logging
import sys
from ipaddress import IPv4Address

from pyatv.scripts.atvproxy import (
    MrpAppleTVProxy,
    publish_mrp_service,
    DEVICE_NAME,
)
from pyatv.support import net
from zeroconf import Zeroconf

# Configure logging to see button presses
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s]: %(message)s",
    stream=sys.stdout,
)

_LOGGER = logging.getLogger(__name__)


async def run_button_capture_proxy(credentials: str, apple_tv_ip: str, device_name: str = "Button Capture Proxy"):
    """Run a button capture proxy.
    
    Args:
        credentials: MRP credentials in format "client_id:credential"
        apple_tv_ip: IP address of the Apple TV to proxy
        device_name: Name of the proxy device (appears in Remote app)
    """
    loop = asyncio.get_event_loop()
    
    # Get local IP address
    local_ip = str(net.get_local_address_reaching(IPv4Address(apple_tv_ip)))
    _LOGGER.info("Using local IP: %s", local_ip)
    
    # Create proxy factory
    def proxy_factory():
        try:
            # Note: You'll need to discover the actual MRP port first
            # For this example, we use the default port 49152
            proxy = MrpAppleTVProxy(loop, apple_tv_ip, 49152, credentials)
            asyncio.ensure_future(proxy.start(), loop=loop)
            return proxy
        except Exception:
            _LOGGER.exception("Failed to start proxy")
            raise
    
    # Start the server
    server = await loop.create_server(proxy_factory, "0.0.0.0")
    port = server.sockets[0].getsockname()[1]
    _LOGGER.info("Started MRP proxy server at port %d", port)
    
    # Publish via mDNS so Remote app can discover it
    zconf = Zeroconf()
    unpublisher = await publish_mrp_service(zconf, local_ip, port, device_name)
    
    _LOGGER.info("=" * 60)
    _LOGGER.info("Button Capture Proxy is running!")
    _LOGGER.info("=" * 60)
    _LOGGER.info("Device name: %s", device_name)
    _LOGGER.info("Connect with the Apple TV Remote app")
    _LOGGER.info("Button presses will be printed to console")
    _LOGGER.info("=" * 60)
    _LOGGER.info("")
    _LOGGER.info("Press Enter to stop...")
    
    # Wait for user to press Enter
    await loop.run_in_executor(None, sys.stdin.readline)
    
    # Cleanup
    _LOGGER.info("Shutting down...")
    await unpublisher()
    server.close()
    await server.wait_closed()
    zconf.close()


def main():
    """Main entry point."""
    if len(sys.argv) < 3:
        print("Usage: python button_capture_example.py <credentials> <apple_tv_ip> [device_name]")
        print("")
        print("Example:")
        print("  python button_capture_example.py 1234567890abcdef:fedcba0987654321 192.168.1.100")
        print("")
        print("Get credentials using:")
        print("  atvremote scan")
        sys.exit(1)
    
    credentials = sys.argv[1]
    apple_tv_ip = sys.argv[2]
    device_name = sys.argv[3] if len(sys.argv) > 3 else "Button Capture"
    
    try:
        asyncio.run(run_button_capture_proxy(credentials, apple_tv_ip, device_name))
    except KeyboardInterrupt:
        print("\nStopped by user")


if __name__ == "__main__":
    main()
