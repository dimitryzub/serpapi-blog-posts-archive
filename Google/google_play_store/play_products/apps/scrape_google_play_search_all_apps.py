from bs4 import BeautifulSoup
import requests, json, lxml, re


def bs4_scrape_all_google_play_store_search_apps(
                                          query: str, 
                                          filter_by: str = "apps",
                                          country: str = "US"):
    # https://docs.python-requests.org/en/master/user/quickstart/#passing-parameters-in-urls
    params = {
        "q": query,     # search query
        "gl": country,  # country of the search. Different country display different apps.
        "c": filter_by  # filter to display list of apps. Other filters: apps, books, movies
    }

    # https://docs.python-requests.org/en/master/user/quickstart/#custom-headers
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.79 Safari/537.36",
    }

    html = requests.get("https://play.google.com/store/search", params=params, headers=headers, timeout=30)
    soup = BeautifulSoup(html.text, "lxml")

    apps_data = []

    for app in soup.select(".mpg5gc"):
        title = app.select_one(".nnK0zc").text
        company = app.select_one(".b8cIId.KoLSrc").text
        description = app.select_one(".b8cIId.f5NCO a").text
        app_link = f'https://play.google.com{app.select_one(".b8cIId.Q9MA7b a")["href"]}'
        developer_link = f'https://play.google.com{app.select_one(".b8cIId.KoLSrc a")["href"]}'
        app_id = app.select_one(".b8cIId a")["href"].split("id=")[1]
        developer_id = app.select_one(".b8cIId.KoLSrc a")["href"].split("id=")[1]
        
        try:
            # https://regex101.com/r/SZLPRp/1
            rating = re.search(r"\d{1}\.\d{1}", app.select_one(".pf5lIe div[role=img]")["aria-label"]).group()
        except:
            rating = None
        
        thumbnail = app.select_one(".yNWQ8e img")["data-src"]
        
        apps_data.append({
            "title": title,
            "company": company,
            "description": description,
            "rating": float(rating) if rating else rating, # float if rating is not None else rating or None
            "app_link": app_link,
            "developer_link": developer_link,
            "app_id": app_id,
            "developer_id": developer_id,
            "thumbnail": thumbnail
        })        

    print(json.dumps(apps_data, indent=2, ensure_ascii=False))
    
bs4_scrape_all_google_play_store_search_apps(query="maps", filter_by="apps", country="US")
# bs4_scrape_all_google_play_store_search_apps(query="maps", filter_by="movies", country="US")