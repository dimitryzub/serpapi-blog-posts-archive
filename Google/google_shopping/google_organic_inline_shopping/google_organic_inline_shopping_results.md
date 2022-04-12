Contents: intro, imports, what will be scraped, process, code, links, outro.

### Intro
This blog post is a continuation of Google's web scraping series. Here you'll see examples of how you can scrape Google Inline Shopping results using Python. An alternative SerpApi solution will be shown.

### Imports
```python
import requests
from bs4 import BeautifulSoup
from serpapi import GoogleSearch
```

### What will be scraped
Top block
![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/y2yz76sk5dhyog6em54m.png)

Right block
![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/x9rytwnanttpvi1r3mn7.png)


### Process

Selecting container
<img width="100%" style="width:100%" src="https://media.giphy.com/media/G7zrxek4t1zBAE6nsN/giphy.gif">


Selecting **Title**
<img width="100%" style="width:100%" src="https://media.giphy.com/media/WWNojMx1JKTFJitidK/giphy.gif">


Selecting **Price**
<img width="100%" style="width:100%" src="https://media.giphy.com/media/gg6SnePnyQ3pniPgb2/giphy.gif">


Selecting **Source**
<img width="100%" style="width:100%" src="https://media.giphy.com/media/FwMJuxf3Cv3ohvdytq/giphy.gif">

*Same process goes for the right block results.*

### Code

```python
import requests, json, lxml
from bs4 import BeautifulSoup

headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    "(KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}

params = {
  "q": "buy coffe", # intentional grammatical error to display right side shopping results
  "hl": "en",
  "gl": "us"
}

response = requests.get("https://www.google.com/search", headers=headers, params=params)
soup = BeautifulSoup(response.text, 'html.parser')

# scrapes both from top and right side shopping results
for result in soup.select('.pla-hovercard-content-ellip'):
    title = result.select_one('.pymv4e').text
    link = result.select_one('.pla-hovercard-content-ellip a.tkXAec')['href']
    ad_link = f"https://www.googleadservices.com/pagead{result.select_one('.pla-hovercard-content-ellip a')['href']}"
    price = result.select_one('.qptdjc').text
    try:
      rating = result.select_one('.Fam1ne.tPhRLe')["aria-label"].replace("Rated ", "").replace(" out of ", "").replace(",", "")
    except:
      rating = None

    try:
      reviews = result.select_one('.GhQXkc').text.replace("(", "").replace(")", "")
    except:
      reviews = None

    source = result.select_one('.zPEcBd.LnPkof').text.strip()

    print(f'{title}\n{link}\n{ad_link}\n{price}\n{rating}\n{reviews}\n{source}\n')

----------
'''
MUD\WTR | Mushroom Coffee Replacement, 90 servings
https://mudwtr.com/collections/shop/products/90-serving-bag
https://www.googleadservices.com/pagead/aclk?sa=l&ai=DChcSEwj5p8u-2rzyAhV2yJQJHfzhBoUYABAHGgJ5bQ&sig=AOD64_3NGBzLzkTv61K7kSrD2f9AREHH_g&ctype=5&q=&ved=2ahUKEwji7MK-2rzyAhWaaM0KHcnaDDcQ9aACegQIAhBo&adurl=
$125.00
4.85
1k+
mudwtr.com
...
'''
```



### Using [Google Inline Shopping API](https://serpapi.com/inline-shopping)
SerpApi is a paid API with a free plan.

The main difference here is that it already supports different Google Inline Shopping results that might appear on top/right parts of the page (*see example outputs*), besides bypassing Google's blocks if they appears.

```python
import json
from serpapi import GoogleSearch

params = {
  "api_key": "YOUR_API_KEY",
  "engine": "google",
  "q": "buy trampoline", # try to use different query to get right side shopping results
}

search = GoogleSearch(params)
results = search.get_dict()

for result in results['shopping_results']:
    print(json.dumps(result, indent=2, ensure_ascii=False))

--------------
'''
{
  "position": 1,
  "block_position": "top",
  "title": "Kangaroo Hoppers 15FT Round Kids Trampoline with Safety Enclosure Net, Basketball Hoop and Ladder, Outdoor Fun Summer Trampoline 15FT / APPLE GREEN",
  "price": "$544.99",
  "extracted_price": 544.99,
  "link": "https://www.google.com/aclk?sa=l&ai=DChcSEwiEt8LggcfxAhUtbG8EHX3OACYYABAEGgJqZg&ae=2&sig=AOD64_1U5ba--51CZ8yLWlN5uVw-QQo6Kw&ctype=5&q=&ved=2ahUKEwjp5bbggcfxAhVBHM0KHeV-AsYQ5bgDegQIAhA8&adurl=",
  "source": "Kangaroo Hopp...",
  "thumbnail": "https://serpapi.com/searches/60e067061988e55ccd479674/images/a89620ac0c8f92b77b5f789e340e17d9aa3a444194265aa1b91bfaaeeaf04717.png",
  "extensions": [
    "Special offer"
  ]
}

...

{
  "position": 1,
  "block_position": "right",
  "title": "Maxwell House Original Roast | 48oz",
  "price": "$10.49",
  "extracted_price": 10.49,
  "link": "https://www.google.com/aclk?sa=l&ai=DChcSEwiGn8aT2rzyAhXgyZQJHZHdBJMYABAEGgJ5bQ&ae=2&sig=AOD64_0jBjdUIMeqJvrXYxn4NGcpwCYrJQ&ctype=5&q=&ved=2ahUKEwiOxLmT2rzyAhWiFVkFHWMNAaEQ5bgDegQIAhBa&adurl=",
  "source": "Boxed",
  "rating": 4.6,
  "reviews": 2000,
  "thumbnail": "https://serpapi.com/searches/611e1b2cfdca3e6a1c9335e6/images/e4ae7f31164ec52021f1c04d8be4e4bda2138b1acd12c868052125eb86ead292.png"
}
...
{
  ...
  "shopping_results": [
    {
      "position": 1,
      "block_position": "right",
      "title": "Banana Republic Men's Slim Legacy Jean Medium Wash Size 32W 34L",
      "price": "$58.00",
      "extracted_price": 58.0,
      "link": "https://www.google.com/aclk?sa=l&ai=DChcSEwjc5-yLsP_sAhVM1sAKHdJ4AjQYABAFGgJpbQ&sig=AOD64_1DUpENWnXUhv0PigCNCOo-NQxHPA&ctype=5&q=&ved=2ahUKEwj3muaLsP_sAhWSLc0KHajQBb8Q5bgDegQIChBW&adurl=",
      "source": "Banana Republic",
      "rating": 4.7,
      "reviews": 86,
      "thumbnail": "<URL to image>",
      "extensions": [
        "Sale"
      ]
    }
'''
```


### Links
[Code in the online IDE](https://replit.com/@DimitryZub1/Google-Scrape-Inline-Shopping-pythonserpapi#main.py) • [Google Inline Shopping API](https://serpapi.com/inline-shopping)

### Outro
If you have any questions or something isn't working correctly or you want to write something else, feel free to drop a comment in the comment section or via Twitter at [@serp_api](https://twitter.com/serp_api).

Yours,
Dimitry, and the rest of SerpApi Team.