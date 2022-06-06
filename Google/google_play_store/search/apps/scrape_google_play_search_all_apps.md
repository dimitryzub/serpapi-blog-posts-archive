- <a href="#what_will_be_scraped">What will be scraped</a>
- <a href="#prerequisites">Prerequisites</a>
- <a href="#full_code">Full Code</a>
- <a href="#links">Links</a>
- <a href="#outro">Outro</a>

___


<h2 id="what_will_be_scraped">What will be scraped</h2>

![image](https://user-images.githubusercontent.com/78694043/162396869-3cb624a0-527b-46db-80e0-5950fa39e466.png)

📌Note: this blog post shows how to scrape 50 results without using pagination. The follow-up blog post will be about scraping all available results with pagination.

<h2 id="prerequisites">Prerequisites</h2>

**Basic knowledge scraping with CSS selectors**

CSS selectors declare which part of the markup a style applies to thus allowing to extract data from matching tags and attributes.

If you haven't scraped with CSS selectors, there's a dedicated blog post of mine about [how to use CSS selectors when web-scraping](https://serpapi.com/blog/web-scraping-with-css-selectors-using-python/) that covers what it is, pros and cons, and why they're matter from a web-scraping perspective and show the most common approaches of using CSS selectors when web scraping.


**Separate virtual environment**

In short, it's a thing that creates an independent set of installed libraries, including different Python versions that can coexist with each other in the same system, thus preventing libraries or Python version conflicts.

If you didn't work with a virtual environment before, have a look at the dedicated [Python virtual environments tutorial using Virtualenv and Poetry](https://serpapi.com/blog/python-virtual-environments-using-virtualenv-and-poetry/) blog post of mine to get familiar.

📌Note: this is not a strict requirement for this blog post.

**Install libraries**:

```lang-none
pip install requests lxml beautifulsoup4 google-search-results
```

**Reduce the chance of being blocked**

There's a chance that a request might be blocked. Have a look at [how to reduce the chance of being blocked while web-scraping](https://serpapi.com/blog/how-to-reduce-chance-of-being-blocked-while-web/), there are eleven methods to bypass blocks from most websites.

___

<h2 id="full_code">Full Code</h2>

```python
from bs4 import BeautifulSoup
import requests, json, lxml, re


def bs4_scrape_all_google_play_store_search_apps(
                                          query: str, 
                                          filter_by: str = "apps",
                                          country: str = "US"):
    params = {
        "q": query,     # search query
        "gl": country,  # country of the search. Different country display different apps.
        "c": filter_by  # filter to display list of apps. Other filters: apps, books, movies
    }

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
```

## Explanation

Import libraries:

```python
from bs4 import BeautifulSoup
import requests, json, lxml, re
```

|Library|Purpose|
|-------|-------|
|`BeautifulSoup`|to parse HTML/XML documents.|
|`requests`|to make a request to the destination website and pass the response to `BeautifulSoup`.|
|`json`|to convert parsed data to JSON format.|
|`lxml`|fast HTML/XML parser that used by `BeautifulSoup`.|
|`re`|to match parts of text via regular expression.|


Define a function:

```python
def bs4_scrape_all_google_play_store_search_apps(
                                          query: str, 
                                          filter_by: str = "apps",
                                          country: str = "US"):
    # further code
```

|Fucntion argument|Explanation|
|----|-----------|
|`query: str`|`query` parameter should be a `string`|
| `filter_by: str = "apps"`|`filted_by` should be a `string` with default value of `"apss"` which is defined with `=`|
| `country: str = "US"`|`country` should be a `string` with default value of `"US"` which is defined with `=`|


Create [request headers](https://docs.python-requests.org/en/master/user/quickstart/#custom-headers) and [URL parameters](https://docs.python-requests.org/en/master/user/quickstart/#passing-parameters-in-urls) that will be passed to the request: 

```python
# https://docs.python-requests.org/en/master/user/quickstart/#passing-parameters-in-urls
params = {
    "q": query,     # search query
    "gl": country,  # country of the search. Different country display different apps.
    "c": filter_by  # filter to display a list of apps. Other filters: apps, books, movies
}

# https://docs.python-requests.org/en/master/user/quickstart/#custom-headers
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.79 Safari/537.36",
}
```

Pass requests headers, URL parameters, make a request and pass response to `BeautifulSoup`:

```python
html = requests.get("https://play.google.com/store/search", params=params, headers=headers, timeout=30)
soup = BeautifulSoup(html.text, "lxml")
```

- [`timeout=30`](https://docs.python-requests.org/en/master/user/quickstart/#timeouts) will tell `reuests` to stop waiting for response after 30 seconds.


Create a temporary `list`, iterate over the "container" with all the data, and extract it:

```python
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
		# Rated 3.9 stars out of five stars - > 3.9
		rating = re.search(r"\d{1}\.\d{1}", app.select_one(".pf5lIe div[role=img]")["aria-label"]).group()
	except:
		rating = None
	
	thumbnail = app.select_one(".yNWQ8e img")["data-src"]
```

|Code|Exmplanation|
|----|------------|
|`select()`|return a `list` of matches.|
|`select_one()`|return a single match.|
|`["href"]`|grabs href attribute.|
|`re.search(r"\d{1}\.\d{1}"`|to grab just digit number from the whole string.|
|`group()`|to return the string matched by the regular expression `re`.|


Append extracted data to the temporary `list` as a dictionary and `print` extracted data:

```python
apps_data.append({
		"title": title,
		"company": company,
		"description": description,
		"rating": float(rating) if rating else rating, # make rating float if the rating is not None else rating or None
		"app_link": app_link,
		"developer_link": developer_link,
		"app_id": app_id,
		"developer_id": developer_id,
		"thumbnail": thumbnail
	})        

print(json.dumps(apps_data, indent=2, ensure_ascii=False))
```

|Code|Explanation|
|----|-----------|
|[`json.dumps()`](https://docs.python.org/3/library/json.html#json.dumps)|to ~~convert~~ serialize `obj` e.g. `list`, `dict` to JSON string using such [conversion table](https://docs.python.org/3/library/json.html#py-to-json-table).|
|`indent=2`|to specify the indentation value.|
|`ensure_ascii=False`|to display ASCII characters as-is. For example, to output Chinese characters (漢字) and not unicode chars.|

Part of the output: 
```json
[
  {
    "title": "Google Maps",
    "company": "Google LLC",
    "description": "Real-time GPS navigation & local suggestions for food, events, & activities",
    "rating": 3.9,
    "app_link": "https://play.google.com/store/apps/details?id=com.google.android.apps.maps",
    "developer_link": "https://play.google.com/store/apps/dev?id=5700313618786177705",
    "app_id": "com.google.android.apps.maps",
    "developer_id": "5700313618786177705",
    "thumbnail": "https://play-lh.googleusercontent.com/Kf8WTct65hFJxBUDm5E-EpYsiDoLQiGGbnuyP6HBNax43YShXti9THPon1YKB6zPYpA=s128-rw"
  },
  {
    "title": "Google Maps Go",
    "company": "Google LLC",
    "description": "Get real-time traffic, directions, search and find places",
    "rating": 4.3,
    "app_link": "https://play.google.com/store/apps/details?id=com.google.android.apps.mapslite",
    "developer_link": "https://play.google.com/store/apps/dev?id=5700313618786177705",
    "app_id": "com.google.android.apps.mapslite",
    "developer_id": "5700313618786177705",
    "thumbnail": "https://play-lh.googleusercontent.com/0uRNRSe4iS6nhvfbBcoScHcBTx1PMmxkCx8rrEsI2UQcQeZ5ByKz8fkhwRqR3vttOg=s128-rw"
  },
  {
    "title": "Waze - GPS, Maps, Traffic Alerts & Live Navigation",
    "company": "Waze",
    "description": "Save time on every drive. Waze tells you about traffic, police, crashes & more",
    "rating": 4.4,
    "app_link": "https://play.google.com/store/apps/details?id=com.waze",
    "developer_link": "https://play.google.com/store/apps/developer?id=Waze",
    "app_id": "com.waze",
    "developer_id": "Waze",
    "thumbnail": "https://play-lh.googleusercontent.com/muSOyE55_Ra26XXx2IiGYqXduq7RchMhosFlWGc7wCS4I1iQXb7BAnnjEYzqcUYa5oo=s128-rw"
  }, ... other results
]
```

____

As an alternative solution could be to use [Google Play Apps Store API](https://serpapi.com/google-play-apps).

The difference is that there's no need to figure out how to make a parser, maintain it, figure out how bypass blocks from the websites, and understand how to scale it.

Code to integrate:

```python
from serpapi import GoogleSearch
import json, os


def serpapi_scrape_all_google_play_store_apps():
    params = {
        "api_key": os.getenv("API_KEY"),  # your serpapi api key
        "engine": "google_play",          # search engine
        "hl": "en",                       # language
        "store": "apps",                  # apps search
        "gl": "us",                       # contry to search from. Different country displays different.
        "q": "weather"                    # search qeury
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
```

Part of the output:

```json
[
  {
    "title": "Google Maps",
    "link": "https://play.google.com/store/apps/details?id=com.google.android.apps.maps",
    "description": "Real-time GPS navigation & local suggestions for food, events, & activities",
    "product_id": "com.google.android.apps.maps",
    "rating": 3.9,
    "thumbnail": "https://play-lh.googleusercontent.com/Kf8WTct65hFJxBUDm5E-EpYsiDoLQiGGbnuyP6HBNax43YShXti9THPon1YKB6zPYpA=s128-rw"
  },
  {
    "title": "Google Maps Go",
    "link": "https://play.google.com/store/apps/details?id=com.google.android.apps.mapslite",
    "description": "Get real-time traffic, directions, search and find places",
    "product_id": "com.google.android.apps.mapslite",
    "rating": 4.3,
    "thumbnail": "https://play-lh.googleusercontent.com/0uRNRSe4iS6nhvfbBcoScHcBTx1PMmxkCx8rrEsI2UQcQeZ5ByKz8fkhwRqR3vttOg=s128-rw"
  },
  {
    "title": "Waze - GPS, Maps, Traffic Alerts & Live Navigation",
    "link": "https://play.google.com/store/apps/details?id=com.waze",
    "description": "Save time on every drive. Waze tells you about traffic, police, crashes & more",
    "product_id": "com.waze",
    "rating": 4.4,
    "thumbnail": "https://play-lh.googleusercontent.com/muSOyE55_Ra26XXx2IiGYqXduq7RchMhosFlWGc7wCS4I1iQXb7BAnnjEYzqcUYa5oo=s128-rw"
  }, ... other results
]
```

___


<h2 id="links">Links</h2>

- [Code in the onlie IDE](https://replit.com/@DimitryZub1/Scrape-All-Apps-from-Google-App-Store-Search#main.py)

___

<h2 id="outro">Outro</h2>

If you have anything to share, any questions, suggestions, or something that isn't working correctly, reach out via Twitter at [@dimitryzub](https://twitter.com/DimitryZub) or [@serp_api](https://twitter.com/serp_api).

Yours,
Dmitriy, and the rest of the SerpApi Team.


<p style="text-align: center;">Join us on <a href="https://twitter.com/serp_api">Twitter</a> | <a href="https://www.youtube.com/channel/UCUgIHlYBOD3yA3yDIRhg_mg">YouTube</a></p>


<p style="text-align: center;">Add a  <a href="https://github.com/serpapi/public-roadmap/issues">Feature Request</a>💫 or a <a href="https://github.com/serpapi/public-roadmap/issues">Bug</a>🐞</p>