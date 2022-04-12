Contents: intro, imports, what will be scraped, process, code, links, outro.

### Intro
This blog post is a continuation of a Bing scraping series. This post will show how to scrape Bing local map results from organic search using Python.

### Imports
```python
from bs4 import BeautifulSoup
import requests
import lxml
import json # used to convert `json` string to python dict
from serpapi import GoogleSearch
```

### What will be scraped
![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/b31ek361sf3j7o9t1nwz.png)

### Process
The whole process was pretty much going back and forwards by testing `CSS` selectors, going to [`.parent`](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#parent) elements, [`splitting`](https://www.w3schools.com/python/ref_string_split.asp), [`replacing`](https://www.w3schools.com/python/ref_string_replace.asp) unwanted parts of the data, converting valid `JSON` string to a Python Dictionary (*latitude, longitude*).

**Examples:**
Before move on, a [CSS Selector Reference](https://www.w3schools.com/cssref/css_selectors.asp).

Get container
<img width="100%" style="width:100%" src="https://media.giphy.com/media/CG8Dlj8AfnXJh7LAaG/giphy.gif">

Get Place ID
<img width="100%" style="width:100%" src="https://media.giphy.com/media/6a1YpUOnrOvDnNqPAR/giphy.gif">

Get Title
<img width="100%" style="width:100%" src="https://media.giphy.com/media/EhS7aKLgtN6KVSBLdx/giphy.gif">

Get Rating
<img width="100%" style="width:100%" src="https://media.giphy.com/media/EAtEMxumBbhx3UF1Li/giphy.gif">

Get Reviews
<img width="100%" style="width:100%" src="https://media.giphy.com/media/njDSHFPnEgBrx733lc/giphy.gif">

Get Address
<img width="100%" style="width:100%" src="https://media.giphy.com/media/LBvMxCCHl5AoiuFtQd/giphy.gif">

Get Latitude, Longitude
<img width="100%" style="width:100%" src="https://media.giphy.com/media/X3jMSkb0YzNSCuFcw2/giphy.gif">


Get website URL
This one was the trickiest. Because if you call an `<a>` tag with the `ibs_2btns` class it will print out `DIRECTIONS` not `WEBSITE` and if you try to use `.next_sibling` or going down the tree e.g. `.a.div.div.div.a` it will return `None`.

Several approaches were tried to come up from different angles and the way with `.parent` was successful so I stopped trying other things right away. *Possibly I missed the most obvious and easiest solution.*
![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/373b5v890avurjp41r4h.png)


### Code
```python
from bs4 import BeautifulSoup
import requests, lxml, json

headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}

html = requests.get('https://www.bing.com/search?q=sf lunch&hl=en', headers=headers)
soup = BeautifulSoup(html.text, 'lxml')

local_map_results = []

for result in soup.select('.b_scard.b_scardf.b_scardh'):
    place_id = result.div.div['data-ypid']
    title = result.select_one('.lc_content h2').text
    rating = result.select_one('.csrc.sc_rc1')['aria-label'].split(' ')[1]
    reviews = result.select_one('.b_factrow a').text.split(' ')[1].replace('(', '').replace(')', '')
    reviews_link = result.select_one('.b_factrow a')['href']
    try:
        location = result.select_one('.b_address').text
    except:
        location = None
    try:
        hours = result.select_one('.opHours > span').text
    except:
        hours = None
    directions = f"https://www.bing.com{result.select_one('a.ibs_2btns')['href']}"
    website = result.select_one('.bm_dir_overlay+ .ibs_2btns .ibs_btn').parent['href']
    latitude = json.loads(result.select_one('.bm_dir_overlay')['data-directionoverlay'])['waypoints'][0]['point']['latitude']
    longitude = json.loads(result.select_one('.bm_dir_overlay')['data-directionoverlay'])['waypoints'][0]['point']['longitude']

    local_map_results.append({
        'place_id': place_id,
        'title': title,
        'rating': rating,
        'reviews': reviews,
        'reviews_link': reviews_link,
        'hours': hours,
        'website': website,
        'directions': directions,
        'location': location,
        'latitude': latitude,
        'longitude': longitude,
    })

print(json.dumps(local_map_results, indent = 2, ensure_ascii = False))


# part of the output:
'''
[
  {
    "place_id": "YN114x189818795",
    "title": "Absinthe Brasserie & Bar",
    "rating": "4",
    "reviews": "596",
    "reviews_link": "https://www.tripadvisor.com/Restaurant_Review-g60713-d349444-Reviews-Absinthe_Brasserie_Bar-San_Francisco_California.html?m=17457",
    "hours": "Closed · Opens tomorrow 11 am",
    "website": "http://absinthe.com/",
    "directions": "https://www.bing.com/maps/directions?rtp=adr.~pos.37.7769889831543_-122.42288970947266_398+Hayes+St%2c+San+Francisco%2c+CA+94102_Absinthe+Brasserie+%26+Bar_(415)+551-1590",
    "location": "398 Hayes St, San Francisco, CA 94102",
    "latitude": 37.7769889831543,
    "longitude": -122.42288970947266
  }
]
'''
```

### Using [Bing Local Pack API](https://serpapi.com/bing-local-pack)
SerpApi is a paid API with a free trial of 5,000 searches.

```python
from serpapi import GoogleSearch
import json

params = {
  "api_key": "YOUR_API_KEY",
  "engine": "bing",
  "q": "sf lunch"
}

search = GoogleSearch(params)
results = search.get_dict()

print(json.dumps(results['local_results']['places'], indent=2, ensure_ascii = False))

# part of the output:
'''
[
  {
    "position": 1,
    "place_id": "YN114x2064839",
    "title": "Lucca Delicatessen",
    "rating": 4.5,
    "reviews": 64,
    "reviews_link": "https://www.tripadvisor.com/Restaurant_Review-g60713-d3859418-Reviews-Lucca_Delicatessen-San_Francisco_California.html?m=17457",
    "hours": "Closed · Opens tomorrow 9 AM",
    "addsass": "2120 Chestnut St, San Francisco",
    "phone": "(415) 921-7873",
    "links": {
      "directions": "https://www.bing.com/maps/directions?rtp=adr.~pos.37.8007698059082_-122.43840026855469_2120+Chestnut+St%2c+San+Francisco%2c+CA+94123_Lucca+Delicatessen_(415)+921-7873",
      "website": "https://www.luccadeli.com/contact"
    },
    "gps_coordinates": {
      "latitude": "37.80077",
      "longitude": "-122.4384"
    }
  }
]
'''
```

### Links
[Code in the online IDE](https://replit.com/@DimitryZub1/Bing-Scrape-Organic-Search-Results-Python-SerpApi#bs4_results/get_local_map_results.py) • [Bing Local Pack API](https://serpapi.com/bing-local-pack)

### Outro
If you want to see how to scrape something specific I didn't write about yet, or want to see something made with SerpApi, or you want to write something else, please, write me a message.

> Yours, D