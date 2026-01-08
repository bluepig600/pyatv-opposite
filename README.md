A Python library for Apple TV and AirPlay devices
=================================================

<img src="https://raw.githubusercontent.com/postlund/pyatv/master/docs/assets/img/logo.svg?raw=true" width="150">

![Tests](https://github.com/postlund/pyatv/workflows/Tests/badge.svg)
![pyatv Actions](https://api.meercode.io/badge/postlund/pyatv?type=ci-success-rate&branch=master&lastDay=30)
[![codecov](https://codecov.io/gh/postlund/pyatv/branch/master/graph/badge.svg)](https://codecov.io/gh/postlund/pyatv)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![PyPi Package](https://badge.fury.io/py/pyatv.svg)](https://badge.fury.io/py/pyatv)
[![Gitpod Ready-to-Code](https://img.shields.io/badge/Gitpod-ready--to--code-blue?logo=gitpod)](https://gitpod.io/#https://github.com/postlund/pyatv)
[![Downloads](https://static.pepy.tech/badge/pyatv)](https://pepy.tech/project/pyatv)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/pyatv.svg)](https://pypi.python.org/pypi/pyatv/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This is an asyncio python library for interacting with Apple TV and AirPlay devices. It mainly
targets Apple TVs (all generations, **including tvOS 15 and later**), but also supports audio streaming via AirPlay
to receivers like the HomePod, AirPort Express and third-party speakers. It can act as remote control to the Music
app/iTunes in macOS.

**NEW**: This library can now also emulate an Apple TV device, allowing you to receive commands from the Apple TV Remote app!

All the documentation you need is available at **[pyatv.dev](https://pyatv.dev)**.

# What can it do?

Some examples include:

* Remote control commands
* Metadata retrieval with push updates
* Stream files via AirPlay
* List and launch installed apps
* List and switch user accounts
* Add, remove or set audio output devices (e.g. HomePods)
* Keyboard support
* Persistent storage of credentials and settings

...and lots more! A complete list is available [here](https://pyatv.dev/documentation/supported_features/).

# Installation

## Installing from GitHub

**Note:** This fork (pyatv-opposite) is not available on PyPI. You must install it directly from GitHub.

Install the latest version from the main branch:

```shell
pip install git+https://github.com/bluepig600/pyatv-opposite.git
```

Or install a specific branch:

```shell
pip install git+https://github.com/bluepig600/pyatv-opposite.git@refs/heads/<branch_name>
```

Or install from a specific commit:

```shell
pip install git+https://github.com/bluepig600/pyatv-opposite.git@<commit_hash>
```

For development, you can clone the repository and install in editable mode:

```shell
git clone https://github.com/bluepig600/pyatv-opposite.git
cd pyatv-opposite
pip install -e .
```

# Great, but how do I use it?

All documentation (especially for developers) are available at [pyatv.dev](https://pyatv.dev).
After installation (see [Installation](#installation) section above), you can set up a new device using `atvremote`:

```raw
$ atvremote wizard
Looking for devices...
Found the following devices:
    Name                      Model                    Address
--  ------------------------  -----------------------  -----------
 1  Receiver+                 airupnp                  10.0.10.200
 2  Receiver                  RX-V773                  10.0.10.82
 3  Pierre's AirPort Express  AirPort Express (gen 2)  10.0.10.168
 4  FakeATV                   Unknown                  10.0.10.254
 5  Vardagsrum                Apple TV 4K              10.0.10.81
 6  Apple TV                  Apple TV 3               10.0.10.83
Enter index of device to set up (q to quit): 4
Starting to set up FakeATV
Starting to pair Protocol.MRP
Enter PIN on screen: 1111
Successfully paired Protocol.MRP, moving on...
Pairing finished, trying to connect and get some metadata...
Currently playing:
  Media type: Music
Device state: Playing
       Title: Never Gonna Give You Up
      Artist: Rick Astley
    Position: 1/213s (0.0%)
      Repeat: Off
     Shuffle: Off
Device is now set up!
```

After setting up a new device, other commands can be run directly:

```raw
$ atvremote -s 10.0.10.254 playing
  Media type: Music
Device state: Playing
       Title: Never Gonna Give You Up
      Artist: Rick Astley
    Position: 1/213s (0.0%)
      Repeat: Off
     Shuffle: Off
$ atvremote -s 10.0.10.254 pause
$ atvremote -n FakeATV play
```

## Running as an Apple TV Server (Fake Apple TV)

One of the most powerful features of pyatv is the ability to emulate an Apple TV device. This allows you to:

- **Receive commands** from the Apple TV Remote app on iOS/iPadOS/macOS
- **Test integrations** without physical Apple TV hardware
- **Develop and debug** Apple TV control applications
- **Build custom media servers** that appear as Apple TV devices on your network

### Quick Start

After installing pyatv from GitHub (see [Installation](#installation) section above), start a fake Apple TV server:

```raw
$ atvserver --name "My Fake Apple TV" --mrp --airplay
INFO - Added MRP service
INFO - Added AirPlay service
INFO - Fake Apple TV server started
INFO - Publishing My Fake Apple TV._mediaremotetv._tcp.local. on port 49152
INFO - Publishing My Fake Apple TV._airplay._tcp.local. on port 49153
INFO - All services published via mDNS
INFO - Server 'My Fake Apple TV' is running. Press Ctrl+C to stop.
```

The fake Apple TV will now appear in the Apple TV Remote app on iOS devices on the same network!

### Command Line Options

The `atvserver` command supports the following options:

**Protocol Options:**
- `--mrp`: Enable Media Remote Protocol (for Apple TV 4 and later). Allows remote control.
- `--airplay`: Enable AirPlay protocol. Allows video/audio streaming.
- `--dmap`: Enable DMAP protocol (for Apple TV 3 and earlier). Legacy remote control.
- `--companion`: Enable Companion protocol. For device pairing and authentication.
- `--raop`: Enable RAOP (Remote Audio Output Protocol). For audio streaming.
- `--all`: Enable all protocols at once.

**Server Options:**
- `--name <name>`: Set custom device name (default: "Fake Apple TV")
- `--id <identifier>`: Set custom unique identifier (default: auto-generated UUID)
- `--debug`: Enable debug logging to see detailed protocol information

**Common Usage Examples:**

```shell
# Basic fake Apple TV with remote control and streaming
$ atvserver --name "Living Room TV" --mrp --airplay

# Enable all protocols for maximum compatibility
$ atvserver --name "Test Device" --all

# Legacy Apple TV 3 emulation
$ atvserver --name "Old Apple TV" --dmap

# Debug mode to see all protocol interactions
$ atvserver --name "Debug TV" --mrp --debug
```

### Programmatic Usage

You can also create a fake Apple TV server in your Python code. This is useful for:
- Building automated tests
- Creating custom integrations
- Embedding a fake Apple TV in your application

**Basic Example:**

```python
import asyncio
from pyatv.const import Protocol
from pyatv.fake_device import FakeAppleTV

async def main():
    loop = asyncio.get_event_loop()
    
    # Create a fake Apple TV instance
    fake_atv = FakeAppleTV(loop, test_mode=False)
    
    # Add services (protocols) you want to support
    fake_atv.add_service(Protocol.MRP)
    fake_atv.add_service(Protocol.AirPlay)
    
    # Start the server
    await fake_atv.start()
    
    # Server is now running and discoverable on the network
    print(f"Fake Apple TV running on port {fake_atv.get_port(Protocol.MRP)}")
    
    # Keep running until interrupted
    try:
        await asyncio.Event().wait()
    except KeyboardInterrupt:
        await fake_atv.stop()

asyncio.run(main())
```

**Advanced Example:**

For more advanced usage including setting initial media state, monitoring commands, and customizing behavior, see the examples:
- `examples/server.py` - Basic server setup with logging
- `examples/advanced_server.py` - Advanced usage with custom state and monitoring

### Testing and Development

The fake Apple TV feature is particularly useful for:

1. **Integration Testing**: Test your Apple TV control code without physical hardware
2. **CI/CD Pipelines**: Run automated tests against a fake device in your continuous integration
3. **Protocol Development**: Experiment with Apple TV protocols without affecting real devices
4. **Demo and Presentations**: Show Apple TV functionality without requiring actual hardware

## Using Docker (Original pyatv)

**Note:** Pre-built Docker images are only available for the original pyatv project, not this fork. You can use the original images to test basic functionality:

```raw
docker run -it --rm --network=host ghcr.io/postlund/pyatv:0.14.0 atvremote scan
```

The `master` tag points to latest commit on the `master` branch and `latest` points to the latest release.

To use this fork with Docker, you'll need to build your own image using the provided Dockerfile.

# I need to change something?

Want to help out with `pyatv-opposite`? You can fork this repository and submit pull requests!

For the original `pyatv` project, you can use the Gitpod environment:

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/postlund/pyatv)

# Shortcuts to the good stuff

To save you some time, here are some shortcuts:

* [Getting started](https://pyatv.dev/documentation/getting-started/)
* [Documentation](https://pyatv.dev/documentation)
* [Development](https://pyatv.dev/development)
* [API Reference](https://pyatv.dev/api)
* [Support](https://pyatv.dev/support)
