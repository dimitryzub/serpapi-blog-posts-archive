from serpapi import GoogleSearch
import json, os


def serpapi_scrape_all_google_play_store_apps():
    params = {
        "api_key": os.getenv("API_KEY"),  # your serpapi api key
        "engine": "google_play",          # search engine
        "hl": "en",                       # language
        "store": "apps",                  # apps search
        "gl": "us",                       # contry to search from. Different country displays different.
        "q": "maps"                       # search qeury
    }

    search = GoogleSearch(params)  # where data extracts
    results = search.get_dict()    # JSON -> Python dictionary

    apps_data = []

    for apps in results["organic_results"]:
        for app in apps["items"]:
            apps_data.append({
                "title": app.get("title"),
                "link": app.get("link"),
                "description": app.get("description"),
                "product_id": app.get("product_id"),
                "rating": app.get("rating"),
                "thumbnail": app.get("thumbnail"),
                })

    print(json.dumps(apps_data, indent=2, ensure_ascii=False))
    
serpapi_scrape_all_google_play_store_apps()