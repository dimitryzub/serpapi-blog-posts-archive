Contents: intro, imports, what will be scraped, process, code, links, outro.

### Intro
Well, hello there to people who came from the last Bing series! This blog post is a continuation of Bing's web scraping series and contains info about how to scrape Bing News results using Python. An alternative solution will be shown after the first block of code.

### Imports
```python
import requests
import lxml
from bs4 import BeautifulSoup
from serpapi import GoogleSearch
```

### What will be scraped
![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/itkaiazpexy8ny3a21o4.png)


### Process
The process is straight-forward. [SelectorGadget](https://selectorgadget.com/) Chrome extension was to grab `CSS` selectors.

The following GIF illustrates how to get `CSS` selectors of the **Title**, **URL**, **Snippet**, **Source website**, and when news has been posted.
<img width="100%" style="width:100%" src="https://media.giphy.com/media/pighwI7rvr6tdFzKCN/giphy.gif">


### Code
```python
from bs4 import BeautifulSoup
import requests, lxml

headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}

html = requests.get('https://www.bing.com/news/search?q=faze+clan', headers=headers)
soup = BeautifulSoup(html.text, 'lxml')

for result in soup.select('.card-with-cluster'):
    title = result.select_one('.title').text
    link = result.select_one('.title')['href']
    snippet = result.select_one('.snippet').text
    source = result.select_one('.source a').text
    date_posted = result.select_one('#algocore span+ span').text
    print(f'{title}\n{link}\n{source}\n{date_posted}\n{snippet}\n')

# part of the output:
'''
FaZe Clan shows off new execute for Mirage against Furia Esports
https://win.gg/news/8521/faze-clan-shows-off-new-execute-for-mirage-against-furia-esports
WIN.gg
2h
During a match against Team Furia in the Gamers Without Borders Cup, the camera spotted an interesting interaction between ...
'''
```

### Using [Bing News Engine Results API](https://serpapi.com/bing-news-api)
SerpApi is a paid API with a free trial of 5,000 searches.

```python
from serpapi import GoogleSearch
import json

params = {
  "api_key": "YOUR_API_KEY",
  "engine": "bing_news",
  "q": "faze clan"
}

search = GoogleSearch(params)
results = search.get_dict()

for result in results['organic_results']:
    print(json.dumps(result, indent=2, ensure_ascii=False))

# part of the output:
'''
{
  "title": "FaZe Clan shows off new execute for Mirage against Furia Esports",
  "link": "https://win.gg/news/8521/faze-clan-shows-off-new-execute-for-mirage-against-furia-esports",
  "snippet": "During a match against Team Furia in the Gamers Without Borders Cup, the camera spotted an interesting interaction between ...",
  "source": "WIN.gg",
  "date": "2h",
  "thumbnail": "https://serpapi.com/searches/60d82f308ccee022b4ab7525/images/62e054f4209c882415dd75f5245f96d23bd4c1538d707fb513a0918671c831d7.jpeg"
}
'''
```

### Link
[Code in the online IDE](https://replit.com/@DimitryZub1/Bing-Scrape-Organic-Search-Results-Python-SerpApi#bs4_results/get_news_results.py) • [Bing News Engine Results API](https://serpapi.com/bing-news-api)

### Outro
If you have any questions or something isn't working correctly or you want to write something else, feel free to drop a comment in the comment section or via Twitter at [@serp_api](https://twitter.com/serp_api).

Yours,
Dimitry, and the rest of SerpApi Team.