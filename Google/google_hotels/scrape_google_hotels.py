from parsel import Selector
import requests, json, os

# https://docs.python-requests.org/en/master/user/quickstart/#passing-parameters-in-urls
params = {
    "q": "samsung",
    "hl": "en",
    "gl": "us"
}


# https://docs.python-requests.org/en/master/user/quickstart/#custom-headers
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.87 Safari/537.36",
}

html = requests.get("https://www.google.com/travel/hotels", params=params, headers=headers, timeout=30)
selector = Selector(html.text)
