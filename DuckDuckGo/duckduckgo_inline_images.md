Contents: intro, imports, what will be scraped, process, code, links, outro.


### Intro
This blog post is a continuation of the DuckDuckGo web scraping series. Here you'll see how to scrape Inline Image results using Python with `selenium` library. An alternative API solution will be shown.

*Prerequisites: familiarity with `selenium` library and regular expressions.*

### Imports
```python
from selenium import webdriver
import re, urllib.parse
```

### What will be scraped
![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/qhp1rfpomloolpaii92z.png)



### Process
The process is very much like from other DuckDuckGo blog posts series.

Selecting container, title, link, thumbnail, image URL CSS selectors from which the `.get_attribute()` method will be used to grab `data-id`, `src`, and `href` attributes.
<img width="100%" style="width:100%" src="https://media.giphy.com/media/Q2h8IVG8EPPi36HJtF/giphy.gif">

*[SelectorGadget](https://selectorgadget.com/) Chrome extension was used in the GIF above to select `CSS` selectors.*

### Code
```python
from selenium import webdriver
import re, urllib.parse

driver = webdriver.Chrome(executable_path='path/to/chromedriver.exe')
driver.get('https://duckduckgo.com/?q=elon musk dogecoin&kl=us-en&ia=web')

for result in driver.find_elements_by_css_selector('.js-images-link'):
    title = result.find_element_by_css_selector('.js-images-link a img').get_attribute('alt')
    link = result.find_element_by_css_selector('.js-images-link a').get_attribute('href')
    thumbnail_encoded = result.find_element_by_css_selector('.js-images-link a img').get_attribute('src')

    # https://regex101.com/r/4pgG5m/1
    match_thumbnail_urls = ''.join(re.findall(r'https\:\/\/external\-content\.duckduckgo\.com\/iu\/\?u\=(.*)&f=1', thumbnail_encoded))

    # https://www.kite.com/python/answers/how-to-decode-a-utf-8-url-in-python
    thumbnail = urllib.parse.unquote(match_thumbnail_urls).replace('&h=160', '')
    image = result.get_attribute('data-id')

    print(f'{title}\n{link}\n{thumbnail}\n{image}\n')

driver.quit()

--------------------------
'''
Dogecoin (DOGE) Price Crash Below Key Support and Even ...
https://duckduckgo.com/?q=elon%20musk%20dogecoin&iax=images&ia=images&iai=https://cdn.coingape.com/wp-content/uploads/2021/07/02195033/dogecoin-elon-musk-snl-memes.jpg&kl=us-en
https://tse1.mm.bing.net/th?id=OIF.UGa1KGFCz%2f5axclMfq0k4w&pid=Api
https://cdn.coingape.com/wp-content/uploads/2021/07/02195033/dogecoin-elon-musk-snl-memes.jpg
...
'''
```

### Using [DuckDuckGo Inline Images API](https://serpapi.com/duckduckgo-inline-images)
SerpApi is a paid API with a free plan.

The difference that you'll see immediately is that API provides 30 results, rather than ~8-10 results.

Alternatively, all you have to do is to iterate over structured `JSON` string without thinking how to scrape data without rendering the page, or how to grab certain elements if they are the ones that hard to get.

```python
import json
from serpapi import GoogleSearch

params = {
  "api_key": "YOUR_API_KEY",
  "engine": "duckduckgo",
  "q": "elon musk dogecoin",
  "kl": "us-en"
}

search = GoogleSearch(params)
results = search.get_dict()

print(json.dumps(results['inline_images'], indent=2, ensure_ascii=False))

----------------------
'''
[
  {
    "position": 1,
    "title": "'Dogefather' Elon Musk Tweets in Support of the ...",
    "link": "https://gadgets.ndtv.com/cryptocurrency/news/elon-musk-dogecoin-price-cryptocurrency-bitcoin-ethereum-ether-twitter-tweet-support-market-gain-2483505",
    "thumbnail": "https://tse1.mm.bing.net/th?id=OIF.ryyLYCT1jVMZDADJDf1LVA&pid=Api",
    "image": "https://i.gadgets360cdn.com/large/elon_musk_reuters_1610084738222.jpg"
  }
...
  {
    "position": 20,
    "title": "Beware! Your love for Elon Musk and Dogecoin may land you ...",
    "link": "http://www.businesstelegraph.co.uk/beware-your-love-for-elon-musk-and-dogecoin-may-land-you-in-a-scam-economic-times/",
    "thumbnail": "https://tse1.mm.bing.net/th?id=OIF.Y4geZY10AJX80AvM8EPCjQ&pid=Api",
    "image": "http://www.businesstelegraph.co.uk/wp-content/uploads/2021/07/Beware-Your-love-for-Elon-Musk-and-Dogecoin-may-land.jpg"
  }
]
'''
```


### Links
[GithHub Gist](https://gist.github.com/dimitryzub/32ea63f9c6ed8c61e609af8e85bc22c2) • [DuckDuckGo Inline Images API](https://serpapi.com/duckduckgo-inline-images)


### Outro
If you have any questions or something isn't working correctly or you want to write something else, feel free to drop a comment in the comment section or via Twitter at [@serp_api](https://twitter.com/serp_api).

Yours,
Dimitry, and the rest of SerpApi Team.