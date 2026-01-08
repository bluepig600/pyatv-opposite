# Apple TV Remote Button Capture

This example shows how to use `atvproxy.py` to capture button presses from the Apple TV Remote app.

## Overview

The `atvproxy` command creates a proxy server that sits between the Apple TV Remote app and your actual Apple TV. When you connect the Remote app to the proxy, it will:

1. Forward all commands to the real Apple TV
2. Print out all button presses to the console
3. Allow you to see what buttons are being pressed in real-time

## Prerequisites

1. An Apple TV on your network
2. MRP credentials for your Apple TV (obtained through pairing)
3. The Apple TV Remote app on iOS/iPadOS

## Getting MRP Credentials

If you don't have MRP credentials yet, you can obtain them using `atvremote`:

```bash
# Scan for Apple TVs on your network
atvremote scan

# Pair with your Apple TV (you'll need to enter PIN from TV screen)
atvremote --id <your_apple_tv_id> --protocol mrp pair

# After pairing, scan again to see credentials
atvremote scan
```

The credentials will be shown in the format: `<client_id>:<credential>`

## Running the Button Capture Proxy

Once you have your credentials, start the proxy:

```bash
atvproxy mrp <credentials> <apple_tv_ip>
```

**Example:**
```bash
atvproxy mrp 1234567890abcdef:fedcba0987654321 192.168.1.100
```

The proxy will:
- Start an MRP server on a random port
- Publish itself via mDNS (Bonjour) so the Remote app can discover it
- Connect to your real Apple TV
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
atvproxy mrp <credentials> <apple_tv_ip> --name "My Proxy"
```

### Specify Local IP
If you have multiple network interfaces:
```bash
atvproxy mrp <credentials> <apple_tv_ip> --local-ip 192.168.1.50
```

### Debug Mode
To see detailed protocol information:
```bash
# The logging is controlled by the script's logging configuration
# Look at the console output for detailed message information
```

## How It Works

The proxy uses the Media Remote Protocol (MRP) to communicate with both the Remote app and the Apple TV:

1. **Discovery**: The proxy publishes itself as an Apple TV device via mDNS
2. **Connection**: The Remote app connects to the proxy thinking it's an Apple TV
3. **Authentication**: The proxy handles HAP pairing automatically
4. **Message Forwarding**: All messages are:
   - Received from the Remote app
   - Inspected for button presses (HID events and commands)
   - Forwarded to the real Apple TV
   - Responses are sent back to the Remote app

## Stopping the Proxy

Press `Enter` or `Ctrl+C` to stop the proxy server.

## Troubleshooting

### "Connection refused" or "No route to host"
- Make sure the Apple TV IP address is correct
- Verify your Apple TV is turned on and connected to the network

### "Authentication failed"
- Make sure you're using valid MRP credentials
- Try re-pairing with your Apple TV using `atvremote`

### Remote app doesn't see the proxy
- Make sure you're on the same network as the proxy
- Check that mDNS/Bonjour is working on your network
- Try using the `--local-ip` option to specify your network interface

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
