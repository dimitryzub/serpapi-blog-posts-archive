- <a href="#what_will_be_scraped">What will be scraped</a>
- <a href="#prerequisites">Prerequisites</a>
- <a href="#full_code">Full Code</a>
- <a href="#links">Links</a>

___


<h2 id="what_will_be_scraped">What will be scraped</h2>

![image](https://user-images.githubusercontent.com/78694043/170428092-2e07dc4f-dce5-4692-9032-d50883469948.png)

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
import json, re


def scrape_researchgate_journal(journal_name: str):
    with sync_playwright() as p:
        
        journal_data = {
            "basic_info": {},
            "publications": [],
            "top_cited_authors": []
        }
        
        browser = p.chromium.launch(headless=True, slow_mo=50)
        page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36")
        page.goto(f"https://www.researchgate.net/journal/{journal_name}")
        selector = Selector(text=page.content())

        journal_data["basic_info"]["title"] = selector.css("nova-legacy-o-stack__item h1::text").get()
        
        for cited_author in selector.css(".nova-legacy-v-person-list-item"):
            name = cited_author.css("nova-legacy-v-person-list-item__title::text").get()
            link = f'https://www.researchgate.net{cited_author.css("nova-legacy-v-person-list-item__title a::attr(href)").get()}'
            avatar = cited_author.css(".nova-legacy-l-flex__item img::attr(src)").get()
            institution = cited_author.css(".nova-legacy-v-person-list-item__meta-item::text").get()
            citations = cited_author.css(".nova-legacy-v-person-list-item__metrics-item::text").get()        
        
            journal_data["top_cited_authors"].append({
                "name": name,
                "link": link,
                "avatar": avatar,
                "institution": institution,
                "citations": citations,
            })
        
        # scrape publications from the first page
        for publication in selector.css(".nova-legacy-v-publication-item"):
            title = publication.css("nova-legacy-v-publication-item__title::text").get()
            link = f'https://www.researchgate.net{publication.css("nova-legacy-v-publication-item__title a::attr(href)").get()}'
            publication_type = publication.css("nova-legacy-v-publication-item__type::text").get()
            publication_date = publication.css(".nova-legacy-v-publication-item__meta-data-item::text").get()
            authors_name = publication.css(".nova-legacy-v-person-inline-item::text").get()
            snippet = publication.css("nova-legacy-e-expandable-text__container::text").get()
            reads = re.search(r"\d+", publication.css(".nova-legacy-v-publication-item__metrics-item::nth-child(1)::text").get()).group()
            citations = re.search(r"\d+", publication.css(".nova-legacy-v-publication-item__metrics-item::nth-child(2)").get()).group()
            
            journal_data["publications"].append({
                "title": title,
                "link": link,
                "publication_type": publication_type,
                "publication_date": publication_date,
                "authors": authors_name,
                "snippet": snippet,
                "reads": reads,
                "citations": citations
            })
            
        # scrape rest of the data starting from the second page
        page_num = 2
        
        while True:
            page.goto(f"https://www.researchgate.net/journal/{journal_name}/{page_num}")
            selector = Selector(text=page.content())

            for publication in selector.css(".nova-legacy-v-publication-item"):
                title = publication.css("nova-legacy-v-publication-item__title::text").get()
                link = f'https://www.researchgate.net{publication.css("nova-legacy-v-publication-item__title a::attr(href)").get()}'
                publication_type = publication.css("nova-legacy-v-publication-item__type::text").get()
                publication_date = publication.css(".nova-legacy-v-publication-item__meta-data-item::text").get()
                authors_name = publication.css(".nova-legacy-v-person-inline-item::text").get()
                snippet = publication.css("nova-legacy-e-expandable-text__container::text").get()
                reads = re.search(r"\d+", publication.css(".nova-legacy-v-publication-item__metrics-item::nth-child(1)::text").get()).group()
                citations = re.search(r"\d+", publication.css(".nova-legacy-v-publication-item__metrics-item::nth-child(2)").get()).group()
                
                journal_data["publications"].append({
                    "title": title,
                    "link": link,
                    "publication_type": publication_type,
                    "publication_date": publication_date,
                    "authors": authors_name,
                    "snippet": snippet,
                    "reads": reads,
                    "citations": citations
                })
            
            
            # checks for selector responsible for disabled pagination
            # if there's no page to paginate -> break
            if selector.css(".nova-legacy-c-pagination__next.is-disabled").get():
                break
            
            page_num += 1

        
        print(json.dumps(journal_data, indent=2, ensure_ascii=False))
        browser.close()
              
        
scrape_researchgate_journal(journal_name="Journal-of-Global-Information-Technology-Management-1097-198X")
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
def scrape_researchgate_journal(journal_name: str):
    with sync_playwright() as p:
        # ...
```
|Code|Explanation|
|----|-----------|
|`publication: str`|to tell Python that `publication` should be an `str`.|

Create a structure for extracted data:

```python
journal_data = {
    "basic_info": {},        # a dict because there's no sequence info, only single amount of data
    "publications": [],      # a list because there's a sequence of publications, it's handy if you need to iterate over them
    "top_cited_authors": []  # a list because there's a sequence of publications, it's handy if you need to iterate over them
}
```

Lunch a browser instance, open `new_page()`, and `goto()` target website:

```python
browser = p.chromium.launch(headless=True, slow_mo=50)
page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36")
page.goto(f"https://www.researchgate.net/journal/{journal_name}") # {journal_name} is a journal name argument passed in the function call
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


Extract basic information data, and iterate over cited authors, and publications and update/append the data to `journal_data` dictionary:

```python
# ["title"] is a new key that will be added to the ["basic_info"] key
journal_data["basic_info"]["title"] = selector.css("nova-legacy-o-stack__item h1::text").get()
        
    for cited_author in selector.css(".nova-legacy-v-person-list-item"):
        name = cited_author.css("nova-legacy-v-person-list-item__title::text").get()
        link = f'https://www.researchgate.net{cited_author.css("nova-legacy-v-person-list-item__title a::attr(href)").get()}'
        avatar = cited_author.css(".nova-legacy-l-flex__item img::attr(src)").get()
        institution = cited_author.css(".nova-legacy-v-person-list-item__meta-item::text").get()
        citations = cited_author.css(".nova-legacy-v-person-list-item__metrics-item::text").get()        
    
        journal_data["top_cited_authors"].append({
            "name": name,
            "link": link,
            "avatar": avatar,
            "institution": institution,
            "citations": citations,
        })
    
    # scrape publications from the first page
    for publication in selector.css(".nova-legacy-v-publication-item"):
        title = publication.css("nova-legacy-v-publication-item__title::text").get()
        link = f'https://www.researchgate.net{publication.css("nova-legacy-v-publication-item__title a::attr(href)").get()}'
        publication_type = publication.css("nova-legacy-v-publication-item__type::text").get()
        publication_date = publication.css(".nova-legacy-v-publication-item__meta-data-item::text").get()
        authors_name = publication.css(".nova-legacy-v-person-inline-item::text").get()
        snippet = publication.css("nova-legacy-e-expandable-text__container::text").get()
        reads = re.search(r"\d+", publication.css(".nova-legacy-v-publication-item__metrics-item::nth-child(1)::text").get()).group()
        citations = re.search(r"\d+", publication.css(".nova-legacy-v-publication-item__metrics-item::nth-child(2)").get()).group()
        
        journal_data["publications"].append({
            "title": title,
            "link": link,
            "publication_type": publication_type,
            "publication_date": publication_date,
            "authors": authors_name,
            "snippet": snippet,
            "reads": reads,
            "citations": citations
        })
```

|Code|Explanation|
|----|-----------|
|`css()`|[to parse data from the passed CSS selector(s)](https://github.com/scrapy/parsel/blob/90397dcd0b2c1cbb91e44f65c50f9e11628ba028/parsel/selector.py#L351-L362). Every [CSS query traslates to XPath using `csselect` package](https://github.com/scrapy/parsel/blob/90397dcd0b2c1cbb91e44f65c50f9e11628ba028/parsel/selector.py#L357-L358) under the hood.|
|`::text`/`::attr(attribute)`|[to extract textual or attribute data](https://github.com/scrapy/parsel/blob/90397dcd0b2c1cbb91e44f65c50f9e11628ba028/parsel/csstranslator.py#L48-L51) from the node.|
|`get()`/`getall()`|[to get actual data from a matched node](https://github.com/scrapy/parsel/blob/90397dcd0b2c1cbb91e44f65c50f9e11628ba028/parsel/selector.py#L197-L204), or to [get a `list` of matched data from nodes](https://github.com/scrapy/parsel/blob/90397dcd0b2c1cbb91e44f65c50f9e11628ba028/parsel/selector.py#L447-L451).|
|`xpath("normalize-space()")`|to parse blank text node as well. By default, blank text node is be skipped by XPath.|
|`f'https://www.researchgate.net{selector.css("<selector>").get()}'`|to add `https://www.researchgate.net` to extracted data from the selector using [`f-string`](https://docs.python.org/3/tutorial/inputoutput.html#fancier-output-formatting).|


Create a `page_num` variable, add a `while` loop to iterate over remaining publications across all pages:

```python
# scrape rest of the data starting from the second page
page_num = 2

while True:
    page.goto(f"https://www.researchgate.net/journal/{journal_name}/{page_num}") # {page_num} = 2,3,4,5...
    selector = Selector(text=page.content())
```

Once again iterate over publications data and `append` to the `["publications"]` key:

```python
for publication in selector.css(".nova-legacy-v-publication-item"):
    title = publication.css("nova-legacy-v-publication-item__title::text").get()
    link = f'https://www.researchgate.net{publication.css("nova-legacy-v-publication-item__title a::attr(href)").get()}'
    publication_type = publication.css("nova-legacy-v-publication-item__type::text").get()
    publication_date = publication.css(".nova-legacy-v-publication-item__meta-data-item::text").get()
    authors_name = publication.css(".nova-legacy-v-person-inline-item::text").get()
    snippet = publication.css("nova-legacy-e-expandable-text__container::text").get()
    reads = re.search(r"\d+", publication.css(".nova-legacy-v-publication-item__metrics-item::nth-child(1)::text").get()).group()
    citations = re.search(r"\d+", publication.css(".nova-legacy-v-publication-item__metrics-item::nth-child(2)").get()).group()
    
    journal_data["publications"].append({
        "title": title,
        "link": link,
        "publication_type": publication_type,
        "publication_date": publication_date,
        "authors": authors_name,
        "snippet": snippet,
        "reads": reads,
        "citations": citations
    })
```

Check if we can paginate to the next page:

```python
# checks for selector responsible for disabled pagination
# if there's no page to paginate -> break
if selector.css(".nova-legacy-c-pagination__next.is-disabled").get():
    break

# paginate to the next page
page_num += 1
```

Print extracted data, `close` browser instance, and call the function:

```python
    # ....
    print(json.dumps(pubilication_data, indent=2, ensure_ascii=False))
    browser.close()

scrape_researchgate_journal(journal_name="Journal-of-Global-Information-Technology-Management-1097-198X")
```

Part of the JSON output:

```json
# TODO: ADD JSON output
```

___

<h2 id="links">Links</h2>

- [GitHub Gist]()

___

<p style="text-align: center;">Join us on <a href="https://twitter.com/serp_api">Twitter</a> | <a href="https://www.youtube.com/channel/UCUgIHlYBOD3yA3yDIRhg_mg">YouTube</a></p>

<p style="text-align: center;">Add a  <a href="https://github.com/serpapi/public-roadmap/issues">Feature Request</a>💫 or a <a href="https://github.com/serpapi/public-roadmap/issues">Bug</a>🐞</p>