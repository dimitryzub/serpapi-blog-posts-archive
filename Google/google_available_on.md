Contents: intro, imports, what will be scraped, process, code, links, outro.

### Intro
This blog post is a continuation of Google's web scraping series. Here you'll see examples on how to scrape Available On search results using Python `BaeutifulSoup`, `Requests`, and `lxml` libraries. An alternative API solution will be shown.

### Imports
```python
import requests, lxml
from bs4 import BeautifulSoup
from serpapi import GoogleSearch
```

### What will be scraped
![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/dpnvn6wbel37gkcgf9ks.png)

### Process
The following GIF shows the process of selecting **Name**, **Link**, and **Price** `CSS` selectors using [SelectorGadget](https://selectorgadget.com/) Chrome extension.
<img width="100%" style="width:100%" src="https://media.giphy.com/media/33wbHRtoOpYkKuRODf/giphy.gif">


### Code
```python
import requests, lxml
from bs4 import BeautifulSoup

headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}

params = {
    "q": "spider man watch online",
    "hl": "en",
    "gl": "us",
}

html = requests.get("https://www.google.com/search", params=params, headers=headers)
soup = BeautifulSoup(html.text, 'lxml')

for result in soup.select('.JkUS4b'):
    name = result.select_one('.i3LlFf').text
    link = result['href']
    price = result.select_one('.V8xno').text
    print(f'{name}\n{link}\n{price}\n')


----------
'''
Hulu
https://www.hulu.com/watch/f82b95f5-13da-4acd-b378-7d3f6864919f
Premium subscription

Sling TV
https://watch.sling.com/1/program/ada829bcd452424d936dfd39a66a3f5e/watch?trackingid=google-feed
Premium subscription
...
'''
```

### Using [Google Available On Results API](https://serpapi.com/available-on)
SerpApi is a paid API with a free trial of 5,000 searches.
```python
import json # just for pretty output
from serpapi import GoogleSearch

params = {
  "api_key": "API_KEY",
  "engine": "google",
  "q": "spider man watch online",
  "gl": "us",
  "hl": "en", # country to use for the Google search
}

search = GoogleSearch(params)
results = search.get_dict()

for results in results['available_on']:
    print(json.dumps(results, indent=2, ensure_ascii=False))

---------
'''
{
  "name": "Hulu",
  "link": "https://www.hulu.com/watch/f82b95f5-13da-4acd-b378-7d3f6864919f",
  "price": "Premium subscription",
  "thumbnail": "https://serpapi.com/searches/60ded28817f923a90145853c/images/c4dcca5efe0b92c0095874b9b1935aa7b3c0b903ab87dba3b1f2d3dea0f89733.png"
}
...
'''
```


### Links
[Code in the online IDE](https://replit.com/@DimitryZub1/Scrape-Google-Available-on-python#main.py) • [Google Available On Results API](https://serpapi.com/available-on)

### Outro
If you have any questions or something isn't working correctly or you want to write something else, feel free to drop a comment in the comment section or via Twitter at [@serp_api](https://twitter.com/serp_api).

Yours,
Dimitry, and the rest of SerpApi Team.

<img width="100%" style="width:100%" src="https://media.giphy.com/media/l36kU80xPf0ojG0Erg/giphy.gif">