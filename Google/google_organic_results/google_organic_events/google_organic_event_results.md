Contents: intro, imports, what will be scraped, process, code, links, outro.

### Intro
This blog post is a continuation of Google's web scraping series.
Here you'll see examples of how you can scrape Google Event Results from organic search using Python. An alternative API solution will be shown.

### Imports
```python
import requests, json
from bs4 import BeautifulSoup
from serpapi import GoogleSearch
```

### What will be scraped
![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/98dw92esnhtdvgxysu2k.png)

### Process
Selecting **Container**, **Title**, **Hours**, **Address** `CSS` selectors
<img width="100%" style="width:100%" src="https://media.giphy.com/media/ZHONUjnm2LGLa9hztf/giphy.gif">


Selecting **Day** and **Month** `CSS` selectors
<img width="100%" style="width:100%" src="https://media.giphy.com/media/xaqFL7Q7zvK3lNY2TY/giphy.gif">


Selecting **Link** `CSS` selector
<img width="100%" style="width:100%" src="https://media.giphy.com/media/60cr6tDfboPdXCz1BT/giphy.gif">


### Code
```python
import requests, json
from bs4 import BeautifulSoup

headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    "(KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}


response = requests.get("https://serpapi.com/searches/00664d3f0c817ad7/60df062e797ac6552141b3d4.html", headers=headers)
soup = BeautifulSoup(response.text, 'lxml')

events_data = []

for event in soup.select('.PaEvOc'):
    title = event.select_one('.YOGjf').text
    link = event.select_one('.odIJnf a')['href']
    date_day = event.select_one('.gsrt.v14Sh.OaCVOb .UIaQzd').text
    date_month = event.select_one('.gsrt.v14Sh.OaCVOb .wsnHcb').text
    when = event.select_one('.cEZxRc:nth-child(1)').text
    address_street = event.select_one('.cEZxRc:nth-child(2)').text
    address_city = event.select_one('.cEZxRc:nth-child(3)').text

    events_data.append({
        'title': title,
        'link': link,
        'date': {'start_date': f'{date_day} ' + date_month, 'when': when},
        'address': f'{address_street} - {address_city}',
    })

    print(json.dumps(events_data, indent=2, ensure_ascii=False))

-----------
'''
[
  {
    "title": "Ronan Keating: Twenty Twenty - London 2021",
    "link": "https://www.google.com/search?q=london+events&oq=london+events&sourceid=chrome&ie=UTF-8&ibp=htl;events&rciv=evn&sa=X&ved=2ahUKEwjnka6iscTxAhWOGs0KHYs4B48Q5bwDegQICBAB#fpstate=tldetail&htidocid=L2F1dGhvcml0eS9ob3Jpem9uL2NsdXN0ZXJlZF9ldmVudC8yMDIwLTA2LTI1fDM4MDE1NTc5MjQ1NTI2NDA1OQ%3D%3D&htivrt=events&mid=/g/11fskmgg3v",
    "date": {
      "start_date": "3 Jul",
      "when": "Tomorrow, 7:30 PM"
    },
    "address": "Eventim Apollo, 45 Queen Caroline St - London, United Kingdom"
  }
]
...
'''
```

### Using [Google Events Engine Results API](https://serpapi.com/google-events-api)
SerpApi is a paid API with a free trial of 5,000 searches.
```python
import json # used for pretty output
from serpapi import GoogleSearch

params = {
  "api_key": "YOUR_API_KEY",
  "engine": "google",
  "q": "london events",
  "gl": "us",
  "hl": "en"
}

search = GoogleSearch(params)
results = search.get_dict()

for event_result in results['events_results']:
    print(json.dumps(event_result, indent=2, ensure_ascii=False))

------------
'''
{
  "title": "Ronan Keating: Twenty Twenty - London 2021",
  "date": {
    "start_date": "Jul 3",
    "when": "Tomorrow, 7:30 PM"
  },
  "address": [
    "Eventim Apollo, 45 Queen Caroline St",
    "London, United Kingdom"
  ],
  "link": "https://www.google.com/search?q=london+events&oq=london+events&sourceid=chrome&ie=UTF-8&ibp=htl;events&rciv=evn&sa=X&ved=2ahUKEwjnka6iscTxAhWOGs0KHYs4B48Q5bwDegQICBAB#fpstate=tldetail&htidocid=L2F1dGhvcml0eS9ob3Jpem9uL2NsdXN0ZXJlZF9ldmVudC8yMDIwLTA2LTI1fDM4MDE1NTc5MjQ1NTI2NDA1OQ%3D%3D&htivrt=events&mid=/g/11fskmgg3v",
  "thumbnail": "https://serpapi.com/searches/60df062e797ac6552141b3d4/images/b43677f4b21fbd9cbf2530c260e8afdb19cef485ab5a5f52c442f77151330da1.jpeg"
}
...
'''
```


### Links
[Code in the online IDE](https://replit.com/@DimitryZub1/Google-Search-Scrape-Events-Results-pythonserpapi#main.py) • [Google Events Engine Results API](https://serpapi.com/google-events-api)

### Outro
If you have any questions or something isn't working correctly or you want to write something else, feel free to drop a comment in the comment section or via Twitter at [@serp_api](https://twitter.com/serp_api).

Yours,
Dimitry, and the rest of SerpApi Team.