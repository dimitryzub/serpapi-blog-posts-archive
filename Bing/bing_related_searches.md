Contents: intro, imports, what will be scraped, process, code, links, outro.

### Intro
This blog post contains visual info about how to scrape Bing Related Searches using Python.

### Imports
```python
from bs4 import BeautifulSoup
import requests
import lxml
from serpapi import GoogleSearch
import os # used for creating an environment variable on replit.com
```
### What will be scraped
![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/8eg8y90d9hj86v3ms99u.png)


### Process
Choosing the right CSS selectors. I'll show two approaches:
1. Using Chrome Dev tools to see the HTML layout and test selectors with [SelectorGadget](https://selectorgadget.com/) extension <img width="100%" style="width:100%" src="https://media.giphy.com/media/46Va9i2GHAd52ac9A4/giphy.gif">
2. Using solely SelectorGadget extension <img width="100%" style="width:100%" src="https://media.giphy.com/media/mxKSfoBsX3fheXTJ6b/giphy.gif">

From there either of selectors from two approaches will work:

<img width="100%" style="width:100%" src="https://media.giphy.com/media/85nbA6QuDBoabnJ6zy/giphy.gif">


### Code
```python
from bs4 import BeautifulSoup
import requests, lxml

headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}

html = requests.get('https://www.bing.com/search?q=lion king&hl=en', headers=headers)
soup = BeautifulSoup(html.content, 'lxml')

for related_search in soup.select('.b_rs ul li'):
    title = related_search.text
    link = f"https://www.bing.com{related_search.a['href']}"
    print(f'{title}\n{link}')

# part of the output:
'''
lion
https://www.bing.com/search?q=lion&FORM=QSRE1
jeremy irons
https://www.bing.com/search?q=jeremy+irons&FORM=QSRE2
'''
```

### Using [Bing Related Searches API](https://serpapi.com/bing-related-searches)
SerpApi is a paid API with a free trial of 5,000 searches.
Here's how you can get the results:

<img width="100%" style="width:100%" src="https://media.giphy.com/media/nbSLExd7cT6n0l3EGM/giphy.gif">

```python
from serpapi import GoogleSearch
import  os

params = {
  "api_key": os.environ["API_KEY"], # pycharm environment
  "engine": "bing",
  "q": "lion king"
}

search = GoogleSearch(params)
results = search.get_dict()

for result in results['related_searches']:
    query = result['query']
    link = result['link']
    print(f'{query}\n{link}')

# part of the output:
'''
elton john circle of life
https://www.bing.com/search?q=elton+john+circle+of+life&FORM=QSRE1
lion king theatre
https://www.bing.com/search?q=lion+king+theatre&FORM=QSRE2
'''
```

### Links
[Code in the online IDE](https://replit.com/@DimitryZub1/Bing-Scrape-Organic-Search-Results-Python-SerpApi#bs4_results/get_related_searches.py) • [Bing Related Searches API](https://serpapi.com/bing-related-searches)

### Outro
If you have any questions or something isn't working correctly or you want to write something else, feel free to drop a comment in the comment section or via Twitter at [@serp_api](https://twitter.com/serp_api).

Yours,
Dimitry, and the rest of SerpApi Team.
