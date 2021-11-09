Contents: intro, what will be scraped, code, links, outro.

### Intro
This blog post is the сontinuation of the previous [blog post](https://dev.to/dimitryzub/scrape-youtube-search-with-python-part-1-j12) where we scraped video search, ad, channel results. This blog post will contain info about how to scrape playlists, movies and categories from YouTube search results.

### What will be scraped
Playlists results
![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/svwmu7ll51zlvq1z65v2.png)

Movie results
![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/escbnvo3favtzqocieaz.png)

Category results
![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/gpsm28cxcijwj00h9klm.png)

### Code
Playlist results
```python
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def get_video_paylist_results():
    options = Options()
    # running selenium in headless mode
    options.headless = True
    driver = webdriver.Chrome(options=options)
    driver.get('https://www.youtube.com/results?search_query=dnb playlist')

    youtube_playlist = []

    for result in driver.find_elements_by_xpath('//*[@id="contents"]/ytd-playlist-renderer'):
        playlist_title = result.find_element_by_css_selector('#video-title').text
        playlist_link = result.find_element_by_css_selector('.style-scope ytd-playlist-renderer a').get_attribute('href')
        channel_name = result.find_element_by_css_selector('#channel-name').text
        video_count = result.find_element_by_css_selector('#overlays > ytd-thumbnail-overlay-side-panel-renderer > yt-formatted-string').text

        youtube_playlist.append({
            'title': playlist_title,
            'link': playlist_link,
            'count': video_count,
            'channel': channel_name,
        })

    print(json.dumps(youtube_playlist, indent=2, ensure_ascii=False))


get_video_paylist_results()

# part of the output:
'''
[
  {
    "title": "Drum & Bass Hits Playlist - Top 100 DnB Songs of 2021",
    "link": "https://www.youtube.com/watch?v=y3Ko9pP6XAY&list=PLMmqTuUsDkRIZ1C1T2AsVz5XIxtVDfSOe",
    "count": "100",
    "channel": "Redlist - World Hits"
  }
]
'''
```


Movie results

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def get_movie_results():
    options = Options()
    # running selenium in headless mode
    options.headless = True
    driver = webdriver.Chrome(options=options)
    driver.get('https://www.youtube.com/results?search_query=mortal kombat 2021 movie')

    for result in driver.find_elements_by_xpath('//*[@id="contents"]/ytd-movie-renderer'):
        title = result.find_element_by_xpath('//*[@id="video-title"]').text
        link = result.find_element_by_xpath('//*[@id="video-title"]').get_attribute('href')
        movie_info = result.find_element_by_xpath('//*[@id="contents"]/ytd-movie-renderer/div[2]/ul[1]/li').text
        desc = result.find_element_by_xpath('//*[@id="description-text"]').text
        additional_desc = result.find_element_by_xpath('//*[@id="contents"]/ytd-movie-renderer/div[2]/ul[2]').text
        channel_name = result.find_element_by_xpath('//*[@id="text"]/a').text
        channel_link = result.find_element_by_xpath('//*[@id="text"]/a').get_attribute('href')
        print(f'{title}\n{link}\n{movie_info}\n{desc}\n{additional_desc}\n{channel_name}\n{channel_link}\n')

get_movie_results()

# output:
'''
Mortal Kombat (2021)
https://www.youtube.com/watch?v=UEd_2E67_qo
Action & Adventure • 2021 • English audio (and 8 more)
MMA fighter Cole Young, accustomed to taking a beating for money, is unaware of his heritage—or why Outworld's Emperor ...
Actors: Lewis Tan, Jessica McNamee, Josh Lawson
Director: Simon McQuoid
YouTube Movies
https://www.youtube.com/channel/UClgRkhTL3_hImCAmdLfDE4g
'''
```

Category results
```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def get_category_results():
    options = Options()
    # running selenium in headless mode
    options.headless = True
    driver = webdriver.Chrome(options=options)
    driver.get('https://www.youtube.com/results?search_query=mojang')

    for result in driver.find_elements_by_css_selector('#contents > ytd-vertical-list-renderer'):
        title = result.find_element_by_css_selector('#video-title > yt-formatted-string').text
        link = result.find_element_by_css_selector('#video-title').get_attribute('href')
        views = result.find_element_by_css_selector('#metadata-line > span:nth-child(1)').text
        date_posted = result.find_element_by_css_selector('#metadata-line > span:nth-child(2)').text
        snippet = result.find_element_by_css_selector('#dismissible > div > div.metadata-snippet-container.style-scope.ytd-video-renderer > yt-formatted-string').text
        channel_name = result.find_element_by_css_selector('.long-byline').text
        channel_link = result.find_element_by_css_selector('#text > a').get_attribute('href')
        try:
            badges = result.find_element_by_css_selector('#badges').text
        except:
            badges = None
        print(f'{title}\n{link}\n{views}\n{date_posted}\n{snippet}\n{channel_name}\n{channel_link}\n{badges}\n')

get_category_results()

# part of the output:
'''
Ask Mojang #18: More Mobs!
https://www.youtube.com/watch?v=miKrxo3uaXU
574K views
2 days ago
Matthew, Anna, and Thommy answer your questions about the glorious dirt block. Just kidding, they're here to talk about mobs!
Minecraft
https://www.youtube.com/user/TeamMojang
New
CC
'''
```

### Using [YouTube Playlist Results API](https://serpapi.com/youtube-playlist-results)
```python
from serpapi import GoogleSearch

def get_video_paylist_results():
  params = {
    "api_key": "YOUR_API_KEY",
    "engine": "youtube",
    "search_query": "dnb playlist"
  }

  search = GoogleSearch(params)
  results = search.get_dict()

  for result in results['playlist_results']:
      playlist_title = result['title']
      playlist_link = result['link']
      videos_count = result['video_count']
      playlist_videos = result['videos']
      print(f'{playlist_title}\n{playlist_link}\n{videos_count}\n{playlist_videos}')


get_video_paylist_results()

# part of the output:
'''
Drum & Bass Hits Playlist - Top 100 DnB Songs of 2021
https://www.youtube.com/watch?v=y3Ko9pP6XAY&list=PLMmqTuUsDkRIZ1C1T2AsVz5XIxtVDfSOe
100
[{'title': 'Bru-C x Bou - Streetside [Music Video]', 'link': 'https://www.youtube.com/watch?v=y3Ko9pP6XAY&list=PLMmqTuUsDkRIZ1C1T2AsVz5XIxtVDfSOe', 'length': '3:40'}, {'title': 'Wiguez & Vizzen - Love Me Better [NCS Release]', 'link': 'https://www.youtube.com/watch?v=RrmL-R-2f28&list=PLMmqTuUsDkRIZ1C1T2AsVz5XIxtVDfSOe', 'length': '2:53'}]
Best of Drum & Bass/Liquid DnB Playlist
https://www.youtube.com/watch?v=tEcggRukZCs&list=PL92k2xCT1v3l7mrk_NEndTvOMmK_621J9
296
[{'title': 'Maduk ft Veela - Ghost Assassin', 'link': 'https://www.youtube.com/watch?v=tEcggRukZCs&list=PL92k2xCT1v3l7mrk_NEndTvOMmK_621J9', 'length': '3:42'}, {'title': 'Meiko - Leave The Lights On (Krot Remix)', 'link': 'https://www.youtube.com/watch?v=uO7kCUjUaUE&list=PL92k2xCT1v3l7mrk_NEndTvOMmK_621J9', 'length': '6:46'}]
'''
```


### Using [YouTube Movie Results API](https://serpapi.com/youtube-movie-results)
```python
from serpapi import GoogleSearch

def get_movie_results():
  params = {
    "api_key": "YOUR_API_KEY",
    "engine": "youtube",
    "search_query": "mortal kombat 2021 movie"
  }

  search = GoogleSearch(params)
  results = search.get_dict()

  for result in results['movie_results']:
      title = result['title']
      link = result['link']
      channel = result['channel']
      desc = result['description']
      movie_info = result['info']
      print(f'{title}\n{link}\n{channel}\n{desc}\n{movie_info}\n')

get_movie_results()

# output:
'''
Mortal Kombat (2021)
https://www.youtube.com/watch?v=Q5s_rHFxbSA
{'name': 'YouTube Movies', 'link': 'https://www.youtube.com/channel/UClgRkhTL3_hImCAmdLfDE4g', 'verified': True}
['Action & Adventure • 2021 • R • English audio (and 8 more)', 'Actors: Lewis Tan, Jessica McNamee, Josh Lawson', 'Director: Simon McQuoid']

Mortal Kombat Legends: Scorpion's Revenge
https://www.youtube.com/watch?v=YA8h-_BMT-E
{'name': 'YouTube Movies', 'link': 'https://www.youtube.com/channel/UClgRkhTL3_hImCAmdLfDE4g', 'verified': True}
['Animation • 2020 • R • English audio (and 4 more)', 'Actor: Darren De Paul', 'Director: Ethan Spaulding']
'''
```


### Using [YouTube Category Results API](https://serpapi.com/youtube-category-results)
```python
from serpapi import GoogleSearch

def get_category_results():
    params = {
      "api_key": "YOR_API_KEY",
      "engine": "youtube",
      "search_query": "mojang"
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    for result in results['latest_from_minecraft']:
        title = result['title']
        link = result['link']
        channel = result['channel']
        published_date = result['published_date']
        views = result['views']
        extensions = result['extensions']
        print(f'{title}\n{link}\n{channel}\n{published_date}\n{views}\n{extensions}\n')


get_category_results()

# part of the output:
'''
Ask Mojang #18: More Mobs!
https://www.youtube.com/watch?v=miKrxo3uaXU
{'name': 'Minecraft', 'link': 'https://www.youtube.com/user/TeamMojang', 'verified': True, 'thumbnail': 'https://yt3.ggpht.com/KYt9rfP_fcswzs2RzvossPvKHOcP7W2gWFylRpAskW7IadpfgUgUrhttiYGtLs-P-LufgXpuc9E=s68-c-k-c0x00ffffff-no-rj'}
2 days ago
574573
['New', 'CC']
'''
```

### Links
Code in the [online IDE](https://replit.com/@DimitryZub1/Scrape-YouTube-search-playlist-movie-category#main.py) (*note: sometimes replit throws an error when using `selenium`, even after added several arguments to run inside replit. If it happens, run the code locally.*)

[YouTube Search Engine Results API](https://serpapi.com/youtube-search-api)

### Outro
If you have any questions or something isn't working correctly or you want to write something else, feel free to drop a comment in the comment section or via Twitter at [@serp_api](https://twitter.com/serp_api).

Yours,
Dimitry, and the rest of SerpApi Team.