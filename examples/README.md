# pyatv Examples

This directory contains practical examples demonstrating how to use the pyatv library to interact with Apple TV and AirPlay devices.

## Setting Up Python Library

### Installation

1. **Install Python 3.9 or higher** (check with `python --version`)

2. **Create a virtual environment** (recommended):
   ```bash
   # Navigate to your project directory
   cd your_project_directory
   
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install pyatv:**
   ```bash
   pip install pyatv
   ```

4. **Verify installation:**
   ```bash
   python -c "import pyatv; print(pyatv.const.__version__)"
   ```

### Creating Your First Script

Create a new Python file (e.g., `my_atv_script.py`):

```python
import asyncio
import pyatv

async def main():
    # Scan for devices
    print("Scanning for Apple TV devices...")
    devices = await pyatv.scan(asyncio.get_event_loop(), timeout=5)
    
    if not devices:
        print("No devices found")
        return
    
    print(f"Found {len(devices)} device(s)")
    
    # Connect to first device
    print(f"Connecting to {devices[0].name}...")
    atv = await pyatv.connect(devices[0], asyncio.get_event_loop())
    
    try:
        # Get what's currently playing
        playing = await atv.metadata.playing()
        print("\nCurrently playing:")
        print(playing)
    finally:
        atv.close()

if __name__ == "__main__":
    asyncio.run(main())
```

Run your script:
```bash
python my_atv_script.py
```

### Project Structure

For larger projects, organize your code like this:

```
your_project/
├── venv/                 # Virtual environment (don't commit)
├── src/
│   ├── __init__.py
│   └── atv_controller.py # Your pyatv code
├── requirements.txt      # Dependencies
└── main.py              # Entry point
```

Create a `requirements.txt`:
```
pyatv>=0.14.0
```

Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Examples

Before running any examples, make sure you have:

1. **Completed the setup above** (installed pyatv in a virtual environment)

2. **Network access** to Apple TV/AirPlay devices on your local network

### Quick Start

The easiest way to get started is with the automatic connection example:

```bash
python auto_connect.py
```

This will automatically discover a device on your network and show what's currently playing.

## Examples Overview

### Basic Connection Examples

#### `scan_and_connect.py` - Simplest Example
The most basic example showing how to scan for devices and connect.

```bash
python scan_and_connect.py
```

**What it does:**
- Scans the network for Apple TV devices
- Connects to the first device found
- Prints what's currently playing

**Best for:** Understanding the basic connection flow

---

#### `auto_connect.py` - Automatic Discovery
Demonstrates the helper function that simplifies connection.

```bash
python auto_connect.py
```

**What it does:**
- Automatically discovers and connects to a device
- Uses the `helpers.auto_connect()` convenience function

**Best for:** Quick prototyping and simple scripts

---

#### `manual_connect.py` - Manual Configuration
Shows how to connect when you already know the device details.

```bash
python manual_connect.py
```

**What it does:**
- Connects without scanning by manually specifying address and credentials
- Useful when device discovery isn't working or for faster connections

**Best for:** Production environments with known device configurations

**Note:** Edit the script to set `ADDRESS`, `NAME`, and `HSGID` for your device

---

### Credential Management

#### `pairing.py` - Device Pairing
Demonstrates the pairing process to obtain credentials.

```bash
python pairing.py
```

**What it does:**
- Scans for devices that support pairing
- Initiates pairing process
- Prompts for PIN code displayed on the Apple TV
- Outputs credentials for future use

**Best for:** First-time setup with a new device

**Important:** You'll need to enter the PIN code shown on your Apple TV screen

---

#### `connect_with_credentials.py` - Saved Credentials
Shows how to store and reuse credentials for multiple devices.

```bash
python connect_with_credentials.py 0
```

**What it does:**
- Uses predefined credentials from a configuration
- Connects to device by index (0 for first device, 1 for second, etc.)

**Best for:** Managing multiple devices with saved credentials

**Note:** Edit the `DEVICES` list in the script to add your devices

---

#### `storage.py` - File-Based Storage
Uses pyatv's built-in file storage for credentials.

```bash
python storage.py <device_ip_address>
```

**Example:**
```bash
python storage.py 10.0.0.50
```

**What it does:**
- Loads credentials from pyatv's default storage location
- Same storage used by `atvremote` command-line tool
- Connects to device at specified IP address

**Best for:** Integration with atvremote or shared credential storage

---

### Streaming Examples

#### `play_url.py` - Stream Video URL
Streams a video URL to an Apple TV via AirPlay.

```bash
python play_url.py <device_id> <airplay_credentials> <video_url>
```

**Example:**
```bash
python play_url.py aabbccddeeff abc123def456 http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4
```

**What it does:**
- Connects to specified device
- Streams video from URL via AirPlay

**Best for:** Casting online videos to Apple TV

**Note:** You need AirPlay credentials from pairing first

---

#### `stream.py` - Stream Local File with Updates
Streams a local file and prints status updates.

```bash
python stream.py <device_ip> <filename>
```

**Example:**
```bash
python stream.py 10.0.0.50 music.mp3
```

**What it does:**
- Streams a local audio/video file
- Listens for playback status updates
- Prints updates as media plays

**Best for:** Streaming local media files and monitoring playback

---

### Server Examples (Emulate Apple TV)

#### `server.py` - Basic Fake Apple TV
Creates a fake Apple TV that other devices can connect to.

```bash
python server.py
```

**What it does:**
- Starts a fake Apple TV server
- Enables MRP and AirPlay protocols
- Accepts remote control commands from iOS Remote app

**Best for:** Testing clients, home automation, or understanding the protocol

**Try it:**
1. Run the server
2. Use `atvremote -s 127.0.0.1:<port> playing` to test
3. Or connect with the Apple TV Remote app on iOS

---

#### `advanced_server.py` - Customized Fake Apple TV
Advanced server example with custom media state.

```bash
python advanced_server.py
```

**What it does:**
- Creates a fake Apple TV with custom initial state
- Sets up "Big Buck Bunny" as currently playing media
- Responds to remote control commands (play, pause, etc.)
- Logs received commands

**Best for:** Testing specific scenarios or building custom Apple TV emulators

---

### Web Application Example

#### `tutorial.py` - Complete Web Application
A full-featured web application demonstrating multiple pyatv features.

```bash
python tutorial.py
```

**What it does:**
- Starts a web server on http://127.0.0.1:8080
- Provides REST API endpoints for:
  - Scanning devices: `GET /scan`
  - Connecting: `GET /connect/<device_id>`
  - Remote control: `GET /remote_control/<device_id>/<command>`
  - Current status: `GET /playing/<device_id>`
  - Live updates: `GET /state/<device_id>` (WebSocket)

**Best for:** Building web-based remote controls or home automation interfaces

**See the full tutorial:** https://pyatv.dev/documentation/tutorial/

---

## Common Use Cases

### Just Want to Control Your Apple TV?
Use the `atvremote` command-line tool (included with pyatv):

```bash
# Set up a device (run once)
atvremote wizard

# Control the device
atvremote -n "Living Room" play
atvremote -n "Living Room" pause
atvremote -n "Living Room" playing
```

### Want to Build an Application?
1. Start with `scan_and_connect.py` to understand basics
2. Use `pairing.py` to get credentials
3. Use `storage.py` to manage credentials
4. Check `tutorial.py` for a complete application example

### Want to Test Your Client?
Use `server.py` or `advanced_server.py` to create a fake Apple TV for testing.

### Want to Stream Media?
- Use `play_url.py` for online videos
- Use `stream.py` for local files

## Troubleshooting

### No Devices Found
- Ensure your Apple TV is on the same network
- Check that multicast/mDNS is enabled on your network
- Try specifying the IP address directly (see `storage.py` or `manual_connect.py`)

### Connection Fails
- Make sure you've paired with the device first (see `pairing.py`)
- Check that credentials are correct
- Verify the device is awake (not in deep sleep)

### Pairing Issues
- Make sure you enter the PIN code quickly (it expires)
- Some protocols don't require pairing (like older DMAP)
- Try pairing with the `atvremote wizard` command first

### Import Errors
Make sure pyatv is installed:
```bash
pip install pyatv
```

## Additional Resources

- **Full Documentation:** https://pyatv.dev
- **Getting Started Guide:** https://pyatv.dev/documentation/getting-started/
- **API Reference:** https://pyatv.dev/api
- **Tutorial:** https://pyatv.dev/documentation/tutorial/
- **GitHub Repository:** https://github.com/postlund/pyatv
- **Report Issues:** https://github.com/postlund/pyatv/issues

## Need Help?

- Check the [FAQ](https://pyatv.dev/support/faq/)
- Read the [troubleshooting guide](https://pyatv.dev/support/troubleshooting/)
- Ask questions in [GitHub Discussions](https://github.com/postlund/pyatv/discussions)
- Report bugs in [GitHub Issues](https://github.com/postlund/pyatv/issues)

## Contributing

Found a bug in an example or have an improvement? Contributions are welcome! 
See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.
