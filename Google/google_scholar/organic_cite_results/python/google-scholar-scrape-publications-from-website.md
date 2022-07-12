- <a href="#what_will_be_scraped">What will be scraped</a>
- <a href="#how_filter">How filtering works</a>
- <a href="#prerequisites">Prerequisites</a>
- <a href="#full_code">Full Code</a>
- <a href="#links">Links</a>
- <a href="#outro">Outro</a>

<h2 id="what_will_be_scraped">What will be scraped</h2>

![image](https://user-images.githubusercontent.com/78694043/165941085-9ff51030-6643-4113-88d3-3ac9d8963422.png)

<h2 id="filter_results">How filtering works</h2>

To filter results by a certain website, you need to use  `site:` operator which restricts search results to papers published by websites containing `<website_name>` in their name. 

This operator can be used in addition to `OR` operator i.e `site:cabdirect.org OR site:<other_website>`. So the search query would become:

```
search terms site:cabdirect.org OR site:<other_website>
```

<h2 id="prerequisites">Prerequisites</h2>

**Basic knowledge scraping with CSS selectors**

CSS selectors declare which part of the markup a style applies to thus allowing to extract of data from matching tags and attributes.

If you haven't scraped with CSS selectors, there's a dedicated blog post of mine about [how to use CSS selectors when web-scraping](https://serpapi.com/blog/web-scraping-with-css-selectors-using-python/) that covers what it is, pros and cons, and why they're matter from a web-scraping perspective and show the most common approaches of using CSS selectors when web scraping.


**Separate virtual environment**

In short, it's a thing that creates an independent set of installed libraries including different Python versions that can coexist with each other in the same system thus preventing libraries or Python version conflicts.

If you didn't work with a virtual environment before, have a look at the dedicated [Python virtual environments tutorial using Virtualenv and Poetry](https://serpapi.com/blog/python-virtual-environments-using-virtualenv-and-poetry/) blog post of mine to get familiar.

📌Note: this is not a strict requirement for this blog post.

**Install libraries**:

```lang-none
pip install requests parsel
```

**Reduce the chance of being blocked**

There's a chance that a request might be blocked. Have a look at [how to reduce the chance of being blocked while web-scraping](https://serpapi.com/blog/how-to-reduce-chance-of-being-blocked-while-web/), there are eleven methods to bypass blocks from most websites.

___


<h2 id="full_code">Full Code</h2>

```python
from parsel import Selector
import requests, json, os


def check_websites(website: list or str):
    if isinstance(website, str):
        return website                                           # cabdirect.org
    elif isinstance(website, list):
        return " OR ".join([f'site:{site}' for site in website]) # site:cabdirect.org OR site:cab.net


def scrape_website_publications(query: str, website: list or str):

    """
    Add a search query and site or multiple websites.

    Following will work:
    ["cabdirect.org", "lololo.com", "brabus.org"] -> list[str]
    ["cabdirect.org"]                             -> list[str]
    "cabdirect.org"                               -> str
    """
    
    # https://docs.python-requests.org/en/master/user/quickstart/#passing-parameters-in-urls
    params = {
        "q": f'{query.lower()} {check_websites(website=website)}',  # search query
        "hl": "en",                                                 # language of the search
        "gl": "us"                                                  # country of the search
    }
    
    # https://docs.python-requests.org/en/master/user/quickstart/#custom-headers
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
    }

    html = requests.get("https://scholar.google.com/scholar", params=params, headers=headers, timeout=30)
    selector = Selector(html.text)
    
    publications = []
    
    # iterate over every element from organic results from the first page and extract the data
    for result in selector.css(".gs_r.gs_scl"):
        title = result.css(".gs_rt").xpath("normalize-space()").get()
        link = result.css(".gs_rt a::attr(href)").get()
        result_id = result.attrib["data-cid"]
        snippet = result.css(".gs_rs::text").get()
        publication_info = result.css(".gs_a").xpath("normalize-space()").get()
        cite_by_link = f'https://scholar.google.com/scholar{result.css(".gs_or_btn.gs_nph+ a::attr(href)").get()}'
        all_versions_link = f'https://scholar.google.com/scholar{result.css("a~ a+ .gs_nph::attr(href)").get()}'
        related_articles_link = f'https://scholar.google.com/scholar{result.css("a:nth-child(4)::attr(href)").get()}'
    
        publications.append({
            "result_id": result_id,
            "title": title,
            "link": link,
            "snippet": snippet,
            "publication_info": publication_info,
            "cite_by_link": cite_by_link,
            "all_versions_link": all_versions_link,
            "related_articles_link": related_articles_link,
        })
    
    # print or return the results
    # return publications

    print(json.dumps(publications, indent=2, ensure_ascii=False))
    

scrape_website_publications(query="biology", website="cabdirect.org")
```

Import libraries and define a function:

```python
from parsel import Selector
import requests, json, os
```

Create a function to check if `website` argument is either a `list` of `str` or a `string`: 

```python
# check if returned website argument is string or a list

def check_websites(website: list or str):
    if isinstance(website, str):
        return website                                           # cabdirect.org
    elif isinstance(website, list):
        return " OR ".join([f'site:{site}' for site in website]) # site:cabdirect.org OR site:cab.com
```

Define a parse function:

```python
def scrape_website_publications(query: str, website: list or str):
    # further code
```

|Code|Explanation|
|----|-----------|
|`query: str`/`website: list or str`|to tell Python that `query` and `website` arguments should be with a type of `list` of `strings` or a `string`|

Create search query parameters, request headers, pass them to request:

```python
# https://docs.python-requests.org/en/master/user/quickstart/#passing-parameters-in-urls
params = {
    "q": f'{query.lower()} site:{website}',  # search query
    "hl": "en",                              # language of the search
    "gl": "us"                               # country of the search
}

# https://docs.python-requests.org/en/master/user/quickstart/#custom-headers
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
}

html = requests.get("https://scholar.google.com/scholar", params=params, headers=headers, timeout=30)
selector = Selector(html.text)
```

|Code|Explanation|
|----|-----------|
|`params`|is a query parameters that passed to `requests.get()` as a `dict`|
|`haeders`|is request headers, and `user-agent` is a thing that is used to act as a "real" user visit so websites (not all and in all cases) don't block the request. We need to pass our `user-agent` because the [default `requests` `user-agent` is `python-requests`]() so websites understand that it's a script.|
|[`timeout`](https://docs.python-requests.org/en/master/user/quickstart/#timeouts)|to tell requests to stop waiting for a response after 30 seconds.|



Create a temporary `list`, iterate over all organic results, and extract the data:

```python
publications = []
    
# iterate over every element from organic results from the first page and extract the data
for result in selector.css(".gs_r.gs_scl"):
    title = result.css(".gs_rt").xpath("normalize-space()").get()
    link = result.css(".gs_rt a::attr(href)").get()
    result_id = result.attrib["data-cid"]
    snippet = result.css(".gs_rs::text").get()
    publication_info = result.css(".gs_a").xpath("normalize-space()").get()
    cite_by_link = f'https://scholar.google.com/scholar{result.css(".gs_or_btn.gs_nph+ a::attr(href)").get()}'
    all_versions_link = f'https://scholar.google.com/scholar{result.css("a~ a+ .gs_nph::attr(href)").get()}'
    related_articles_link = f'https://scholar.google.com/scholar{result.css("a:nth-child(4)::attr(href)").get()}'
```

|Code|Explanation|
|----|-----------|
|`css(<selector>)`|[to extarct data from a given CSS selector](https://github.com/scrapy/parsel/blob/90397dcd0b2c1cbb91e44f65c50f9e11628ba028/parsel/selector.py#L351-L362). In the background `parsel` translates every CSS query into XPath query using `cssselect`.|
|`xpath("normalize-space()")`|[to get blank text nodes as well](https://github.com/scrapy/parsel/issues/62#issuecomment-1042309376). By default, blank text nodes will be skipped resulting not a complete output.|
|`::text`/`::attr()`|is a [`parsel` pseudo-elements to extract text or attribute](https://github.com/scrapy/parsel/blob/90397dcd0b2c1cbb91e44f65c50f9e11628ba028/parsel/csstranslator.py#L48-L51) data from the HTML node.|
|`get()`|to get actual data.|

Append extracted data to the `list` as a `dict`, and `return` or `print` the results:

```python
publications.append({
    "result_id": result_id,
    "title": title,
    "link": link,
    "snippet": snippet,
    "publication_info": publication_info,
    "cite_by_link": cite_by_link,
    "all_versions_link": all_versions_link,
    "related_articles_link": related_articles_link,
})

# print or return the results
# return publications

print(json.dumps(publications, indent=2, ensure_ascii=False))
    

# call the function
scrape_website_publications(query="biology", website="cabdirect.org")
```


Outputs: 

```json
[
  {
    "result_id": "6zRLFbcxtREJ",
    "title": "The biology of mycorrhiza.",
    "link": "https://www.cabdirect.org/cabdirect/abstract/19690600367",
    "snippet": "In the second, revised and extended, edition of this work [cf. FA 20 No. 4264], two new ",
    "publication_info": "JL Harley - The biology of mycorrhiza., 1969 - cabdirect.org",
    "cite_by_link": "https://scholar.google.com/scholar/scholar?cites=1275980731835430123&as_sdt=2005&sciodt=0,5&hl=en",
    "all_versions_link": "https://scholar.google.com/scholar/scholar?cluster=1275980731835430123&hl=en&as_sdt=0,5",
    "related_articles_link": "https://scholar.google.com/scholar/scholar?q=related:6zRLFbcxtREJ:scholar.google.com/&scioq=biology+site:cabdirect.org&hl=en&as_sdt=0,5"
  }, ... other results
]
```

_____

Alternatively, you can do the same thing using [Google Scholar Organic Results API](https://serpapi.com/google-scholar-organic-results) from SerpApi. It's a paid API with a free plan.

The difference is that you don't have to create the parser from scratch, maintain it, figure out how to scale it, how bypass blocks from Google, and figure out which proxy/captcha providers are good.


```python
# pip install google-search-results

import os, json
from serpapi import GoogleSearch
from urllib.parse import urlsplit, parse_qsl


def serpapi_scrape(query: str, website: str):
    params = {
        # https://docs.python.org/3/library/os.html#os.getenv
        "api_key": os.getenv("API_KEY"), # your serpapi API key
        "engine": "google_scholar",      # search engine
        "q": f"{query} site:{website}",  # search query
        "hl": "en",                      # language
        # "as_ylo": "2017",              # from 2017
        # "as_yhi": "2021",              # to 2021
        "start": "0"                     # first page
    }
    
    search = GoogleSearch(params)
    
    publications = []
    
    publications_is_present = True
    while publications_is_present:
        results = search.get_dict()
    
        print(f"Currently extracting page #{results.get('serpapi_pagination', {}).get('current')}..")
    
        for result in results["organic_results"]:
            position = result["position"]
            title = result["title"]
            publication_info_summary = result["publication_info"]["summary"]
            result_id = result["result_id"]
            link = result.get("link")
            result_type = result.get("type")
            snippet = result.get("snippet")
    
            publications.append({
                "page_number": results.get("serpapi_pagination", {}).get("current"),
                "position": position + 1,
                "result_type": result_type,
                "title": title,
                "link": link,
                "result_id": result_id,
                "publication_info_summary": publication_info_summary,
                "snippet": snippet,
                })
    
            
            if "next" in results.get("serpapi_pagination", {}):
                # splits URL in parts as a dict and passes it to a GoogleSearch() class.
                search.params_dict.update(dict(parse_qsl(urlsplit(results["serpapi_pagination"]["next"]).query)))
            else:
                papers_is_present = False
    
    print(json.dumps(organic_results_data, indent=2, ensure_ascii=False))
```

___


<h2 id="links">Links</h2>

- [Code in the online IDE](https://replit.com/@DimitryZub1/Scrape-Google-Scholar-Papers-from-a-certain-website#serpapi_solution.py)
- [Google Scholar Organic Results API](https://serpapi.com/google-scholar-organic-results)

___

<p style="text-align: center;">Join us on <a href="https://twitter.com/serp_api">Twitter</a> | <a href="https://www.youtube.com/channel/UCUgIHlYBOD3yA3yDIRhg_mg">YouTube</a></p>


<p style="text-align: center;">Add a  <a href="https://github.com/serpapi/public-roadmap/issues">Feature Request</a>💫 or a <a href="https://github.com/serpapi/public-roadmap/issues">Bug</a>🐞</p>