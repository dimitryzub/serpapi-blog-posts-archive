This blog post will show you how to scrape the title, link, displayed link, video thumbnail, and video duration from Brave Search Organic Video results.
___
- <a href="#brave">What is Brave Search</a>
- <a href="#intro">Intro</a>
    - <a href="#prerequisites">Prerequisites</a>
    - <a href="#imports">Imports</a>
- <a href="#what_will_be_scraped">What will be scraped</a>
    - <a href="#process">Process</a>
- <a href="#code">Code</a>
- <a href="#links">Links</a>
- <a href="#outro">Outro</a>

<h3 id="brave">What is Brave Search</h3>

For the sake of non-duplicating content, I already wrote about [what is Brave search](https://serpapi.com/blog/scrape-brave-search-organic-results-with-python/) in my first Brave blog post.

<h3 id="intro">Intro</h3>

This blog post is a continuation of the Brave Search web scraping series. Here you'll see how to scrape Organic Video Results from Brave Search using Python with `beautifulsoup`, `requests`, `lxml` libraries.

> Note: HTML layout might be changed in the future thus some of `CSS` selectors might not work. <a href="#outro"> Let me know</a> if something isn't working.

<h3 id="prerequisites">Prerequisites</h3>

```python
pip install requests
pip install lxml 
pip install beautifulsoup4
```

Make sure you have a basic knowledge of the libraries mentioned above, since this blog post is *not exactly a tutorial for beginners*, so **be sure** you have a basic familiarity with them.  I'll try my best to show in code that it's not that difficult.

Also, make sure you have a basic understanding of  `CSS` selectors because of  `select()`/`select_one()` `beautifulsoup` methods that accepts `CSS` selectors.  [`CSS` selectors reference](https://www.w3schools.com/cssref/css_selectors.asp).


<h3 id="imports">Imports</h3>

```python
from bs4 import BeautifulSoup
import requests, lxml, json
```

<h3 id="what_will_be_scraped">What will be scraped</h3>

Not only 3 video results will be scraped, but 6 instead (*if you click on the right arrow button*), which is all in this case.

![Brave Search Organic Video Results](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/8d2zjwlo8a5nqk9cg82k.png)


<h3 id="process">Process</h3>

Continuing to wander through Dune, let's scrape Organic Video results about Dune.

Code is basically identical to scraping [Brave Search News results](https://serpapi.ghost.io/blog/ghost/#/editor/post/61791d3d2ba02e003b9bc682/), except we need to add *video duration* data and remove *website source* data from the output.

As in the previous post, we need to find a container with needed data:

![Container with needed data](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/p3lciumjueci69pd73g3.png)



Which translates to this (*only `id` value is changed from `#news-carousel` to `#video-carousel`*):
```python
for video_result in soup.select('#video-carousel .card'):
    # further code..
```

After picking a container, we need to grab other elements, such as title, link, displayed link, video thumbnail and video duration with appropriate `CSS` selectors.

<img width="100%" style="width:100%" src="https://media.giphy.com/media/vIelEQ35P6Jx1toqsr/giphy.gif">

___

<h3 id="code">Code</h3>

```python
from bs4 import BeautifulSoup
import requests, lxml, json

headers = {
  'User-agent':
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}

params = {
  'q': 'dune 2021',
  'source': 'web'
}

def get_organic_video_results():

  html = requests.get('https://search.brave.com/search', headers=headers, params=params)
  soup = BeautifulSoup(html.text, 'lxml')

  data = []

  for video_result in soup.select('#video-carousel .card'):
    title = video_result.select_one('.title').text.strip()
    link = video_result['href']
    source = video_result.select_one('.anchor').text.strip()
    favicon = video_result.select_one('.favicon')['src']
    thumbnail = video_result.select_one('.img-bg')['style'].split(', ')[0].replace("background-image: url('", "").replace("')", "")
    try:
      video_duration = video_result.select_one('.duration').text.strip()
    except: video_duration = None

    data.append({
      'title': title,
      'link': link,
      'source': source,
      'favicon': favicon,
      'thumbnail': thumbnail,
      'video_duration': video_duration
    })

  print(json.dumps(data, indent=2, ensure_ascii=False))


get_organic_video_results()

---------------
'''
[
# first result
 {
    "title": "Dune | Official Main Trailer - YouTube",
    "link": "https://www.youtube.com/watch?v=8g18jFHCLXk",
    "source": "youtube.com",
    "favicon": "https://imgr.search.brave.com/_l2jz03v6ptkaRq7BbdclpMEfo0AtVjCzta7SCwUTL0/fit/32/32/ce/1/aHR0cDovL2Zhdmlj/b25zLnNlYXJjaC5i/cmF2ZS5jb20vaWNv/bnMvOTkyZTZiMWU3/YzU3Nzc5YjExYzUy/N2VhZTIxOWNlYjM5/ZGVjN2MyZDY4Nzdh/ZDYzMTYxNmI5N2Rk/Y2Q3N2FkNy93d3cu/eW91dHViZS5jb20v",
    "thumbnail": "https://imgr.search.brave.com/-Ut-yfD45SCozeHmuatVUuDNJcTB3_JBS2pRhNylInw/fit/200/200/ce/1/aHR0cHM6Ly9pLnl0/aW1nLmNvbS92aS84/ZzE4akZIQ0xYay9t/YXhyZXNkZWZhdWx0/LmpwZw",
    "duration": "03:28"
  },
# last result
  {
    "title": "Dune (2021) Future Fashion Featurette - YouTube",
    "link": "https://www.youtube.com/watch?v=0SzLFIdpmbw",
    "source": "youtube.com",
    "source_website_icon": "https://imgr.search.brave.com/_l2jz03v6ptkaRq7BbdclpMEfo0AtVjCzta7SCwUTL0/fit/32/32/ce/1/aHR0cDovL2Zhdmlj/b25zLnNlYXJjaC5i/cmF2ZS5jb20vaWNv/bnMvOTkyZTZiMWU3/YzU3Nzc5YjExYzUy/N2VhZTIxOWNlYjM5/ZGVjN2MyZDY4Nzdh/ZDYzMTYxNmI5N2Rk/Y2Q3N2FkNy93d3cu/eW91dHViZS5jb20v",
    "thumbnail": "https://imgr.search.brave.com/fA0LnkpZ-0eQi3PcH0oidTJKC0H-ULoYuAUsVcYpcaU/fit/200/200/ce/1/aHR0cHM6Ly9pLnl0/aW1nLmNvbS92aS8w/U3pMRklkcG1idy9t/YXhyZXNkZWZhdWx0/LmpwZw",
    "video_duration": "02:54"
  }
]
'''
```

<h3 id="links">Links</h3>

[Code in the online IDE](https://replit.com/@DimitryZub1/Brave-Search-Scrape-Organic-Video-Results#bs4_result.py) • [SelectorGadget](https://selectorgadget.com/)


<h3 id="outro">Outro</h3>

If you have any questions or suggestions, or something isn't working correctly, feel free to drop a comment in the comment section.

If you want to access that feature via SerpApi, upvote on the [Support Brave Search](https://serpapi.canny.io/feature-requests/p/support-brave-search) feature request, which is currently *under review*.

Yours,
Dimitry, and the rest of SerpApi Team.