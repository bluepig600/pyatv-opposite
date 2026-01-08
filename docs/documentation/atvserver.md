---
layout: template
title: atvserver - Fake Apple TV Server
permalink: /documentation/atvserver/
link_group: documentation
---
# :computer: Table of Contents
{:.no_toc}
* TOC
{:toc}

# atvserver - Fake Apple TV Server

`atvserver` is a command-line tool that allows you to run a fake Apple TV server. This server emulates an Apple TV device on your network, allowing you to:

- **Receive commands** from the Apple TV Remote app on iOS/iPadOS/macOS
- **Test integrations** without physical Apple TV hardware
- **Develop and debug** Apple TV control applications
- **Build custom media servers** that appear as Apple TV devices

The fake Apple TV server implements the same protocols as real Apple TV devices, making it perfect for development, testing, and experimentation.

## Installation

**Important:** This fork (pyatv-opposite) is not available on PyPI. You must install it directly from GitHub:

```shell
pip install git+https://github.com/bluepig600/pyatv-opposite.git
```

For more installation options, see the [Installation section in the main README](https://github.com/bluepig600/pyatv-opposite#installation).

## Quick Start

Start a basic fake Apple TV server with remote control support:

```shell
atvserver --name "My Fake Apple TV" --mrp
```

The server will start and publish itself on the network via mDNS (Bonjour). You should now see "My Fake Apple TV" in:
- The Apple TV Remote app on iOS/iPadOS
- The Remote widget in Control Center on iOS/iPadOS  
- System Preferences > Remotes on macOS
- Any app that scans for Apple TV devices (including `atvremote scan`)

## Command Line Options

### Protocol Options

You can enable one or more protocols depending on what functionality you want to emulate:

| Option | Protocol | Description | Use Case |
|--------|----------|-------------|----------|
| `--mrp` | Media Remote Protocol | Modern Apple TV remote control (Apple TV 4 and later) | Remote control, metadata, playback state |
| `--airplay` | AirPlay | Video and photo streaming | Stream content from iOS/macOS to the fake device |
| `--dmap` | DMAP | Legacy Apple TV protocol (Apple TV 3 and earlier) | Legacy device emulation |
| `--companion` | Companion | Device pairing and authentication | Advanced pairing scenarios |
| `--raop` | RAOP | Remote Audio Output Protocol | Audio streaming |
| `--all` | All protocols | Enable all protocols at once | Maximum compatibility |

### Server Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `--name <name>` | Set custom device name that appears on the network | "Fake Apple TV" |
| `--id <identifier>` | Set custom unique identifier (UUID) | Auto-generated |
| `--debug` | Enable debug logging to see detailed protocol information | Disabled |

## Usage Examples

### Basic Remote Control

Enable just the MRP protocol for remote control functionality:

```shell
atvserver --name "Living Room TV" --mrp
```

Now you can control the fake device using `atvremote`:

```shell
atvremote -s 127.0.0.1 play
atvremote -s 127.0.0.1 pause
atvremote -s 127.0.0.1 playing
```

### Remote Control + Streaming

Enable both MRP and AirPlay for full functionality:

```shell
atvserver --name "Bedroom TV" --mrp --airplay
```

This allows both remote control and streaming content to the fake device.

### All Protocols Enabled

Enable all protocols for maximum compatibility:

```shell
atvserver --name "Test Device" --all
```

### Legacy Apple TV 3

Emulate an older Apple TV 3 device using DMAP:

```shell
atvserver --name "Old Apple TV" --dmap
```

### Debug Mode

Enable debug logging to see detailed protocol interactions:

```shell
atvserver --name "Debug TV" --mrp --debug
```

This is useful when:
- Debugging connection issues
- Understanding protocol behavior
- Developing new features

## Programmatic Usage

For more control and flexibility, you can create a fake Apple TV server in your Python code.

### Basic Example

```python
import asyncio
from pyatv.const import Protocol
from pyatv.fake_device import FakeAppleTV

async def main():
    """Run a basic fake Apple TV server."""
    loop = asyncio.get_event_loop()
    
    # Create fake Apple TV instance
    fake_atv = FakeAppleTV(loop, test_mode=False)
    
    # Add MRP service for remote control
    mrp_state, mrp_usecase = fake_atv.add_service(Protocol.MRP)
    
    # Start the server
    await fake_atv.start()
    
    # Get the port where MRP is running
    mrp_port = fake_atv.get_port(Protocol.MRP)
    print(f"Fake Apple TV running on port {mrp_port}")
    
    # Keep running until interrupted
    try:
        await asyncio.Event().wait()
    except KeyboardInterrupt:
        print("Shutting down...")
    finally:
        await fake_atv.stop()

if __name__ == "__main__":
    asyncio.run(main())
```

### Advanced Example with Custom State

```python
import asyncio
from pyatv.const import Protocol, DeviceState, MediaType
from pyatv.fake_device import FakeAppleTV

async def main():
    """Run a fake Apple TV with custom initial state."""
    loop = asyncio.get_event_loop()
    
    # Create fake Apple TV
    fake_atv = FakeAppleTV(loop, test_mode=False)
    
    # Add MRP service and get state/usecase objects
    mrp_state, mrp_usecase = fake_atv.add_service(Protocol.MRP)
    
    # Set initial playing state
    mrp_usecase.example_video(
        title="Big Buck Bunny",
        total_time=596,  # Duration in seconds
        position=0,
    )
    
    # Start the server
    await fake_atv.start()
    
    mrp_port = fake_atv.get_port(Protocol.MRP)
    print(f"Fake Apple TV running with 'Big Buck Bunny' on port {mrp_port}")
    
    try:
        await asyncio.Event().wait()
    except KeyboardInterrupt:
        print("Shutting down...")
    finally:
        await fake_atv.stop()

if __name__ == "__main__":
    asyncio.run(main())
```

### Example Code Files

The repository includes several example files demonstrating fake Apple TV usage:

- **`examples/server.py`**: Basic server setup with proper logging
- **`examples/advanced_server.py`**: Advanced usage with custom state and monitoring

You can run these examples directly:

```shell
python examples/server.py
python examples/advanced_server.py
```

## Use Cases

### 1. Integration Testing

Test your Apple TV control code without needing physical hardware:

```python
import asyncio
from pyatv.const import Protocol
from pyatv.fake_device import FakeAppleTV
import pyatv

async def test_remote_control():
    """Test remote control functionality against fake device."""
    loop = asyncio.get_event_loop()
    
    # Start fake Apple TV
    fake_atv = FakeAppleTV(loop, test_mode=False)
    fake_atv.add_service(Protocol.MRP)
    await fake_atv.start()
    
    # Connect to it using pyatv client
    config = await pyatv.scan(loop, timeout=5)
    atv = await pyatv.connect(config[0], loop)
    
    # Test remote control
    await atv.remote_control.play()
    await atv.remote_control.pause()
    
    # Clean up
    atv.close()
    await fake_atv.stop()

asyncio.run(test_remote_control())
```

### 2. CI/CD Pipelines

Run automated tests in your continuous integration without physical devices:

```yaml
# .github/workflows/test.yml
name: Test Apple TV Integration

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Install pyatv-opposite
        run: pip install git+https://github.com/bluepig600/pyatv-opposite.git
      - name: Run tests with fake device
        run: python -m pytest tests/
```

### 3. Development Without Hardware

Develop and debug Apple TV integrations without access to physical devices:

```shell
# Terminal 1: Start fake device
atvserver --name "Dev TV" --mrp --airplay --debug

# Terminal 2: Test your application
python my_appletv_app.py
```

### 4. Protocol Exploration

Experiment with Apple TV protocols safely:

```shell
# Start with debug logging
atvserver --name "Research TV" --mrp --debug

# In another terminal, send commands and observe the protocol
atvremote -s 127.0.0.1 play
atvremote -s 127.0.0.1 pause
atvremote -s 127.0.0.1 playing
```

## How It Works

The fake Apple TV server:

1. **Starts protocol servers**: Opens TCP/HTTP servers for each enabled protocol
2. **Publishes via mDNS**: Advertises the fake device on the network using Bonjour/Zeroconf
3. **Accepts connections**: Handles incoming connections from clients (Remote app, atvremote, etc.)
4. **Processes commands**: Responds to remote control commands, streaming requests, etc.
5. **Maintains state**: Keeps track of playback state, media metadata, etc.

The implementation is designed to be compatible with pyatv's own client code, but may have limitations compared to real Apple TV devices.

## Limitations

The fake Apple TV server is intended for **testing and development** purposes. Keep in mind:

- **Not feature-complete**: Some advanced features may not be implemented
- **Simplified behavior**: The fake device takes shortcuts compared to real hardware
- **Best effort compatibility**: Primarily designed to work with pyatv client code
- **Not for production**: Should not be used as a production media server
- **Limited streaming**: Actual video/audio playback is simulated, not real

For testing real-world scenarios, you should still validate against actual Apple TV hardware when possible.

## Troubleshooting

### Device Not Appearing on Network

If the fake device doesn't appear in the Remote app or when scanning:

1. **Check firewall**: Ensure your firewall allows mDNS (port 5353 UDP) and the protocol ports
2. **Network connectivity**: Ensure you're on the same network as the device you're testing from
3. **Check logs**: Run with `--debug` to see detailed information
4. **Verify services**: Use `atvremote scan` to see if the device is discoverable

### Connection Refused

If you can see the device but can't connect:

1. **Check protocol**: Ensure you've enabled the correct protocol (e.g., `--mrp`)
2. **Port availability**: Make sure the required ports aren't already in use
3. **Pairing**: Some protocols may require pairing (though fake device typically doesn't)

### Debug Mode

Always start with `--debug` when troubleshooting:

```shell
atvserver --name "Debug TV" --mrp --debug
```

This will show:
- When connections are accepted
- What commands are received
- Any errors or exceptions
- Protocol-level details

## Related Documentation

- [atvremote](../atvremote/) - Command-line tool for controlling Apple TVs
- [Getting Started](../getting-started/) - General introduction to pyatv
- [Concepts](../concepts/) - Understanding pyatv architecture
- [Development](../../development/) - Writing code with pyatv

## Examples in Repository

Check out these example files for working code:

- `examples/server.py` - Basic fake Apple TV server
- `examples/advanced_server.py` - Advanced server with custom state
- `tests/` - Test suite uses fake devices extensively

## Contributing

Found a bug or want to improve the fake Apple TV server? Contributions are welcome!

- Report issues: [GitHub Issues](https://github.com/bluepig600/pyatv-opposite/issues)
- Submit pull requests: [GitHub Pull Requests](https://github.com/bluepig600/pyatv-opposite/pulls)
- Discuss ideas: [GitHub Discussions](https://github.com/bluepig600/pyatv-opposite/discussions)
