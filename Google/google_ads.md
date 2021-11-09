#### There're two types of ad results that contain different layouts:
1. Google Shopping Ads
2. Google Regular Website Ads

# Logic:
1. Import libraries to work with.
2. Add [user-agent](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/User-Agent) to fake real user visit.
3. Enter a search query.
4. Get HTML response.
5. Get HTML сode.
6. Find and indicate where to scrape data.
7. Iterate over it until nothing left.

#### Google could block a request if:
* identify script as a script, e.g. [python-requests](https://github.com/psf/requests/blob/589c4547338b592b1fb77c65663d8aa6fbb7e38b/requests/utils.py#L808-L814).
* there're too many requests from one IP address.
* not acting like a human. Basically everything above.

#### There're several ways to go around blocking script from Google:
* using referer or in case of python-requests [Session Objects](https://docs.python-requests.org/en/latest/user/advanced/#session-objects).
* using [custom headers](https://docs.python-requests.org/en/master/user/quickstart/#custom-headers) -User Agents. [List](https://www.whatismybrowser.com/guides/the-latest-user-agent/edge) of user agents.
* using headless browser or browser automation frameworks, such as * [selenium](https://www.selenium.dev/documentation/en/) or [pyppeteer](https://github.com/pyppeteer/pyppeteer).
* using [proxies](https://docs.python-requests.org/en/master/user/advanced/#proxies) and rotate them.
* using CAPTCHA solving services.
* using request delays. A lot slower.

# Shopping Ads
![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/h9prxjsnnz8mucy306xq.png)

```python
import requests, lxml, urllib.parse
from bs4 import BeautifulSoup

# Adding User-agent (default user-agent from requests library is 'python-requests')
# https://github.com/psf/requests/blob/589c4547338b592b1fb77c65663d8aa6fbb7e38b/requests/utils.py#L808-L814
headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3538.102 Safari/537.36 Edge/18.19582"
}

# Search query
params = {'q': 'сoffee buy'}

# Getting HTML response
html = requests.get(f'https://www.google.com/search?q=',
                    headers=headers,
                    params=params).text

# Getting HTML code from BeautifulSoup
soup = BeautifulSoup(html, 'lxml')

# Looking for container that has all necessary data findAll() or find_all()
for container in soup.findAll('div', class_='RnJeZd top pla-unit-title'):
  # Scraping title
  title = container.text
  
  # Creating beginning of the link to join afterwards
  startOfLink = 'https://www.googleadservices.com/pagead'
  # Scraping end of the link to join afterwards
  endOfLink = container.find('a')['href']
  # Combining (joining) relative and absolute URL's (adding begining and end link)
  ad_link = urllib.parse.urljoin(startOfLink, endOfLink)

  # Printing each title and link on a new line
  print(f'{title}\n{ad_link}\n')
  
  
# Output
''' 
Jot Ultra Coffee Triple | Ultra Concentrated
https://www.googleadservices.com/aclk?sa=l&ai=DChcSEwiP0dmfvcbwAhX48OMHHYyRBuoYABABGgJ5bQ&sig=AOD64_0x-PlrWek-JFlDTSo7E9Z7YhUOjg&ctype=5&q=&ved=2ahUKEwjhr9GfvcbwAhXHQs0KHQCbCAUQww96BAgCED4&adurl=
MUD\WTR | A Healthier Coffee Alternative, 30 servings
https://www.googleadservices.com/aclk?sa=l&ai=DChcSEwiP0dmfvcbwAhX48OMHHYyRBuoYABAJGgJ5bQ&sig=AOD64_3gltZJ6kPrxic5o8yUO5cuJrHXnw&ctype=5&q=&ved=2ahUKEwjhr9GfvcbwAhXHQs0KHQCbCAUQww96BAgCEEg&adurl=
Jot Ultra Coffee Double | 2 bottles = 28 cups
https://www.googleadservices.com/aclk?sa=l&ai=DChcSEwiP0dmfvcbwAhX48OMHHYyRBuoYABAHGgJ5bQ&sig=AOD64_3hD0JWZSLr8NUgoTW5K0HMzdFvng&ctype=5&q=&ved=2ahUKEwjhr9GfvcbwAhXHQs0KHQCbCAUQww96BAgCEE4&adurl=
'''
```
Note: sometimes there will be zero results because Google didn't show ads at the script runtime. Simply run it again.

# Regular Website Ads
![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/julm8rnb3ljopljyobck.png)

```python
import requests, lxml, urllib.parse
from bs4 import BeautifulSoup

# Adding user-agent to fake real user visit
headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3538.102 Safari/537.36 Edge/18.19582"
}

# Search query
params = {'q': 'coffee buy'}

# HTML response
html = requests.get(f'https://www.google.com/search?q=',
                    headers=headers,
                    params=params).text
# HTML code from BeautifulSoup
soup = BeautifulSoup(html, 'lxml')

# Looking for container that has needed data and iterating over it 
for container in soup.findAll('span', class_='Zu0yb LWAWHf qzEoUe'):
  # Using .text since in 'span' there's no other text other than link
  ad_link = container.text
  # Printing links
  print(ad_link)

# Output
'''
https://www.coffeeam.com/
https://www.sfbaycoffee.com/
https://www.onyxcoffeelab.com/
https://www.enjoybettercoffee.com/
https://www.klatchroasting.com/
https://www.pachamamacoffee.com/
https://www.bulletproof.com/
'''
``` 

# Using Google Ad Results API
Alternatively, you can do the same thing with [Google Ad Results API](https://serpapi.com/google-ads) from SerpApi, except you don't have to think about solving CAPTCHA if you send too many requests, finding proxies, reduces the complexity of development, provides easier data manipulation, and Legal US Shield.

It's a paid API with a free trial of 5,000 searches.

Code to integrate:
```python
import os
from serpapi import GoogleSearch

params = {
  "engine": "google",
  "q": "kitchen table",
  "api_key": os.getenv("API_KEY"),
  "no_cache":"true" # add this param if it throws an error
}

search = GoogleSearch(params)
results = search.get_dict()

for ad in results['ads']: # shopping ads -> ['shopping_results']
  shopping_ad = ad['tracking_link'] # shopping ads -> ['link']
  print(shopping_ad)

# Output for regular ads
'''
https://www.google.com/aclk?sa=l&ai=DChcSEwje1bnojtHwAhWRhMgKHY0kC1oYABAPGgJxdQ&ae=2&sig=AOD64_2ZH32FlwxW1XqO9V49i2L8J5qy2A&q&adurl
https://www.google.com/aclk?sa=l&ai=DChcSEwje1bnojtHwAhWRhMgKHY0kC1oYABAMGgJxdQ&ae=2&sig=AOD64_2l1PVJAqbVmrcu8UpkGPVk-VK3UA&q&adurl
https://www.google.com/aclk?sa=l&ai=DChcSEwje1bnojtHwAhWRhMgKHY0kC1oYABAQGgJxdQ&sig=AOD64_2DDuyRZUcFi04jfneAzwnOQBuLtw&q&adurl
'''
# Output for shopping ads
'''
https://www.google.com/aclk?sa=l&ai=DChcSEwijuI27jtHwAhVA5uMHHUUWAWkYABAEGgJ5bQ&ae=2&sig=AOD64_2zCyytR6tDeB3BjdOX5sFQQKwOAA&ctype=5&q=&ved=2ahUKEwjh9oO7jtHwAhUId6wKHa8mByUQ5bgDegQIARA8&adurl=
https://www.google.com/aclk?sa=l&ai=DChcSEwijuI27jtHwAhVA5uMHHUUWAWkYABAFGgJ5bQ&ae=2&sig=AOD64_2HeGVTNF91vkSHjg-wRDtC1ouATw&ctype=5&q=&ved=2ahUKEwjh9oO7jtHwAhUId6wKHa8mByUQ5bgDegQIARBI&adurl=
https://www.google.com/aclk?sa=l&ai=DChcSEwijuI27jtHwAhVA5uMHHUUWAWkYABAGGgJ5bQ&ae=2&sig=AOD64_1n4ztvwQxiSMInwgntgY-WyVc2eQ&ctype=5&q=&ved=2ahUKEwjh9oO7jtHwAhUId6wKHa8mByUQ5bgDegQIARBY&adurl=
'''
```

You can find the full example in the online IDE [here](https://medium.com/r?url=https%3A%2F%2Freplit.com%2F%40DimitryZub1%2FScrape-Google-Ad-Results-Python-SerpApi%23serpapi_solution.py).

If you have any questions or something isn't working correctly or you want to write something else, feel free to drop a comment in the comment section or via Twitter at [@serp_api](https://twitter.com/serp_api).

Yours,
Dimitry, and the rest of SerpApi Team.