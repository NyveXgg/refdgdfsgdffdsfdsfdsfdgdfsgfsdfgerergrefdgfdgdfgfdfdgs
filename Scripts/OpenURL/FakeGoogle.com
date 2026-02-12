import webbrowser

url = "https://localgoogle.netlify.app"
webbrowser.open(url)
