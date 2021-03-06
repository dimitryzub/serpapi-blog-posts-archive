- <a href="#what_will_be_scraped">What will be scraped</a>
- <a href="#prerequisites">Prerequisites</a>
- <a href="#full_code">Full Code</a>

___

<h2 id="what_will_be_scraped">What will be scraped</h2>

![image](https://user-images.githubusercontent.com/78694043/169801695-de596d5a-3989-486e-b96a-32f3bd471c20.png)

<h2 id="prerequisites">Prerequisites</h2>

**Basic knowledge scraping with CSS selectors**

CSS selectors declare which part of the markup a style applies to thus allowing to extract of data from matching tags and attributes.

If you haven't scraped with CSS selectors, there's a dedicated blog post of mine about [how to use CSS selectors when web-scraping](https://serpapi.com/blog/web-scraping-with-css-selectors-using-python/) that covers what it is, pros and cons, and why they're matter from a web-scraping perspective and show the most common approaches of using CSS selectors when web scraping.

**Reduce the chance of being blocked**

There's a chance that a request might be blocked. Have a look at [how to reduce the chance of being blocked while web-scraping](https://serpapi.com/blog/how-to-reduce-chance-of-being-blocked-while-web/), there are eleven methods to bypass blocks from most websites.

**Install libraries**:

```lang-none
pip install parsel playwright
```

<h2 id="full_code">Full Code</h2>

```python
from parsel import Selector
from playwright.sync_api import sync_playwright
import json, re 


def scrape_researchgate_profile(profile: str):
    with sync_playwright() as p:
        
        profile_data = {
            "basic_info": {},
            "about": {},
            "co_authors": [],
            "publications": [],
        }
        
        browser = p.chromium.launch(headless=True, slow_mo=50)
        page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36")
        page.goto(f"https://www.researchgate.net/profile/{profile}")
        selector = Selector(text=page.content())
        
        profile_data["basic_info"]["name"] = selector.css(".nova-legacy-e-text.nova-legacy-e-text--size-xxl::text").get()
        profile_data["basic_info"]["institution"] = selector.css(".nova-legacy-v-institution-item__stack-item a::text").get()
        profile_data["basic_info"]["department"] = selector.css(".nova-legacy-e-list__item.nova-legacy-v-institution-item__meta-data-item:nth-child(1)").xpath("normalize-space()").get()
        profile_data["basic_info"]["current_position"] = selector.css(".nova-legacy-e-list__item.nova-legacy-v-institution-item__info-section-list-item").xpath("normalize-space()").get()
        profile_data["basic_info"]["lab"] = selector.css(".nova-legacy-o-stack__item .nova-legacy-e-link--theme-bare b::text").get()
        
        profile_data["about"]["number_of_publications"] = re.search(r"\d+", selector.css(".nova-legacy-c-card__body .nova-legacy-o-grid__column:nth-child(1)").xpath("normalize-space()").get()).group()
        profile_data["about"]["reads"] = re.search(r"\d+", selector.css(".nova-legacy-c-card__body .nova-legacy-o-grid__column:nth-child(2)").xpath("normalize-space()").get()).group()
        profile_data["about"]["citations"] = re.search(r"\d+", selector.css(".nova-legacy-c-card__body .nova-legacy-o-grid__column:nth-child(3)").xpath("normalize-space()").get()).group()
        profile_data["about"]["introduction"] = selector.css(".nova-legacy-o-stack__item .Linkify").xpath("normalize-space()").get()
        profile_data["about"]["skills"] = selector.css(".nova-legacy-l-flex__item .nova-legacy-e-badge ::text").getall()
        
        for co_author in selector.css(".nova-legacy-c-card--spacing-xl .nova-legacy-c-card__body--spacing-inherit .nova-legacy-v-person-list-item"):
            profile_data["co_authors"].append({
                "name": co_author.css(".nova-legacy-v-person-list-item__align-content .nova-legacy-e-link::text").get(),
                "link": co_author.css(".nova-legacy-l-flex__item a::attr(href)").get(),
                "avatar": co_author.css(".nova-legacy-l-flex__item .lite-page-avatar img::attr(data-src)").get(),
                "current_institution": co_author.css(".nova-legacy-v-person-list-item__align-content li").xpath("normalize-space()").get()
            })

        for publication in selector.css("#publications+ .nova-legacy-c-card--elevation-1-above .nova-legacy-o-stack__item"):
            profile_data["publications"].append({
                "title": publication.css(".nova-legacy-v-publication-item__title .nova-legacy-e-link--theme-bare::text").get(),
                "date_published": publication.css(".nova-legacy-v-publication-item__meta-data-item span::text").get(),
                "authors": publication.css(".nova-legacy-v-person-inline-item__fullname::text").getall(),
                "publication_type": publication.css(".nova-legacy-e-badge--theme-solid::text").get(),
                "description": publication.css(".nova-legacy-v-publication-item__description::text").get(),
                "publication_link": publication.css(".nova-legacy-c-button-group__item .nova-legacy-c-button::attr(href)").get(),
            })
            
            
        print(json.dumps(profile_data, indent=2, ensure_ascii=False))

        browser.close()
        
    
scrape_researchgate_profile(profile="Agnis-Stibe")
```

### Code explanation

Import libraries:

```python
from parsel import Selector
from playwright.sync_api import sync_playwright
import re, json, time
```

|Code|Explanation|
|----|-----------|
|[`parsel`](https://parsel.readthedocs.io/)|to parse HTML/XML documents. Supports XPath.|
|[`playwright`](https://playwright.dev/python/docs/intro#first-script)|to render the page with a browser instance.|
|`re`|to match parts of the data with regular expression.|
|`json`|to convert Python dictionary to JSON string.|

Define a function:

```python
def scrape_researchgate_profile(profile: str):
    # ...
```
|Code|Explanation|
|----|-----------|
|`profile: str`|to tell Python that `profile` should be an `str`.|


Open a `playwright` with a [context manager](https://book.pythontips.com/en/latest/context_managers.html):

```python
with sync_playwright() as p:
    # ...
```

Define the structure of the extracted data:

```python
profile_data = {
    "basic_info": {},
    "about": {},
    "co_authors": [],
    "publications": [],
}
```

Lunch a browser instance, open and `goto` the page and pass response to HTML/XML parser:

```python
browser = p.chromium.launch(headless=True, slow_mo=50)
page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36")
page.goto(f"https://www.researchgate.net/profile/{profile}")
selector = Selector(text=page.content())
```

|Code|Explanation|
|----|-----------|
|[`p.chromium.launch()`](https://github.com/microsoft/playwright-python/blob/3b7968fb2ea4238a89447b3c7766f9f1f9c9c0e3/playwright/sync_api/_generated.py#L11423)|to launch Chromium browser instance.|
|[`headless`](https://github.com/microsoft/playwright-python/blob/3b7968fb2ea4238a89447b3c7766f9f1f9c9c0e3/playwright/sync_api/_generated.py#L11500-L11504)|to explicitly tell `playwright` to run in headless mode even though it's a defaut value.|
|[`slow_mo`](https://github.com/microsoft/playwright-python/blob/3b7968fb2ea4238a89447b3c7766f9f1f9c9c0e3/playwright/sync_api/_generated.py#L11514-L11515)|to tell `playwright` to slow down execution.|
|[`browser.new_page()`](https://playwright.dev/python/docs/api/class-browser#browser-new-page)|to open new page. `user_agent` is used to act a real user makes a request from the browser. If not used, it will default to `playwright` value which is `None`. [Check what's your user-agent](https://www.whatismybrowser.com/detect/what-is-my-user-agent/).|

 
Update `basic_info` dictionary key, create new keys, and assing extracted data:

```python
profile_data["basic_info"]["name"] = selector.css(".nova-legacy-e-text.nova-legacy-e-text--size-xxl::text").get()
profile_data["basic_info"]["institution"] = selector.css(".nova-legacy-v-institution-item__stack-item a::text").get()
profile_data["basic_info"]["department"] = selector.css(".nova-legacy-e-list__item.nova-legacy-v-institution-item__meta-data-item:nth-child(1)").xpath("normalize-space()").get()
profile_data["basic_info"]["current_position"] = selector.css(".nova-legacy-e-list__item.nova-legacy-v-institution-item__info-section-list-item").xpath("normalize-space()").get()
profile_data["basic_info"]["lab"] = selector.css(".nova-legacy-o-stack__item .nova-legacy-e-link--theme-bare b::text").get()
```

|Code|Explanation|
|----|-----------|
|`profile_data["basic_info"]["name"]`|to access earlier created `basic_info` key, and then create a new `["name"]` key, and assign extracted data.|
|`css()`|[to parse data from the passed CSS selector(s)](https://github.com/scrapy/parsel/blob/90397dcd0b2c1cbb91e44f65c50f9e11628ba028/parsel/selector.py#L351-L362). Every [CSS query traslates to XPath using `csselect` package](https://github.com/scrapy/parsel/blob/90397dcd0b2c1cbb91e44f65c50f9e11628ba028/parsel/selector.py#L357-L358) under the hood.|
|`::text`|[to extract textual data](https://github.com/scrapy/parsel/blob/90397dcd0b2c1cbb91e44f65c50f9e11628ba028/parsel/csstranslator.py#L48-L51) from the node.|
|`get()`|[to get actual data from a matched node](https://github.com/scrapy/parsel/blob/90397dcd0b2c1cbb91e44f65c50f9e11628ba028/parsel/selector.py#L197-L204)|
|`xpath("normalize-space()")`|to parse blank text node as well. By default, blank text node is be skipped by XPath.|

Update `about` dictionary key, create new keys, and assing extracted data:

```python
profile_data["about"]["number_of_publications"] = re.search(r"\d+", selector.css(".nova-legacy-c-card__body .nova-legacy-o-grid__column:nth-child(1)").xpath("normalize-space()").get()).group()
profile_data["about"]["reads"] = re.search(r"\d+", selector.css(".nova-legacy-c-card__body .nova-legacy-o-grid__column:nth-child(2)").xpath("normalize-space()").get()).group()
profile_data["about"]["citations"] = re.search(r"\d+", selector.css(".nova-legacy-c-card__body .nova-legacy-o-grid__column:nth-child(3)").xpath("normalize-space()").get()).group()
profile_data["about"]["introduction"] = selector.css(".nova-legacy-o-stack__item .Linkify").xpath("normalize-space()").get()
profile_data["about"]["skills"] = selector.css(".nova-legacy-l-flex__item .nova-legacy-e-badge ::text").getall()
```

|Code|Explanation|
|----|-----------|
|`profile_data["basic_info"]["name"]`|to access earlier created `basic_info` key, and then create a new `["name"]` key, and assign extracted data.|
|`re.search(r"\d+", <returned_data_from_parsel>).group()`|to extract digit data via [`re.search()`](https://docs.python.org/3/library/re.html#re.search) regular expression [`\d+`](https://docs.python.org/3/library/re.html#regular-expression-syntax) from the returned string. [`group()`](https://docs.python.org/3/library/re.html#re.Match.group) is to extract substring that was matched by the regular expression.|
|`css()`|[to parse data from the passed CSS selector(s)](https://github.com/scrapy/parsel/blob/90397dcd0b2c1cbb91e44f65c50f9e11628ba028/parsel/selector.py#L351-L362). Every [CSS query traslates to XPath using `csselect` package](https://github.com/scrapy/parsel/blob/90397dcd0b2c1cbb91e44f65c50f9e11628ba028/parsel/selector.py#L357-L358) under the hood.|
|`::text`|[to extract textual data](https://github.com/scrapy/parsel/blob/90397dcd0b2c1cbb91e44f65c50f9e11628ba028/parsel/csstranslator.py#L48-L51) from the node.|
|`get()`/`getall()`|[to get actual data from a matched node](https://github.com/scrapy/parsel/blob/90397dcd0b2c1cbb91e44f65c50f9e11628ba028/parsel/selector.py#L197-L204), or to [get a `list` of matched data from nodes](https://github.com/scrapy/parsel/blob/90397dcd0b2c1cbb91e44f65c50f9e11628ba028/parsel/selector.py#L447-L451).|
|`xpath("normalize-space()")`|to parse blank text node as well. By default, blank text node is be skipped by XPath.|

Iterate over co-authors and extract individual co-author, and append to the temporary list:

```python
for co_author in selector.css(".nova-legacy-c-card--spacing-xl .nova-legacy-c-card__body--spacing-inherit .nova-legacy-v-person-list-item"):
    profile_data["co_authors"].append({
        "name": co_author.css(".nova-legacy-v-person-list-item__align-content .nova-legacy-e-link::text").get(),
        "link": co_author.css(".nova-legacy-l-flex__item a::attr(href)").get(),
        "avatar": co_author.css(".nova-legacy-l-flex__item .lite-page-avatar img::attr(data-src)").get(),
        "current_institution": co_author.css(".nova-legacy-v-person-list-item__align-content li").xpath("normalize-space()").get()
    })
```

|Code|Explanation|
|----|-----------|
|`::attr(attribute)`|[to extract attribute data](https://github.com/scrapy/parsel/blob/90397dcd0b2c1cbb91e44f65c50f9e11628ba028/parsel/csstranslator.py#L48-L51) from the node.|

Next is to iterate over all publications and extract individual publications, and append to a temporary list:

```python
for publication in selector.css("#publications+ .nova-legacy-c-card--elevation-1-above .nova-legacy-o-stack__item"):
    profile_data["publications"].append({
        "title": publication.css(".nova-legacy-v-publication-item__title .nova-legacy-e-link--theme-bare::text").get(),
        "date_published": publication.css(".nova-legacy-v-publication-item__meta-data-item span::text").get(),
        "authors": publication.css(".nova-legacy-v-person-inline-item__fullname::text").getall(),
        "publication_type": publication.css(".nova-legacy-e-badge--theme-solid::text").get(),
        "description": publication.css(".nova-legacy-v-publication-item__description::text").get(),
        "publication_link": publication.css(".nova-legacy-c-button-group__item .nova-legacy-c-button::attr(href)").get(),
    })
```


Print extracted data, and [`close`](https://playwright.dev/python/docs/api/class-browser#browser-close) browser instance:

```python
print(json.dumps(profile_data, indent=2, ensure_ascii=False))

browser.close()


# call function. "profiles" could be a list of authors.
# author name should be with a "-", othwerwise ResearchGate doesn't recognize it.
scrape_researchgate_profile(profile="Agnis-Stibe")
```

Part of the JSON output:

```json
{
  "basic_info": {
    "name": "Agnis Stibe",
    "institution": "EM Normandie Business School",
    "department": "Supply Chain Management & Decision Sciences",
    "current_position": "Artificial Inteligence Program Director",
    "lab": "Riga Technical University"
  },
  "about": {
    "number_of_publications": "71",
    "reads": "40",
    "citations": "572",
    "introduction": "4x TEDx speaker, MIT alum, YouTube creator. Globally recognized corporate consultant and scientific advisor at AgnisStibe.com. Provides a science-driven STIBE method and practical tools for hyper-performance. Academic Director on Artificial Intelligence and Professor of Transformation at EM Normandie Business School. Paris Lead of Silicon Valley founded Transformative Technology community. At the renowned Massachusetts Institute of Technology, he established research on Persuasive Cities.",
    "skills": [
      "Social Influence",
      "Behavior Change",
      "Persuasive Design",
      "Motivational Psychology",
      "Artificial Intelligence",
      "Change Management",
      "Business Transformation"
    ]
  },
  "co_authors": [
    {
      "name": "Mina Khan",
      "link": "profile/Mina-Khan-2",
      "avatar": "https://i1.rgstatic.net/ii/profile.image/387771463159814-1469463329918_Q64/Mina-Khan-2.jpg",
      "current_institution": "Massachusetts Institute of Technology"
    }, ... other co-authors
  ],
  "publications": [
    {
      "title": "Change Masters: Using the Transformation Gene to Empower Hyper-Performance at Work",
      "date_published": "May 2020",
      "authors": [
        "Agnis Stibe"
      ],
      "publication_type": "Article",
      "description": "Achieving hyper-performance is an essential aim not only for organizations and societies but also for individuals. Digital transformation is reshaping the workplace so fast that people start falling behind, with their poor attitudes remaining the ultimate obstacle. The alignment of human-machine co-evolution is the only sustainable strategy for the...",
      "publication_link": "https://www.researchgate.net/publication/342716663_Change_Masters_Using_the_Transformation_Gene_to_Empower_Hyper-Performance_at_Work"
    }, ... other publications
  ]
}
```

___


<p style="text-align: center;">Join us on <a href="https://twitter.com/serp_api">Twitter</a> | <a href="https://www.youtube.com/channel/UCUgIHlYBOD3yA3yDIRhg_mg">YouTube</a></p>

<p style="text-align: center;">Add a  <a href="https://github.com/serpapi/public-roadmap/issues">Feature Request</a>???? or a <a href="https://github.com/serpapi/public-roadmap/issues">Bug</a>????</p>