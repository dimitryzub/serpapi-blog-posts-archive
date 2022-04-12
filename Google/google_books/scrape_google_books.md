- <a href="#what_will_be_scraped">What will be scraped</a>
- <a href="#prerequisites">Prerequisites</a>
- <a href="#full_code">Full Code</a>
- <a href="#links">Links</a>
- <a href="#outro">Outro</a>

___

<h2 id="what_will_be_scraped">What will be scraped</h2>

![image](https://user-images.githubusercontent.com/78694043/153621290-26216177-2574-43f5-8676-82237e46b1b1.png)

<h2 id="prerequisites">Prerequisites</h2>

**Basic knowledge scraping with CSS selectors**

`CSS` selectors declare which part of the markup a style applies to thus allowing to extract data from matching tags and attributes.

If you haven't scraped with `CSS` selectors, there's a dedicated blog post of mine about [how to use `CSS` selectors when web-scraping](https://serpapi.com/blog/web-scraping-with-css-selectors-using-python/) that covers what it is, pros and cons, and why they're matter from a web-scraping perspective.


**Separate virtual environment**

In short, it's a thing that creates an independent set of installed libraries including different Python versions that can coexist with each other at the same system thus preventing libraries or Python version conflicts.

If you didn't work with a virtual environment before, have a look at the dedicated [Python virtual environments tutorial using Virtualenv and Poetry](https://serpapi.com/blog/python-virtual-environments-using-virtualenv-and-poetry/) blog post of mine to get familiar.

📌Note: this is not a strict requirement for this blog post.

**Install libraries**:

```lang-none
pip install requests, parsel
```

**Reduce the chance of being blocked**

There's a chance that a request might be blocked. Have a look at [how to reduce the chance of being blocked while web-scraping](https://serpapi.com/blog/how-to-reduce-chance-of-being-blocked-while-web/), there are eleven methods to bypass blocks from most websites.

___

<h2 id="full_code">Full Code</h2>

```python
from parsel import Selector
import requests, json, re

params = {
    "q": "richard branson",
    "tbm": "bks",
    "gl": "us",
    "hl": "en"
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.87 Safari/537.36",
}

html = requests.get("https://www.google.com/search", params=params, headers=headers, timeout=30)
selector = Selector(text=html.text)

books_results = []

# https://regex101.com/r/mapBs4/1
book_thumbnails = re.findall(r"s=\\'data:image/jpg;base64,(.*?)\\'", str(selector.css("script").getall()), re.DOTALL)

for book_thumbnail, book_result in zip(book_thumbnails, selector.css(".Yr5TG")):
    title = book_result.css(".DKV0Md::text").get()
    link = book_result.css(".bHexk a::attr(href)").get()
    displayed_link = book_result.css(".tjvcx::text").get()
    snippet = book_result.css(".cmlJmd span::text").get()
    author = book_result.css(".fl span::text").get()
    author_link = f'https://www.google.com/search{book_result.css(".N96wpd .fl::attr(href)").get()}'
    date_published = book_result.css(".fl+ span::text").get()
    preview_link = book_result.css(".R1n8Q a.yKioRe:nth-child(1)::attr(href)").get()
    more_editions_link = book_result.css(".R1n8Q a.yKioRe:nth-child(2)::attr(href)").get()

    books_results.append({
        "title": title,
        "link": link,
        "displayed_link": displayed_link,
        "snippet": snippet,
        "author": author,
        "author_link": author_link,
        "date_published": date_published,
        "preview_link": preview_link,
        "more_editions_link": f"https://www.google.com{more_editions_link}" if more_editions_link is not None else None,
        "thumbnail": bytes(bytes(book_thumbnail, "ascii").decode("unicode-escape"), "ascii").decode("unicode-escape")
    })


print(json.dumps(books_results, indent=2))
```

Import libraries:

```python
from parsel import Selector
import requests, json
```

- [`parsel`](https://parsel.readthedocs.io/en/latest/index.html) is a library to extract and remove data from HTML and XML using XPath and CSS selectors. It's similar to `beautifulsoup4` except it supports full XPath and has its own CSS pseudo-elements support, for example `::text` or `::attr(<attribute_name>)`.


Create search query parameters and request headers:

```python
# https://docs.python-requests.org/en/master/user/quickstart/#passing-parameters-in-urls
params = {
    "q": "richard branson",  # search query
    "tbm": "bks",            # book results
    "gl": "us",              # country to search from
    "hl": "en"               # language
}

# https://requests.readthedocs.io/en/master/user/quickstart/#custom-headers
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.87 Safari/537.36",
}
```

- `user-agent` is used to act as a "real" user visit so website think it's a user, not the bot/script that sends a request. It's the most basic form of avoiding being blocked by a website.

Pass query params, request headers to the request and create a `Selector` object:

```python
html = requests.get("https://www.google.com/search", params=params, headers=headers, timeout=30)
selector = Selector(text=html.text)
```

- [`timeout=30`](https://docs.python-requests.org/en/master/user/quickstart/#timeouts) tells `requests` to stop waiting for a response after 30 seconds.
- `Selector()` is like `BeautifulSoup()` except you get a full XPath support, and [every CSS selector query translates to XPath](https://github.com/scrapy/parsel/blob/f5f73d34ba787ad0c9df25de295de6e196ecd91d/parsel/selector.py#L350-L351) using [`cssselect`](https://github.com/scrapy/cssselect) package and names it [`FunctionalPseudoElement`](https://github.com/scrapy/cssselect/blob/f564dfd93358ea55bbd55b75beeb71872a06ed12/cssselect/parser.py#L142).


Create a temporary `list` to store the data:

```python
books_results = []
```

Match thumbnails data using regular expression:

```python
# https://regex101.com/r/mapBs4/1
book_thumbnails = re.findall(r"s=\\'data:image/jpg;base64,(.*?)\\'", str(selector.css("script").getall()), re.DOTALL)
```

The reason why we need to parse the data from `<script>` tags is because if you parse book thumbnail from `<img>` `["src"]` attribute you'll get a 1x1 placeholder instead of a thumbnail.

- `re.findall()` return a `list` of all matches.
- `selector.css("script")` return a list of all found `<script>` tags and `getall()` will get the `data` value from translated XPath returned by `<class 'SelectorList'>` or `<class 'Selector'>` instance.
- [`re.DOTALL`](https://docs.python.org/3/library/re.html#re.DOTALL) will match everything including new line. Note that you have to have `.` switch, otherwise it will match every charter except a new line.

Iterate over matched thumbnails and CSS container with all the needed data and extract it:

```python
for book_thumbnail, book_result in zip(book_thumbnails, selector.css(".Yr5TG")):
    title = book_result.css(".DKV0Md::text").get()
    link = book_result.css(".bHexk a::attr(href)").get()
    displayed_link = book_result.css(".tjvcx::text").get()
    snippet = book_result.css(".cmlJmd span::text").get()
    author = book_result.css(".fl span::text").get()
    author_link = f'https://www.google.com/search{book_result.css(".N96wpd .fl::attr(href)").get()}'
    date_published = book_result.css(".fl+ span::text").get()
    preview_link = book_result.css(".R1n8Q a.yKioRe:nth-child(1)::attr(href)").get()
    more_editions_link = book_result.css(".R1n8Q a.yKioRe:nth-child(2)::attr(href)").get()
```

- [`zip()`](https://docs.python.org/3/library/functions.html#zip) aggregates multiple iterables in parallel and returns a tuple with an item from each one.
- `css(".Yr5TG")` is like calling `soup.select(".Yr5TG")` with `bs4`, which will return a `list` of matches.
- `css(".DKV0Md::text")` where CSS3 pseudo-element `::text` will get text, and [`get()`](https://github.com/scrapy/parsel/blob/f5f73d34ba787ad0c9df25de295de6e196ecd91d/parsel/selector.py#L415-L433) will get the [textual `data`](https://github.com/scrapy/parsel/blob/f5f73d34ba787ad0c9df25de295de6e196ecd91d/parsel/selector.py#L507) value from translated XPath. If using without `get()` you'll get a translated XPath `<class 'SelectorList'>` or `<class 'Selector'>` instance from CSS selector.
- `::attr(href)` is also a pseudo-element to grab an attribute.

Append the data to temporary `list` as a `dict`:

```python
books_results.append({
    "title": title,
    "link": link,
    "displayed_link": displayed_link,
    "snippet": snippet,
    "author": author,
    "author_link": author_link,
    "date_published": date_published,
    "preview_link": preview_link,
    # if URL is present, add "https://www.google.com" to the URL, instead to None: "Nonehttps://www.google.com"
    "more_editions_link": f"https://www.google.com{more_editions_link}" if more_editions_link is not None else None, 
    "thumbnail": bytes(bytes(book_thumbnail, "ascii").decode("unicode-escape"), "ascii").decode("unicode-escape")
})
```

- `bytes().decode()` will decode unicode escape characters. We have to do it twice, because after first decoding some unicode characters are still present for some reason.

Print the data:

```python
print(json.dumps(books_results, indent=2))
```

Part of the JSON output:

```json
[
  {
    "title": "The Virgin Way: How to Listen, Learn, Laugh and Lead",
    "link": "https://books.google.com/books?id=Jkp1AgAAQBAJ&printsec=frontcover&dq=richard+branson&hl=en&newbks=1&newbks_redir=1&sa=X&ved=2ahUKEwin3IrX-_n1AhXclmoFHbMHDfIQ6AF6BAgIEAI",
    "displayed_link": "books.google.com",
    "snippet": "This is not a conventional book on leadership. There are no rules \u2013 but rather the secrets of leadership that he has learned along the way from his days at Virgin Records, to his recent work with The Elders.",
    "author": "Sir Richard Branson",
    "author_link": "https://www.google.com/search/search?gl=us&hl=en&tbm=bks&tbm=bks&q=inauthor:%22Sir+Richard+Branson%22&sa=X&ved=2ahUKEwin3IrX-_n1AhXclmoFHbMHDfIQ9Ah6BAgIEAU",
    "date_published": "2014",
    "preview_link": "https://books.google.com/books?id=Jkp1AgAAQBAJ&printsec=frontcover&dq=richard+branson&hl=en&newbks=1&newbks_redir=1&sa=X&ved=2ahUKEwin3IrX-_n1AhXclmoFHbMHDfIQuwV6BAgIEAc",
    "more_editions_link": "https://www.google.com/books/edition/The_Virgin_Way/Jkp1AgAAQBAJ?hl=en&gl=us&kptab=editions&sa=X&ved=2ahUKEwin3IrX-_n1AhXclmoFHbMHDfIQmBZ6BAgIEAg",
    "thumbnail": "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"
  }, ... other results
]
```


<h2 id="links">Links</h2>

- [Code in the online IDE](https://replit.com/@DimitryZub1/Scrape-Google-Books)

___

<h2 id="outro">Outro</h2>

If you have anything to share, any questions, suggestions, or something that isn't working correctly, reach out via Twitter at [@dimitryzub](https://twitter.com/DimitryZub), or [@serp_api](https://twitter.com/serp_api).

Yours,
Dmitriy, and the rest of SerpApi Team.

___

<p style="text-align: center;">Join us on <a href="https://www.reddit.com/r/SerpApi/">Reddit</a> | <a href="https://twitter.com/serp_api">Twitter</a> | <a href="https://www.youtube.com/channel/UCUgIHlYBOD3yA3yDIRhg_mg">YouTube</a></p>

<p style="text-align: center;">Add a  <a href="https://github.com/serpapi/public-roadmap/issues">Feature Request</a>💫 or a <a href="https://github.com/serpapi/public-roadmap/issues">Bug</a>🐞</p>