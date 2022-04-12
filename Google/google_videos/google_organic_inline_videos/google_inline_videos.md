Contents: intro, imports, what will be scraped, process, code, links, outro.

### Intro
This blog post is a continuation of Google's web scraping series. Here you'll see examples of how you can scrape Inline Videos from Google Search using Python using `beautifulsoup`, `requests` and `lxml` libraries. An alternative API solution will be shown.

### Imports
```python
import requests, lxml
from bs4 import BeautifulSoup
from serpapi import GoogleSearch
```

### What will be scraped
![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/itjft09zz5rcsspsnb96.png)

### Process

Selecting **Container**. **Link** lays directly in the container under `href` attribute.
<img width="100%" style="width:100%" src="https://media.giphy.com/media/1gueUSV5QBRIJSUNkG/giphy.gif">

Selecting **Title**, **Channel name**, **Platform**, **Date**, **Duration** `CSS` selectors.
<img width="100%" style="width:100%" src="https://media.giphy.com/media/sXps0zdLri6KcQG5Z1/giphy.gif">


### Code
```python
import requests, lxml
from bs4 import BeautifulSoup

headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}

response = requests.get("https://www.google.com/search?q=the last of us 2 reviews", headers=headers)
soup = BeautifulSoup(response.text, 'lxml')

for result in soup.select('.WpKAof'):
    title = result.select_one('.p5AXld').text
    link = result['href']
    channel = result.select_one('.YnLDzf').text.replace(' · ', '')
    video_platform = result.select_one('.hDeAhf').text
    date = result.select_one('.rjmdhd span').text
    duration = result.select_one('.MyDQSe span').text
    print(f'{title}\n{link}\n{video_platform}\n{channel}\n{date}\n{duration}\n')

---------------
'''
The Last of Us 2 Review
https://www.youtube.com/watch?v=QwreMeXlFoY
YouTube
IGN
Jun 12, 2020
8:01
'''
```

### Using [Google Inline Videos API](https://serpapi.com/inline-videos)
SerpApi is a paid API that provides a free trial of 5,000 searches.

The main differences is you don't have to maintain the parser, e.g. if layout/selectors is changed there's no need for debugging since it already done for the end-user, because at times it could annoying...
<img width="100%" style="width:100%" src="https://media.giphy.com/media/7SEDmthjL4GL0LSCn8/giphy.gif">

```python
import json # used for pretty print output
from serpapi import GoogleSearch

params = {
  "api_key": "YOUR_API_KEY",
  "engine": "google",
  "q": "the last of us 2 review",
  "gl": "us",
  "hl": "en"
}

search = GoogleSearch(params)
results = search.get_dict()

for results in results['inline_videos']:
    print(json.dumps(results, indent=2, ensure_ascii=False))

--------------------
'''
{
  "position": 1,
  "title": "The Last of Us 2 Review",
  "link": "https://www.youtube.com/watch?v=QwreMeXlFoY",
  "thumbnail": "https://serpapi.com/searches/60e144a7d737d7a357e568fc/images/b8492386da38ba88cc43d7cb6b9076998ce8d724281cad47c9ee2d1516f61052.jpeg",
  "channel": "IGN",
  "duration": "8:01",
  "platform": "YouTube",
  "date": "Jun 12, 2020"
}
...
'''
```

### Links
[Code in the online IDE](https://replit.com/@DimitryZub1/Scrape-Google-Inline-Videos-pythonserpapi#main.py) • [Google Inline Videos API](https://serpapi.com/inline-videos)

### Outro
If you have any questions or something isn't working correctly or you want to write something else, feel free to drop a comment in the comment section or via Twitter at [@serp_api](https://twitter.com/serp_api).

Yours,
Dimitry, and the rest of SerpApi Team.

<img width="100%" style="width:100%" src="https://media.giphy.com/media/J47zreUx5lBT2SqjUY/giphy.gif">