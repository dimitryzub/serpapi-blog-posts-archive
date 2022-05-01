- <a href="#what_will_be_scraped">What will be scraped</a>
- <a href="#filter_results">How to filtering works</a>
- <a href="#prerequisites">Prerequisites</a>
- <a href="#full_code">Full Code</a>
- <a href="#links">Links</a>
- <a href="#outro">Outro</a>



<h2 id="what_will_be_scraped">What will be scraped</h2>

![image](https://user-images.githubusercontent.com/78694043/165787899-987bfd3b-3fac-401f-9075-b7c998b05ac0.png)

<h2 id="filter_results">How filtering works</h2>

To filter results, you need to use  `source:` operator which restricts search results to documents published by sources containing `"NIPS"` in their name. 

This operator can be used in addition to `OR` operator i.e `source:NIPS OR source:"Neural Information"`. So the search query would become:

```
search terms source:NIPS OR source:"Neural Information"
```

<h2 id="prerequisites">Prerequisites</h2>

**Basic knowledge scraping with CSS selectors**

CSS selectors declare which part of the markup a style applies to thus allowing to extract data from matching tags and attributes.

If you haven't scraped with CSS selectors, there's a dedicated blog post of mine about [how to use CSS selectors when web-scraping](https://serpapi.com/blog/web-scraping-with-css-selectors-using-python/) that covers what it is, pros and cons, and why they're matter from a web-scraping perspective and show the most common approaches of using CSS selectors when web scraping.


**Separate virtual environment if it will be a project**

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


def check_sources(source: list or str):
    if isinstance(source, str):
        return source                                             # NIPS
    elif isinstance(source, list):
        return " OR ".join([f'source:{item}' for item in source]) # source:NIPS OR source:Neural Information


def scrape_conference_publications(query: str, source: list or str):
    # https://docs.python-requests.org/en/master/user/quickstart/#passing-parameters-in-urls
    params = {
        "q": f'{query.lower()} {check_sources(source=source)}',  # search query
        "hl": "en",                         # language of the search
        "gl": "us"                          # country of the search
    }

    # https://docs.python-requests.org/en/master/user/quickstart/#custom-headers
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
    }

    html = requests.get("https://scholar.google.com/scholar", params=params, headers=headers, timeout=30)
    selector = Selector(html.text)
    
    publications = []
    
    for result in selector.css(".gs_r.gs_scl"):
        title = result.css(".gs_rt").xpath("normalize-space()").get()
        link = result.css(".gs_rt a::attr(href)").get()
        result_id = result.attrib["data-cid"]
        snippet = result.css(".gs_rs::text").get()
        publication_info = result.css(".gs_a").xpath("normalize-space()").get()
        cite_by_link = f'https://scholar.google.com/scholar{result.css(".gs_or_btn.gs_nph+ a::attr(href)").get()}'
        all_versions_link = f'https://scholar.google.com/scholar{result.css("a~ a+ .gs_nph::attr(href)").get()}'
        related_articles_link = f'https://scholar.google.com/scholar{result.css("a:nth-child(4)::attr(href)").get()}'
        pdf_file_title = result.css(".gs_or_ggsm a").xpath("normalize-space()").get()
        pdf_file_link = result.css(".gs_or_ggsm a::attr(href)").get()
    
        publications.append({
            "result_id": result_id,
            "title": title,
            "link": link,
            "snippet": snippet,
            "publication_info": publication_info,
            "cite_by_link": cite_by_link,
            "all_versions_link": all_versions_link,
            "related_articles_link": related_articles_link,
            "pdf": {
                "title": pdf_file_title,
                "link": pdf_file_link
            }
        })
        
    # return publications

    print(json.dumps(publications, indent=2, ensure_ascii=False))
    

scrape_conference_publications(query="anatomy", source=["NIPS", "Neural Information"])
```

### Code explanation


Add a function that accepts either `list` of `str` or a `str` and transforms it if it's a `list`: 

```python
def check_sources(source: list or str):
    if isinstance(source, str):
        return source                                             # NIPS
    elif isinstance(source, list):
        return " OR ".join([f'source:{item}' for item in source]) # source:NIPS OR source:Neural Information
```

Define a parse function:

```python
def scrape_conference_publications(query: str, source: list or str):
    # further code...
```

|Code|Explanation|
|----|-----------|
|`query: str`|tells Python that `query` argument should be a `string`.|
|`source: list or str`|tells Python that `source` argument should be a `list` or a `string`.|


Create URL parameters, `user-agent` and pass them to a request:

```python
# https://docs.python-requests.org/en/master/user/quickstart/#passing-parameters-in-urls
params = {
    "q": f'{query.lower()} {sources}',  # search query
    "hl": "en",                         # language of the search
    "gl": "us"                          # country of the search
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
|[`timeout`](https://docs.python-requests.org/en/master/user/quickstart/#timeouts)|to tell requests to stop waiting for a response after 30 seconds.|
|`Selector`|is a HTML/XML processor that parses data. Like [`BeautifulSoup()`](https://www.crummy.com/software/BeautifulSoup/bs4/doc/).|
|[`user-agent`](https://developer.mozilla.org/en-US/docs/Glossary/User_agent)|is used to act as a "real" user visit. [Default `requests` `user-agent` is a `python-requests`](https://github.com/psf/requests/blob/589c4547338b592b1fb77c65663d8aa6fbb7e38b/requests/utils.py#L808-L814) so websites understand that it's a script that sends a request and might block it. [Check what's your `user-agent`](https://www.whatismybrowser.com/detect/what-is-my-user-agent).|



Create a temporary `list` to store the data, and iterate over organic results:

```python
publications = []
        
for result in selector.css(".gs_r.gs_scl"):
    title = result.css(".gs_rt").xpath("normalize-space()").get()
    link = result.css(".gs_rt a::attr(href)").get()
    result_id = result.attrib["data-cid"]
    snippet = result.css(".gs_rs::text").get()
    publication_info = result.css(".gs_a").xpath("normalize-space()").get()
    cite_by_link = f'https://scholar.google.com/scholar{result.css(".gs_or_btn.gs_nph+ a::attr(href)").get()}'
    all_versions_link = f'https://scholar.google.com/scholar{result.css("a~ a+ .gs_nph::attr(href)").get()}'
    related_articles_link = f'https://scholar.google.com/scholar{result.css("a:nth-child(4)::attr(href)").get()}'
    pdf_file_title = result.css(".gs_or_ggsm a").xpath("normalize-space()").get()
    pdf_file_link = result.css(".gs_or_ggsm a::attr(href)").get()
```

|Code|Explanation|
|----|-----------|
|`css(<selector>)`|[to extarct data from a given CSS selector](https://github.com/scrapy/parsel/blob/90397dcd0b2c1cbb91e44f65c50f9e11628ba028/parsel/selector.py#L351-L362). In the background `parsel` translates every CSS query into XPath query using `cssselect`.|
|`xpath("normalize-space()")`|[to get blank text nodes as well](https://github.com/scrapy/parsel/issues/62#issuecomment-1042309376). By default, blank text nodes will be skipped resulting not a complete output.|
|`::text`/`::attr()`|is a [`parsel` pseudo-elements to extract text or attribute](https://github.com/scrapy/parsel/blob/90397dcd0b2c1cbb91e44f65c50f9e11628ba028/parsel/csstranslator.py#L48-L51) data from the HTML node.|
|`get()`|to get actual data.|

Append the results as a dictionary to a temporary list, return or print extracted data:

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
        "pdf": {
            "title": pdf_file_title,
            "link": pdf_file_link
        }
    })
    
# return publications

print(json.dumps(publications, indent=2, ensure_ascii=False))


scrape_conference_publications(query="anatomy", source=["NIPS", "Neural Information"])
```


Outputs: 

```json
[
  {
    "result_id": "hjgaRkq_oOEJ",
    "title": "Differential representation of arm movement direction in relation to cortical anatomy and function",
    "link": "https://iopscience.iop.org/article/10.1088/1741-2560/6/1/016006/meta",
    "snippet": "… ",
    "publication_info": "T Ball, A Schulze-Bonhage, A Aertsen… - Journal of neural …, 2009 - iopscience.iop.org",
    "cite_by_link": "https://scholar.google.com/scholar/scholar?cites=16258204980532099206&as_sdt=2005&sciodt=0,5&hl=en",
    "all_versions_link": "https://scholar.google.com/scholar/scholar?cluster=16258204980532099206&hl=en&as_sdt=0,5",
    "related_articles_link": "https://scholar.google.com/scholar/scholar?q=related:hjgaRkq_oOEJ:scholar.google.com/&scioq=anatomy+source:NIPS+OR+source:Neural+Information&hl=en&as_sdt=0,5",
    "pdf": {
      "title": "[PDF] psu.edu",
      "link": "http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.324.1523&rep=rep1&type=pdf"
    }
  }, ... other results
]
```

____

Alternatively, you can achieve it using [Google Scholar Organic Results API](https://serpapi.com/google-scholar-organic-results) from SerpApi.

The biggest difference is that you don't need to create a parser from scratch, maintain it, figure out how to scale it, and most importantly, how to bypass blocks from Google thus figuring out how to set up proxies and CAPTCHA solving solutions.


```python
# pip install google-search-results

import os, json
from serpapi import GoogleSearch
from urllib.parse import urlsplit, parse_qsl

params = {
    # https://docs.python.org/3/library/os.html#os.getenv
    "api_key": os.getenv("API_KEY"), # your serpapi API key
    "engine": "google_scholar",      # search engine
    "q": "AI source:NIPS",           # search query
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

<h2 id="links">Links</h2>

- [Code in the onlie IDE](https://replit.com/@DimitryZub1/how-to-search-in-google-scholar-within-a-particular-confere#main.py)
- [SerpApi Google Scholar Organic Results API](https://serpapi.com/google-scholar-organic-results)

___


<p style="text-align: center;">Join us on <a href="https://twitter.com/serp_api">Twitter</a> | <a href="https://www.youtube.com/channel/UCUgIHlYBOD3yA3yDIRhg_mg">YouTube</a></p>


<p style="text-align: center;">Add a  <a href="https://github.com/serpapi/public-roadmap/issues">Feature Request</a>💫 or a <a href="https://github.com/serpapi/public-roadmap/issues">Bug</a>🐞</p>