- <a href="#what_will_be_scraped">What will be scraped</a>
- <a href="#how_to_search_uni">How university filtering works</a>
- <a href="#prerequisites">Prerequisites</a>
- <a href="#full_code">Full Code</a>
  - <a href="#code_explanation">Code explanation</a>
- <a href="#serpapi">SerpApi Solution</a>
- <a href="#links">Links</a>
- <a href="#outro">Outro</a>

<h2 id="what_will_be_scraped">What will be scraped</h2>

![image](https://user-images.githubusercontent.com/78694043/154103222-8d3471a7-cbfe-46ed-9ddb-9369b7c6a518.png)

<h2 id="how_to_search_uni">How university filtering works</h2>

| Search engine operators | Explanation |Search query |
|-------------------------|-------------|-------------|
| Label: `label:<keyword>` | Label is a search keyword | [`label:computer_vision`](https://scholar.google.com/citations?hl=en&view_op=search_authors&mauthors=label%3Acomputer_vision+&btnG=) |
| Double-quotes: `""` | Specific `<university name>` search | [`label:computer_vision "Michigan State University"`](https://scholar.google.com/citations?hl=en&view_op=search_authors&mauthors=label%3Acomputer_vision%20Michigan%20State%20University&btnG=)|
|  Pipe operator: `\|` | `<univ. name>` OR `<univ. abbrivation name>` | [`label:computer_vision "Michigan State University"\|"U.Michigan"`](https://scholar.google.com/citations?hl=en&view_op=search_authors&mauthors=label%3Acomputer_vision%20%22Michigan%20State%20University%22%7C%22U.Michigan%22&btnG=)|

![gif_1_02](https://user-images.githubusercontent.com/78694043/159514111-a28b2fc6-c876-4ed4-be47-e3a505b22f2d.gif)

<h2 id="prerequisites">Prerequisites</h2>

**Basic knowledge scraping with CSS selectors**

CSS selectors declare which part of the markup a style applies to thus allowing to extract data from matching tags and attributes.

If you haven't scraped with CSS selectors, there's a dedicated blog post of mine about [how to use CSS selectors when web-scraping](https://serpapi.com/blog/web-scraping-with-css-selectors-using-python/) that covers what it is, pros and cons, and why they're matter from a web-scraping perspective.


**Separate virtual environment**

If you didn't work with a virtual environment before, have a look at the dedicated [Python virtual environments tutorial using Virtualenv and Poetry](https://serpapi.com/blog/python-virtual-environments-using-virtualenv-and-poetry/) blog post of mine to get familiar.

In short, it's a thing that creates an independent set of installed libraries including different Python versions that can coexist with each other at the same system thus preventing libraries or Python version conflicts.

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

<h2 id="code_explanation">Code Explanation</h2>

Import libraries:

```python
import requests, re, json
from parsel import Selector
```

| Library    | Explanation                                             |
|------------|---------------------------------------------------------|
| `requests` | to make a request.                                      |
| `re`       | to match parts of HTML via regular expression.          |
| `json`     | to make pretty printing, in this case.                  |
|[`parsel`](https://parsel.readthedocs.io/en/latest/index.html)| to extract and remove data from HTML and XML documents. |


Define a function:

```python
def scrape_all_authors_from_university(label: str, university_name: str) -> list[dict[str]]:
    # further code
```

| Code                               | Explanation                                                                           |
|------------------------------------|---------------------------------------------------------------------------------------|
| `label: str, university_name: str` | parameter annotations which tells that `label` and `university_name` should be a `str`|
|`-> list[dict[str]]`|[function return annotation](https://www.python.org/dev/peps/pep-3107/#syntax)|


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

|Code| Explanation                                                                |
|----|----------------------------------------------------------------------------|
|[`User-Agent`](https://developer.mozilla.org/en-US/docs/Glossary/User_agent)| to pretend that it's a "real" user sends a request, not a bot or a script. |


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

| Code                                                                                                                        | Explanation                                                      |
|-----------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------|
| [`timeout=30`](https://docs.python-requests.org/en/master/user/quickstart/#timeouts)                                        | to tell `requests` to stop waiting for response after 30 seconds. |
| [`Selector()`](https://github.com/scrapy/parsel/blob/f5f73d34ba787ad0c9df25de295de6e196ecd91d/parsel/selector.py#L221-L233) | like `BeautifulSoup()` object, if you used it before.        |


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

|Code| Explanation                                                                                                            |
|----|------------------------------------------------------------------------------------------------------------------------|
|`::text` or `::attr(<attribute_name>)`| `parsel` pseudo-element to grab the text or attributes out of the element node, and `get()` will grab the actual data. |
|`xpath('normalize-space()')`| to [grab blank next child nodes](https://github.com/scrapy/parsel/issues/62).                                          |
|`getall()`| to return al `list` of all matches.                                                                                    |


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

| Code                     | Explanation                                       |
|--------------------------|---------------------------------------------------|
| `re.search()`            | to search next page token via regular expression. |
| `params["astart"] += 10` | to increment query parameter to a next page.      |

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

<h2 id="serpapi">SerpApi Solution</h2>

Alternatively, you can achieve the same by using [Google Scholar Profiles API](https://serpapi.com/google-scholar-profiles-api) from SerpApi.

The difference is that there's no need to create the parser and maintain it, figure out how to bypass blocks from search engines and how to scale it.

Example code to integrate to achieve almost the same as in the `parsel` example: 

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

| Code      | Explanation                                                      |
|-----------|------------------------------------------------------------------|
| `os`      | to access environment variable key.                              |
| `urllib`  | to split URL in parts and pass new page data to `GoogleSearch()` |


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

| Code                 | Explanation                                                      |
|----------------------|------------------------------------------------------------------|
| `search.get_dict()`  | needs to be in the `while` loop because after each `while` iteration search parameters will be updated. If it will be outside `while` loop, the same search parameters (token ID) will be applying over and over again.|

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

If you have anything to share, any questions, suggestions, or something that isn't working correctly,reach out via Twitter at [@dimitryzub](https://twitter.com/DimitryZub), or [@serp_api](https://twitter.com/serp_api).

Yours, 
Dmitriy, and the rest of SerpApi Team.

___

<p style="text-align: center;">Join us on <a href="https://www.reddit.com/r/SerpApi/">Reddit</a> | <a href="https://twitter.com/serp_api">Twitter</a> | <a href="https://www.youtube.com/channel/UCUgIHlYBOD3yA3yDIRhg_mg">YouTube</a></p>

<p style="text-align: center;">Add a  <a href="https://github.com/serpapi/SerpApi/issues">Feature Request</a>💫 or a <a href="https://github.com/serpapi/SerpApi/issues">Bug</a>🐞</p>
