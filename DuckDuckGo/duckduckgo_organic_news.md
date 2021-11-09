Contents: intro, imports, what will be scraped, process, code, links, outro.

### Intro
This blog post is a continuation of DuckDuckGo web scraping series. Here you'll see how to scrape News Results from Organic Search using Python with `selenium` library. An alternative API solution will be shown.

*Prerequisites: familiarity with `selenium` library and regular expressions.*

### Imports
```python
from selenium import webdriver
import urllib.parse, re
```

### What will be scraped
![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/a7ere4vb6r12yo9tev4b.png)


### Process
Grabbing container, title, link, source, date published `CSS` selectors.

To get an accurate selection you need to specify `id` selector followed by a `class` selector. [CSS selectors reference](https://www.w3schools.com/cssref/css_selectors.asp).

<img width="100%" style="width:100%" src="https://media.giphy.com/media/XuGrjqV1bMgxlHr7my/giphy.gif">

*[SelectorGadget](https://selectorgadget.com/) extension was used to grab `CSS` selectors.*

**Extract and decode thumbnail URL**

A convenient way to extract thumbnail is to use `regex` which you can see in action on [regex101](https://regex101.com/r/98r2qW/1/) or in the [online IDE](https://replit.com/@DimitryZub1/ForkedDelayedDrupal#main.py).

You can use either:
```python
re.findall(pattern, string) # returns an array
re.finditer(pattern, string) # returns an iterator 
```
Basically, when using `findall()` method you <u>can't</u> specify [`.group()` including named groups](https://docs.python.org/3/howto/regex.html#non-capturing-and-named-groups) while `finditer()` method can.

*Screenshot to show what is being captured with a regular expression*:
![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/venhp0nl6fizzp7c6gtr.png)

*Note: I'm not sure if it great overall regular expression for this task, but it works.*

After that, URL needs to be decoded with `urllib.parse.unquote()` method, that's an easy one.

```lang-none
# encoded
>>> https%3A%2F%2Fimage.cnbcfm.com%2Fapi%2Fv1%2Fimage%2F106261274-1574442599483rtx7a0ls.jpg%3Fv%3D1574452686
# decoded
>>> https://image.cnbcfm.com/api/v1/image/106261274-1574442599483rtx7a0ls.jpg?v=1574452686
```

### Code
```python
from selenium import webdriver
import urllib.parse, re

driver = webdriver.Chrome(executable_path='C:/Users/dimit/PycharmProjects/pythonProject/Scrape Search Engines/Walmart/chromedriver.exe')
driver.get('https://duckduckgo.com/?q=elon musk&kl=us-en&ia=web')

for result in driver.find_elements_by_css_selector('#m1-0 .has-image'):
    title = result.find_element_by_css_selector('#m1-0 .js-carousel-item-title').text.strip()
    link = result.find_element_by_css_selector('#m1-0 .js-carousel-item-title').get_attribute('href')
    source = result.find_element_by_css_selector('#m1-0 .result__url').text
    date = result.find_element_by_css_selector('#m1-0 .tile__time').text
    thumbnail_encoded = result.find_element_by_css_selector('#m1-0 .module--carousel__image').get_attribute('style')

    # https://regex101.com/r/98r2qW/1
    match_thumbnail_urls = ''.join(re.findall(r'background-image: url\(\"\/\/external-content\.duckduckgo\.com\/iu\/\?u=(.*)&f=1&h=110\"\);', thumbnail_encoded))

    # https://www.kite.com/python/answers/how-to-decode-a-utf-8-url-in-python
    thumbnail = urllib.parse.unquote(match_thumbnail_urls)
    print(f'{title}\n{link}\n{source}\n{date}\n{thumbnail}\n')

driver.quit()

-------------------
'''
Elon Musk admits Tesla's Cybertruck could flop
https://www.cnbc.com/2021/07/15/elon-musk-admits-the-cybertruck-could-flop.html
CNBC
4h
https://image.cnbcfm.com/api/v1/image/106261274-1574442599483rtx7a0ls.jpg?v=1574452686
'''
```

### Using [DuckDuckGo News Results API](https://serpapi.com/duckduckgo-news-results)
SerpApi is a paid API with a free plan.

Here you'll see the difference is that there's no need to figuring out how to scrape thumbnails if they're needed. All that needs to be done is to iterate over a structured `JSON` string.


```python
from serpapi import GoogleSearch
import json # for pretty printing

params = {
  "api_key": "YOUR_API_KEY",
  "engine": "duckduckgo",
  "q": "elon musk",
  "kl": "us-en"
}

search = GoogleSearch(params)
results = search.get_dict()

print(json.dumps(results['news_results'], indent=2, ensure_ascii=False))

------------------------
'''
[
  {
    "position": 1,
    "title": "Elon Musk admits Tesla's Cybertruck could flop",
    "link": "https://www.cnbc.com/2021/07/15/elon-musk-admits-the-cybertruck-could-flop.html",
    "snippet": "Tesla CEO Elon Musk admitted Thursday on Twitter that the Cybertruck might flop but said he doesn't care because he loves its unusual trapezoid-like design.",
    "source": "CNBC",
    "date": "4 hours ago",
    "thumbnail": "https://image.cnbcfm.com/api/v1/image/106261274-1574442599483rtx7a0ls.jpg?v=1574452686"
  }
]
'''
```


### Links
[GitHub Gist](https://gist.github.com/dimitryzub/5586a7015fcd058450bf68854548c4cb) • [DuckDuckGo News Results API](https://serpapi.com/duckduckgo-news-results)


### Outro
If you have any questions or something isn't working correctly or you want to write something else, feel free to drop a comment in the comment section or via Twitter at [@serp_api](https://twitter.com/serp_api).

Yours,
Dimitry, and the rest of SerpApi Team.