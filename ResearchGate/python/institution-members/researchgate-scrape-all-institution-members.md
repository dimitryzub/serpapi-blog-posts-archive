- <a href="#what_will_be_scraped">What will be scraped</a>
- <a href="#prerequisites">Prerequisites</a>
- <a href="#full_code">Full Code</a>
- <a href="#links">Links</a>
- <a href="#outro">Outro</a>

___


<h2 id="what_will_be_scraped">What will be scraped</h2>

![image](https://user-images.githubusercontent.com/78694043/167081287-3cbb8a5b-f500-4e94-a0e6-b2ab41ef2bf1.png)

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
pip install requests parsel playwright
```

**Reduce the chance of being blocked**

There's a chance that a request might be blocked. Have a look at [how to reduce the chance of being blocked while web-scraping](https://serpapi.com/blog/how-to-reduce-chance-of-being-blocked-while-web/), there are eleven methods to bypass blocks from most websites.

<h2 id="full_code">Full Code</h2>

```python
from parsel import Selector
from playwright.sync_api import sync_playwright
import re, json, time


def scrape_institution_members(institution: str):
    with sync_playwright() as p:
        
        institution_memebers = []
        page_num = 1 
        
        members_is_present = True
        while members_is_present:
            
            browser = p.chromium.launch(headless=True, slow_mo=50)
            page = browser.new_page()
            page.goto(f"https://www.researchgate.net/institution/{institution}/members/{page_num}")
            selector = Selector(text=page.content())
            
            print(f"page number: {page_num}")
            
            for member in selector.css(".nova-legacy-v-person-list-item"):
                name = member.css(".nova-legacy-v-person-list-item__align-content a::text").get()
                link = f'https://www.researchgate.net{member.css(".nova-legacy-v-person-list-item__align-content a::attr(href)").get()}'
                profile_photo = member.css(".nova-legacy-l-flex__item img::attr(src)").get()
                department = member.css(".nova-legacy-v-person-list-item__stack-item:nth-child(2) span::text").get()
                desciplines = member.css("span .nova-legacy-e-link::text").getall()
                
                institution_memebers.append({
                    "name": name,
                    "link": link,
                    "profile_photo": profile_photo,
                    "department": department,
                    "descipline": desciplines
                })
                
            # check for Page not found selector
            if selector.css(".headline::text").get():
                members_is_present = False
            else:
                time.sleep(2) # use proxies and captcha solver instead of this
                page_num += 1 # increment a one. Pagination

        print(json.dumps(institution_memebers, indent=2, ensure_ascii=False))
        print(len(institution_memebers)) # 624 from a EM-Normandie-Business-School

        browser.close()
        
        """
        you can also render the page and extract data from the inline JSON string,
        however, it's messy and from my perspective, it is easier to scrape the page directly.
        """
        
        # https://regex101.com/r/8qjfnH/1
        # extracted_data = re.findall(r"\s+RGCommons\.react\.mountWidgetTree\(({\"data\":{\"menu\".*:true})\);;",
        #                        str(page.content()))[0]
        # json_data = json.loads(extracted_data)
        # print(json_data)
    
scrape_institution_members(institution="EM-Normandie-Business-School")
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
|`time`| is not a practical way to bypass request blocks. Use proxies/captcha solver instead.|

Define a function:

```python
def scrape_institution_members(institution: str):
    # ...
```
|Code|Explanation|
|----|-----------|
|`institution: str`|to tell Python that `institution` should be an `str`.|


Open a `playwright` with a [context manager](https://book.pythontips.com/en/latest/context_managers.html):

```python
with sync_playwright() as p:
    # ...
```

Lunch a browser instance, open and `goto` the page and pass response to HTML/XML parser:

```python
browser = p.chromium.launch(headless=True, slow_mo=50)
page = browser.new_page()
page.goto(f"https://www.researchgate.net/institution/{institution}/members/{page_num}")
selector = Selector(text=page.content())
```

|Code|Explanation|
|----|-----------|
|[`p.chromium.launch()`](https://github.com/microsoft/playwright-python/blob/3b7968fb2ea4238a89447b3c7766f9f1f9c9c0e3/playwright/sync_api/_generated.py#L11423)|to launch Chromium browser instance.|
|[`headless`](https://github.com/microsoft/playwright-python/blob/3b7968fb2ea4238a89447b3c7766f9f1f9c9c0e3/playwright/sync_api/_generated.py#L11500-L11504)|to explicitly tell `playwright` to run in headless mode even though it's a defaut value.|
|[`slow_mo`](https://github.com/microsoft/playwright-python/blob/3b7968fb2ea4238a89447b3c7766f9f1f9c9c0e3/playwright/sync_api/_generated.py#L11514-L11515)|to tell `playwright` to slow down execution.|
|[`browser.new_page()`](https://playwright.dev/python/docs/api/class-browser#browser-new-page)|to open new page.|


Add a temporary list, set up a page number, while loop, and check for an exception to exit the loop:

```python
institution_memebers = []
page_num = 1

members_is_present = True
while members_is_present:

      # extraction code

      # check for Page not found selector
      if selector.css(".headline::text").get():
          members_is_present = False
      else:
          time.sleep(2) # use proxies and captcha solver instead of this
          page_num += 1 # increment a one. Pagination
```

Iterate over member results on each page, extract the data and `append` to a temporary `list`:

```python
for member in selector.css(".nova-legacy-v-person-list-item"):
    name = member.css(".nova-legacy-v-person-list-item__align-content a::text").get()
    link = f'https://www.researchgate.net{member.css(".nova-legacy-v-person-list-item__align-content a::attr(href)").get()}'
    profile_photo = member.css(".nova-legacy-l-flex__item img::attr(src)").get()
    department = member.css(".nova-legacy-v-person-list-item__stack-item:nth-child(2) span::text").get()
    desciplines = member.css("span .nova-legacy-e-link::text").getall()
    
    institution_memebers.append({
        "name": name,
        "link": link,
        "profile_photo": profile_photo,
        "department": department,
        "descipline": desciplines
    })
```

|Code|Explanation|
|----|-----------|
|`css()`|[to parse data from the passed CSS selector(s)](https://github.com/scrapy/parsel/blob/90397dcd0b2c1cbb91e44f65c50f9e11628ba028/parsel/selector.py#L351-L362). Every [CSS query traslates to XPath using `csselect` package](https://github.com/scrapy/parsel/blob/90397dcd0b2c1cbb91e44f65c50f9e11628ba028/parsel/selector.py#L357-L358) under the hood.|
|`::text`/`::attr(attribute)`|[to extract textual or attribute data](https://github.com/scrapy/parsel/blob/90397dcd0b2c1cbb91e44f65c50f9e11628ba028/parsel/csstranslator.py#L48-L51) from the node.|
|`get()`/`getall()`|[to get actual data from a matched node](https://github.com/scrapy/parsel/blob/90397dcd0b2c1cbb91e44f65c50f9e11628ba028/parsel/selector.py#L197-L204), or to [get a `list` of matched data from nodes](https://github.com/scrapy/parsel/blob/90397dcd0b2c1cbb91e44f65c50f9e11628ba028/parsel/selector.py#L447-L451).|

Print extracted data, `length` of extracted members, and `close` browser instance:

```python
print(json.dumps(institution_memebers, indent=2, ensure_ascii=False))
print(len(institution_memebers)) # 624 from a EM-Normandie-Business-School

browser.close()
```

Part of the JSON output (fist result is a first member, last is the latest member):

```json
[
  {
    "name": "Sylvaine Castellano",
    "link": "https://www.researchgate.netprofile/Sylvaine-Castellano",
    "profile_photo": "https://i1.rgstatic.net/ii/profile.image/341867548954625-1458518983237_Q64/Sylvaine-Castellano.jpg",
    "department": "EM Normandie Business School",
    "descipline": [
      "Sustainable Development",
      "Sustainability",
      "Innovation"
    ]
  }, ... other results
  {
    "name": "Constance Biron",
    "link": "https://www.researchgate.netprofile/Constance-Biron-3",
    "profile_photo": "https://c5.rgstatic.net/m/4671872220764/images/template/default/profile/profile_default_m.jpg",
    "department": "Marketing",
    "descipline": []
  }
]
```

<h2 id="full_code">Extracting data from the JSON string</h2>

You can scrape the data without using `parsel` by printing page [`content()`](https://playwright.dev/python/docs/api/class-page#page-content) data which will get the full HTML contents of the page, including the doctype, and parsing the data using regular expression. 

I'm showing this option as well, just in case some of you prefer this approach over directly parsing the page.

```python
# https://regex101.com/r/8qjfnH/1
extracted_data = re.findall(r"\s+RGCommons\.react\.mountWidgetTree\(({\"data\":{\"menu\".*:true})\);;",
                       str(page.content()))[0]
json_data = json.loads(extracted_data)
print(json_data)
```

Outputs:

![image](https://user-images.githubusercontent.com/78694043/167090719-4c829164-96f8-4142-bcc4-dc96b4fefd72.png)

Here's the thing, extracting data seems to be practically more convincing from the JSON string but let's look at the example of accessing the `fullName` key:

```
                                     👇👇👇👇👇
initState.rigel.store.account(id:\\\"AC:2176142\\\").fullName
```

This way, we also got two additional steps: _find_ and _compare_ user ID to make sure that ID would match the user ID. 
___

<h2 id="links">Links</h2>

- [GitHub file in the repository](https://github.com/dimitryzub/serpapi-blog-posts-archive/tree/main/ResearchGate/python/institution-members/researchgate-scrape-all-institution-members-parsel-playwright.py)

___

<p style="text-align: center;">Join us on <a href="https://twitter.com/serp_api">Twitter</a> | <a href="https://www.youtube.com/channel/UCUgIHlYBOD3yA3yDIRhg_mg">YouTube</a></p>

<p style="text-align: center;">Add a  <a href="https://github.com/serpapi/public-roadmap/issues">Feature Request</a>💫 or a <a href="https://github.com/serpapi/public-roadmap/issues">Bug</a>🐞</p>

<div style="text-align: center;"><p>🌼</p></div>