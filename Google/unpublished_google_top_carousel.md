Contents: intro, imports, what will be scraped, process, code, links, outro.

### Intro
This blog post is a continuation of Google's web scraping series. Here you'll see how to scrape Top Carousel Results from Google Search using Python with `beautifulsoup`, `requests` libraries. An alternative API solution will be shown.

### Imports
```python
from bs4 import BeautifulSoup
import requests, lxml, re, json
from serpapi import GoogleSearch
```

### What will be scraped
![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/igeu7sjdtibs4wmwxb9x.png)


### Process

[SelectorGadet](https://selectorgadget.com/) Chrome extension was used to visually grab `CSS` selectors. I used this extension to check if the selector is extracting the right data. This can be also achieved via Chrome Dev Tool Console - `$$(".EsIlz.klitem")`

Selecting container with all needed data
<img width="100%" style="width:100%" src="https://media.giphy.com/media/ZibnyUKkktk6aLLnXn/giphy.gif">


Selecting **link** selector
<img width="100%" style="width:100%" src="https://media.giphy.com/media/lGt8vdbEqg0vqRQZtV/giphy.gif">


Selecting **name** selector
<img width="100%" style="width:100%" src="https://media.giphy.com/media/VG9QuKav4gkqzNBcBj/giphy.gif">

I used `regex` to get rid of any digits from the string since it scrapes them as well and don't have any separation between words and digits. It can also be achieved with proper `CSS` selector, but I choose to use `regex` path.

[Regex link](https://regex101.com/r/3ls0p7/1) to see on example how it works, or see the screenshot. *Note that it will capture whitespaces as well as you can see below.*

![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/pjfk9vrzlti0tjocqwdn.png)


Selecting **year** selector
<img width="100%" style="width:100%" src="https://media.giphy.com/media/TgDqkx2kUi2dRpEqHq/giphy.gif">



### Code
```python
from bs4 import BeautifulSoup
import requests, lxml, re, json

headers = {
    'User-agent':
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}

params = {
  'q': 'eminem albums',
  'hl': 'en',
  'gl': 'us',
}

html = requests.get('https://www.google.com/search?q=', headers=headers, params=params).text
soup = BeautifulSoup(html, 'lxml')

data = []

extension_name = soup.select_one('#extabar > div:nth-child(2) > div > div:nth-child(1) > div > div.EyBRub > div.LXqMce > span.Wkr6U.z4P7Tc').text
for result in soup.select('.EsIlz.klitem'):
    name_to_fix = result.select_one('.dAassd').text
    # using regex to grab only non-digit elements
    name_match = re.findall(r'\D+', name_to_fix)
    # converts from list to a string
    name = ''.join(name_match)
    link = f"https://www.google.com{result.parent['href']}"
    year = result.select_one('.cp7THd').text
    # print(f'{name}\n{link}\n{year}\n')

    data.append({
        'extension_name': extension_name,
        'name': name,
        'link': link,
        'year': year,
    })

print(json.dumps(data, indent=2, ensure_ascii=False))

-------------
'''
[
  {
    "extention_name": "Albums",
    "name": "The Marshall Mathers LP",
    "link": "https://www.google.com/search?hl=en&gl=us&q=Eminem+The+Marshall+Mathers+LP&stick=H4sIAAAAAAAAAONgFuLSz9U3MCwrTi_KU-IEs40LTZO0xLOTrfRzS4szk_UTi0oyi0usEnOSSnOLHzFmcAu8_HFPWCp-0pqT1xgjuXCpFLLjYnPNK8ksqRSS4-KTQrJHg0GKhwuJbyTCxaufrm9omG2WnWSek2wosPfHVEaeRaxyrrmZeam5CiEZqQq-iUXFGYk5OUBGSUZqUbGCT8AENkYAILWltMEAAAA&sa=X&ved=2ahUKEwjXh5bdsczxAhXQRzABHbL6DJ8Q-BYwNHoECAEQOw",
    "year": "2000"
  },
  {
    "extention_name": "Albums",
    "name": "Kamikaze",
    "link": "https://www.google.com/search?hl=en&gl=us&q=Eminem+Kamikaze&stick=H4sIAAAAAAAAAONgFuLSz9U3MCwrTi_KU-LVT9c3NEyzLMvKMDHK1RLPTrbSzy0tzkzWTywqySwusUrMSSrNLX7EmMEt8PLHPWGp-ElrTl5jjOTCpVLIjovNNa8ks6RSSI6LTwrJLg0GKR4uJL6RCBfE9myz7CTznGRDgb0_pjLyLGLld83NzEvNVfBOzM3MTqxKncDGCAA80JGytgAAAA&sa=X&ved=2ahUKEwjXh5bdsczxAhXQRzABHbL6DJ8Q-BYwNXoECAEQPg",
    "year": "2018"
  }
]
...
'''
```

### Using [Google Top Carousel API](https://serpapi.com/top-carousel)
SerpApi is a paid API with a free trial of 5,000 searches.

The main difference is that the process is much faster and easier to get things done since you don't have to build everything from scratch and maintain after without even thinking how to bypass blocking from Google.
```python
from serpapi import GoogleSearch
import os, json

params = {
  "api_key": os.environ["API_KEY"],
  "engine": "google",
  "q": "eminem albums",
  "gl": "us",
  "hl": "en"
}

search = GoogleSearch(params)
results = search.get_dict()

for result in results['knowledge_graph']['albums']:
    print(json.dumps(result, indent=2))
---------------------
'''
{
  "name": "The Marshall Mathers LP",
  "extensions": "2000",
  "link": "https://www.google.com/search?gl=us&hl=en&q=Eminem+The+Marshall+Mathers+LP&stick=H4sIAAAAAAAAAONgFuLSz9U3MCwrTi_KU-IEs40LTZO0xLOTrfRzS4szk_UTi0oyi0usEnOSSnOLHzFmcAu8_HFPWCp-0pqT1xgjuXCpFLLjYnPNK8ksqRSS4-KTQrJHg0GKhwuJbyTCxaufrm9omG2WnWSek2wosPfHVEaeRaxyrrmZeam5CiEZqQq-iUXFGYk5OUBGSUZqUbGCT8AENkYAILWltMEAAAA&sa=X&ved=2ahUKEwiS3cCVsszxAhUMSTABHYM5Du4Q-BZ6BAgBEDs",
  "image": "https://serpapi.com/searches/60e338d9eb690fdd2877188d/images/66b1f08805e45f71979349ed840bff8675778506fbee48d1e75c2c6213859b54.jpeg"
}
...
'''
```


### Links
[Code in the online IDE](https://replit.com/@DimitryZub1/Scrape-Google-Top-Carousel-Results-with-Python#main.py) • [Google Top Carousel API](https://serpapi.com/top-carousel)

### Outro
If you have any questions or something isn't working correctly or you want to write something else, feel free to drop a comment in the comment section or via Twitter at [@serp_api](https://twitter.com/serp_api).

Yours,
Dimitry, and the rest of SerpApi Team.


<img width="100%" style="width:100%" src="https://media.giphy.com/media/DAoMUVZMNwloc/giphy.gif">