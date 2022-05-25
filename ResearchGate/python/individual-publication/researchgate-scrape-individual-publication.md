- <a href="#what_will_be_scraped">What will be scraped</a>
- <a href="#prerequisites">Prerequisites</a>
- <a href="#full_code">Full Code</a>
- <a href="#links">Links</a>

___


<h2 id="what_will_be_scraped">What will be scraped</h2>

![image](https://user-images.githubusercontent.com/78694043/170227531-dfe243c9-35ac-46b2-9890-07029d0a1e50.png)

<h2 id="prerequisites">Prerequisites</h2>

**Basic knowledge scraping with CSS selectors**

If you haven't scraped with CSS selectors, there's a dedicated blog post of mine about [how to use CSS selectors when web-scraping](https://serpapi.com/blog/web-scraping-with-css-selectors-using-python/) that covers what it is, pros and cons, and why they're matter from a web-scraping perspective and show the most common approaches of using CSS selectors when web scraping.

**Separate virtual environment**

If you didn't work with a virtual environment before, have a look at the dedicated [Python virtual environments tutorial using Virtualenv and Poetry](https://serpapi.com/blog/python-virtual-environments-using-virtualenv-and-poetry/) blog post of mine to get familiar.

**Reduce the chance of being blocked**

There's a chance that a request might be blocked. Have a look at [how to reduce the chance of being blocked while web-scraping](https://serpapi.com/blog/how-to-reduce-chance-of-being-blocked-while-web/), there are eleven methods to bypass blocks from most websites.

📌Note: this is not a strict requirement for this blog post.

**Install libraries**:

```lang-none
pip install parsel playwright
```

<h2 id="full_code">Full Code</h2>

```python
from parsel import Selector
from playwright.sync_api import sync_playwright
import json

def scrape_researchgate_publication(publication: str):
    
    with sync_playwright() as p:
        
        browser = p.chromium.launch(headless=True, slow_mo=50)
        page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36",
                                java_script_enabled=True)
        page.goto(f"https://www.researchgate.net/publication/{publication}")
        selector = Selector(text=page.content())

        pubilication_data = {
            "publication_info": {},
            "references": [],
            "recomendations": []   
        }
        
        pubilication_data["publication_info"]["publication_title"] = selector.css(".research-detail-header-section__title::text").get()
        pubilication_data["publication_info"]["publication_type"] = selector.css(".research-detail-header-section__badge:nth-child(2)::text").get()
        pubilication_data["publication_info"]["publication_authors"] = selector.css(".nova-legacy-v-person-list-item__align-content div::text").getall()
        pubilication_data["publication_info"]["publication_date"] = selector.css(".nova-legacy-e-text--color-grey-700 .nova-legacy-e-list__item:nth-child(1)::text").get()
        pubilication_data["publication_info"]["pdf_availability"] = selector.css(".research-detail-header-section__badge:nth-child(3)::text").get()
        pubilication_data["publication_info"]["pdf_link"] = f'https://www.researchgate.net{selector.css(".research-detail-header-cta__buttons a:nth-child(1)::attr(href)").get()}'
        pubilication_data["publication_info"]["publication_full_text_link"] = selector.css(".research-detail-header-cta__buttons a:nth-child(2)::attr(href)").get()
        pubilication_data["publication_info"]["publication_journal"] = selector.css(".nova-legacy-e-text--color-grey-700+ .nova-legacy-e-text--color-grey-700 .nova-legacy-e-link--theme-decorated::text").get()
        pubilication_data["publication_info"]["publication_journal_link"] = f'https://www.researchgate.net{selector.css(".nova-legacy-e-text--color-grey-700+ .nova-legacy-e-text--color-grey-700 .nova-legacy-e-link--theme-decorated::attr(href)").get()}'
        pubilication_data["publication_info"]["citation_link"] = selector.css(".nova-legacy-l-flex__item.hide-l a:nth-child(1)::attr(href)").get()
        
        for reference in selector.css(".publication-citations__item--redesign"):
            pubilication_data["references"].append({
                "title": reference.css(".nova-legacy-v-publication-item__title::text").get(),
                "link": f'https://www.researchgate.net{reference.css(".nova-legacy-v-publication-item__title a::attr(href)").get()}',
                "reference_type": reference.css(".nova-legacy-v-publication-item__type::text").get(),
                "full_text_availability": reference.css(".nova-legacy-v-publication-item__fulltext::text").get(),
                "authors": reference.css(".nova-legacy-v-person-inline-item__fullname::text").getall(),
                "publication_date": reference.css(".nova-legacy-v-publication-item__meta-data-item:nth-child(1) span::text").get(),
            })
        
        for recommendation in selector.css(".nova-legacy-c-card__body.nova-legacy-c-card__body--spacing-inherit"):
            pubilication_data["recomendations"].append({
                "type": recommendation.css(".nova-legacy-e-badge::text").get(),
                "title": recommendation.css(".nova-legacy-e-text.nova-legacy-e-text--size-l a::text").get(),
                "link": recommendation.css(".nova-legacy-e-text.nova-legacy-e-text--size-l a::attr(href)").get(),
                "authors": recommendation.css(".nova-legacy-v-person-inline-item__fullname::text").getall(),
                "date": recommendation.css(".nova-legacy-e-text span:nth-child(1)::text").getall(),
            })

        print(json.dumps(pubilication_data, indent=2, ensure_ascii=False))
        
        browser.close()


# accepts publication ID: 340715390
# as well as full path: researchgate.net/publication/340715390_Transforming_Technology_for_Global_Business_Acceleration_and_Change_Management
scrape_researchgate_publication(publication="352677424")
```

### Code explanation

Import libraries:

```python
from parsel import Selector
from playwright.sync_api import sync_playwright
import json
```

|Code|Explanation|
|----|-----------|
|[`parsel`](https://parsel.readthedocs.io/)|to parse HTML/XML documents. Supports XPath.|
|[`playwright`](https://playwright.dev/python/docs/intro#first-script)|to render the page with a browser instance.|
|`json`|to convert Python dictionary to JSON string.|

Define a function and open a `playwright` with a [context manager](https://book.pythontips.com/en/latest/context_managers.html)::

```python
def scrape_researchgate_publication(publication: str):
    with sync_playwright() as p:
        # ...
```
|Code|Explanation|
|----|-----------|
|`publication: str`|to tell Python that `publication` should be an `str`.|


Lunch a browser instance, open `new_page()`, and `goto()` target website:

```python
browser = p.chromium.launch(headless=True, slow_mo=50)
page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36",
                        java_script_enabled=True)
page.goto(f"https://www.researchgate.net/publication/{publication}")
selector = Selector(text=page.content())
```

|Code|Explanation|
|----|-----------|
|[`p.chromium.launch()`](https://github.com/microsoft/playwright-python/blob/3b7968fb2ea4238a89447b3c7766f9f1f9c9c0e3/playwright/sync_api/_generated.py#L11423)|to launch Chromium browser instance.|
|[`headless`](https://github.com/microsoft/playwright-python/blob/3b7968fb2ea4238a89447b3c7766f9f1f9c9c0e3/playwright/sync_api/_generated.py#L11500-L11504)|to explicitly tell `playwright` to run in headless mode even though it's a defaut value.|
|[`slow_mo`](https://github.com/microsoft/playwright-python/blob/3b7968fb2ea4238a89447b3c7766f9f1f9c9c0e3/playwright/sync_api/_generated.py#L11514-L11515)|to tell `playwright` to slow down execution.|
|[`browser.new_page()`](https://playwright.dev/python/docs/api/class-browser#browser-new-page)|to open new page. `user_agent` is used to act a real user makes a request from the browser. If not used, it will default to `playwright` value which is `None`. [Check what's your user-agent](https://www.whatismybrowser.com/detect/what-is-my-user-agent/).|
|[`goto()`](https://playwright.dev/python/docs/api/class-page#page-goto)|to make a request to specific URL with passed query and page parameters.|
|`Selector()`|to pass returned HTML data from the [`page.content()`](https://playwright.dev/python/docs/api/class-page#page-content) and process it.|


Create a dictionary structure to append extracted data:

```python
pubilication_data = {
    "publication_info": {},  # dict is used bacause there will be one occurence of specifc data
    "references": [],        # list is used because there will be more than a 1 reference
    "recomendations": []     # list is used because there will be more than a 1 recomendadtion
}
```


Extract basic information data from the page and update exitsting `["publication_info"]` `dict` key with a newly added key `["<new_key>"]` and pass extracted data:

```python
pubilication_data["publication_info"]["publication_title"] = selector.css(".research-detail-header-section__title::text").get()
pubilication_data["publication_info"]["publication_type"] = selector.css(".research-detail-header-section__badge:nth-child(2)::text").get()
pubilication_data["publication_info"]["publication_authors"] = selector.css(".nova-legacy-v-person-list-item__align-content div::text").getall()
pubilication_data["publication_info"]["publication_date"] = selector.css(".nova-legacy-e-text--color-grey-700 .nova-legacy-e-list__item:nth-child(1)::text").get()
pubilication_data["publication_info"]["pdf_availability"] = selector.css(".research-detail-header-section__badge:nth-child(3)::text").get()
pubilication_data["publication_info"]["pdf_link"] = f'https://www.researchgate.net{selector.css(".research-detail-header-cta__buttons a:nth-child(1)::attr(href)").get()}'
pubilication_data["publication_info"]["publication_full_text_link"] = selector.css(".research-detail-header-cta__buttons a:nth-child(2)::attr(href)").get()
pubilication_data["publication_info"]["publication_journal"] = selector.css(".nova-legacy-e-text--color-grey-700+ .nova-legacy-e-text--color-grey-700 .nova-legacy-e-link--theme-decorated::text").get()
pubilication_data["publication_info"]["publication_journal_link"] = f'https://www.researchgate.net{selector.css(".nova-legacy-e-text--color-grey-700+ .nova-legacy-e-text--color-grey-700 .nova-legacy-e-link--theme-decorated::attr(href)").get()}'
pubilication_data["publication_info"]["citation_link"] = selector.css(".nova-legacy-l-flex__item.hide-l a:nth-child(1)::attr(href)").get()
```

Iterate over reference, recommendation results and `update` corresponding `dict` key:

```python
for reference in selector.css(".publication-citations__item--redesign"):
    pubilication_data["references"].append({
        "title": reference.css(".nova-legacy-v-publication-item__title::text").get(),
        "link": f'https://www.researchgate.net{reference.css(".nova-legacy-v-publication-item__title a::attr(href)").get()}',
        "reference_type": reference.css(".nova-legacy-v-publication-item__type::text").get(),
        "full_text_availability": reference.css(".nova-legacy-v-publication-item__fulltext::text").get(),
        "authors": reference.css(".nova-legacy-v-person-inline-item__fullname::text").getall(),
        "publication_date": reference.css(".nova-legacy-v-publication-item__meta-data-item:nth-child(1) span::text").get(),
    })

for recommendation in selector.css(".nova-legacy-c-card__body.nova-legacy-c-card__body--spacing-inherit"):
    pubilication_data["recomendations"].append({
        "type": recommendation.css(".nova-legacy-e-badge::text").get(),
        "title": recommendation.css(".nova-legacy-e-text.nova-legacy-e-text--size-l a::text").get(),
        "link": recommendation.css(".nova-legacy-e-text.nova-legacy-e-text--size-l a::attr(href)").get(),
        "authors": recommendation.css(".nova-legacy-v-person-inline-item__fullname::text").getall(),
        "date": recommendation.css(".nova-legacy-e-text span:nth-child(1)::text").getall(),
    })
```

|Code|Explanation|
|----|-----------|
|`css()`|[to parse data from the passed CSS selector(s)](https://github.com/scrapy/parsel/blob/90397dcd0b2c1cbb91e44f65c50f9e11628ba028/parsel/selector.py#L351-L362). Every [CSS query traslates to XPath using `csselect` package](https://github.com/scrapy/parsel/blob/90397dcd0b2c1cbb91e44f65c50f9e11628ba028/parsel/selector.py#L357-L358) under the hood.|
|`::text`/`::attr(attribute)`|[to extract textual or attribute data](https://github.com/scrapy/parsel/blob/90397dcd0b2c1cbb91e44f65c50f9e11628ba028/parsel/csstranslator.py#L48-L51) from the node.|
|`get()`/`getall()`|[to get actual data from a matched node](https://github.com/scrapy/parsel/blob/90397dcd0b2c1cbb91e44f65c50f9e11628ba028/parsel/selector.py#L197-L204), or to [get a `list` of matched data from nodes](https://github.com/scrapy/parsel/blob/90397dcd0b2c1cbb91e44f65c50f9e11628ba028/parsel/selector.py#L447-L451).|
|`xpath("normalize-space()")`|to parse blank text node as well. By default, blank text node is be skipped by XPath.|
|`f'https://www.researchgate.net{selector.css("<selector>").get()}'`|to add `https://www.researchgate.net` to extracted data from the selector using [`f-string`](https://docs.python.org/3/tutorial/inputoutput.html#fancier-output-formatting).|


Print extracted data, `close` browser instance, and call the function:

```python
    # ....
    print(json.dumps(pubilication_data, indent=2, ensure_ascii=False))
    browser.close()

scrape_researchgate_publication(publication="352677424")
```

Part of the JSON output:

```json
# TODO: ADD JSON output
```

___

<h2 id="links">Links</h2>

- [GitHub Gist](https://gist.github.com/dimitryzub/4bce8fdb02629c47e7c8011668349589)

___

<p style="text-align: center;">Join us on <a href="https://twitter.com/serp_api">Twitter</a> | <a href="https://www.youtube.com/channel/UCUgIHlYBOD3yA3yDIRhg_mg">YouTube</a></p>

<p style="text-align: center;">Add a  <a href="https://github.com/serpapi/public-roadmap/issues">Feature Request</a>💫 or a <a href="https://github.com/serpapi/public-roadmap/issues">Bug</a>🐞</p>