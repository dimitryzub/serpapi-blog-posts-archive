Contents: intro, imports, what will be scraped, process, code, links, outro.

### Intro
This blog post is a continuation of Google's web scraping series. Here you'll see examples of how you can scrape Google Video Results using Python using `beautifulsoup`, `requests`, `lxml` libraries. An alternative API solution will be shown.

### Imports
```python
import requests, lxml
from bs4 import BeautifulSoup
from serpapi import GoogleSearch
```

### What will be scraped

![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/p250d8t8lf4hoksozv72.png)


### Process

Selecting **Container** with all needed data
<img width="100%" style="width:100%" src="https://media.giphy.com/media/4wlqd2YmmirS0AllC1/giphy.gif">


Selecting **Displayed link**
<img width="100%" style="width:100%" src="https://media.giphy.com/media/t9rCWNLlhvWBq2uN37/giphy.gif">


Selecting **Title**, **Snippet**, **Uploaded by**, **Uploaded date**
<img width="100%" style="width:100%" src="https://media.giphy.com/media/LdoUTlsYxywXT7nvzW/giphy.gif">


### Code
```python
import requests, lxml
from bs4 import BeautifulSoup

headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}

params = {
    "q": "somebody toucha my spaghet",
    "tbm": "vid",
    "hl": "en" # get english results
}

response = requests.get("https://www.google.com/search", headers=headers, params=params)
soup = BeautifulSoup(response.text, 'lxml')

for results in soup.select('.tF2Cxc'):
    title = results.select_one('.DKV0Md').text
    link = results.a['href']
    displayed_link = results.select_one('.TbwUpd.NJjxre').text
    snippet = results.select_one('.aCOpRe span').text
    uploaded_by = results.select_one('.uo4vr span').text.split(' ')[2]
    upload_date = results.select_one('.fG8Fp.uo4vr').text.split(' · ')[0]
    print(f'{title}\n{link}\n{displayed_link}\n{snippet}\n{upload_date}\n{uploaded_by}\n')

--------------
'''
SOMEBODY TOUCHA MY SPAGHET - YouTube
https://www.youtube.com/watch?v=cE1FrqheQNI
www.youtube.com › watch
SOMEBODY TOUCHA MY SPAGHET. 10,319,777 views10M views. Dec 26, 2017. 166K. 1.8K. Share. Save ...
Dec 27, 2017
Darkcode
...
'''
```
*Note that program above won't scrape such layout:*
![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/9f9jcr9ce8f38lxxbymn.png)

_________

### Using [Google Video Results API](https://serpapi.com/videos-results)
SerpApi is a paid API with a free trial of 5,000 searches and scrapes additional layouts that might appear on Google Search, e.g. program above scrapes only this specific layout while SerpApi don't.

```python
from serpapi import GoogleSearch
import json # used for pretty output

params = {
  "api_key": "YOUR_API_KEY",
  "engine": "google",
  "q": "somebody toucha my spaghet",
  "tbm": "vid",
  "hl": "en",
}

search = GoogleSearch(params)
results = search.get_dict()

[print(json.dumps(result, indent=2, ensure_ascii=False)) for result in results['video_results']]

------------
'''
{
  "position": 1,
  "title": "SOMEBODY TOUCHA MY SPAGHET - YouTube",
  "link": "https://www.youtube.com/watch?v=cE1FrqheQNI",
  "displayed_link": "www.youtube.com › watch",
  "thumbnail": "https://serpapi.com/searches/60e1662d654a8c2684edee33/images/7554019104074b78f0fdde1c47929f2b933bcacc846404a15245dd2ae68bffe1.jpeg",
  "snippet": "SOMEBODY TOUCHA MY SPAGHET. 10,319,777 views10M views. Dec 26, 2017. 166K. 1.8K. Share. Save ...",
  "rich_snippet": {
      "extensions": [
        "Dec 26, 2017",
        "Uploaded by Darkcode"
      ]
   }
}
...
'''
```


### Links
[Code in the online IDE](https://replit.com/@DimitryZub1/Scrape-Google-Video-Results-pythonserpapi#main.py) • [Google Video Results API](https://serpapi.com/videos-results)

### Outro
If you have any questions or something isn't working correctly or you want to write something else, feel free to drop a comment in the comment section or via Twitter at [@serp_api](https://twitter.com/serp_api).

Yours,
Dimitry, and the rest of SerpApi Team.
