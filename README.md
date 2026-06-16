# Tuya PC Power Bridge

A small local Python bridge for controlling a Tuya/Smart Life PC power/reset card over LAN using TinyTuya.

This is intended for cases where:

- A remote gaming, VR, or Parsec PC needs to be powered on remotely.
- The PC sometimes crashes and needs a reset.
- Smart Life/Tuya sharing is blocked by different regional data centres.
- You want your own private web portal instead of sharing Smart Life accounts.

Tested with a Tuya-based PC power card reporting as:

- Model: `JH-PcMini`
- Tuya protocol version: `3.5`
- Power control: DPS `1`
- Reset control: DPS `101 = "forceReset"`

## What it does

The local service provides a simple web page with:

- Login
- Power On
- Power Off
- Reset
- Basic action logging

The service runs on a machine inside your home network and talks directly to the Tuya device over LAN.

```text
Remote user
    ↓
Private web portal / tunnel / VPN
    ↓
Always-on local bridge machine
    ↓
TinyTuya
    ↓
Tuya PC power card
    ↓
Motherboard power/reset pins
```

## Important safety warning

Do **not** expose this directly to the public internet with router port forwarding.

Recommended access methods:

- Cloudflare Tunnel
- Tailscale
- WireGuard VPN
- A website command queue where this bridge polls your web server

## What you need

- A Tuya/Smart Life compatible PC power/reset card
- The device IP address
- Device ID
- Local Key
- Protocol version, usually `3.5`
- Python 3.10+ for development/building
- An always-on machine on the same LAN as the Tuya device

## Finding the Tuya details

Install TinyTuya:

```bash
pip install tinytuya
```

Scan your network:

```bash
python -m tinytuya scan
```

Run the wizard to pull local keys:

```bash
python -m tinytuya wizard
```

You will likely need a Tuya IoT developer account and a linked Smart Life account.

## Device command mapping

For the tested Tuya PC power card:

```python
# Power on
d.set_value(1, True)

# Power off
d.set_value(1, False)

# Reset / force reset
d.set_value(101, "forceReset")
```

## Setup

1. Copy `config.example.json` to `config.json`.
2. Edit `config.json` with your device details and password hashes.
3. Install requirements:

```bash
pip install -r requirements.txt
```

4. Generate password hashes:

```bash
python setup_users.py
```

5. Run the service:

```bash
python app.py
```

6. Open:

```text
http://127.0.0.1:8787
```

## Building a Windows EXE

Run:

```bat
build_exe.bat
```

The EXE will be created in:

```text
dist\PCSwitchService.exe
```

Keep `config.json` next to the EXE when running it.

## Do not commit secrets

Never commit:

- `config.json`
- `tinytuya.json`
- `devices.json`
- `snapshot*.json`
- `tuya-raw.json`
- local keys
- Tuya API keys/secrets
- real IP addresses if you want privacy
- action logs

## Licence

MIT
