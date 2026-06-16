from __future__ import annotations

import json
import time
from datetime import datetime
from pathlib import Path
from functools import wraps

import tinytuya
from flask import Flask, request, redirect, url_for, session, render_template_string, flash
from werkzeug.security import check_password_hash

BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / "config.json"
LOG_PATH = BASE_DIR / "actions.log"

def load_config() -> dict:
    if not CONFIG_PATH.exists():
        raise FileNotFoundError("config.json is missing. Copy config.example.json to config.json and edit it.")
    with CONFIG_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)

config = load_config()

app = Flask(__name__)
app.secret_key = config["app_secret"]

DEVICE_ID = config["tuya"]["device_id"]
DEVICE_IP = config["tuya"]["device_ip"]
LOCAL_KEY = config["tuya"]["local_key"]
VERSION = float(config["tuya"].get("version", 3.5))

def get_device():
    d = tinytuya.OutletDevice(DEVICE_ID, DEVICE_IP, LOCAL_KEY)
    d.set_version(VERSION)
    d.set_socketTimeout(5)
    return d

def log_action(username: str, action: str, result: object):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(f"{timestamp} | {username} | {action} | {result}\n")

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("login"))
        return func(*args, **kwargs)
    return wrapper

def allowed_user(username: str, password: str) -> bool:
    users = config.get("users", {})
    if username not in users:
        return False
    return check_password_hash(users[username]["password_hash"], password)

PAGE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>PC Switch Control</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body { font-family: system-ui, sans-serif; background:#121212; color:#eee; margin:0; }
    main { max-width: 520px; margin: 40px auto; padding: 24px; }
    .card { background:#1e1e1e; border:1px solid #333; border-radius:18px; padding:24px; box-shadow:0 8px 30px #0008; }
    h1 { margin-top:0; font-size:1.6rem; }
    .status { padding:14px; border-radius:12px; background:#262626; margin:16px 0; }
    button, input { width:100%; padding:14px; border-radius:12px; border:0; margin:8px 0; font-size:1rem; }
    input { box-sizing:border-box; background:#111; color:#eee; border:1px solid #444; }
    button { cursor:pointer; font-weight:700; }
    .on { background:#20c05c; color:#071b0d; }
    .off { background:#ff5b5b; color:#220000; }
    .reset { background:#ffc857; color:#231600; }
    .logout { background:#444; color:#eee; }
    .msg { padding:10px; background:#333; border-radius:10px; margin:10px 0; }
    small { color:#aaa; overflow-wrap:anywhere; }
  </style>
</head>
<body><main><div class="card">
  {% with messages = get_flashed_messages() %}
    {% if messages %}{% for m in messages %}<div class="msg">{{ m }}</div>{% endfor %}{% endif %}
  {% endwith %}
  {{ content|safe }}
</div></main></body></html>
"""

@app.route("/", methods=["GET"])
@login_required
def index():
    status_text = "Unknown"
    raw = ""
    try:
        result = get_device().status()
        raw = str(result)
        dps = result.get("dps", {})
        if dps.get("1") is True:
            status_text = "ON"
        elif dps.get("1") is False:
            status_text = "OFF"
    except Exception as e:
        raw = repr(e)
        status_text = "ERROR"

    content = f"""
    <h1>PC Power Bridge</h1>
    <p>Logged in as <b>{session['user']}</b></p>
    <div class="status"><b>Status:</b> {status_text}<br><small>{raw}</small></div>
    <form method="post" action="/action">
      <button class="on" name="action" value="power_on">Power On</button>
      <button class="off" name="action" value="power_off">Power Off</button>
      <button class="reset" name="action" value="reset" onclick="return confirm('Reset the PC now?')">Reset</button>
    </form>
    <form method="post" action="/logout"><button class="logout">Logout</button></form>
    """
    return render_template_string(PAGE, content=content)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        if allowed_user(username, password):
            session["user"] = username
            return redirect(url_for("index"))
        flash("Wrong username or password.")
    content = """
    <h1>Login</h1>
    <form method="post">
      <input name="username" placeholder="Username" autocomplete="username">
      <input name="password" type="password" placeholder="Password" autocomplete="current-password">
      <button class="on">Login</button>
    </form>
    """
    return render_template_string(PAGE, content=content)

@app.route("/logout", methods=["POST"])
@login_required
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/action", methods=["POST"])
@login_required
def action():
    action_name = request.form.get("action", "")
    d = get_device()
    try:
        if action_name == "power_on":
            result = d.set_value(1, True)
        elif action_name == "power_off":
            result = d.set_value(1, False)
        elif action_name == "reset":
            result = d.set_value(101, "forceReset")
        else:
            flash("Unknown action.")
            return redirect(url_for("index"))
        log_action(session["user"], action_name, result)
        flash(f"Sent command: {action_name}")
    except Exception as e:
        log_action(session.get("user", "?"), action_name, repr(e))
        flash(f"Command failed: {e}")
    time.sleep(0.5)
    return redirect(url_for("index"))

if __name__ == "__main__":
    host = config.get("host", "127.0.0.1")
    port = int(config.get("port", 8787))
    app.run(host=host, port=port)
