- <a href="#what_will_be_scraped">What will be scraped</a>
- <a href="#prerequisites">Prerequisites</a>
- <a href="#process">Process</a>
- <a href="#full_code">Full Code</a>
- <a href="#links">Links</a>
- <a href="#outro">Outro</a>

___

<h2 id="what_will_be_scraped">What will be scraped</h2>

![image](https://user-images.githubusercontent.com/78694043/156001367-7d131a1d-be28-48d0-b8e5-1ecf78bdabca.png)

<h2 id="prerequisites">Prerequisites</h2>

**Basic knowledge scraping with CSS selectors**

If you haven't scraped with `CSS` selectors, there's a dedicated blog post of mine about [how to use `CSS` selectors when web-scraping](https://serpapi.com/blog/web-scraping-with-css-selectors-using-python/) that covers what it is, pros and cons, and why they're matter from a web-scraping perspective.

`CSS` selectors declare which part of the markup a style applies to thus allowing to extract data from matching tags and attributes.

**Separate virtual environment**

If you didn't work with a virtual environment before, have a look at the dedicated [Python virtual environments tutorial using Virtualenv and Poetry](https://serpapi.com/blog/python-virtual-environments-using-virtualenv-and-poetry/) blog post of mine to get familiar.

In short, it's a thing that creates an independent set of installed libraries including different Python versions that can coexist with each other at the same system thus preventing libraries or Python version conflicts.

📌Note: this is not a strict requirement for this blog post.

**Install libraries**:

```lang-none
pip install requests, parsel
```

**Reduce the chance of being blocked**

There's a chance that a request might be blocked. Have a look at [how to reduce the chance of being blocked while web-scraping](https://serpapi.com/blog/how-to-reduce-chance-of-being-blocked-while-web/), there are eleven methods to bypass blocks from most websites and some of them will be covered in this blog post.


___

<h2 id="full_code">Full Code</h2>

```python
import requests, json
from parsel import Selector

# https://docs.python-requests.org/en/master/user/quickstart/#passing-parameters-in-urls
params = {
    "query": "minecraft",
    "where": "web"  # works with nexearch as well
}

# https://docs.python-requests.org/en/master/user/quickstart/#custom-headers
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.87 Safari/537.36",
}

html = requests.get("https://search.naver.com/search.naver", params=params, headers=headers, timeout=30)
selector = Selector(html.text)

related_results = []

for index, related_result in enumerate(selector.css(".related_srch .keyword"), start=1):
    keyword = related_result.css(".tit::text").get().strip()
    link = f'https://search.naver.com/search.naver{related_result.css("a::attr(href)").get()}'

    related_results.append({
        "position": index,
        "title": keyword,
        "link": link
    })


print(json.dumps(related_results, indent=2, ensure_ascii=False))
```

Output:

```json
[
  {
    "position": 1,
    "title": "마인크래프트",
    "link": "https://search.naver.com/search.naver?where=nexearch&query=%EB%A7%88%EC%9D%B8%ED%81%AC%EB%9E%98%ED%94%84%ED%8A%B8&ie=utf8&sm=tab_she&qdt=0"
  },
  {
    "position": 2,
    "title": "minecraft 뜻",
    "link": "https://search.naver.com/search.naver?where=nexearch&query=minecraft+%EB%9C%BB&ie=utf8&sm=tab_she&qdt=0"
  },
  {
    "position": 3,
    "title": "craft",
    "link": "https://search.naver.com/search.naver?where=nexearch&query=craft&ie=utf8&sm=tab_she&qdt=0"
  },
  {
    "position": 4,
    "title": "mine",
    "link": "https://search.naver.com/search.naver?where=nexearch&query=mine&ie=utf8&sm=tab_she&qdt=0"
  },
  {
    "position": 5,
    "title": "mojang",
    "link": "https://search.naver.com/search.naver?where=nexearch&query=mojang&ie=utf8&sm=tab_she&qdt=0"
  }
]
```

___


Alternatively, you can achieve the same by using [Naver Related results API](https://serpapi.com/naver-related-results) from SerpApi. It is a paid API with a free plan.

It's almost the same, except you don't need to create the parser from scratch, figure out which proxy/CAPTCHA providers is reliable, how to scale it, and don't need to maintain it if something is broken.

```python
from serpapi import NaverSearch
import os, json

params = {
    "api_key": os.getenv("API_KEY"),
    "engine": "naver",
    "query": "minecraft",
    "where": "web"
}

search = NaverSearch(params)
results = search.get_dict()

related_results = []

for related_result in results["related_results"]:
    related_results.append({
        "position": related_result["position"],
        "title": related_result["title"],
        "link": related_result["link"]
    })

print(json.dumps(related_results, indent=2, ensure_ascii=False))
```

Output:

```json
[
  {
    "position": 1,
    "title": "마인크래프트",
    "link": "https://search.naver.com?where=nexearch&query=%EB%A7%88%EC%9D%B8%ED%81%AC%EB%9E%98%ED%94%84%ED%8A%B8&ie=utf8&sm=tab_she&qdt=0"
  },
  {
    "position": 2,
    "title": "minecraft 뜻",
    "link": "https://search.naver.com?where=nexearch&query=minecraft+%EB%9C%BB&ie=utf8&sm=tab_she&qdt=0"
  },
  {
    "position": 3,
    "title": "craft",
    "link": "https://search.naver.com?where=nexearch&query=craft&ie=utf8&sm=tab_she&qdt=0"
  },
  {
    "position": 4,
    "title": "mine",
    "link": "https://search.naver.com?where=nexearch&query=mine&ie=utf8&sm=tab_she&qdt=0"
  },
  {
    "position": 5,
    "title": "mojang",
    "link": "https://search.naver.com?where=nexearch&query=mojang&ie=utf8&sm=tab_she&qdt=0"
  }
]
```

___

<h2 id="links">Links</h2>

- [Code in the online IDE](https://replit.com/@DimitryZub1/Scrape-Naver-Related-Results#main.py)
- [Naver Related results API](https://serpapi.com/naver-related-results)

___

<h2 id="outro">Outro</h2>

If you have anything to share, any questions, suggestions, or something that isn't working correctly, feel free to drop a comment in the
comment section or reach out via Twitter at [@dimitryzub](https://twitter.com/DimitryZub), or [@serp_api](https://twitter.com/serp_api).

Yours, 
Dmitriy, and the rest of SerpApi Team.

___

<p style="text-align: center;">Join us on <a href="https://www.reddit.com/r/SerpApi/">Reddit</a> | <a href="https://twitter.com/serp_api">Twitter</a> | <a href="https://www.youtube.com/channel/UCUgIHlYBOD3yA3yDIRhg_mg">YouTube</a></p>

<p style="text-align: center;">Add a  <a href="https://forum.serpapi.com/feature-requests">Feature Request</a>💫 or a <a href="https://forum.serpapi.com/bugs">Bug</a>🐞</p>

