# Apple TV Remote Button Capture

This example shows how to use `atvproxy.py` to capture button presses from the Apple TV Remote app.

## Overview

The `atvproxy` command creates a server that allows the Apple TV Remote app to connect and prints out all button presses to the console.

**NEW: No credentials required!** The proxy now works in standalone mode without needing to connect to a real Apple TV.

## Two Modes of Operation

### 1. Standalone Mode (Recommended - No Credentials Needed)

In this mode, the proxy simply captures button presses without forwarding to a real Apple TV:

```bash
atvproxy mrp
```

That's it! No credentials, no Apple TV needed. Just run the command and connect with the Remote app.

### 2. Proxy Mode (Forward to Real Apple TV)

In this mode, the proxy forwards commands to a real Apple TV while capturing button presses:

```bash
atvproxy mrp --credentials <credentials> --remote-ip <apple_tv_ip>
```

## Quick Start (No Credentials Required)

1. Run the proxy:
```bash
atvproxy mrp
```

2. Open the Apple TV Remote app on your iOS device

3. Look for a device named "Proxy"

4. Tap on it to connect

5. Press buttons and watch them appear in the console!

## Getting MRP Credentials (Only for Proxy Mode)

If you want to forward commands to a real Apple TV, you'll need credentials:

```bash
# Scan for Apple TVs on your network
atvremote scan

# Pair with your Apple TV (you'll need to enter PIN from TV screen)
atvremote --id <your_apple_tv_id> --protocol mrp pair

# After pairing, scan again to see credentials
atvremote scan
```

The credentials will be shown in the format: `<client_id>:<credential>`

## Running the Button Capture

### Standalone Mode (No Apple TV Required)

Just run:
```bash
atvproxy mrp
```

Optional arguments:
```bash
# Custom device name
atvproxy mrp --name "My Button Capture"

# Specify local IP (if multiple network interfaces)
atvproxy mrp --local-ip 192.168.1.50
```

### Proxy Mode (Forward to Apple TV)

Once you have your credentials, start the proxy:

```bash
atvproxy mrp --credentials <credentials> --remote-ip <apple_tv_ip>
```

**Example:**
```bash
atvproxy mrp --credentials 1234567890abcdef:fedcba0987654321 --remote-ip 192.168.1.100
```

The proxy will:
- Start an MRP server on a random port
- Publish itself via mDNS (Bonjour) so the Remote app can discover it
- Connect to your real Apple TV (if in proxy mode)
- Wait for the Remote app to connect

## Connecting the Apple TV Remote App

1. Open the Apple TV Remote app on your iOS device
2. Look for a device named "Proxy" (or the custom name if you used `--name`)
3. Tap on it to connect
4. The proxy will handle authentication automatically

## What You'll See

When you press buttons on the Remote app, you'll see output like:

```
>>> BUTTON PRESSED: UP <<<

>>> BUTTON PRESSED: DOWN <<<

>>> BUTTON PRESSED: SELECT <<<

>>> COMMAND: PLAY <<<

>>> COMMAND: PAUSE <<<
```

## Supported Buttons

The proxy can detect the following buttons:

### Directional Buttons:
- UP
- DOWN
- LEFT
- RIGHT
- SELECT

### Menu Buttons:
- MENU
- HOME
- TOP_MENU

### Media Controls:
- PLAY
- PAUSE
- TOGGLEPLAYPAUSE
- STOP
- NEXTTRACK / NEXT
- PREVIOUSTRACK / PREVIOUS

### Volume:
- VOLUMEUP
- VOLUMEDOWN

### Other:
- SUSPEND
- WAKEUP

## Advanced Options

### Custom Device Name
```bash
atvproxy mrp --name "My Proxy"
```

### Specify Local IP
If you have multiple network interfaces:
```bash
atvproxy mrp --local-ip 192.168.1.50
```

### Proxy Mode with All Options
```bash
atvproxy mrp \
  --credentials 1234567890abcdef:fedcba0987654321 \
  --remote-ip 192.168.1.100 \
  --remote-port 49152 \
  --name "My Proxy" \
  --local-ip 192.168.1.50
```

## How It Works

The proxy uses the Media Remote Protocol (MRP) to communicate with the Remote app:

### Standalone Mode
1. **Discovery**: The proxy publishes itself as an Apple TV device via mDNS
2. **Connection**: The Remote app connects to the proxy thinking it's an Apple TV
3. **Authentication**: The proxy handles HAP pairing automatically
4. **Button Capture**: All button presses are captured and printed
5. **Responses**: The proxy sends success responses back to keep the Remote app happy

### Proxy Mode
1. **Discovery**: The proxy publishes itself as an Apple TV device via mDNS
2. **Connection**: The Remote app connects to the proxy
3. **Authentication**: The proxy handles HAP pairing
4. **Message Forwarding**: All messages are:
   - Received from the Remote app
   - Inspected for button presses (HID events and commands)
   - Forwarded to the real Apple TV
   - Responses are sent back to the Remote app

## Stopping the Proxy

Press `Enter` or `Ctrl+C` to stop the proxy server.

## Troubleshooting

### Remote app doesn't see the proxy
- Make sure you're on the same network as the proxy
- Check that mDNS/Bonjour is working on your network
- Try using the `--local-ip` option to specify your network interface

### Proxy Mode Issues

#### "Connection refused" or "No route to host"
- Make sure the Apple TV IP address is correct
- Verify your Apple TV is turned on and connected to the network

#### "Authentication failed"
- Make sure you're using valid MRP credentials
- Try re-pairing with your Apple TV using `atvremote`

### No button presses are printed
- Make sure the Remote app is connected to the proxy, not directly to the Apple TV
- Check the console for any error messages
- Verify that you selected "Proxy" (or your custom name) in the Remote app

## Use Cases

This button capture functionality can be useful for:

- **Development**: Understanding what commands the Remote app sends
- **Testing**: Verifying button press behavior
- **Debugging**: Troubleshooting Apple TV control issues
- **Learning**: Understanding the MRP protocol
- **Integration**: Building custom Apple TV control systems
