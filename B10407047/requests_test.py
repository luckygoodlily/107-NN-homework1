import requests
url = "https://www.google.com/"
data = {"search?q": "cat", "source": "lnms", "tbm": "isch"}
response = requests.get(url)

print(response.text)