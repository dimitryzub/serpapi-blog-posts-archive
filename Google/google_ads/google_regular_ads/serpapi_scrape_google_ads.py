# scrapes both regular and shopping ads (top, right blocks)

from serpapi import GoogleSearch
import json, os

params = {
    "api_key": os.getenv("API_KEY"),
    "engine": "google",
    "q": "buy coffee",
    "gl": "us",
    "hl": "en"
}

search = GoogleSearch(params)
results = search.get_dict()

if results.get("ads", []):
    for ad in results["ads"]:
        print(json.dumps(ad, indent=2))

if results.get("shopping_results", []):
    for shopping_ad in results["shopping_results"]:
        print(json.dumps(shopping_ad, indent=2))
else:
    print("no shopping ads found.")
