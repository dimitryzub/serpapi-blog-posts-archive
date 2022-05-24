- <a href="#what_will_be_scraped">What will be scraped</a>
- <a href="#prerequisites">Prerequisites</a>
- <a href="#full_code">Full Code</a>
- <a href="#links">Links</a>

___


<h2 id="what_will_be_scraped">What will be scraped</h2>

![image](https://user-images.githubusercontent.com/78694043/170032839-68b274dd-80c5-4e2b-b47f-3ae135008132.png)

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


def scrape_researchgate_publications(query: str):
    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True, slow_mo=50)
        page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36")
        
        publications = []
        page_num = 1

        while True:
            page.goto(f"https://www.researchgate.net/search/publication?q={query}&page={page_num}")
            selector = Selector(text=page.content())
            
            for publication in selector.css(".nova-legacy-c-card__body--spacing-inherit"):
                title = publication.css(".nova-legacy-v-publication-item__title .nova-legacy-e-link--theme-bare::text").get().title()
                title_link = f'https://www.researchgate.net{publication.css(".nova-legacy-v-publication-item__title .nova-legacy-e-link--theme-bare::attr(href)").get()}'
                publication_type = publication.css(".nova-legacy-v-publication-item__badge::text").get()
                publication_date = publication.css(".nova-legacy-v-publication-item__meta-data-item:nth-child(1) span::text").get()
                publication_doi = publication.css(".nova-legacy-v-publication-item__meta-data-item:nth-child(2) span").xpath("normalize-space()").get()
                publication_isbn = publication.css(".nova-legacy-v-publication-item__meta-data-item:nth-child(3) span").xpath("normalize-space()").get()
                authors = publication.css(".nova-legacy-v-person-inline-item__fullname::text").getall()
                source_link = f'https://www.researchgate.net{publication.css(".nova-legacy-v-publication-item__preview-source .nova-legacy-e-link--theme-bare::attr(href)").get()}'

                publications.append({
                    "title": title,
                    "link": title_link,
                    "source_link": source_link,
                    "publication_type": publication_type,
                    "publication_date": publication_date,
                    "publication_doi": publication_doi,
                    "publication_isbn": publication_isbn,
                    "authors": authors
                })

            print(f"page number: {page_num}")

            # checks if next page arrow key is greyed out `attr(rel)` (inactive) and breaks out of the loop
            if selector.css(".nova-legacy-c-button-group__item:nth-child(9) a::attr(rel)").get():
                break
            else:
                page_num += 1


        print(json.dumps(publications, indent=2, ensure_ascii=False))

        browser.close()
        
    
scrape_researchgate_publications(query="coffee")
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
def scrape_researchgate_publications(query: str):
    with sync_playwright() as p:
        # ...
```
|Code|Explanation|
|----|-----------|
|`query: str`|to tell Python that `query` should be an `str`.|


Lunch a browser instance, open `new_page` with passed `user-agent`:

```python
browser = p.chromium.launch(headless=True, slow_mo=50)
page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36")
```

|Code|Explanation|
|----|-----------|
|[`p.chromium.launch()`](https://github.com/microsoft/playwright-python/blob/3b7968fb2ea4238a89447b3c7766f9f1f9c9c0e3/playwright/sync_api/_generated.py#L11423)|to launch Chromium browser instance.|
|[`headless`](https://github.com/microsoft/playwright-python/blob/3b7968fb2ea4238a89447b3c7766f9f1f9c9c0e3/playwright/sync_api/_generated.py#L11500-L11504)|to explicitly tell `playwright` to run in headless mode even though it's a defaut value.|
|[`slow_mo`](https://github.com/microsoft/playwright-python/blob/3b7968fb2ea4238a89447b3c7766f9f1f9c9c0e3/playwright/sync_api/_generated.py#L11514-L11515)|to tell `playwright` to slow down execution.|
|[`browser.new_page()`](https://playwright.dev/python/docs/api/class-browser#browser-new-page)|to open new page. `user_agent` is used to act a real user makes a request from the browser. If not used, it will default to `playwright` value which is `None`. [Check what's your user-agent](https://www.whatismybrowser.com/detect/what-is-my-user-agent/).|

Add a temporary list, set up a while loop, and open a new URL:

```python
authors = []

while True:
    page.goto(f"https://www.researchgate.net/search/publication?q={query}&page={page_num}")
    selector = Selector(text=page.content())
    # ...
```

|Code|Explanation|
|----|-----------|
|`goto()`|to make a request to specific URL with passed query and page parameters.|
|`Selector()`|to pass returned HTML data with `page.content()` and process it.|

Iterate over author results on each page, extract the data and `append` to a temporary `list`:

```python
for publication in selector.css(".nova-legacy-c-card__body--spacing-inherit"):
    title = publication.css(".nova-legacy-v-publication-item__title .nova-legacy-e-link--theme-bare::text").get().title()
    title_link = f'https://www.researchgate.net{publication.css(".nova-legacy-v-publication-item__title .nova-legacy-e-link--theme-bare::attr(href)").get()}'
    publication_type = publication.css(".nova-legacy-v-publication-item__badge::text").get()
    publication_date = publication.css(".nova-legacy-v-publication-item__meta-data-item:nth-child(1) span::text").get()
    publication_doi = publication.css(".nova-legacy-v-publication-item__meta-data-item:nth-child(2) span").xpath("normalize-space()").get()
    publication_isbn = publication.css(".nova-legacy-v-publication-item__meta-data-item:nth-child(3) span").xpath("normalize-space()").get()
    authors = publication.css(".nova-legacy-v-person-inline-item__fullname::text").getall()
    source_link = f'https://www.researchgate.net{publication.css(".nova-legacy-v-publication-item__preview-source .nova-legacy-e-link--theme-bare::attr(href)").get()}'

    publications.append({
        "title": title,
        "link": title_link,
        "source_link": source_link,
        "publication_type": publication_type,
        "publication_date": publication_date,
        "publication_doi": publication_doi,
        "publication_isbn": publication_isbn,
        "authors": authors
    })
```

|Code|Explanation|
|----|-----------|
|`css()`|[to parse data from the passed CSS selector(s)](https://github.com/scrapy/parsel/blob/90397dcd0b2c1cbb91e44f65c50f9e11628ba028/parsel/selector.py#L351-L362). Every [CSS query traslates to XPath using `csselect` package](https://github.com/scrapy/parsel/blob/90397dcd0b2c1cbb91e44f65c50f9e11628ba028/parsel/selector.py#L357-L358) under the hood.|
|`::text`/`::attr(attribute)`|[to extract textual or attribute data](https://github.com/scrapy/parsel/blob/90397dcd0b2c1cbb91e44f65c50f9e11628ba028/parsel/csstranslator.py#L48-L51) from the node.|
|`get()`/`getall()`|[to get actual data from a matched node](https://github.com/scrapy/parsel/blob/90397dcd0b2c1cbb91e44f65c50f9e11628ba028/parsel/selector.py#L197-L204), or to [get a `list` of matched data from nodes](https://github.com/scrapy/parsel/blob/90397dcd0b2c1cbb91e44f65c50f9e11628ba028/parsel/selector.py#L447-L451).|
|`xpath("normalize-space()")`|to parse blank text node as well. By default, blank text node is be skipped by XPath.|

Check if the next page is present and paginate:

```python
# checks if the next page arrow key is greyed out `attr(rel)` (inactive) -> breaks out of the loop
if selector.css(".nova-legacy-c-button-group__item:nth-child(9) a::attr(rel)").get():
    break
else:
    page_num += 1
```

Print extracted data, and `close` browser instance:

```python
print(json.dumps(publications, indent=2, ensure_ascii=False))

browser.close()

# call the function
scrape_researchgate_publications(query="coffee")
```

Part of the JSON output:

```json
[
   {
      "title":"The Social Life Of Coffee Turkey’S Local Coffees",
      "link":"https://www.researchgate.netpublication/360540595_The_Social_Life_of_Coffee_Turkey%27s_Local_Coffees?_sg=kzuAi6HlFbSbnLEwtGr3BA_eiFtDIe1VEA4uvJlkBHOcbSjh5XlSQe6GpYvrbi12M0Z2MQ6grwnq9fI",
      "source_link":"https://www.researchgate.netpublication/360540595_The_Social_Life_of_Coffee_Turkey%27s_Local_Coffees?_sg=kzuAi6HlFbSbnLEwtGr3BA_eiFtDIe1VEA4uvJlkBHOcbSjh5XlSQe6GpYvrbi12M0Z2MQ6grwnq9fI",
      "publication_type":"Conference Paper",
      "publication_date":"Apr 2022",
      "publication_doi":null,
      "publication_isbn":null,
      "authors":[
         "Gülşen Berat Torusdağ",
         "Merve Uçkan Çakır",
         "Cinucen Okat"
      ]
   },
   {
      "title":"Coffee With The Algorithm",
      "link":"https://www.researchgate.netpublication/359599064_Coffee_with_the_Algorithm?_sg=3KHP4SXHm_BSCowhgsa4a2B0xmiOUMyuHX2nfqVwRilnvd1grx55EWuJqO0VzbtuG-16TpsDTUywp0o",
      "source_link":"https://www.researchgate.netNone",
      "publication_type":"Chapter",
      "publication_date":"Mar 2022",
      "publication_doi":"DOI: 10.4324/9781003170884-10",
      "publication_isbn":"ISBN: 9781003170884",
      "authors":[
         "Jakob Svensson"
      ]
   }, ... other publications
   {
      "title":"Coffee In Chhattisgarh", # last publication
      "link":"https://www.researchgate.netpublication/353118247_COFFEE_IN_CHHATTISGARH?_sg=CsJ66DoWjFfkMNdujuE-R9aVTZA4kVb_9lGiy1IrYXls1Nur4XFMdh2s5E9zkF5Skb5ZZzh663USfBA",
      "source_link":"https://www.researchgate.netNone",
      "publication_type":"Technical Report",
      "publication_date":"Jul 2021",
      "publication_doi":null,
      "publication_isbn":null,
      "authors":[
         "Krishan Pal Singh",
         "Beena Nair Singh",
         "Dushyant Singh Thakur",
         "Anurag Kerketta",
         "Shailendra Kumar Sahu"
      ]
   }
]
```

___

<h2 id="links">Links</h2>

- [GitHub Gist](https://gist.github.com/dimitryzub/eee343faac72cb8b9894099e034381eb)

___

<p style="text-align: center;">Join us on <a href="https://twitter.com/serp_api">Twitter</a> | <a href="https://www.youtube.com/channel/UCUgIHlYBOD3yA3yDIRhg_mg">YouTube</a></p>

<p style="text-align: center;">Add a  <a href="https://github.com/serpapi/public-roadmap/issues">Feature Request</a>💫 or a <a href="https://github.com/serpapi/public-roadmap/issues">Bug</a>🐞</p>