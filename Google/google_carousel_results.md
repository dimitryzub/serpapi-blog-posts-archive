This blog post will show how to scrape the title, thumbnail, link, and extensions from Google Organic Carousel Results results using Python.

- <a href="#intro">Intro</a>
    - <a href="#prerequisites">Prerequisites</a>
    - <a href="#imports">Imports</a>
- <a href="#what_will_be_scraped">What will be scraped</a>
    - <a href="#process">Process</a>
- <a href="#code">Code</a>
- <a href="#links">Links</a>
- <a href="#outro">Outro</a>

<h3 id="intro">Intro</h3>

This blog post is a continuation of Google's web scraping series. Here you'll see how to scrape Google Top Carousel results using Python with `beautifulsoup`, `requests`, `lxml`, `re` libraries. An alternative API solution will be shown.

> Note: this blog post shows how to scrape specific carousel layout that you'll see in "What will be scraped" section.


<h3 id="intro">Prerequisites</h3>
```python
$ pip install requests
$ pip install lxml 
$ pip install beautifulsoup4
$ pip install google-search-results 
```

Make sure you have a basic knowledge of libraries mentioned above (*except API*), since this blog post is *not exactly a tutorial for beginners*, so **be sure** you have a basic familiarity with them.

Also, make sure you have a basic understanding of  `CSS` selectors because of  `select()`/`select_one()` `beautifulsoup` methods which accepts `CSS` selectors.  [`CSS` selectors reference](https://www.w3schools.com/cssref/css_selectors.asp).

<h3 id="imports">Imports</h3>
```python
from bs4 import BeautifulSoup
import requests, lxml, re, json
from serpapi import GoogleSearch # API solution
```

<h3 id="what_will_be_scraped">What will be scraped</h3>

![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/xz2ar03o59g3nmya5b7x.png)


<h3 id="process">Process</h3>
#### Thumbnail extraction
Let's start with hardest part, thumbnails extraction. *If you don't need thumbnails, scroll down to other extraction parts.*

![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/0rizh90hcllr4rlnorhg.png)

If you try to parse thumbnails from `g-img.img` or simply `rISBZc` `CSS` class to grab `src` attribute, you'll get a `data:image` URL, but it will be a 1x1 placeholder, instead of 120x120 image.

Thumbnails are located in the `<script>` tags, so we need to grab them somehow. But first, how on Earth do I think that thumbnails are located in the `<script>` tags?

If you're curious (*if not, skip this part*):
1. Locate image element via Dev Tools.
2. Copy `id` value. ![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/r4y93v2la4nzt16byicr.png)
3. Open page source (CTRL+U), press CTRL+F and paste `id` value to find it.

Most likely you'll see two occurrences, and the second one will be somewhere in the `<script>` tags. That's what we're looking for.
____
To scrape data from `<script>` tags we need to use `regex` and grab needed data in capture group:
```python
# grabbing every script element
all_script_tags = soup.select('script')

# quick and dirty regex
# https://regex101.com/r/NYdrL5/1/
matched_thumbnails = re.findall(r"<script nonce=\".*?\">\(\w+\(\)\{\w+\s?\w+='(.*?)';\w+\s?\w+=\['\w+'\];\w+\(\w+,\w+\);\}\)\(\);<\/script>", str(all_script_tags))
```
Then `data:image` URLs needs to decoded *in a loop*:
```python
for thumbnail in thumbnails:
    decoded_thumbnail = bytes(thumbnail, 'ascii').decode('unicode-escape')
```
_____
#### Title, link and extensions extraction
![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/3ar97qh46156j5bz0ezp.png)

To parse title, link and extensions (*lightly grayed text*) we need to iterate over `ct5Ked` `CSS` selector using `for` loop and call specific data:

```python
for result in soup.select('.ct5Ked'):
    title = result["aria-label"]  # call aria-label attribute
    link = f"https://www.google.com{result['href']}"  # call href attribute
    try:
      # sometimes it's empty because of no result in Google output
      extentions = result.select_one(".cp7THd .FozYP").text
    except: extentions = None
```

Next step is to combine thumbnail extraction and the rest of the data, because currently, it's two different `for` loops. To do that, one of the easiest functions I find is to use `zip()`:

```python
for result, thumbnail in zip(soup.select('.ct5Ked'), thumbnails):
  title = result["aria-label"]
  link = f"https://www.google.com{result['href']}"
  try:
    extentions = result.select_one(".cp7THd .FozYP").text
  except: extentions = None
  decoded_thumbnail = bytes(thumbnail, 'ascii').decode('unicode-escape')
```

___
<h3 id="code">Full code</h3>

```python
from bs4 import BeautifulSoup
import requests, lxml, re, json

headers = {
    'User-agent':
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}

params = {
  'q': 'dune actors',
  'gl': 'us',
}

def get_top_carousel():

  html = requests.get('https://www.google.com/search', headers=headers, params=params)
  soup = BeautifulSoup(html.text, 'lxml')

  carousel_name = soup.select_one('.F0gfrd+ .z4P7Tc').text
  
  # creating hash before iterating over title, link, extensions
  data = {f"{carousel_name}": []}

  all_script_tags = soup.select('script')

  thumbnails = re.findall(r"<script nonce=\"\w+\D{1,2}?\">\(\w+\(\)\{\w+\s?\w+='(.*?)';\w+\s?\w+=\['\w+'\];\w+\(\w+,\w+\);\}\)\(\);<\/script>", str(all_script_tags))

  for result, thumbnail in zip(soup.select('.ct5Ked'), thumbnails):
    title = result["aria-label"]
    link = f"https://www.google.com{result['href']}"
    try:
      extensions = result.select_one(".cp7THd .FozYP").text
    except: extensions = None
    
    decoded_thumbnail = bytes(thumbnail, 'ascii').decode('unicode-escape')
    # print(f'{title}\n{link}\n{extensions}\n{decoded_thumbnail}\n')

    data[carousel_name].append({
      'title': title,
      'link': link,
      'extentions': [extensions],
      'thumbnail': decoded_thumbnail
    })
  
  print(json.dumps(data, indent=2, ensure_ascii=False))


get_top_carousel()

--------------------
# part of the output
'''
}
  ]
    {
    "name": "Timothée Chalamet",
    "link": "https://www.google.com/search?hl=en&gl=us&q=Timoth%C3%A9e+Chalamet&stick=H4sIAAAAAAAAAONgFuLVT9c3NEzLqko2ii8xUOLSz9U3KDDKM0wr0BLKTrbST8vMyQUTVsmJxSWPGJcycgu8_HFPWGo246Q1J68xTmHkwqJOyJCLzTWvJLOkUkhQip8L1RIjEahAtll2hpFZXqHAwmWzGJWcjUx2XZp2jk1P8FkoA0Ndb4iDkiLnFCHrhswn7-wFXd__299ywsBBgkWBQYPB8JElq8P6KYwHtBgOMDI17VtxiI2Fg1GAwYpJg6mKiYOFZxGrUEhmbn5JxuGVqQrOGYk5ibmpJRPYGAHILgFT8gAAAA&sa=X&ved=2ahUKEwiMxLi-ksXzAhUAl2oFHf88AN0Q-BZ6BAgBEDQ",
    "extensions": [
      "Paul Atreides"
    ],
    "thumbnail": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBwgHBgkIBwgKCgkLDRYPDQwMDRsUFRAWIB0iIiAdHx8kKDQsJCYxJx8fLT0tMTU3Ojo6Iys/RD84QzQ5OjcBCgoKDQwNGg8PGjclHyU3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3N//AABEIAHgAeAMBIgACEQEDEQH/xAAbAAABBQEBAAAAAAAAAAAAAAAEAAIDBQYBB//Ra8hFKlUWo8h+PocKVKlU4w//Z" # the URL is much longer, I shorten it on purpose.
    }
  ]
}
'''
```

### Using [Google Direct Answer Box API](https://serpapi.com/direct-answer-box-api)

SerpApi is a paid API with a free plan. Using API is not necessary since you can code it yourself but it gives you time, which is equivalent to getting results faster.

In other words, you don't need to think about things you don't want to think about, or figuring out how things work and then maintain it over time if something crashes since everything is already done for the end-user.


```python
from serpapi import GoogleSearch
import os, json

def get_top_carousel():
    params = {
      "api_key": os.getenv("API_KEY"),
      "engine": "google",
      "q": "dune actors",
      "hl": "en"
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    for result in results['knowledge_graph']['cast']:
        print(json.dumps(result, indent=2))


get_top_carousel()

-------------
'''
# part of the output
{
  "name": "Timothée Chalamet",
  "extensions": [
    "Paul Atreides"
  ],
  "link": "https://www.google.com/search?hl=en&gl=us&q=Timoth%C3%A9e+Chalamet&stick=H4sIAAAAAAAAAONgFuLVT9c3NEzLqko2ii8xUOLSz9U3KDDKM0wr0BLKTrbST8vMyQUTVsmJxSWPGJcycgu8_HFPWGo246Q1J68xTmHkwqJOyJCLzTWvJLOkUkhQip8L1RIjEahAtll2hpFZXqHAwmWzGJWcjUx2XZp2jk1P8FkoA0Ndb4iDkiLnFCHrhswn7-wFXd__299ywsBBgkWBQYPB8JElq8P6KYwHtBgOMDI17VtxiI2Fg1GAwYpJg6mKiYOFZxGrUEhmbn5JxuGVqQrOGYk5ibmpJRPYGAHILgFT8gAAAA&sa=X&ved=2ahUKEwiMxLi-ksXzAhUAl2oFHf88AN0Q-BZ6BAgBEDQ",
  "image": "https://serpapi.com/searches/6165a3dcfa86759a4fa42ba4/images/94afec67f82aa614bb572a123ec09cf051cf10bde8e0bc8025daf21915c49798.jpeg"
}
...
'''
```


<h3 id="links">Links</h3>

[Code in the online IDE](https://replit.com/@DimitryZub1/Scrape-Google-Top-Carousel-Results-with-Python#bs4_result.py) • [Google Direct Answer Box API](https://serpapi.com/direct-answer-box-api) • [Playground](https://serpapi.com/playground?q=dune+cast&location=Austin%2C+Texas%2C+United+States&gl=us&hl=en) • [Reduce chance of being blocked while web scraping](https://dev.to/dimitryzub/how-to-reduce-chance-being-blocked-while-web-scraping-search-engines-1o46)


<h3 id="outro">Outro</h3>

If you have any questions or suggestions, or something isn't working correctly, feel free to drop a comment in the comment section or via Twitter at [@serp_api](https://twitter.com/serp_api).

Yours,
Dimitry, and the rest of SerpApi Team.