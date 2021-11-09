Contents: intro, imports, organic results, related searches, related items, links, possible use cases, outro.

### Intro
This blog post as my other blog posts will contain code examples that you can overlay over each other to get the desired outcomes. Each block of code will be represented with an alternative solution Ebay Search Engine Results API from SerpApi.


While scraping eBay, `select()`, `select_one()` `bs4` methods in combo with [SelectorGadget](https://selectorgadget.com/) Chrome extension really speed ups the process and shortens the lines of code significantely because we don't have to specify from which element we're trying to get certain `tag`, `class`, `value` or `attribute` link with `find()` or `find_all()` methods. In short, eBay website structure is consistent which means that it's much easier to scrape.

### Imports
```python
from bs4 import BeautifulSoup
import requests, json, lxml, os
from serpapi import GoogleSearch
```

### Organic Search Results
This part is about scraping this container:
![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/3jtnfy4nyly469dr07te.png)
```python
from bs4 import BeautifulSoup
import requests, json, lxml

headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}


def get_organic_results():
    html = requests.get('https://www.ebay.com/sch/i.html?_nkw=Minecraft Creeper Figure', headers=headers).text
    soup = BeautifulSoup(html, 'lxml')

    data = []

    for item in soup.select('.s-item__wrapper.clearfix'):
        title = item.select_one('.s-item__title').text
        link = item.select_one('.s-item__link')['href']
        
        try:
            condition = item.select_one('.SECONDARY_INFO').text
        except:
            condition = None

        try:
            shipping = item.select_one('.s-item__logisticsCost').text
        except:
            shipping = None

        try:
            location = item.select_one('.s-item__itemLocation').text
        except:
            location = None

        try:
            watchers_sold = item.select_one('.NEGATIVE').text
        except:
            watchers_sold = None

        if item.select_one('.s-item__etrs-badge-seller') is not None:
            top_rated = True
        else:
            top_rated = False

        try:
            bid_count = item.select_one('.s-item__bidCount').text
        except:
            bid_count = None

        try:
            bid_time_left = item.select_one('.s-item__time-left').text
        except:
            bid_time_left = None

        try:
            reviews = item.select_one('.s-item__reviews-count span').text.split(' ')[0]
        except:
            reviews = None

        try:
            exctention_buy_now = item.select_one('.s-item__purchase-options-with-icon').text
        except:
            exctention_buy_now = None

        try:
            price = item.select_one('.s-item__price').text
        except:
            price = None

        data.append({
            'item': {'title': title, 'link': link, 'price': price},
            'condition': condition,
            'top_rated': top_rated,
            'reviews': reviews,
            'watchers_or_sold': watchers_sold,
            'buy_now_extention': exctention_buy_now,
            'delivery': {'shipping': shipping, 'location': location},
            'bids': {'count': bid_count, 'time_left': bid_time_left},
        })

    print(json.dumps(data, indent = 2, ensure_ascii = False))


get_organic_results()

# part of the output:
'''
[
  {
    "item": {
      "title": "Minecraft Overworld Diamond Action Figure Toy Steve Enderman Creeper Collection",
      "link": "https://www.ebay.com/itm/224433499750?_trkparms=ispr%3D1&hash=item3441476e66:g:EaAAAOSw20xgf7dY&amdata=enc%3AAQAGAAACoPYe5NmHp%252B2JMhMi7yxGiTJkPrKr5t53CooMSQt2orsSvtkx670Z0mbyfWqmxLFLYRANDiPOYlNvip6TXpLHigEvqpL5r0bHCZUi1RNW0AmKOb%252FIUIc%252FFDzouRq6XEAsFgkUTV%252BjgofDCIitmj01UxQo9UMhLDq7opbN31c0RL%252Bv07UXSMfkwzYWkzLu1XwuH7LWKtqdxneY%252FEurfMj466vHliEzbyo96BcRaAk7Ho7FLNvIjMxvNUPLzS8QBggEMASGqfLydtgQwyvdqxf2Zga4D%252F9615pGPPBKVkuunMdDwDKBYTMujyu%252Fxo7wlc93IfWRgnww4SRLtHemWiwCmImsWbAqScgH7zXbMD62Vup%252F8HtJPyYsfspo2aagZ6CFOSSmXaIkVRylV1UjrD2TCjuDKGG9tKfcYn3%252BKNFigCjw0FQWkKu7hCigpsWHZYzQUg2rz35j%252BXNIkcawoYJ7HTDYV4uZY95BzLzZ0GWYfqEOWj7TVBOGFdzocR1Ic98dMcHYk4YPPi14Qo0R2CQdMmwmfKxnH2ROIkCYtrKu8rQlPmiDqMRYWVz08g9o1KlD7sJGKL2unIjAFS7AwWxZCpTl0EHiFJo03tGWuS6q5VD%252F88EVpwvvTVFb4zpDeaLUD3q2y6QXbzc3lPJAh2HydbilTqpbhnaAkiLNadxmdxB0DKD7skTcHnq8Vq%252FixA1dqtTCF%252BqnFaNxCnruZMBBxXvUXxPUkxVAGOE%252BByPPGU9uYLKuoSvBVyvUwUwrRRXOIi%252F325u374W%252F%252FwhgKUCHEQ1aK4Z%252BVHCiSAMECrONLheth4CMqO9%252BbJf7Hk3wcDuD1JG5utkYst2C82PJwZDRgKGueCimYYsOL60YBSrz95uE9nd9JF9ZDWwnF42iavQpOw%253D%253D%7Campid%3APL_CLK%7Cclp%3A2334524",
      "price": "$6.70 to $37.65"
    },
    "condition": "Brand New",
    "top_rated": false,
    "reviews": null,
    "watchers_or_sold": "5+ watchers",
    "buy_now_extention": "Buy It Now",
    "delivery": {
      "shipping": "Free International Shipping",
      "location": "from China"
    },
    "bids": {
      "count": null,
      "time_left": null
    }
  }
]
'''
```

### Using [Ebay Organic Results API](https://serpapi.com/ebay-organic-results)
```python
from serpapi import GoogleSearch
import os, json


def get_organic_results():
    params = {
        "engine": "ebay",
        "ebay_domain": "ebay.com",
        "_nkw": "minecraft creeper figure",
        "api_key": os.getenv("API_KEY"),
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    data = []

    for result in results['organic_results']:
        try:
            sponsoerd = result['sponsored']
        except:
            sponsoerd = None
        title = result['title']
        link = result['link']
        try:
            subtitle = result['subtitle']
        except:
            subtitle = None

        try:
            condition = result['condition']
        except:
            condition = None

        try:
            shipping = result['shipping'].split(' ')[0]
        except:
            shipping = None

        try:
            price = result['price']['raw']
        except:
            price = None

        try:
            review = result['reviews']
        except:
            review = None

        try:
            returns = result['returns']
        except:
            returns = False

        try:
            top_rated = result['top_rated']
        except:
            top_rated = False

        try:
            bid_count = result['bids']['count']
        except:
            bid_count = None

        try:
            bid_time_left = result['bids']['time_left']
        except:
            bid_time_left = None

        try:
            buy_now_extensions = result['extensions']
        except:
            buy_now_extensions = None
            

        data.append({
            "title": title,
            "subtitle": subtitle,
            'link': link,
            "price": price,
            "shipping_cost": shipping,
            'returns': returns,
            "sponsored": sponsoerd,
            "item_condition": condition,
            'top_rated': top_rated,
            'reviews': review,
            'bids': {'count': bid_count, 'time_left': bid_time_left},
            'buy_now': buy_now_extensions,
        })

    print(json.dumps(data, indent=2, ensure_ascii=False))


get_organic_results()

# Part of the output:
'''
[
  {
    "title": "🔥Minecraft Earth Boost Minis Repairing Villager & Mining Creeper Figure",
    "subtitle": "4 of the Minecraft Earth boost",
    "link": "https://www.ebay.com/itm/203469124018?epid=22043750949&_trkparms=ispr%3D1&hash=item2f5fb471b2:g:JSoAAOSwzwBgqu0Y&amdata=enc%3AAQAGAAACkPYe5NmHp%252B2JMhMi7yxGiTJkPrKr5t53CooMSQt2orsSjVt3vLKCbov98Z19qhuwY9LA8W0Em6QYY3I%252Fr7%252FM8Lv%252BRg4EVj7%252FeJulg1E4gFPZsMHjNyXn7JFogjli2WhcweKt0p9AEGk6hT6ZhQ6IBAUfg7OEgFF182lbGMPjLWAnrfGSE15Q6j32Yc6PIvt4vPItRcIazFpSR3eKOJvbVT4oEAaZAMsFUl7%252FjmMIbIdG8QhV8FMPRhHFRz7QolIZUA%252FgbSAwH5EocbMsY%252FXY%252BwESDJPZ0THibIecs4fHFQHEqvi3%252Bx5EmXTW%252Fw%252BdJAOA2LjeDASPJprhpmlhZoiXAkcgstS2xlSut1lD3ghKEvr8eIrbxTPfVMxuC9vj%252FaWJoF7TiLWXXGbUL8ogOB580H%252Fe6MhCsqT4RsMKlIHVBN9bauI0gEMEG636Soc7oHZSKoz86gl91rmUOWTV4QUuKi2AJb61ysUdJ58nLOiXFlIMsbJiRJvU8QrrYGSiZr5tts%252F%252Bw9btKcIXaHYA9RprVb2Bh70lMkI74VyGPKQRV3Vj2VF0JVKm2TjUc%252BhRPZrc%252FU9lGLoLEXOk0Rijgeq8DGiiGXdf2EeFXLO6J7WYjIwJyaYQLOi5VzNvcT0YTtJBBdX%252Bgq8yv%252BEEQi6K64Gnq0Ed8V1q%252F9YOO7WAGZIW9G%252FurMmE9Mg0WB8IBvTfjzCb2dzyfprvuZZsLBtwCNpsZtrwgGi60DfGznTaX9J%252FFVWthqBVnsad5ovxIZ48HRSp8aa5LcgdUeokf22nCOwy7DrvJzfDRnhDNYG%252BrhGINq3o78FVkFTpLv%252FfBE4ot3sgzwl1a4bZwcp1MLIecgzbNXTeJ0nyJpO4pigSvigKxP1X%7Campid%3APL_CLK%7Cclp%3A2334524",
    "price": "$27.65",
    "shipping_cost": "+$17.55",
    "returns": false,
    "sponsored": null,
    "item_condition": "Brand New",
    "top_rated": false,
    "reviews": null,
    "bids": {
      "count": null,
      "time_left": null
    },
    "buy_now": [
      "or Best Offer"
    ]
  }
]
'''
```

### Related Search Results
This part is about scraping this container:
![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/bia3yy9m1uk1f37lxal7.png)
```python
from bs4 import BeautifulSoup
import requests, lxml

headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}


def get_related_search_results():
    html = requests.get('https://www.ebay.com/sch/i.html?_nkw=Minecraft Creeper Figure', headers=headers).text
    soup = BeautifulSoup(html, 'lxml')

    for result in soup.select('.srp-related-searches a'):
        title = result.text
        link = result['href']
        print(f'{title}\n{link}')

get_related_search_results()

# output:
'''
minecraft enderman figure
https://www.ebay.com/sch/i.html?_nkw=minecraft+enderman+figure&_sop=12
minecraft zombie figure
https://www.ebay.com/sch/i.html?_nkw=minecraft+zombie+figure&_sop=12
minecraft steve figure
https://www.ebay.com/sch/i.html?_nkw=minecraft+steve+figure&_sop=12
'''
```

### Using [Ebay Related Searches API](https://serpapi.com/ebay-related-searches)
```python
from serpapi import GoogleSearch

def get_related_search_results():
    params = {
        "engine": "ebay",
        "ebay_domain": "ebay.com",
        "_nkw": "minecraft creeper figure",
        "api_key": "YOUR_API_KEY",
    }

    search = GoogleSearch(params)
    results = search.get_dict()


    for result in results['related_searches']:
        title = result['query']
        link = result['link']
        print(f'{title}\n{link}')


get_related_search_results()

# output:
'''
minecraft enderman figure
https://www.ebay.com/sch/i.html?_nkw=minecraft+enderman+figure&_sop=12
minecraft zombie figure
https://www.ebay.com/sch/i.html?_nkw=minecraft+zombie+figure&_sop=12
minecraft steve figure
https://www.ebay.com/sch/i.html?_nkw=minecraft+steve+figure&_sop=12
'''
```

### Related Items Results
```python
from bs4 import BeautifulSoup
import requests, lxml, re

headers = {
    "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}


def get_related_items_results():
    html = requests.get('https://www.ebay.com/sch/i.html?_nkw=minecraft', headers=headers).text
    soup = BeautifulSoup(html, 'lxml')

    for result in soup.select('.srp-carousel-list__item-link--truncated-small-item'):
        title = result.text
        link = result['href']
        print(f'{title}\n{link}')


get_related_items_results()

# part of the output:
'''
Video Games - apply Category filter
https://www.ebay.com/sch/i.html?_nkw=minecraft&_sacat=139973
Action Figures - apply Category filter
https://www.ebay.com/sch/i.html?_nkw=minecraft&_sacat=261068
'''
```

### Using [Ebay Related Items API](https://serpapi.com/ebay-related-items)
```python
from serpapi import GoogleSearch

def get_related_items_results():
    params = {
        "engine": "ebay",
        "ebay_domain": "ebay.com",
        "_nkw": "toster",
        "api_key": "YOUR_API_KEY",
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    for result in results['related_items']:
        title = result['title']
        link = result['link']
        thumbnail = result['thumbnail']
        print(f'{title}\n{link}\n{thumbnail}\n')


get_related_items_results()
```

### Links
Code in the [online IDE](https://replit.com/@DimitryZub1/Scrape-eBay-Search-Results-bs4-requests-serpapi#main.py) • [Ebay Search Engine Results API](https://serpapi.com/ebay-search-api)

### Possible use cases
- Price monitor for competitors price changes.
- If the product on Amazon is more expensive, find it on eBay.
- Find good selling item on Amazon, find the same item on eBay for cheaper and sell it on Amazon (*dropshipping*)
- Build a dropshipping item research tool.

### Outro
If you have any questions or something isn't working correctly or you want to write something else, feel free to drop a comment in the comment section or via Twitter at [@serp_api](https://twitter.com/serp_api).

Yours,
Dimitry, and the rest of SerpApi Team.