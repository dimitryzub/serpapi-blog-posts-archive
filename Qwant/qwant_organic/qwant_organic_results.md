👉**Briefly about the essence**: tutorial blog post about scraping: website position for SEO rank tracking, title, link, displayed link, snippet, and favicon data from qwant.com search results using Python.

🔨**What is required**: understanding of loops, data structures, exception handling, and basic knowledge of `CSS` selectors. `bs4`, `requests`, `lxml` libraries.

⏱️**How long will it take**: ~15-30 minutes.

___

- <a href="#intro">What is Qwant Search</a>
- <a href="#what_will_be_scraped">What will be scraped</a>
- <a href="#prerequisites">Prerequisites</a>
- <a href="#process">Process</a>
  - <a href="#organic_results">Organic Results</a>
  - <a href="#advertisement_results">Ad Results</a>
- <a href="#code">Code</a>
- <a href="#links">Links</a>
- <a href="#outro">Outro</a>

___

<h2 id="intro">What is Qwant Search</h2>

[Qwant](https://www.qwant.com/) is a European Paris-based no user tracking for advertising search engine with its independent indexing engine and available in 26 languages with more than [30 million individual monthly users worldwide](https://www.similarweb.com/website/qwant.com/).

___

<h2 id="what_will_be_scraped">What will be scraped</h2>

![qwant_organic_results_02](https://user-images.githubusercontent.com/78694043/146533506-32bdec38-78d1-4f2f-bb70-c1c3f40ca5a0.png)

<h2 id="prerequisites">Prerequisites</h2>

**Basic knowledge scraping with CSS selectors**

If you haven't scraped with `CSS` selectors, there's a dedicated blog post of mine about [how to use `CSS` selectors when web-scraping](https://serpapi.com/blog/web-scraping-with-css-selectors-using-python/) that covers what it is, pros and cons, and why they're matter from a web-scraping perspective.

`CSS` selectors declare which part of the markup a style applies to thus allowing to extract data from matching tags and attributes.

**Separate virtual environment**

If you didn't work with a virtual environment before, have a look at the dedicated [Python virtual environments tutorial using Virtualenv and Poetry](https://serpapi.com/blog/python-virtual-environments-using-virtualenv-and-poetry/) blog post of mine to get familiar.

In short, it's a thing that creates an independent set of installed libraries including different Python versions that can coexist with each other at the same system thus prevention libraries or Python version conflicts.

**Install  libraries**:

```lang-none
pip install requests
pip install lxml 
pip install beautifulsoup4
```

**Reduce the chance of being blocked**

There's a chance that a request might be blocked. Have a look at [how to reduce the chance of being blocked while web-scraping](https://serpapi.com/blog/how-to-reduce-chance-of-being-blocked-while-web/), there's eleven methods to bypass blocks from most websites.

___

<h2 id="process">Process</h2>

If you don't need an explanation:
- jump to the <a href="#code">full code section</a>,
- [try it in the online IDE](https://replit.com/@DimitryZub1/Scrape-Qwant-Organic-and-Ad-Results#main.py).

**Starting code** for both organic and ad resuts:


```python
from bs4 import BeautifulSoup
import requests, lxml, json

headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; HD1913) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.105 Mobile Safari/537.36 EdgA/46.1.2.5140"
}

params = {
    "q": "minecraft",
    "t": "web"
}


html = requests.get("https://www.qwant.com/", params=params, headers=headers, timeout=20)
soup = BeautifulSoup(html.text, "lxml")
# further code...
```

**Import libraries**:

```python
from bs4 import BeautifulSoup
import requests, lxml, json
```

**Add [`user-agent`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/User-Agent) and [query parameters](https://docs.python-requests.org/en/master/user/quickstart/#passing-parameters-in-urls)** to request:

```python
headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; HD1913) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.105 Mobile Safari/537.36 EdgA/46.1.2.5140"
}

params = {
    "q": "minecraft",  # search query
    "t": "web"         # qwant query argument for displaying web results 
}
```

**Make a request**, [add `timeout` arugment](https://docs.python-requests.org/en/master/user/quickstart/#timeouts), create `BeautifulSoup()` object:

```python
html = requests.get("https://www.qwant.com/", params=params, headers=headers, timeout=20)
soup = BeautifulSoup(html.text, "lxml")
```

- `timeout` parameter will tell `requests` to stop waiting for responce after a X number of seconds.
- `BeautifulSoup()` is what pulls all the HTML data. `lxml` is an HTML parser.

<h2 id="organic_results">Extract Organic Results</h2>

```python
def scrape_organic_results():

    organic_results_data = []

    for index, result in enumerate(soup.select("[data-testid=webResult]"), start=1):
        title = result.select_one(".WebResult-module__title___MOBFg").text
        link = result.select_one(".Stack-module__VerticalStack___2NDle.Stack-module__Spacexxs___3wU9G a")["href"]
        snippet = result.select_one(".Box-module__marginTopxxs___RMB_d").text

        try:
            displayed_link = result.select_one(".WebResult-module__permalink___MJGeh").text
            favicon = result.select_one(".WebResult-module__iconBox___3DAv5 img")["src"]
        except:
            displayed_link = None
            favicon = None

        organic_results_data.append({
            "position": index,
            "title": title,
            "link": link,
            "displayed_link": displayed_link,
            "snippet": snippet,
            "favicon": favicon
        })

    print(json.dumps(organic_results_data, indent=2))


scrape_oragnic_results()
```

**Create temporary `list()`** to store extracted data:

```python
organic_results_data = []
```

**Iterate and extract** the data:

```python
for index, result in enumerate(soup.select("[data-testid=webResult]"), start=1):
    title = result.select_one(".WebResult-module__title___MOBFg").text
    link = result.select_one(".Stack-module__VerticalStack___2NDle.Stack-module__Spacexxs___3wU9G a")["href"]
    snippet = result.select_one(".Box-module__marginTopxxs___RMB_d").text

    try:
        displayed_link = result.select_one(".WebResult-module__permalink___MJGeh").text
        favicon = result.select_one(".WebResult-module__iconBox___3DAv5 img")["src"]
    except:
        displayed_link = None
        favicon = None
```

To get the position index, we can use [`enumerate()` function which adds a counter to an iterable and returns it](https://www.programiz.com/python-programming/methods/built-in/enumerate) and set `start` to `1` so the count would start from 1, not from 0.

To handle `None` values, we can use `try/except` block so if there's nothing on the Qwant backend, we'll set it to `None` as well, otherwise it will throw an error saying that there's no such element or attribute.


**Append extracted data** to temporary `list()` as a dictionary:

```python
organic_results_data.append({
    "position": index,
    "title": title,
    "link": link,
    "displayed_link": displayed_link,
    "snippet": snippet,
    "favicon": favicon
})
```

**Print the data**:

```python
print(json.dumps(organic_results_data, indent=2))


# part of the output:
'''
[
  {
    "position": 1,
    "title": "Minecraft Official Site | Minecraft",
    "link": "https://www.minecraft.net/",
    "displayed_link": "minecraft.net",
    "snippet": "Get all-new items in the Minecraft Master Chief Mash-Up DLC on 12/10, and the Superintendent shirt in Character Creator, free for a limited time! Learn more. Climb high and dig deep. Explore bigger mountains, caves, and biomes along with an increased world height and updated terrain generation in the Caves & Cliffs Update: Part II! Learn more . Play Minecraft games with Game Pass. Get your ...",
    "favicon": "https://s.qwant.com/fav/m/i/www_minecraft_net.ico"
  },
  
  ... other results
  
  {
    "position": 10,
    "title": "Minecraft - download free full version game for PC ...",
    "link": "http://freegamepick.net/en/minecraft/",
    "displayed_link": "freegamepick.net",
    "snippet": "Minecraft Download Game Overview. Minecraft is a game about breaking and placing blocks. It's developed by Mojang. At first, people built structures to protect against nocturnal monsters, but as the game grew players worked together to create wonderful, imaginative things. It can als o be about adventuring with friends or watching the sun rise over a blocky ocean.",
    "favicon": "https://s.qwant.com/fav/f/r/freegamepick_net.ico"
  }
]
'''
```

___

<h2 id="advertisement_results">Extract Ad Results</h2>

```python
def scrape_ad_results():

    ad_results_data = []

    for index, ad_result in enumerate(soup.select("[data-testid=adResult]"), start=1):
        ad_title = ad_result.select_one(".WebResult-module__title___MOBFg").text
        ad_link = ad_result.select_one(".Stack-module__VerticalStack___2NDle a")["href"]
        ad_displayed_link = ad_result.select_one(".WebResult-module__domain___1LJmo").text
        ad_snippet = ad_result.select_one(".Box-module__marginTopxxs___RMB_d").text
        ad_favicon = ad_result.select_one(".WebResult-module__iconBox___3DAv5 img")["src"]

        ad_results_data.append({
            "ad_position": index,
            "ad_title": ad_title,
            "ad_link": ad_link,
            "ad_displayed_link": ad_displayed_link,
            "ad_snippet": ad_snippet,
            "ad_favicon": ad_favicon
        })

    print(json.dumps(ad_results_data, indent=2))
    

scrape_ad_results()
```

**Create temporary `list()`** to store extracted data:
```python
ad_results_data = []
```

**Iterate and extract**:

```python
for index, ad_result in enumerate(soup.select("[data-testid=adResult]"), start=1):
    ad_title = ad_result.select_one(".WebResult-module__title___MOBFg").text
    ad_link = ad_result.select_one(".Stack-module__VerticalStack___2NDle a")["href"]
    ad_displayed_link = ad_result.select_one(".WebResult-module__domain___1LJmo").text
    ad_snippet = ad_result.select_one(".Box-module__marginTopxxs___RMB_d").text
    ad_favicon = ad_result.select_one(".WebResult-module__iconBox___3DAv5 img")["src"]
```

The same approach was used to get the position index. The only difference is different `CSS` "container" selector `[data-testid=adResult]` while in organic results it's `[data-testid=webResult]`.

**Append extracted data to temporary `list()`** as a dictionary:

```python
ad_results_data.append({
    "ad_position": index,
    "ad_title": ad_title,
    "ad_link": ad_link,
    "ad_displayed_link": ad_displayed_link,
    "ad_snippet": ad_snippet
})
```

**Print the data**:

```python
print(json.dumps(ad_results_data, indent=2))

# output:
'''
[
  {
    "ad_position": 1,
    "ad_title": "Watch Movies & TV on Amazon - Download in HD on Amazon Video",
    "ad_link": "https://www.bing.com/aclick?ld=e8pyYjhclU87kOyQ4ap78CRzVUCUxgK0MGMfKx1YlQe_w7Nbzamra9cSRmPFAtSOVF4MliAqbJNdotR3G-aqHSaMOI0tqV9K0EAFRTemYDKhbqLyjFW93Lsh0mnyySb8oIj6GXADnoePUk-etFDgSvPdZI0xObBo4hesqbOHypYhSGeJ-ZbG1eY0kijv95k0XJ9WKPPA&u=aHR0cHMlM2ElMmYlMmZ3d3cuYW1hem9uLmNvLnVrJTJmcyUyZiUzZmllJTNkVVRGOCUyNmtleXdvcmRzJTNkbWluZWNyYWZ0JTJidGhlJTI2aW5kZXglM2RhcHMlMjZ0YWclM2RoeWRydWtzcG0tMjElMjZyZWYlM2RwZF9zbF8ydmdscmFubWxwX2UlMjZhZGdycGlkJTNkMTE0NDU5MjQzNjk0ODQzOSUyNmh2YWRpZCUzZDcxNTM3MTUwMzgzNDA4JTI2aHZuZXR3JTNkcyUyNmh2cW10JTNkZSUyNmh2Ym10JTNkYmUlMjZodmRldiUzZG0lMjZodmxvY2ludCUzZCUyNmh2bG9jcGh5JTNkMTQxMTcxJTI2aHZ0YXJnaWQlM2Rrd2QtNzE1Mzc2Njc4MjI5NzklM2Fsb2MtMjM1JTI2aHlkYWRjciUzZDU5MTJfMTg4MTc4NQ&rlid=c61aa73b62e916116cbdc687c021190a",
    "ad_displayed_link": "amazon.co.uk",
    "ad_snippet": "Download now. Watch anytime on Amazon Video.",
    "ad_favicon": "https://s.qwant.com/fav/a/m/www_amazon_co_uk.ico"
  }
]
'''
```

___

<h2 id="code">Full Code</h2>

```python
from bs4 import BeautifulSoup
import requests, lxml, json

headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; HD1913) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.105 Mobile Safari/537.36 EdgA/46.1.2.5140"
}

params = {
    "q": "minecraft",
    "t": "web"
}

html = requests.get("https://www.qwant.com/", params=params, headers=headers, timeout=20)
soup = BeautifulSoup(html.text, "lxml")


def scrape_organic_results():

    organic_results_data = []

    for index, result in enumerate(soup.select("[data-testid=webResult]"), start=1):
        title = result.select_one(".WebResult-module__title___MOBFg").text
        link = result.select_one(".Stack-module__VerticalStack___2NDle.Stack-module__Spacexxs___3wU9G a")["href"]
        snippet = result.select_one(".Box-module__marginTopxxs___RMB_d").text

        try:
            displayed_link = result.select_one(".WebResult-module__permalink___MJGeh").text
            favicon = result.select_one(".WebResult-module__iconBox___3DAv5 img")["src"]
        except:
            displayed_link = None
            favicon = None

        organic_results_data.append({
            "position": index,
            "title": title,
            "link": link,
            "displayed_link": displayed_link,
            "snippet": snippet,
            "favicon": favicon
        })

    print(json.dumps(organic_results_data, indent=2))


def scrape_ad_results():

    ad_results_data = []

    for index, ad_result in enumerate(soup.select("[data-testid=adResult]"), start=1):
        ad_position = index + 1
        ad_title = ad_result.select_one(".WebResult-module__title___MOBFg").text
        ad_link = ad_result.select_one(".Stack-module__VerticalStack___2NDle a")["href"]
        ad_displayed_link = ad_result.select_one(".WebResult-module__domain___1LJmo").text
        ad_snippet = ad_result.select_one(".Box-module__marginTopxxs___RMB_d").text
        ad_favicon = ad_result.select_one(".WebResult-module__iconBox___3DAv5 img")["src"]

        ad_results_data.append({
            "ad_position": index,
            "ad_title": ad_title,
            "ad_link": ad_link,
            "ad_displayed_link": ad_displayed_link,
            "ad_snippet": ad_snippet,
            "ad_favicon": ad_favicon
        })

    print(json.dumps(ad_results_data, indent=2))
```

___

<h2 id="links">Links</h2>

- [Code in the Online IDE](https://replit.com/@DimitryZub1/Scrape-Qwant-Organic-and-Ad-Results#main.py)

___

<h2 id="outro">Outro</h2>

If you have anything to share, any questions or suggestions to this blog post, feel free to reach out via Twitter at [@dimitryzub](https://twitter.com/DimitryZub), or [@serp_api](https://twitter.com/serp_api).

Yours,
Dimitry, and the rest of SerpApi Team.

___

<p style="text-align: center;">Join us on <a href="https://www.reddit.com/r/SerpApi/">Reddit</a> | <a href="https://twitter.com/serp_api">Twitter</a> | <a href="https://www.youtube.com/channel/UCUgIHlYBOD3yA3yDIRhg_mg">YouTube</a></p>

<p style="text-align: center;">Add a  <a href="https://forum.serpapi.com/feature-requests">Feature Request</a>💫 or a <a href="https://forum.serpapi.com/bugs">Bug</a>🐞</p>