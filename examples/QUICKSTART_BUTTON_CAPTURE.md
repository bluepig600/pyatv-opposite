# Quick Start: Capture Apple TV Remote Button Presses

Want to see what buttons are pressed on your Apple TV Remote app? Here's the fastest way:

## Step 1: Run the command

```bash
atvproxy mrp
```

That's it! No credentials needed, no setup required.

## Step 2: Connect the Remote app

1. Open the **Apple TV Remote** app on your iPhone/iPad
2. Look for a device named **"Proxy"**
3. Tap it to connect

## Step 3: Press buttons!

Watch your terminal - you'll see output like:

```
>>> BUTTON PRESSED: UP <<<

>>> BUTTON PRESSED: DOWN <<<

>>> BUTTON PRESSED: SELECT <<<

>>> COMMAND: PLAY <<<
```

## That's All!

Every button you press on the Remote app will be printed to your console.

---

## Want More?

- **Custom name**: `atvproxy mrp --name "My Device"`
- **Forward to real Apple TV**: `atvproxy mrp --credentials <creds> --remote-ip <ip>`
- **Full documentation**: See [button_capture.md](button_capture.md)

## Supported Buttons

All standard Apple TV Remote buttons are supported:
- **Navigation**: Up, Down, Left, Right, Select
- **Menu**: Menu, Home, Top Menu
- **Playback**: Play, Pause, Stop, Next, Previous
- **Volume**: Volume Up, Volume Down
- **And more...**

## Stop the Proxy

Press **Enter** or **Ctrl+C** to stop.
