# Flowchart

```text
Remote user
    ↓
Private website / tunnel / VPN
    ↓
Always-on local bridge machine
    ↓
TinyTuya over LAN
    ↓
Tuya PC switch device
    ↓
Motherboard power/reset pins
```

## Crash recovery

```text
PC crashes → remote user opens portal → presses Reset → bridge sends DPS 101 = "forceReset" → PC reboots
```

## Power saving

```text
PC off most of the day → remote user presses Power On → bridge sends DPS 1 = True → PC boots → user connects via Parsec
```
