Contents: intro, imports, what will be scraped, process, code, links, outro.


### Intro
This blog post is a continuation of the DuckDuckGo web scraping series. Here you'll see how to scrape Related Search Results using Python with `selenium` library. An alternative API solution will be shown.

*This blog post assumes that you know the basics of [`selenium`](https://www.selenium.dev/documentation/en/webdriver/browser_manipulation/)*


### Imports
```python
from selenium import webdriver
```

### What will be scraped
![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/jvkb166m77st9qbabl0k.png)


### Process
For some reason `request-html` can't locate elements at the bottom of the page when using `xpath` or `css` selectors, and `scrolldown=` parameter didn't help either.

This time `selenium` was used since it is the easiest way to get the data but at the same time, not the fastest.

Selecting `CSS` selector to grab **query** and a **link** and running the script.
<img width="100%" style="width:100%" src="https://media.giphy.com/media/0tKMZpqOCHzIm3lSLF/giphy.gif">

*Note №1: running `selenium` in <u>headless</u> mode didn't return any results, or I was doing something wrong.*

*Note №2: the data could be extracted from the <script> tag without `selenium` use, but it will be a much more time-consuming process.*

### Code
```python
from selenium import webdriver

driver = webdriver.Chrome(executable_path='/path/to/chromedriver.exe')
driver.get('https://duckduckgo.com/?q=fus ro dah&kl=us-en&ia=web')

for result in driver.find_elements_by_css_selector('.result__a.related-searches__link'):
    query = result.text
    link = result.get_attribute('href')
    print(f'{query}\n{link}\n')
driver.quit()

------------------
'''
fus ro dah meme
https://duckduckgo.com/?q=fus%20ro%20dah%20meme&kl=us-en

fus ro dah sound
https://duckduckgo.com/?q=fus%20ro%20dah%20sound&kl=us-en

fus ro dah skyrim
https://duckduckgo.com/?q=fus%20ro%20dah%20skyrim&kl=us-en
...
'''
```

### Using [DuckDuckGo Related Searches API](https://serpapi.com/duckduckgo-related-searches)
SerpApi is a paid API with a free plan.

The difference in using an API solution is that you'll get a faster response since there's no need to render the page. Additionally, iterating over structured `JSON` is a bit faster process rather than searching selectors from scratch or finding ways to avoid something.

```python
import json
from serpapi import GoogleSearch

params = {
  "api_key": "YOUR_API_KEY",
  "engine": "duckduckgo",
  "q": "fus ro dah",
  "kl": "us-en"
}

search = GoogleSearch(params)
results = search.get_dict()

for result in results['related_searches']:
    print(json.dumps(result, indent=2))
```

<img width="100%" style="width:100%" src="https://media.giphy.com/media/FDEwcpBrUe5sXMINWe/giphy.gif">

### Links
[Code in the online IDE](https://replit.com/@DimitryZub1/DuckDuckGo-Scrape-Related-Searches-python#main.py) • [DuckDuckGo Related Searches API](https://serpapi.com/duckduckgo-related-searches)


### Outro
If you have any questions or something isn't working correctly or you want to write something else, feel free to drop a comment in the comment section or via Twitter at [@serp_api](https://twitter.com/serp_api).

Yours,
Dimitry, and the rest of SerpApi Team.