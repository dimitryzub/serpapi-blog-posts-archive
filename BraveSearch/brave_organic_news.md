This blog post will show you how to scrape title, link, displayed link, source website, thumbnail, date the news was posted from Organic News results from Brave Search.
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

For the sake of non-duplicating content, I already wrote about [what is Brave search](https://serpapi.com/blog/scrape-brave-search-organic-results-with-python/) in the previous Brave blog post.

<h3 id="intro">Intro</h3>

This blog post is a continuation of the Brave Search web scraping series. Here you'll see how to scrape Organic News Results from Brave Search using Python with `beautifulsoup`, `requests`, `lxml` libraries.

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

![What is being scraped (Brave Search News results)](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/tinq1vl4nciavuu4xczv.png)


<h3 id="process">Process</h3>
Continuing Dune adventure let's scrape news about Dune movie from the Brave search.

As usually, we need to find a container with needed data first, in order to iterate over each element afterwards:

![container with needed data](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/n6ov8s9fpg0hppnmnff3.png)

Screenshot translates to this:

```python
for news_result in soup.select('#news-carousel .card'):
    # further code..
```

After picking a container, we need to grab other elements, such as title, link, displayed link, source website, and a thumbnail with appropriate `CSS` selectors:

<img width="100%" style="width:100%" src="https://media.giphy.com/media/BJcohDYT4QWorWrYG5/giphy.gif">



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

def get_organic_news_results():

  html = requests.get('https://search.brave.com/search', headers=headers, params=params)
  soup = BeautifulSoup(html.text, 'lxml')

  data = []

  for news_result in soup.select('#news-carousel .card'):
    title = news_result.select_one('.title').text.strip()
    link = news_result['href']
    time_published = news_result.select_one('.card-footer__timestamp').text.strip()
    source = news_result.select_one('.anchor').text.strip()
    favicon = news_result.select_one('.favicon')['src']
    thumbnail = news_result.select_one('.img-bg')['style'].split(', ')[0].replace("background-image: url('", "").replace("')", "")

    data.append({
      'title': title,
      'link': link,
      'time_published': time_published,
      'source': source,
      'favicon': favicon,
      'thumbnail': thumbnail
    })

  print(json.dumps(data, indent=2, ensure_ascii=False))


get_organic_news_results()

---------------
# part of the output
'''
[
  {
    "title": "Zendaya talks potential 'Dune' sequel, what she admires about Tom ...",
    "link": "https://www.goodmorningamerica.com/culture/story/zendaya-talks-potential-dune-sequel-admires-tom-holland-80555190",
    "time_published": "17 hours ago",
    "source": "goodmorningamerica.com",
    "favicon": "https://imgr.search.brave.com/NygzuIHo7PzzX-7H4OjswMN4xwJ7u3_eEXq55_xXDog/fit/32/32/ce/1/aHR0cDovL2Zhdmlj/b25zLnNlYXJjaC5i/cmF2ZS5jb20vaWNv/bnMvZDQwMjIyNDJk/MjRjZGRmNjI4NmY2/NzUzY2I5YTkyMzIz/YTM4OTJiOTM3YjBm/NDk3OTVjNTIwOTY0/Nzg0YmUwYy93d3cu/Z29vZG1vcm5pbmdh/bWVyaWNhLmNvbS8",
    "thumbnail": "https://imgr.search.brave.com/z-Za3HgnUCgTAP8vloSHS33eC0UkjIM8JsMdngGw_Rk/fit/200/200/ce/1/aHR0cHM6Ly9zLmFi/Y25ld3MuY29tL2lt/YWdlcy9HTUEvemVu/ZGF5YS1maWxlLWd0/eS1qZWYtMjExMDEz/XzE2MzQxMzkxNzQw/MjNfaHBNYWluXzE2/eDlfOTkyLmpwZw"
  }
 ...
]
'''
```

<h3 id="links">Links</h3>

[Code in the online IDE](https://replit.com/@DimitryZub1/Brave-Search-Scrape-Organic-News-Results#bs4_result.py) • [SelectorGadget](https://selectorgadget.com/)


<h3 id="outro">Outro</h3>

If you have any questions or suggestions, or something isn't working correctly, feel free to drop a comment in the comment section.

If you want to access that feature via SerpApi, upvote on the [Support Brave Search](https://serpapi.canny.io/feature-requests/p/support-brave-search) feature request, which is currently *under review*.

Yours,
Dimitry, and the rest of SerpApi Team.