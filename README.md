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

# Quick Start

**Installation:**
```bash
pip install pyatv
```

**For Command-Line Usage** (no coding required):
```bash
# Discover and set up a device
atvremote wizard

# Control your device
atvremote -n "Living Room" playing
atvremote -n "Living Room" play
```

**For Python Development:**
```python
import asyncio
import pyatv

async def main():
    # Discover devices
    devices = await pyatv.scan(asyncio.get_event_loop())
    
    # Connect to first device
    atv = await pyatv.connect(devices[0], asyncio.get_event_loop())
    
    # Print what's playing
    print(await atv.metadata.playing())
    
    atv.close()

asyncio.run(main())
```

See the [examples/](examples/) directory for more code samples, or check the [Getting Started](https://pyatv.dev/documentation/getting-started/) guide for full details.

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

# More Examples

All documentation (especially for developers) is available at [pyatv.dev](https://pyatv.dev).

## Command-Line Tool

The library includes `atvremote`, a command-line tool for controlling devices without writing code:

```raw
$ pip install pyatv
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

## Running as an Apple TV Server

You can also run pyatv as a server that emulates an Apple TV, allowing you to receive commands from the Apple TV Remote app:

```raw
$ pip install pyatv
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

Available server options:
- `--mrp`: Enable Media Remote Protocol (Apple TV 4 and later)
- `--airplay`: Enable AirPlay protocol
- `--dmap`: Enable DMAP protocol (Apple TV 3 and earlier)
- `--companion`: Enable Companion protocol
- `--raop`: Enable RAOP (Remote Audio Output Protocol)
- `--all`: Enable all protocols
- `--name`: Set custom device name
- `--id`: Set custom unique identifier
- `--debug`: Enable debug logging

You can also create a fake Apple TV server programmatically. See `examples/server.py` for a complete example.

```python
import asyncio
from pyatv.const import Protocol
from pyatv.fake_device import FakeAppleTV

async def main():
    loop = asyncio.get_event_loop()
    fake_atv = FakeAppleTV(loop, test_mode=False)
    fake_atv.add_service(Protocol.MRP)
    await fake_atv.start()
    # Server is now running...

asyncio.run(main())
```

You can also run it inside a container (x86_64, aarch64, armv7):

```raw
docker run -it --rm --network=host ghcr.io/postlund/pyatv:0.14.0 atvremote scan
```

The `master` tag points to latest commit on the `master` branch and `latest`
points to the latest release.

# I need to change something?

Want to help out with `pyatv`? Press the button below to get a fully prepared development environment and get started right away!

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/postlund/pyatv)

# Shortcuts to the good stuff

To save you some time, here are some shortcuts:

* **[Examples](examples/)** - Code examples for common tasks
* [Getting started](https://pyatv.dev/documentation/getting-started/)
* [Documentation](https://pyatv.dev/documentation)
* [Development](https://pyatv.dev/development)
* [API Reference](https://pyatv.dev/api)
* [Support](https://pyatv.dev/support)
