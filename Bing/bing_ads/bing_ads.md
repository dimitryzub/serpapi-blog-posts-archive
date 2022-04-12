Contents: intro, imports, what will be scraped, process, code, links, outro.

### Intro
This blog post is a continuation of Bing's web scraping series and contains info about how to scrape Ad results from Bing search using Python. An alternative API solution using SerpApi will be shown.

### Imports
```python
from bs4 import BeautifulSoup
import requests
import lxml
from serpapi import GoogleSearch
```

### What will be scraped
Expanded ads
![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/zbnwv2jolj8ukyhjgzkd.png)

Inline ads
![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/9qh3s860ottnpzfvajvx.png)


### Process
Selecting title/link `CSS` selectors from expanded ad results
<img width="100%" style="width:100%" src="https://media.giphy.com/media/I4QiG589RS5p2jroeT/giphy.gif">

Selecting title/link `CSS` selectors from inline ad results
<img width="100%" style="width:100%" src="https://media.giphy.com/media/t8JRQNl3WeaeJ8TI0L/giphy.gif">


**Inline ads code snippet:**
```python
for inline_ad in soup.select('.b_algo .b_vList.b_divsec .b_annooverride a'):
    inline_ad_title = inline_ad.text
    inline_ad_link = inline_ad['href']
```
**Expanded ads code snippet:**
```python
for expanded_ad in soup.select('.deeplink_title'):
    expanded_ad_title = expanded_ad.text
    expanded_ad_link = expanded_ad.a['href']
```

### Code
```python
from bs4 import BeautifulSoup
import requests, lxml

headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
}

html = requests.get('https://www.bing.com/search?q=john deere tractors buy', headers=headers)
soup = BeautifulSoup(html.text, 'lxml')

try:
    for expanded_ad in soup.select('.deeplink_title'):
        expanded_ad_title = expanded_ad.text
        expanded_ad_displayed_link = expanded_ad.a['href']
        print(f'{expanded_ad_title}\n{expanded_ad_displayed_link}')
except:
    pass

try:
    for inline_ad in soup.select('.b_algo .b_vList.b_divsec .b_annooverride a'):
        inline_ad_title = inline_ad.text
        inline_ad_displayed_link = inline_ad['href']
        print(f'{inline_ad_title}\n{inline_ad_displayed_link}')
except:
    pass


# parts of the output:
'''
# expanded ads
Compact Tractors
https://www.deere.com/en/tractors/compact-tractors/
View The Utility Tractors
https://www.deere.com/en/tractors/utility-tractors/

---------------------------------------------------

# inline ads
2032R
https://www.deere.com/en/tractors/compact-tractors/2-series-compact-tractors/2032r/
1025R
https://www.deere.com/en/tractors/compact-tractors/1-series-sub-compact-tractors/1025r/
'''
```

### Using [Bing Ad Results API](https://serpapi.com/bing-ads)
SerpApi is a paid API with a free trial of 5,000 searches.

```python
from serpapi import GoogleSearch

params = {
    "api_key": "YOUR_API_KEY",
    "engine": "bing",
    "q": "john deere tractors"
}

search = GoogleSearch(params)
results = search.get_dict()

for ads in results['ads']:
    title = ads['title']
    link = ads['displayed_link']
    print(title)
    print(link)

# part of the output:
'''
John Deere® Official Site - The Select Series Tractors
https://www.deere.com
John Deere Tractors | tractorhouse.com
https://www.tractorhouse.com/JohnDeere/Tractors
'''
```

### Links
[Code in the online IDE](https://replit.com/@DimitryZub1/Bing-Scrape-Organic-Search-Results-Python-SerpApi#bs4_results/get_ads.py) • [Bing Ad Results API](https://serpapi.com/bing-ads)

### Outro
If you have any questions or something isn't working correctly or you want to write something else, feel free to drop a comment in the comment section or via Twitter at [@serp_api](https://twitter.com/serp_api).

Yours,
Dimitry, and the rest of SerpApi Team.