Contents: intro, imports, what will be scraped, code, fuckit,  links, outro.

### Intro
This blog post will show how to scrape YouTube organic search, ad and channel results.

**Each section will be represented with the screenshot that will show which part is being scraped.**

I decided to use not the fastest solution `Selenium` but I wanted to scrape everything to the bottom of the search results page, which could be done by calling DOM directly like so:
```python
driver.execute_script("var scrollingElement = (document.scrollingElement || document.body);scrollingElement.scrollTop = scrollingElement.scrollHeight;")
# https://stackoverflow.com/a/57076690/15164646 (contains several references for a better understanding)
```
### Imports
```python
from selenium import webdriver
from serpapi import GoogleSearch
import json, time # this two could be skipped (prettier output/time buffer)
```
### What will be scraped

Video Search Results
![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/q34pcfdllzcuxbe3udq3.png)


### Code
```python
from selenium import webdriver
import json, time


def get_video_results():
    driver = webdriver.Chrome()
    driver.get('https://www.youtube.com/results?search_query=minecraft')

    youtube_data = []

    # scrolling to the end of the page
    # https://stackoverflow.com/a/57076690/15164646
    while True:
        # end_result = "No more results" string at the bottom of the page
        # this will be used to break out of the while loop
        end_result = driver.find_element_by_css_selector('#message').is_displayed()
        driver.execute_script("var scrollingElement = (document.scrollingElement || document.body);scrollingElement.scrollTop = scrollingElement.scrollHeight;")
        # time.sleep(1) # could be removed
        print(end_result)

        # once element is located, break out of the loop
        if end_result == True:
            break

    print('Extracting results. It might take a while...')

    for result in driver.find_elements_by_css_selector('.text-wrapper.style-scope.ytd-video-renderer'):
        title = result.find_element_by_css_selector('.title-and-badge.style-scope.ytd-video-renderer').text
        link = result.find_element_by_css_selector('.title-and-badge.style-scope.ytd-video-renderer a').get_attribute('href')
        channel_name = result.find_element_by_css_selector('.long-byline').text
        channel_link = result.find_element_by_css_selector('#text > a').get_attribute('href')
        views = result.find_element_by_css_selector('.style-scope ytd-video-meta-block').text.split('\n')[0]

        try:
            time_published = result.find_element_by_css_selector('.style-scope ytd-video-meta-block').text.split('\n')[1]
        except:
            time_published = None

        try:
            snippet = result.find_element_by_css_selector('.metadata-snippet-container').text
        except:
            snippet = None

        try:
            if result.find_element_by_css_selector('#channel-name .ytd-badge-supported-renderer') is not None:
                verified_badge = True
            else:
                verified_badge = False
        except:
            verified_badge = None

        try:
            extensions = result.find_element_by_css_selector('#badges .ytd-badge-supported-renderer').text
        except:
            extensions = None
        print(verified_badge)

        youtube_data.append({
            'title': title,
            'link': link,
            'channel': {'channel_name': channel_name, 'channel_link': channel_link},
            'views': views,
            'time_published': time_published,
            'snippet': snippet,
            'verified_badge': verified_badge,
            'extensions': extensions,
        })

    print(json.dumps(youtube_data, indent=2, ensure_ascii=False))

    driver.quit()

get_video_results()


# part of the output:
'''
[
  {
    "title": "I Survived 100 Days in Ancient Greece on Minecraft.. Here's What Happened..",
    "link": "https://www.youtube.com/watch?v=hUAjdnhpTXU",
    "channel": {
      "channel_name": "Forrestbono",
      "channel_link": "https://www.youtube.com/user/ForrestboneMC"
    },
    "views": "2.6M views",
    "time_published": "5 days ago",
    "snippet": "I had to survive for 100 Days of Hardcore Minecraft in Ancient Greece and battle Poseidon, God of the Sea, and Cronos, the God ...",
    "verified_badge": true,
    "extensions": "New"
  }
]
'''
```


### Using [YouTube Video Results API](https://serpapi.com/youtube-video-results)
SerpApi is paid API with a free plan.
```python
from serpapi import GoogleSearch

def get_video_results():
    params = {
      "api_key": "YOUR_API_KEY",
      "engine": "youtube",
      "search_query": "minecraft"
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    for results in results['video_results']:
        title = results['title']
        link = results['link']
        channel = results['channel']
        try:
            published_date = results['published_date']
        except:
            published_date = None
        try:
            views = results['views']
        except:
            views = None
        try:
            video_length = results['length']
        except:
            video_length = None
        try:
            extensions = results['extensions']
        except:
            extensions = None

        print(f'{title}\n{link}\n{channel}\n{published_date}\n{views}\n{video_length}\n{extensions}\n')

get_video_results()

# part of the output:
'''
I Spent 100 Days in Medieval Times in Minecraft... Here's What Happened
https://www.youtube.com/watch?v=hjV30hf6yEM
{'name': 'Forge Labs', 'link': 'https://www.youtube.com/user/AirsoftXX', 'verified': True, 'thumbnail': 'https://yt3.ggpht.com/ytc/AAUvwnjgpo-Pvk7jrXkd4HFErsnrLr2Nwru5f8TgtWGJ7w=s68-c-k-c0x00ffffff-no-rj'}
6 days ago
10136089
1:49:28
['New']
'''
```

### Ad results
![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/ae5gzjxrp1ms3ia637nb.png)
```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def get_video_ad_results():
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    driver.get('https://www.youtube.com/results?search_query=how to tie a tie')

    for result in driver.find_elements_by_css_selector('.style-scope ytd-search-pyv-renderer'):
        title = result.find_element_by_css_selector('#video-title').text
        channel_name = result.find_element_by_css_selector('#channel-name').text
        channel_link = result.find_element_by_css_selector('#text a').get_attribute('href')
        video_link = result.find_element_by_css_selector('#endpoint').get_attribute('href')
        views = result.find_element_by_css_selector('#metadata-line').text
        desc = result.find_element_by_css_selector('#description-text').text
        print(f'{title}\n{channel_name}\n{channel_link}{video_link}\n{views}\n{desc}\n')

get_video_ad_results()

# output:
'''
How to tie a tie EASY WAY
How to tie a tie
https://www.youtube.com/channel/UC4UuK5vs0b8HhqLDE6ssWOA
https://www.googleadservices.com/pagead/aclk?sa=L&ai=Cw7aOxrTOYIL4LdqJ9u8PgtWd-AWTucasY9mO756NDsCNtwEQASAAYKWWo4b0IoIBF2NhLXB1Yi02MjE5ODExNzQ3MDQ5MzcxoAGP3d7QA6kC1tyMLsuvYz6oAwSqBIgCT9Cnglg6NKBsd-PDBGHllhIo3j6gxAjkcwDoAkp7nHUsJEW7DGH5yhXLGFX1ZUysJkVvRncH4iJh7A9q1X-LRwJD1cSE8ZODyrNzKmP3YswA23bToV2p5yCKzb3SJJw7pZnp6HBJFQy3_bV4ZZbR5YU7txo9LNOqyCzXHB0zKe8HIRgLCYwz8_lQJwdjzYvtEfQn84kRsvGs646kym5AM7AuK7ZkzYZs68dxtuZU4EV64-8mG4_0kuyKt6GXcFHxydZSYSqQUBm5N8WBFmVYqTTX2MZs6uv7JL_T2ilO_GSvWAXSm_TeJcvwdI0zQlPNvqIF-8kBfRZzx5xLfimBFeJF4hdIS_cqkgUMCBIw4qn4ztD9_P5fkgUHCBN4qZauMKAGVYAH2aKhL5AHBKgHhAioB6jSG6gHtgeoB-DPG6gH6dQbqAeMzRuoB7HcG6gH8NkbqAekmrECqAeBxhuoB9XOG6gHq8UbqAfezhuoB5zcG5IIC1hfM3o3UW5lRk9JqAgB0ggFCIBBEAGxCXHg2OWyEZICyAkXyAmPAZgLAboLHggDEAUYBiAGKAEwBUABSABYC2AAaABwAYgBAJgBAdALE7gMAbgT____________AbAUA8AVgYCAQNAVAdgVAYAXAaAXAQ&num=1&cid=CAASFeRoSrmeG6BSAe4hx5xjr7z2wLbhwQ&sig=AOD64_2-SpesMfmcgSQlQ9oXqQ3KeRo52g&adurl=https://www.youtube.com/watch%3Fv%3DX_3z7QneFOI&ctype=21&video_id=X_3z7QneFOI&client=ca-pub-6219811747049371
43K views 
How to tie a tie quick and easy Best tutorial
'''
``` 

### Using [YouTube Ad Results API](https://serpapi.com/youtube-ad-results)
```python
from serpapi import GoogleSearch

def get_video_ad_results():
    params = {
      "api_key": "YOUR_API_KEY",
      "engine": "youtube",
      "search_query": "how to tie a tie"
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    for result in results['ads_results']:
        title = result['title']
        link = result['link']
        channel = result['channel']
        description = result['description']
        print(f'{title}\n{link}\n{channel}\n{description}\n')
        
get_video_ad_results()

# output:
'''
How to tie a tie EASY WAY
https://www.youtube.com/watch?v=X_3z7QneFOI
{'name': 'How to tie a tie', 'link': 'https://www.youtube.com/channel/UC4UuK5vs0b8HhqLDE6ssWOA'}
How to tie a tie quick and easy Best tutorial
'''
```

### Channel results
![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/qemlkckuepoofalujgwm.png)
```python
from selenium import webdriver

def get_channel_results():
    driver = webdriver.Chrome()
    driver.get('https://www.youtube.com/results?search_query=mojang')

    title = driver.find_element_by_css_selector('#info #text').text
    link = driver.find_element_by_css_selector('#main-link').get_attribute('href')
    subs = driver.find_element_by_css_selector('#subscribers').text
    video_count = driver.find_element_by_css_selector('#video-count').text
    desc = driver.find_element_by_css_selector('#description').text
    print(f'{title}\n{link}\n{subs}\n{video_count}\n{desc}')

get_channel_results()

# output:
'''
Minecraft
https://www.youtube.com/user/TeamMojang
7.4M subscribers
542 videos
This is the official YouTube channel of Minecraft. We tell stories about the Minecraft Universe. ESRB Rating: Everyone 10+ with ...
'''
```

### Using [YouTube Channel Results API](https://serpapi.com/youtube-channel-results)
```python
from serpapi import GoogleSearch

def get_channel_results():
    params = {
      "api_key": "YOUR_API_KEY",
      "engine": "youtube",
      "search_query": "mojang"
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    for result in results['channel_results']:
        title = result['title']
        link = result['link']
        verified = result['verified']
        subs = result['subscribers']
        video_count = result['video_count']
        desc = result['description']
        print(f'{title}\n{link}\n{verified}\n{subs}\n{video_count}\n{desc}\n')

get_channel_results()

# output:
'''
Minecraft
https://www.youtube.com/user/TeamMojang
True
7400000.0
542
This is the official YouTube channel of Minecraft. We tell stories about the Minecraft Universe. ESRB Rating: Everyone 10+ with ...
'''
```

### [Fuckit module](https://github.com/ajalt/fuckitpy)
If you don't like too many `try/except` blocks, then you can use context manager from [fuckit](https://github.com/ajalt/fuckitpy#as-a-context-manager) module that will continue to run, skipping the statements that cause errors.

```python
# pip install fuckit
import fuckit

with fuckit:
    title = result.find_element_by_css_selector('.title-and-badge.style-scope.ytd-video-renderer').text
    link = result.find_element_by_css_selector('.title-and-badge.style-scope.ytd-video-renderer a').get_attribute('href')
    channel_name = result.find_element_by_css_selector('.long-byline').text
    channel_link = result.find_element_by_css_selector('#text > a').get_attribute('href')
    views = result.find_element_by_css_selector('.style-scope ytd-video-meta-block').text.split('\n')[0]
    time_published = result.find_element_by_css_selector('.style-scope ytd-video-meta-block').text.split('\n')[1]
    snippet = result.find_element_by_css_selector('.metadata-snippet-container').text
    extensions = result.find_element_by_css_selector('#badges .ytd-badge-supported-renderer').text
```

### Links
Code in the [online IDE](https://replit.com/@DimitryZub1/Scrape-YouTube-Search-organic-ads-channel-results#main.py) • [YouTube Search Engine Results API](https://serpapi.com/youtube-search-api)

### Outro
You can also scrape YouTube by using `requests-html` library where you still have to render the page by calling [`html.render()`](https://docs.python-requests.org/projects/requests-html/en/latest/#javascript-support), I'm not tested how much quicker it compare to `selenium`.

`Selenium` could be also run [headless](https://www.selenium.dev/documentation/en/driver_idiosyncrasies/driver_specific_capabilities/#firefox) mode in Firefox. If the first solution didn't work for you, check out [this](https://stackoverflow.com/a/55834112/15164646) or [this](https://stackoverflow.com/a/53967684/15164646) answer from stackoverflow. Firefox webdriver [download](https://github.com/mozilla/geckodriver/releases/).

Or if you're using `selenium` with Chrome, you can do it like [so](https://stackoverflow.com/a/46929945/15164646). Chrome webdriver [download](https://github.com/ajalt/fuckitpy).

If you have any questions or something isn't working correctly or you want to write something else, feel free to drop a comment in the comment section or via Twitter at [@serp_api](https://twitter.com/serp_api).

Yours,
Dimitry, and the rest of SerpApi Team.