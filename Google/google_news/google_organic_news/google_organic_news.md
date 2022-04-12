Contents: intro, imports, what will be scraped, process, code, code with pagination, links, outro.

### Intro
This blog post is a continuation of Google's web scraping series. Here you'll see how to scrape Google News Results using Python with `beautifulsoup`, `requests`, `lxml` libraries. An alternative API solution will be shown.

### Imports
```python
import requests, lxml
from bs4 import BeautifulSoup
from serpapi import GoogleSearch
```

### What will be scraped
![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/vr0a02qjk31qv6pdfmgb.png)


### Process

Selecting **container, title, link, source, snippet, published time**.
<img width="100%" style="width:100%" src="https://media.giphy.com/media/WwAOMVPxAvFhvG3MWB/giphy.gif">


Make sure to pass `user-agent`, because Google might block your requests eventually and you'll receive a different HTML thus empty output. [Check what is your user-agent](https://www.whatismybrowser.com/detect/what-is-my-user-agent).

Basically, `user-agent` let identifies the browser, its version number, and its host operating system that representing a person (browser) in a Web context that lets servers and network peers identify if it's a bot or not. And we're faking "real" user visit.

### Code
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

-------------
'''
San Andreas: Cesar & Kendl Is Grand Theft Auto's Best Relationship
https://screenrant.com/gta-san-andreas-cesar-kendl-best-relationship-why/
Many Grand Theft Auto relationships are negative or purely transactional. 
That makes Cesar and Kendl's genuine love for each other stand out.
4 hours ago
Screen Rant
'''
```

### Code with pagination
```python

from bs4 import BeautifulSoup
import requests, urllib.parse, lxml

def paginate(url, previous_url=None):
    # Break from infinite recursion
    if url == previous_url: return

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                      "Chrome/72.0.3538.102 Safari/537.36 Edge/18.19582"
    }

    response = requests.get(url, headers=headers).text
    soup = BeautifulSoup(response, 'lxml')

    # First page
    yield soup

    next_page_node = soup.select_one('a#pnnext')

    # Stop when there is no next page
    if next_page_node is None: return

    next_page_url = urllib.parse.urljoin('https://www.google.com/', next_page_node['href'])

    # Pages after the first one
    yield from paginate(next_page_url, url)


def scrape():
    pages = paginate("https://www.google.com/search?hl=en-US&q=gta san andreas&tbm=nws")

    for soup in pages:
        print(f'Current page: {int(soup.select_one(".YyVfkd").text)}\n')

        for result in soup.select('.dbsr'):
            title = result.select_one('.nDgy9d').text
            link = result.a['href']
            source = result.select_one('.WF4CUc').text
            snippet = result.select_one('.Y3v8qd').text
            date_published = result.select_one('.WG9SHc span').text
            print(f'{title}\n{link}\n{snippet}\n{date_published}\n{source}\n')

scrape()

-------------------
'''
Current page: 1

San Andreas: Cesar & Kendl Is Grand Theft Auto's Best Relationship
https://screenrant.com/gta-san-andreas-cesar-kendl-best-relationship-why/
Many Grand Theft Auto relationships are negative or purely transactional. 
That makes Cesar and Kendl's genuine love for each other stand out.
4 hours ago
Screen Rant

...

Current page: 8

Il recréé des covers d'album sur "GTA : San Andreas" et c'est ...
https://intrld.com/gtpmagazine-le-magazine-parodique-du-jeu-gta/
On a trouvé LE compte parodique à suivre : Grand Theft Parody, le magazine 
qui revisite des pochettes mythiques sur GTA : San Andreas.
2 weeks ago
Interlude
'''
```

### Using [Google News Result API](https://serpapi.com/news-results)
SerpApi is a paid API with a free plan.

The main differences as I usually write in this blog post is that it's much faster and straightforward process rather than tinkering `CSS`, `XPath` selectors or dealing with Javascript-driven websites e.g. Google Maps which SerpApi scrapes like a charm.

If you want to get things quickly and write code faster, and don't want to maintain the parser then, I believe that API solution is a way to go.

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

------------------
'''
{'position': 1, 'link': 'https://www.sportskeeda.com/gta/5-strange-gta-san-andreas-glitches', 'title': '5 strange GTA San Andreas glitches', 'source': 'Sportskeeda', 'date': '9 hours ago', 'snippet': 'GTA San Andreas has a wide assortment of interesting and strange glitches.', 'thumbnail': 'https://serpapi.com/searches/60e71e1f8b7ed2dfbde7629b/images/1394ee64917c752bdbe711e1e56e90b20906b4761045c01a2cefb327f91d40bb.jpeg'}
'''
```


### Google News Results API with Pagination
```python
# https://github.com/serpapi/google-search-results-python
from serpapi import GoogleSearch
import os


def scrape():
    params = {
        "engine": "google",
        "q": "coca cola",
        "tbm": "nws",
        "api_key": "YOUR_API_KEY",
    }

    search = GoogleSearch(params)
    pages = search.pagination()

    for result in pages:
        print(f"Current page: {result['serpapi_pagination']['current']}")

        for news_result in result["news_results"]:
            print(f"Title: {news_result['title']}\nLink: {news_result['link']}\n")


scrape()


-------------------
'''
Current page: 1
Title: 5 strange GTA San Andreas glitches
Link: https://www.sportskeeda.com/gta/5-strange-gta-san-andreas-glitches

...

Current page: 14
Title: Ambitious Grand Theft Auto: San Andreas Mod Turns It Into A Spider-Man Game
Link: https://gamerant.com/grand-theft-auto-san-andreas-spider-man-game-mod/
...
'''
```

### Links
[Code in the online IDE](https://replit.com/@DimitryZub1/Scrape-Google-News-with-Pagination-python-serpapi#main.py) • [Google News Result API](https://serpapi.com/news-results)

### Outro
If you have any questions or something isn't working correctly or you want to write something else, feel free to drop a comment in the comment section or via Twitter at [@serp_api](https://twitter.com/serp_api).

Yours,
Dimitry, and the rest of SerpApi Team.