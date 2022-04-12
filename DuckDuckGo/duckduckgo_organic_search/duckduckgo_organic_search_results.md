Contents: intro, imports, what will be scraped, process, code, links, outro.

### Intro
This is the first blog post of the DuckDuckGo web scraping series. Here you'll see how to scrape Organic Search Results using Python and `requests_html` library. An alternative API solution will be shown.

In short, it's a good idea to focus not only on one place (Google) because DuckDuckGo users [get a higher conversion rate](https://neilpatel.com/blog/beyond-google-how-to-perform-seo-for-other-search-engines/) and [tend to have a lower bounce rate](https://neilpatel.com/blog/duckduckgo/).

Data from [Similarweb](https://www.similarweb.com/website/duckduckgo.com/#overview) to show that the total amount of visits on June 2021 was almost **1 billion** with a bounce rate of **14.04%**!

![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/7wqm2z1tcenebapshn2j.png)


<img width="100%" style="width:100%" src="https://media.giphy.com/media/EuHPq27pBn4OqQepal/giphy.gif">


### Imports
```python
from requests_html import HTMLSession
```

### What will be scraped
![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/722dhb7a1ovwj5dk7vw3.png)


### Process

Selecting container with all data, title, link, snippet, icon with [SelectorGadget](https://selectorgadget.com/) Chrome extension.
<img width="100%" style="width:100%" src="https://media.giphy.com/media/UE8fCnkFbSNptv1Uef/giphy.gif">

The reason why `request-html` was used instead of `beautifulsoup` is because everything comes from the `javascript` and to get the data it needs to be rendered. It could be also done with `selenium`. It's the easiest approach to get this data I found.

But, you **can** parse this data from `<script>` tag which will require a lot more time to find the right data and a lot of trial and error.

Also, an alternative way to scrape DuckDuckGo [without Selenium](https://stackoverflow.com/a/68379691/15164646).

### Code
```python
from requests_html import HTMLSession

session = HTMLSession()
response = session.get('https://duckduckgo.com/?q=fus+ro+dah&kl=us-en')
response.html.render()

for result in response.html.find('.links_deep'):
    title = result.find('.js-result-title-link', first=True).text
    link = result.find('.result__extras__url', first=True).text
    snippet = result.find('.js-result-snippet', first=True).text
    icon = f"https:{result.find('img.result__icon__img', first=True).attrs['data-src']}"
    print(f'{title}\n{link}\n{snippet}\n{icon}\n')

------------------
'''
Urban Dictionary: Fus ro dah
https://www.urbandictionary.com/define.php?term=Fus ro dah
Fus ro dah. Literally means Force, Balance, and Push. The first dragon shout you learn in The Elder Scrolls V: Skyrim. In their tongue he is known as Dovahkiin, Dragonborn, Fus ro dah.
https://external-content.duckduckgo.com/ip3/www.urbandictionary.com.ico

Fus Ro Dah - Instant Sound Effect Button | Myinstants
https://www.myinstants.com/instant/fus-ro-dah/
Instant sound effect button of Fus Ro Dah . Fus Ro Dah. From skyrim. 8,072 users favorited this sound button.
https://external-content.duckduckgo.com/ip3/www.myinstants.com.ico
...
'''
```

<img width="100%" style="width:100%" src="https://media.giphy.com/media/v85BsmyGbPYOXm5Ra0/giphy.gif">


### Using [DuckDuckGo Organic Results API](https://serpapi.com/duckduckgo-organic-results)
SerpApi is a paid API with a free plan.

The first difference that you might encounter is that you will get 30 results instead of 10. The second difference is that you don't have to render `javascript` which will lead to faster program execution. The third difference is that you immediately get access to a structured `JSON` string and don't have to figure out how to scrape certain elements.

```python
import json # for pretty output
from serpapi import GoogleSearch

params = {
  "api_key": "YOUR_API_KEY",
  "engine": "duckduckgo",
  "q": "fus ro dah",
  "kl": "us-en"
}

search = GoogleSearch(params)
results = search.get_dict()

for result in results['organic_results']:
    print(json.dumps(result, indent=2))


-------------------
'''
{
  "position": 1,
  "title": "FUS RO DAH!!! - YouTube",
  "link": "https://www.youtube.com/watch?v=Ip7QZPw04Ks",
  "snippet": "Finally found original upload of the prank footage: http://www.youtube.com/watch?v=wmM00L...(video is older but original poster)I am the original poster/crea...",
  "favicon": "https://external-content.duckduckgo.com/ip3/www.youtube.com.ico"
}
...
'''
```

<img width="100%" style="width:100%" src="https://media.giphy.com/media/X1Co4XveZlcMoU5ksl/giphy.gif">


### Links
[Code in the online IDE](https://replit.com/@DimitryZub1/DuckDuckGo-Scrape-Organic-Results-python#requests_html_result.py) • [DuckDuckGo Organic Results API](https://serpapi.com/duckduckgo-organic-results) • [Neil Patel Blog](https://neilpatel.com/) • [DuckDuckGo Instant Answer API](https://duckduckgo.com/api) • [Scrape without Selenium](https://stackoverflow.com/a/68379691/15164646)


### Outro
If you have any questions or something isn't working correctly or you want to write something else, feel free to drop a comment in the comment section or via Twitter at [@serp_api](https://twitter.com/serp_api).

Yours,
Dimitry, and the rest of SerpApi Team.