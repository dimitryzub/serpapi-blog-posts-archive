- <a href="#what_will_be_scraped">What will be scraped</a>
- <a href="#prerequisites">Prerequisites</a>
- <a href="#full_code">Full Code</a>
- <a href="#links">Links</a>


<h2 id="what_will_be_scraped">What will be scraped</h2>

![image](https://user-images.githubusercontent.com/78694043/170258164-ea6ced1e-d6a6-40cf-a017-9d61a87931bc.png)

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


def scrape_researchgate_questions(query: str):
    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True, slow_mo=50)
        page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36")
        
        questions = []
        page_num = 1

        while True:
            page.goto(f"https://www.researchgate.net/search/question?q={query}&page={page_num}")
            selector = Selector(text=page.content())
            
            for question in selector.css(".nova-legacy-c-card__body--spacing-inherit"):
                title = question.css(".nova-legacy-v-question-item__title .nova-legacy-e-link--theme-bare::text").get().title()
                title_link = f'https://www.researchgate.net{question.css(".nova-legacy-v-question-item__title .nova-legacy-e-link--theme-bare::attr(href)").get()}'
                question_type = question.css(".nova-legacy-v-question-item__badge::text").get()
                question_date = question.css(".nova-legacy-v-question-item__meta-data-item:nth-child(1) span::text").get()
                snippet = question.css(".redraft-text::text").get()

                views = question.css(".nova-legacy-v-question-item__metrics-item:nth-child(1) .nova-legacy-e-link--theme-bare::text").get()
                views_link = question.css(".nova-legacy-v-question-item__metrics-item:nth-child(1) .nova-legacy-e-link--theme-bare::attr(href)").get()

                answer = question.css(".nova-legacy-v-question-item__metrics-item+ .nova-legacy-v-question-item__metrics-item .nova-legacy-e-link--theme-bare::text").get()
                answer_link = question.css(".nova-legacy-v-question-item__metrics-item+ .nova-legacy-v-question-item__metrics-item .nova-legacy-e-link--theme-bare::attr(href)").get()

                questions.append({
                    "title": title,
                    "link": title_link,
                    "snippet": snippet,
                    "question_type": question_type,
                    "question_date": question_date,
                    "views": {
                        "views_count": views,
                        "views_link": views_link
                        },
                    "answer": {
                        "answer_count": answer,
                        "answers_link": answer_link
                    }
                })

            print(f"page number: {page_num}")

            # checks if next page arrow key is greyed out `attr(rel)` (inactive) and breaks out of the loop
            if selector.css(".nova-legacy-c-button-group__item:nth-child(9) a::attr(rel)").get():
                break
            else:
                page_num += 1


        print(json.dumps(questions, indent=2, ensure_ascii=False))
        browser.close()
        

scrape_researchgate_questions(query="coffee")
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
scrape_researchgate_questions(query="coffee"):
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
questions = []

while True:
    page.goto(f"https://www.researchgate.net/search/question?q={query}&page={page_num}")
    selector = Selector(text=page.content())
    # ...
```

|Code|Explanation|
|----|-----------|
|`goto()`|to make a request to specific URL with passed query and page parameters.|
|`Selector()`|to pass returned HTML data with `page.content()` and process it.|

Iterate over author results on each page, extract the data and `append` to a temporary `list`:

```python
for question in selector.css(".nova-legacy-c-card__body--spacing-inherit"):
    title = question.css(".nova-legacy-v-question-item__title .nova-legacy-e-link--theme-bare::text").get().title()
    title_link = f'https://www.researchgate.net{question.css(".nova-legacy-v-question-item__title .nova-legacy-e-link--theme-bare::attr(href)").get()}'
    question_type = question.css(".nova-legacy-v-question-item__badge::text").get()
    question_date = question.css(".nova-legacy-v-question-item__meta-data-item:nth-child(1) span::text").get()
    snippet = question.css(".redraft-text::text").get()

    views = question.css(".nova-legacy-v-question-item__metrics-item:nth-child(1) .nova-legacy-e-link--theme-bare::text").get()
    views_link = question.css(".nova-legacy-v-question-item__metrics-item:nth-child(1) .nova-legacy-e-link--theme-bare::attr(href)").get()

    answer = question.css(".nova-legacy-v-question-item__metrics-item+ .nova-legacy-v-question-item__metrics-item .nova-legacy-e-link--theme-bare::text").get()
    answer_link = question.css(".nova-legacy-v-question-item__metrics-item+ .nova-legacy-v-question-item__metrics-item .nova-legacy-e-link--theme-bare::attr(href)").get()

    questions.append({
        "title": title,
        "link": title_link,
        "snippet": snippet,
        "question_type": question_type,
        "question_date": question_date,
        "views": {
            "views_count": views,
            "views_link": views_link
            },
        "answer": {
            "answer_count": answer,
            "answers_link": answer_link
        }
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
scrape_researchgate_questions(query="coffee")
```

Part of the JSON output:

```json
# TODO add JSON output
```

___

<h2 id="links">Links</h2>

- [GitHub Gist]()

___

<p style="text-align: center;">Join us on <a href="https://twitter.com/serp_api">Twitter</a> | <a href="https://www.youtube.com/channel/UCUgIHlYBOD3yA3yDIRhg_mg">YouTube</a></p>

<p style="text-align: center;">Add a  <a href="https://github.com/serpapi/public-roadmap/issues">Feature Request</a>💫 or a <a href="https://github.com/serpapi/public-roadmap/issues">Bug</a>🐞</p>