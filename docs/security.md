# Security Notes

This controls real hardware. Treat it like remote admin access.

Do not port-forward this directly to the public internet.

Use one of:

- Cloudflare Tunnel
- Tailscale
- WireGuard VPN
- Reverse proxy with HTTPS and strong authentication
- Polling command queue from your website

Never commit `config.json`, Tuya local keys, `devices.json`, `tinytuya.json`, `snapshot*.json`, `tuya-raw.json`, or `actions.log`.
