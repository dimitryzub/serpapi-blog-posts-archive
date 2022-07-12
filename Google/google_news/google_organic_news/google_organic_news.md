- <a href="#what_will_be_scraped">What will be scraped</a>
- <a href="#prerequisites">Prerequisites</a>
- <a href="#fullcode">Full Code</a>
- <a href="#code_explanation">Code Exmplanation</a>
- <a href="#links">Links</a>

<h2 id="what_will_be_scraped">What will be scraped</h2>

![image](https://user-images.githubusercontent.com/78694043/178466361-261a854e-30fd-4c09-bd11-839be94cfca7.png)


<h2 id="prerequisites">Prerequisites</h2>

**Basic knowledge scraping with CSS selectors**

CSS selectors declare which part of the markup a style applies to thus allowing to extract data from matching tags and attributes.

If you haven't scraped with CSS selectors, there's a dedicated blog post of mine
about [how to use CSS selectors when web-scraping](https://serpapi.com/blog/web-scraping-with-css-selectors-using-python/) that covers what it is, pros and cons, and why they matter from a web-scraping perspective.

**Separate virtual environment**

In short, it's a thing that creates an independent set of installed libraries including different Python versions that can coexist with each other in the same system thus preventing libraries or Python version conflicts.

If you didn't work with a virtual environment before, have a look at the
dedicated [Python virtual environments tutorial using Virtualenv and Poetry](https://serpapi.com/blog/python-virtual-environments-using-virtualenv-and-poetry/) blog post of mine to get a little bit more familiar.


📌Note: this is not a strict requirement for this blog post.

**Install libraries**:

```lang-none
pip install requests bs4 google-search-results
```

`google-search-results` is a SerpApi API package.

**Reduce the chance of being blocked**

There's a chance that a request might be blocked. Have a look
at [how to reduce the chance of being blocked while web-scraping](https://serpapi.com/blog/how-to-reduce-chance-of-being-blocked-while-web/), there are eleven methods to bypass blocks from most websites.

Make sure to pass `user-agent`, because Google might block your requests eventually and you'll receive a different HTML thus empty output. [Check what is your user-agent](https://www.whatismybrowser.com/detect/what-is-my-user-agent).

Basically, `user-agent` let identifies the browser, its version number, and its host operating system that representing a person (browser) in a Web context that lets servers and network peers identify if it's a bot or not. And we're faking "real" user visit.

<h2 id="fullcode">Full Code</h2>

```python
import requests, lxml
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}

params = {
    "q": "gta san andreas",
    "hl": "en",
    "tbm": "nws",
}

response = requests.get("https://www.google.com/search", headers=headers, params=params)
soup = BeautifulSoup(response.text, 'lxml')

for result in soup.select('.dbsr'):
    title = result.select_one('.nDgy9d').text
    link = result.a['href']
    source = result.select_one('.WF4CUc').text
    snippet = result.select_one('.Y3v8qd').text
    date_published = result.select_one('.WG9SHc span').text
    print(f'{title}\n{link}\n{snippet}\n{date_published}\n{source}\n')
```


### Using [Google News Result API](https://serpapi.com/news-results)

The main differences is that it's quickier approach if you don't want to create the parser from scratch and maintain it overtime, and figure out how to scale the number of requests without getting blocked.

```python
from serpapi import GoogleSearch

params = {
  "api_key": "YOUR_API_KEY",
  "engine": "google",
  "q": "gta san andreas",
  "gl": "us",
  "tbm": "nws"
}

search = GoogleSearch(params)
results = search.get_dict()

for result in results['news_results']:
    print(result)
```

Outputs:

```json
{
   "position":1,
   "link":"https://www.sportskeeda.com/gta/5-strange-gta-san-andreas-glitches",
   "title":"5 strange GTA San Andreas glitches",
   "source":"Sportskeeda",
   "date":"9 hours ago",
   "snippet":"GTA San Andreas has a wide assortment of interesting and strange glitches.",
   "thumbnail":"https://serpapi.com/searches/60e71e1f8b7ed2dfbde7629b/images/1394ee64917c752bdbe711e1e56e90b20906b4761045c01a2cefb327f91d40bb.jpeg"
}
```


### Google News Results API with Pagination

If there's a need to extract all results from all pages, SerpApi has a great Python `pagination()` method that iterates over all pages under the hood and returns an iterator:

```python
# https://github.com/serpapi/google-search-results-python
from serpapi import GoogleSearch
import os


params = {
    "engine": "google",
    "q": "coca cola",
    "tbm": "nws",
    "api_key": "YOUR_API_KEY",
}

search = GoogleSearch(params)
pages = search.pagination()

for page in pages:
    print(f"Current page: {page['serpapi_pagination']['current']}")

    for result in page["news_results"]:
        print(f"Title: {result['title']}\nLink: {result['link']}\n")
```


Outputs:
```lang-none
Current page: 1
Title: 5 strange GTA San Andreas glitches
Link: https://www.sportskeeda.com/gta/5-strange-gta-san-andreas-glitches

...

Current page: 14
Title: Ambitious Grand Theft Auto: San Andreas Mod Turns It Into A Spider-Man Game
Link: https://gamerant.com/grand-theft-auto-san-andreas-spider-man-game-mod/
```


<h2 id="links">Links</h2>

- [Code in the online IDE](https://replit.com/@DimitryZub1/Scrape-Google-News-with-Pagination-python-serpapi#main.py)
- [Google News Result API](https://serpapi.com/news-results)


<p style="text-align: center;">Join us on <a href="https://twitter.com/serp_api">Twitter</a> | <a href="https://www.youtube.com/channel/UCUgIHlYBOD3yA3yDIRhg_mg">YouTube</a></p>

<p style="text-align: center;">Add a  <a href="https://github.com/serpapi/SerpApi/issues/">Feature Request</a>💫 or a <a href="https://github.com/serpapi/SerpApi/issues/">Bug</a>🐞</p>