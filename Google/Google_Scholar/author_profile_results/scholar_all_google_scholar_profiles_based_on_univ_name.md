🔨**What is required**: Understanding of loops, data structures, basic knowledge of CSS selectors and XPath. `requests`
, `parsel`, `serpapi` libraries.

⏱️**How long will it take**: ~10-20 minutes.

___

- <a href="#what_will_be_scraped">What will be scraped</a>
- <a href="#prerequisites">Prerequisites</a>
- <a href="#process">Process</a>
- <a href="#full_code">Full Code</a>
- <a href="#links">Links</a>
- <a href="#outro">Outro</a>

___

<h2 id="what_will_be_scraped">What will be scraped</h2>

![image](https://user-images.githubusercontent.com/78694043/154103222-8d3471a7-cbfe-46ed-9ddb-9369b7c6a518.png)

<h2 id="prerequisites">Prerequisites</h2>

**Basic knowledge scraping with CSS selectors**

`CSS` selectors declare which part of the markup a style applies to thus allowing to extract data from matching tags and attributes.

If you haven't scraped with `CSS` selectors, there's a dedicated blog post of mine
about [how to use `CSS` selectors when web-scraping](https://serpapi.com/blog/web-scraping-with-css-selectors-using-python/) that covers
what it is, pros and cons, and why they're matter from a web-scraping perspective.


**Separate virtual environment**

If you didn't work with a virtual environment before, have a look at the dedicated [Python virtual environments tutorial using Virtualenv and Poetry](https://serpapi.com/blog/python-virtual-environments-using-virtualenv-and-poetry/) blog post of mine to get familiar.

In short, it's a thing that creates an independent set of installed libraries including different Python versions that can coexist with each
other at the same system thus preventing libraries or Python version conflicts.

📌Note: this is not a strict requirement for this blog post.

**Install libraries**:

```lang-none
pip install requests, parsel, google-search-results
```

**Reduce the chance of being blocked**

There's a chance that a request might be blocked. Have a look at [how to reduce the chance of being blocked while web-scraping](https://serpapi.com/blog/how-to-reduce-chance-of-being-blocked-while-web/), there are eleven methods to bypass blocks from most websites.


___

<h2 id="full_code">Full Code</h2>

```python
import requests, re, json
from parsel import Selector

def scrape_all_authors_from_university(label: str, university_name: str) -> list[dict[str]]:

    params = {
        "view_op": "search_authors",                       # author results
        "mauthors": f'label:{label} "{university_name}"',  # search query
        "hl": "en",                                        # language
        "astart": 0                                        # page number
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.87 Safari/537.36",
    }

    profile_results = []

    profiles_is_present = True
    while profiles_is_present:

        html = requests.get("https://scholar.google.com/citations", params=params, headers=headers, timeout=30)
        select = Selector(html.text)

        print(f"extracting authors at page #{params['astart']}.")

        for profile in select.css(".gs_ai_chpr"):
            name = profile.css(".gs_ai_name a::text").get()
            link = f'https://scholar.google.com{profile.css(".gs_ai_name a::attr(href)").get()}'
            affiliations = profile.css(".gs_ai_aff").xpath('normalize-space()').get()
            email = profile.css(".gs_ai_eml::text").get()
            cited_by = re.search(r"\d+", profile.xpath('//div[@class="gs_ai_cby"]').get()).group()  # Cited by 17143 -> 17143
            interests = profile.css(".gs_ai_one_int::text").getall()

            profile_results.append({
                "profile_name": name,
                "profile_link": link,
                "profile_affiliations": affiliations,
                "profile_email": email,
                "profile_city_by_count": cited_by,
                "profile_interests": interests
            })

        # if next page token is present -> update next page token and increment 10 to get the next page
        if select.css("button.gs_btnPR::attr(onclick)").get():
            # https://regex101.com/r/e0mq0C/1
            params["after_author"] = re.search(r"after_author\\x3d(.*)\\x26", select.css("button.gs_btnPR::attr(onclick)").get()).group(1)  # -> XB0HAMS9__8J
            params["astart"] += 10
        else:
            profiles_is_present = False

    return profile_results


print(json.dumps(scrape_all_authors_from_university(label="biology", university_name="Michigan University"), indent=2))
```

Import libraries:

```python
import requests, re, json
from parsel import Selector
```

- `requests` to make a request.
- `re` to match parts of the HTML via regular expression.
- `json` for pretty printing, in this case.
- [`parsel`](https://parsel.readthedocs.io/en/latest/index.html) is a library to extract and remove data from HTML and XML documents using XPath and CSS selectors. It's similar to `beautifulsoup4` except it supports XPath and has its own CSS pseudo-elements support, for example `::text` or `::attr(<attribute_name>)`. Also, [every CSS selector query translates to XPath](https://github.com/scrapy/parsel/blob/f5f73d34ba787ad0c9df25de295de6e196ecd91d/parsel/selector.py#L350-L351) using [`cssselect`](https://github.com/scrapy/cssselect) package.

Define a function:

```python
def scrape_all_authors_from_university(label: str, university_name: str) -> list[dict[str]]:
    # further code
```

- `label: str, university_name: str` is a parameter annotations which tells people who read the program or libraries/programs such as `pylint` that `label` and `university_name` should be a `str`.
- `-> list[dict[str]]` is a [function return annotation](https://www.python.org/dev/peps/pep-3107/#syntax).

Create search query params, request headers and make a request:

```python
# https://docs.python-requests.org/en/master/user/quickstart/#passing-parameters-in-urls
params = {
    "view_op": "search_authors",                       # author results
    "mauthors": f'label:{label} "{university_name}"',  # search query
    "hl": "en",                                        # language
    "astart": 0                                        # page number
}

# https://docs.python-requests.org/en/master/user/quickstart/#custom-headers
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.87 Safari/537.36",
}
```

- [`User-Agent`](https://developer.mozilla.org/en-US/docs/Glossary/User_agent) is used to pretend that it's a "real" user sends a request, not a bot or a script.  


Create temporary `list` to store extracted data:

```python
profile_results = []
```

Create a `while` loop:

```python
profiles_is_present = True
while profiles_is_present:
    # further code..
```

Make a request and pass URL `params` and `headers`:

```python
html = requests.get("https://scholar.google.com/citations", params=params, headers=headers, timeout=30)
select = Selector(html.text)
```

- [`timeout=30`](https://docs.python-requests.org/en/master/user/quickstart/#timeouts) tells `requests` to stop waiting for response after 30 seconds.
- `Selector()` is like `BeautifulSoup()` object, if you used it before.

Extract the data:

```python
for profile in select.css(".gs_ai_chpr"):
    name = profile.css(".gs_ai_name a::text").get()
    link = f'https://scholar.google.com{profile.css(".gs_ai_name a::attr(href)").get()}'
    affiliations = profile.css(".gs_ai_aff").xpath('normalize-space()').get()
    email = profile.css(".gs_ai_eml::text").get()
    cited_by = re.search(r"\d+", profile.xpath('//div[@class="gs_ai_cby"]').get()).group()  # Cited by 17143 -> 17143
    interests = profile.css(".gs_ai_one_int::text").getall()
```

- `for profile in select.css(".gs_ai_chpr")` is a CSS container with all the profile data over which we need to iterate.
- `css()` is like [`select()`](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#css-selectors) `beautifulsoup` method.
- `::text` or `::attr(<attribute_name>)` is a `parsel` pseudo-element to grab the text or attributes out of the element node, and `get()` will grab the actual data. 
- `xpath('normalize-space()')` will grab those blank text nodes since `css(<selector>::text)` will ignore blank text nodes
 since [`parsel` `css()` method translates everything to XPath](https://github.com/scrapy/parsel/blob/f5f73d34ba787ad0c9df25de295de6e196ecd91d/parsel/selector.py#L350-L351) and pseudo-element `::text` will be translated to XPath `/text()` which ignores blank text nodes.
 `xpath('normalize-space()')` will grab those blank text nodes child nodes. There's an [issue `#62` on Parsel](https://github.com/scrapy/parsel/issues/62) regarding this topic. 
- `getall()` return a `list` of all matches.


Append extracted data as to temporary `list` as dictionary:

```python
profile_results.append({
    "profile_name": name,
    "profile_link": link,
    "profile_affiliations": affiliations,
    "profile_email": email,
    "profile_city_by_count": cited_by,
    "profile_interests": interests
})
```

Check `if` the next page token is present:

```python
# if next page token is present -> update next page token and increment 10 to get the next page
if select.css("button.gs_btnPR::attr(onclick)").get():
    # https://regex101.com/r/e0mq0C/1
    params["after_author"] = re.search(r"after_author\\x3d(.*)\\x26", select.css("button.gs_btnPR::attr(onclick)").get()).group(1)  # -> XB0HAMS9__8J
    params["astart"] += 10
else:
    profiles_is_present = False
```

- `::attr(onclick)` will grab `"onclick"` attribute. 

Return and print the data:

```python
return profile_results

print(json.dumps(scrape_all_authors_from_university(label="biology", university_name="Michigan University"), indent=2))
```

Part of the output:

```json
[
  {
    "profile_name": "Richard McCabe",
    "profile_link": "https://scholar.google.com/citations?hl=en&user=EL414mgAAAAJ",
    "profile_affiliations": "Central Michigan University",
    "profile_email": "Verified email at cmich.edu",
    "profile_city_by_count": "992",
    "profile_interests": [
      "Biology",
      "Physiology",
      "Pathophysiology"
    ]
  }, ... other profiles
]
```

___


Alternatively, you can achieve the same by using [Google Scholar Profiles API](https://serpapi.com/google-scholar-profiles-api) from SerpApi.

The difference is that there's no need to create the parser and maintain it, figure out how to bypass blocks from search engines and how to scale it.

Example code to integrate: 

```python
import os
from urllib.parse import urlsplit, parse_qsl
from serpapi import GoogleSearch


def serpapi_scrape_all_authors_from_university(label: str, university_name: str) -> list[dict[str]]:
    params = {
        "api_key": os.getenv("API_KEY"),                   # SerpApi API key
        "engine": "google_scholar_profiles",               # profile results search engine
        "mauthors":  f'label:{label} "{university_name}"'  # search query
    }
    search = GoogleSearch(params)

    profile_results_data = []

    profiles_is_present = True
    while profiles_is_present:
        profile_results = search.get_dict()

        for profile in profile_results["profiles"]:
            thumbnail = profile["thumbnail"]
            name = profile["name"]
            link = profile["link"]
            author_id = profile["author_id"]
            affiliations = profile["affiliations"]
            email = profile.get("email")
            cited_by = profile.get("cited_by")
            interests = profile.get("interests")

            profile_results_data.append({
                "thumbnail": thumbnail,
                "name": name,
                "link": link,
                "author_id": author_id,
                "email": email,
                "affiliations": affiliations,
                "cited_by": cited_by,
                "interests": interests
            })

            if "next" in profile_results.get("pagination", []):
                # splits URL in parts as a dict() and update search "params" variable to a new page that will be passed to GoogleSearch()
                search.params_dict.update(dict(parse_qsl(urlsplit(profile_results.get("pagination").get("next")).query)))
            else:
                profiles_is_present = False

    return profile_results_data


print(json.dumps(serpapi_scrape_all_authors_from_university(label="biology", university_name="Michigan University"), indent=2))
```

Import libraries:

```python
import os
from urllib.parse import urlsplit, parse_qsl
from serpapi import GoogleSearch
```

- `os` to access environment variable key.
- `urllib` to split URL and pass new page data to the search.

Define a function with argument and return annotations:

```python
def serpapi_scrape_all_authors_from_university(label: str, university_name: str) -> list[dict[str]]:
    # further code
```

Create search parameters and pass them to the search:

```python
params = {
    "api_key": os.getenv("API_KEY"),                   # SerpApi API key
    "engine": "google_scholar_profiles",               # profile results search engine
    "mauthors":  f'label:{label} "{university_name}"'  # search query
}
search = GoogleSearch(params)                          # where data extraction happens
```

Create a temporary `list` where all the extracted data will be stored:

```python
profile_results_data = []
```

Create a `while` loop:

```python
profiles_is_present = True
while profiles_is_present:
    profile_results = search.get_dict()  # JSON converted to Python dictionary 
    # further code..
```

- `search.get_dict()` needs to be in the `while` loop because after each `while` iteration search parameters will be updated. If it will be outside `while` loop, the same search parameters (token ID) will be applying over and over again.  

Iterate over profile results:

```python
for profile in profile_results["profiles"]:

    print(f'Currently extracting {profile["name"]} with {profile["author_id"]} ID.')

    thumbnail = profile["thumbnail"]
    name = profile["name"]
    link = profile["link"]
    author_id = profile["author_id"]
    affiliations = profile["affiliations"]
    email = profile.get("email")
    cited_by = profile.get("cited_by")
    interests = profile.get("interests")
```

Append the extracted data to temporary `list`:

```python
 profile_results_data.append({
    "thumbnail": thumbnail,
    "name": name,
    "link": link,
    "author_id": author_id,
    "email": email,
    "affiliations": affiliations,
    "cited_by": cited_by,
    "interests": interests
})
```

Check `if` `next` page token is present: 

```python
if "next" in profile_results.get("pagination", []):
    # splits URL in parts as a dict() and update search "params" variable to a new page that will be passed to GoogleSearch()
    search.params_dict.update(dict(parse_qsl(urlsplit(profile_results.get("pagination").get("next")).query)))
else:
    profiles_is_present = False

return profile_results_data
```

Print extracted data:

```python
print(json.dumps(serpapi_scrape_all_profiles_from_university(label="Deep_Learning", university_name="Harvard University"), indent=2))
```

Part of the output:

```json
[
  {
    "thumbnail": "https://scholar.googleusercontent.com/citations?view_op=small_photo&user=EL414mgAAAAJ&citpid=3",
    "name": "Richard McCabe",
    "link": "https://scholar.google.com/citations?hl=en&user=EL414mgAAAAJ",
    "author_id": "EL414mgAAAAJ",
    "email": "Verified email at cmich.edu",
    "affiliations": "Central Michigan University",
    "cited_by": 992,
    "interests": [
      {
        "title": "Biology",
        "serpapi_link": "https://serpapi.com/search.json?engine=google_scholar_profiles&hl=en&mauthors=label%3Abiology",
        "link": "https://scholar.google.com/citations?hl=en&view_op=search_authors&mauthors=label:biology"
      },
      {
        "title": "Physiology",
        "serpapi_link": "https://serpapi.com/search.json?engine=google_scholar_profiles&hl=en&mauthors=label%3Aphysiology",
        "link": "https://scholar.google.com/citations?hl=en&view_op=search_authors&mauthors=label:physiology"
      },
      {
        "title": "Pathophysiology",
        "serpapi_link": "https://serpapi.com/search.json?engine=google_scholar_profiles&hl=en&mauthors=label%3Apathophysiology",
        "link": "https://scholar.google.com/citations?hl=en&view_op=search_authors&mauthors=label:pathophysiology"
      }
    ]
  }, ... other profiles results
]
```

___

<h2 id="links">Links</h2>

- [Code in the online IDE](https://replit.com/@DimitryZub1/Scrape-all-Google-Scholar-Profiles-from-certain-University)
- [Google Scholar Profiles API](https://serpapi.com/google-scholar-profiles-api)
- [SerpApi Libraries](https://serpapi.com/libraries)

___

<h2 id="outro">Outro</h2>

If you have anything to share, any questions, suggestions, or something that isn't working correctly, feel free to drop a comment in the comment section or reach out via Twitter at [@dimitryzub](https://twitter.com/DimitryZub), or [@serp_api](https://twitter.com/serp_api).

Yours, Dmitriy, and the rest of SerpApi Team.

___

<p style="text-align: center;">Join us on <a href="https://www.reddit.com/r/SerpApi/">Reddit</a> | <a href="https://twitter.com/serp_api">Twitter</a> | <a href="https://www.youtube.com/channel/UCUgIHlYBOD3yA3yDIRhg_mg">YouTube</a></p>

<p style="text-align: center;">Add a  <a href="https://forum.serpapi.com/feature-requests">Feature Request</a>💫 or a <a href="https://forum.serpapi.com/bugs">Bug</a>🐞</p>

