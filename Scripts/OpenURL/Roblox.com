import webbrowser

url = "https://www.roblox.com/de/login"
webbrowser.open(url)
