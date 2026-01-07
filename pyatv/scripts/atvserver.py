#!/usr/bin/env python3
"""Simple script to run a fake Apple TV server that can receive commands."""

import argparse
import asyncio
import logging
from ipaddress import IPv4Address
import sys

from zeroconf import ServiceInfo
from zeroconf.asyncio import AsyncZeroconf

from pyatv.const import Protocol
from pyatv.fake_device import FakeAppleTV
from pyatv.support.net import get_local_address_reaching


_LOGGER = logging.getLogger(__name__)

DEFAULT_NAME = "Fake Apple TV"
DEFAULT_ID = "4D797FD3-3538-427E-A47B-A32FC6CF3A6A"


def _mdns_type(protocol: Protocol) -> str:
    """Return mDNS service type for a protocol."""
    types = {
        Protocol.AirPlay: "_airplay._tcp.local.",
        Protocol.Companion: "_companion-link._tcp.local.",
        Protocol.DMAP: "_touch-able._tcp.local.",
        Protocol.MRP: "_mediaremotetv._tcp.local.",
        Protocol.RAOP: "_raop._tcp.local.",
    }
    return types.get(protocol)


async def _publish_service(aiozc: AsyncZeroconf, name: str, service_id: str, protocol: Protocol, port: int):
    """Publish a service via mDNS."""
    import socket
    
    service_type = _mdns_type(protocol)
    if not service_type:
        _LOGGER.warning("No mDNS service type for protocol %s", protocol)
        return

    # Get local IP address
    local_ip = get_local_address_reaching(IPv4Address("8.8.8.8"))
    if local_ip is None:
        # Fallback: get hostname IP
        try:
            hostname_ip = socket.gethostbyname(socket.gethostname())
            local_ip = IPv4Address(hostname_ip)
        except Exception:
            # Last resort: use loopback
            local_ip = IPv4Address("127.0.0.1")
    
    props = {}
    if protocol == Protocol.MRP:
        props = {
            b"Name": name.encode("utf-8"),
            b"txtvers": b"1",
            b"AllowPairing": b"YES",
            b"SystemBuildVersion": b"18M60",
            b"UniqueIdentifier": service_id.encode("utf-8"),
        }
    elif protocol == Protocol.AirPlay:
        props = {
            b"deviceid": b"AA:BB:CC:DD:EE:FF",
            b"features": b"0x1",
            b"model": b"AppleTV6,2",
            b"srcvers": b"220.68",
        }
    elif protocol == Protocol.DMAP:
        props = {
            b"DvNm": name.encode("utf-8"),
            b"RemV": b"10000",
            b"DvTy": b"iPod",
            b"RemN": b"Remote",
        }
    elif protocol == Protocol.Companion:
        props = {
            b"rpBA": b"AA:BB:CC:DD:EE:FF",
            b"rpAD": service_id.encode("utf-8"),
            b"rpHN": b"FAKE_DEV",
            b"rpVr": b"220.1",
        }

    service_name = f"{name}.{service_type}"
    
    info = ServiceInfo(
        service_type,
        service_name,
        addresses=[local_ip.packed],
        port=port,
        properties=props,
        server=f"{name.replace(' ', '-')}.local.",
    )
    
    _LOGGER.info("Publishing %s on port %d (IP: %s)", service_name, port, local_ip)
    await aiozc.async_register_service(info)
    return info


async def run_server(args):
    """Run the fake Apple TV server."""
    logging.basicConfig(
        level=logging.DEBUG if args.debug else logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    loop = asyncio.get_event_loop()
    fake_atv = FakeAppleTV(loop, test_mode=False)

    # Add services based on arguments
    protocols = []
    if args.mrp:
        protocols.append(Protocol.MRP)
        fake_atv.add_service(Protocol.MRP)
        _LOGGER.info("Added MRP service")
    
    if args.airplay:
        protocols.append(Protocol.AirPlay)
        fake_atv.add_service(Protocol.AirPlay)
        _LOGGER.info("Added AirPlay service")
    
    if args.dmap:
        protocols.append(Protocol.DMAP)
        fake_atv.add_service(Protocol.DMAP)
        _LOGGER.info("Added DMAP service")
    
    if args.companion:
        protocols.append(Protocol.Companion)
        fake_atv.add_service(Protocol.Companion)
        _LOGGER.info("Added Companion service")
    
    if args.raop:
        protocols.append(Protocol.RAOP)
        fake_atv.add_service(Protocol.RAOP)
        _LOGGER.info("Added RAOP service")

    if not protocols:
        _LOGGER.error("No protocols specified. Use --mrp, --airplay, --dmap, --companion, or --raop")
        return 1

    # Start the fake device
    await fake_atv.start()
    _LOGGER.info("Fake Apple TV server started")

    # Publish via mDNS
    aiozc = AsyncZeroconf()
    services = []
    
    for protocol in protocols:
        port = fake_atv.get_port(protocol)
        service = await _publish_service(aiozc, args.name, args.id, protocol, port)
        if service:
            services.append(service)
    
    _LOGGER.info("All services published via mDNS")
    _LOGGER.info("Server '%s' is running. Press Ctrl+C to stop.", args.name)
    
    try:
        # Keep running until interrupted
        await asyncio.Event().wait()
    except KeyboardInterrupt:
        _LOGGER.info("Shutting down...")
    finally:
        # Clean up
        for service in services:
            await aiozc.async_unregister_service(service)
        await aiozc.async_close()
        await fake_atv.stop()
    
    return 0


def main():
    """Entry point for atvserver command."""
    parser = argparse.ArgumentParser(
        description="Run a fake Apple TV server that can receive commands from the Apple TV Remote app"
    )
    parser.add_argument(
        "--name",
        default=DEFAULT_NAME,
        help=f"Name of the fake Apple TV (default: {DEFAULT_NAME})",
    )
    parser.add_argument(
        "--id",
        default=DEFAULT_ID,
        help=f"Unique identifier for the fake Apple TV (default: {DEFAULT_ID})",
    )
    parser.add_argument(
        "--mrp",
        action="store_true",
        help="Enable Media Remote Protocol (MRP) - for Apple TV 4 and later",
    )
    parser.add_argument(
        "--airplay",
        action="store_true",
        help="Enable AirPlay protocol",
    )
    parser.add_argument(
        "--dmap",
        action="store_true",
        help="Enable DMAP protocol - for Apple TV 3 and earlier",
    )
    parser.add_argument(
        "--companion",
        action="store_true",
        help="Enable Companion protocol",
    )
    parser.add_argument(
        "--raop",
        action="store_true",
        help="Enable RAOP (Remote Audio Output Protocol)",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Enable all protocols",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging",
    )

    args = parser.parse_args()

    # If --all is specified, enable all protocols
    if args.all:
        args.mrp = True
        args.airplay = True
        args.dmap = True
        args.companion = True
        args.raop = True

    try:
        return asyncio.run(run_server(args))
    except Exception as e:
        _LOGGER.exception("Error running server: %s", e)
        return 1


if __name__ == "__main__":
    sys.exit(main())
