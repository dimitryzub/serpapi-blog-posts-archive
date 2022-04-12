Contents: intro, imports, what will be scraped, process, code, links, outro.

### Intro
This blog post is a continuation of Google's web scraping series.
Here you'll see examples of how you can scrape Autocomplete Suggestion using Python. An alternative API solution will be shown.

### Imports
```python
import os, requests, json
```

### What will be scraped
![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/i165f4fuo1ir2k7p5kmh.png)


### Process

All that needs to be done is to add `/complete/` and `client` parameter (`...&client=chrome...)` the search URL.
```lang-none
This URL: https://www.google.com/search?q=minecraft is better than  # no '/complete/' word in the url
Becomes this URL: http://google.com/complete/search?client=chrome&q=minecraft is better than # added '/complete/' as well as 'client' param
```

### Code
```python
import requests, json

headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}
# client param could be replaced with firefox or other browser
response = requests.get('http://google.com/complete/search?client=chrome&q=minecraft is better than', headers=headers)
for result in json.loads(response.text)[1]:
    print(result)

-----------
'''
minecraft is better than roblox
minecraft is better than fortnite
minecraft is better than terraria
minecraft is better than fortnite memes
minecraft is better than among us
minecraft is better than roblox and fortnite
minecraft is better than fortnite song
minecraft is better than fortnite reddit
'''
```

### Using [Google Autocomplete API](https://serpapi.com/google-autocomplete-api)
SerpApi is a paid API with a free trial of 5,000 searches and essentially it does the same as a code above except you can use some of the advanced autocomplete parameters such as:
* Cursor pointer which can be used to refine completion.

Example with below query `q`: `minecraft is better than` and `cp`:`8` will give completely different results as you see in the code below.
```python
import os 
from serpapi import GoogleSearch

params = {
  "engine": "google_autocomplete",
  "q": "minecraft",
  "api_key": os.getenv("API_KEY"), # environment variable 
}

search = GoogleSearch(params)
results = search.get_dict()

for result in results["suggestions"]:
  print(result['value'])

--------------
'''
default (0) "cp" param
minecraft java
minecraft 1.17
minecraft classic
minecraft mods
....

"cp" param set to 2
minecraft classic
minecraft 1.17
minecraft education edition
minecraft free
'''
```


### Links
[Code in the online IDE](https://replit.com/@DimitryZub1/Scrape-Google-Autocomplete-python-serpapi#custom_results.py) • [Google Autocomplete API](https://serpapi.com/google-autocomplete-api)

### Outro
If you have any questions or something isn't working correctly or you want to write something else, feel free to drop a comment in the comment section or via Twitter at [@serp_api](https://twitter.com/serp_api).

Yours,
Dimitry, and the rest of SerpApi Team.

<img width="100%" style="width:100%" src="https://media.giphy.com/media/8hJAgQcpkMBby/giphy.gif">