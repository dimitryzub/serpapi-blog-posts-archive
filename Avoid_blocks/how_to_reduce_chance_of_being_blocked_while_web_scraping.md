This blog post is about different ways to reduce the chance of being blocked while web scraping search engines or other websites with Python, Ruby code examples.

<h7 id="top">Contents</h7>:
- <a href="#methods">Methods</a>
    - <a href="#dev_toolz">Check Network Tab First</a>
    - <a href="#delays">Delays</a>
    - <a href="#user-agent">User-Agent</a>
    - <a href="#code">Code and Response examples with/without User-Agent</a>
    - <a href="#rotate-user-agents">Rotate User-Agents</a>
    - <a href="#add_headers">Additional Headers</a>
    - <a href="#ordered_headers">Ordered Headers</a>
    - <a href="#ip">IP Rate Limit</a>
    - <a href="#proxies">Proxies</a>
    - <a href="#non_overused_proxies">Non-Overused Proxies</a>
    - <a href="#whitelisted">Become Whitelisted</a>
    - <a href="#serpapi">Using SerpApi</a>
- <a href="#links">Links</a>
- <a href="#outro">Outro</a>


<h2 id="methods">Methods</h2>

- Check the network tab first to make a direct request to API/Server.
- Add delays.
- Pass `user-agent` into request headers.
- Pass additional HTTP request headers (*cookies, auth, authority, etc.*).
- Add proxies.
- Become whitelisted.
- SerpApi.

<h2 id="dev_toolz">Check Network Tab First</h2>

Before you try to make the most stealth bypass system, take a look in the Network tab under dev tools first and see if the data you want can be extracted via direct API/Server request call. This way you don't need to make things complicated.

*Note: API calls are also protected. For example, the Home Depot and Walmart block API requests without proper `headers`.*

To check it, go to the `Dev Tools -> Network -> Fetch/XHR`. On the left side you'll see a bunch of requests send from/to the server, when you click on one of those requests, on the right side you'll see the response via *preview* tab.

![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/tdrcphqtyptmn0y1cd4v.png)
![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/48wfupjfay0l7mn31lr0.png)


If some of those request have the data you want, click on it, go to *headers* tab on the right and copy URL to make a requests using Python `requests.get()` or Ruby `HTTParty.get()`.
![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/anfqt9e1is55kva1fjm9.png)

____

<h2 id="delays">Delays</h2>

Delays could do the trick sometimes, but it very depends on the use case, and it will depend on whether you should use them or not.

In Python, you can use built-in [`time.sleep`](https://docs.python.org/3/library/time.html#time.sleep) method:

```python
from time import sleep

sleep(0.05)  # 50 milliseconds of sleep
sleep(0.5)   # half a second of sleep
sleep(3)     # 3 seconds of sleep 
```

In Ruby, it's an identical process using [`sleep`](https://apidock.com/ruby/Kernel/sleep) method as well:

```ruby
# Called without an argument, sleep() will sleep forever
sleep(0.5) # half a second
sleep(4.minutes)

# or longer..
sleep(2.hours)
sleep(3.days)
```
____

<h2 id="user-agent">User-Agent</h2>

It's the most basic one and usually, for most websites, it will be enough, but `user-agent` does not guarantee that your request won't be declined or blocked.

In basic explanation, `user-agent` is needed to act as a "real" user visit, which is also known as [`user-agent` spoofing](https://developer.mozilla.org/en-US/docs/Glossary/User_agent), when bot or browser send a fake `user-agent` string to announce themselves as a different client.

The reason why request might be blocked is that, for example in Python `requests` library, default `user-agent` is [`python-requests`](https://github.com/psf/requests/blob/589c4547338b592b1fb77c65663d8aa6fbb7e38b/requests/utils.py#L808-L814) and websites understands that it's a bot and might block a request in order to protect the website from overload, *if there's a lot of requests being sent*.

`User-agent` [syntax](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/User-Agent#syntax) looks like this:
```lang-none
User-Agent: <product> / <product-version> <comment>
```

Check [what's your `user-agent`](https://www.whatismybrowser.com/detect/what-is-my-user-agent).

In Python `requests` library, you can pass `user-agent` into request [`headers`](https://docs.python-requests.org/en/master/user/quickstart/#custom-headers) as a `dict()` like so:

```python
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}

# add request headers to request
requests.get("YOUR_URL", headers=headers)
```

In Ruby with [`HTTPary`](https://github.com/jnunemaker/httparty/blob/master/examples/headers_and_user_agents.rb) gem it's identical process:

```ruby
headers = {
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}

# add request headers to request
HTTParty.get("YOUR_URL", headers:headers)
```

_____

<h2 id="code">Code and response examples with and without user-agent</h2>

Examples below will be using Python and `requests` library. This problem is *very* common on StackOverFlow.

Let's try to get data from Google Search with and without `user-agent` passed into request headers. The example below will try to get the stock price.

##### Making request without passing `user-agent` into request headers:

```python
import requests, lxml
from bs4 import BeautifulSoup

params = {
  "q": "Nasdaq composite",
  "hl": "en",
}

soup = BeautifulSoup(requests.get('https://www.google.com/search', params=params).text, 'lxml')
print(soup.select_one('[jsname=vWLAgc]').text)
```

Firstly, it will throw and `AttributeError` because the response contains different HTML with different selectors:
```lang-none
print(soup.select_one('[jsname=vWLAgc]').text)
AttributeError: 'NoneType' object has no attribute 'text'
```

Secondly, if you try to `print` `soup` object or response from `requests.get()` you'll see that it's a HTML with `<script>` tags, or HTML that contains some sort of an error.

##### Making requests with `user-agent`:

```python
import requests, lxml
from bs4 import BeautifulSoup

headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}

params = {
  "q": "Nasdaq composite",
  "hl": "en",
}

soup = BeautifulSoup(requests.get('https://www.google.com/search', headers=headers, params=params).text, 'lxml')
print(soup.select_one('[jsname=vWLAgc]').text)

# 15,363.52
```
_____

<h2 id="rotate-user-agents">Rotate User-Agents</h2>

If you are making a large number of requests for web scraping a website, it's a good idea to make each request look random by sending a different set of HTTP headers to make it look like the request is coming from different computers/different browsers.

The process:
1. Collect a list of User-Agent strings of some recent real browsers from [WhatIsMyBrowser.com](https://developers.whatismybrowser.com/useragents/explore/).
2. Put them in Python `list()` or `txt` file.
3. Make each request pick a random string from this `list()` using `random.choice()`.

```python
import requests, random

user_agent_list = [
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
]

for _ in range(len(user_agent_list)):
  #Pick a random user agent
  user_agent = random.choice(user_agent_list)

  #Set the headers 
  headers = {'User-Agent': user_agent}

requests.get('URL', headers=headers)
```

Learn more at ScrapeHero about [how to fake and rotate User Agents using Python](https://www.scrapehero.com/how-to-fake-and-rotate-user-agents-using-python-3/).

_____

<h2 id="add_headers">Additional Headers</h2>

Sometimes passing only `user-agent` isn't enough. You can pass additional headers. For example:
- [Accept](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Accept): `Accept: <MIME_type>/<MIME_subtype>; Accept: <MIME_type>/*; Accept: */*`
- [Accept-Language](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Accept-Language): `Accept-Language: <language>; Accept-Language: *`
- [Content-Type](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Type): `Content-Type: text/html; img/png`

See [more HTTP request headers](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers) that you can send while making a request.

Additionally, if you need to send authentification data, you can use [`requests.Session()`](https://2.python-requests.org/en/master/user/advanced/#session-objects):
```python
session = requests.Session()
session.auth = ('user', 'pass')
session.headers.update({'x-test': 'true'})

# both 'x-test' and 'x-test2' are sent
session.get('https://httpbin.org/headers', headers={'x-test2': 'true'})
```

Or if you need to send cookies:
```python
session = requests.Session()

response = session.get('https://httpbin.org/cookies', cookies={'from-my': 'browser'})
print(response .text)
# '{"cookies": {"from-my": "browser"}}'

response = session.get('https://httpbin.org/cookies')
print(response.text)
# '{"cookies": {}}'
```

You can view all *request/response* headers under `DevTools -> Network -> Click on the URL -> Headers`.

In [Insomnia](https://insomnia.rest/) (*right click on URL -> copy as cURL (Bash)*) you can see what HTTP request headers being sent and play around with them dynamically:
![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/xw72pvacn0gma0rklm2o.png)

It can also generate code for you (*not perfect all the time*):
![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/irvy3y6fw9wgf0lb5wgv.png)

_____

<h2 id="ordered_headers">Ordered Headers</h2>

In unusual circumstances, you may want to provide headers in an ordered manner.

To do so, you can do it like so:
```python
from collections import OrderedDict
import requests

session = requests.Session()
session.headers = OrderedDict([
    ('Connection', 'keep-alive'), 
    ('Accept-Encoding', 'gzip,deflate'),
    ('Origin', 'example.com'),
    ('User-Agent', 'Mozilla/5.0 ...'),
])

# other code ...

custom_headers = OrderedDict([('One', '1'), ('Two', '2')])
req = requests.get('https://httpbin.org/get', headers=custom_headers)
prep = session.prepare_request(req)
print(*prep.headers.items(), sep='\n')

# prints:
'''
('Connection', 'keep-alive')
('Accept-Encoding', 'gzip,deflate')
('Origin', 'example.com')
('User-Agent', 'Mozilla/5.0 ...')
('One', '1')
('Two', '2')
'''
```

Code was taken from StackOverFlow answer by [jfs](https://ru.stackoverflow.com/questions/326833/python-requests-%d0%bf%d1%80%d0%b8-%d1%83%d0%ba%d0%b0%d0%b7%d0%b0%d0%bd%d0%b8%d0%b8-%d0%b7%d0%b0%d0%b3%d0%be%d0%bb%d0%be%d0%b2%d0%ba%d0%be%d0%b2-%d0%b7%d0%b0%d0%bf%d1%80%d0%be%d1%81%d1%8b-%d0%bf%d0%be-%d1%81%d0%b5%d1%82%d0%b8-%d0%b8%d0%b4%d1%83%d1%82-%d0%b2-%d1%81%d0%bb%d1%83%d1%87%d0%b0%d0%b9%d0%bd%d0%be%d0%bc-%d0%bf%d0%be%d1%80%d1%8f%d0%b4%d0%ba/722145#722145?newreg=ece4a9a047434f67af05221d34fcfe61). Please, read his answer to get more out of it (*note: it's written in Russian.*). Learn more about [Requests Header Ordering](https://requests.kennethreitz.org/en/master/user/advanced/#header-ordering).

____

<h2 id="ip">IP Rate Limit</h2>

IP rate limits work similar to API rate limits, but there is usually no public information about them.

It's a basic security system that can ban or block incoming requests from the same IP. It means that a regular user would not made 100 requests to the same domain in a few seconds, so "they" proceed to tag (*or whatever they do*) that connection as dangerous/unusual/suspicious so we cannot know for sure how many requests we can do per X period of time safely.

Try to save HTML locally first, test everything you need there, and then start making actual requests to the website(s).

____

<h2 id="proxies">Proxies</h2>

Sometimes passing request headers isn't enough. That's when you can try to use proxies in combination with request headers.

Why proxies in the first place?
1. If you want to scrape at scale. While web scraping there's could a lot of traffic while making requests. Proxies are used to make traffic look like regular user traffic making things balanced.
2. If destination website you want to scrape only available in some countries, then you make a request from a specific geographical region or device.
3. If you want to have an ability to make concurrent sessions to the same or different websites which will reduce chances to get banned or blocked by the website(s).

Using Python to pass [`proxies`](https://2.python-requests.org/en/master/user/advanced/#proxies) into request  (*same as passing `user-agent`*):
```python
proxies = {
  'http': 'http://10.10.1.10:3128',
  'https': 'http://10.10.1.10:1080',
}

requests.get('http://example.org', proxies=proxies)
```

Using [`HTTParty` to add proxies](https://github.com/jnunemaker/httparty/blob/master/lib/httparty.rb#L93-L104) like so, or like in the code snippet shown below:
```ruby
http_proxy = {
  http_proxyaddr: "PROXY_ADDRESS",
  http_proxyport: "PROXY_PORT"
}

HTTParty.get("YOUR_URL", http_proxy:http_proxy)
```

Or using [`HTTPrb` to add proxies](https://github.com/httprb/http/wiki/Proxy-Support):
```ruby
HTTP.via("proxy-hostname.local", 8080)
  .get("http://example.com/resource")

HTTP.via("proxy-hostname.local", 8080, "username", "password")
  .get("http://example.com/resource")
```

_____

<h2 id="non_overused_proxies">Non-overused proxies</h2>

To keep things short, if possible, do not use overused proxies because:
- Public proxies are the unsafest and the most unreliable proxies.
- Shared proxies are usually the cheapest proxies, because many clients split the cost and get to use more proxies for the same price.

You **can** scrape a lot of public proxies and store them in the `list()` or save it to `.txt` file to save memory and iterate over them while making a request to see what's the results would be, and then move to different types of proxies if the result is not what you were looking for.

Learn more about other [types of proxies](https://smartproxy.com/what-is-a-proxy/types-of-proxies) and which one of them is the best for use case.

<h2 id="whitelisted">Become Whitelisted</h2>

Get whitelisted means to add IP addresses to allow lists in website which explicitly allows some identified entities to access a particular privilege, i.e. it is a list of things allowed when everything is denied by default.

One of the ways to become whitelisted is you can regularly do something useful for "them" based on scraped data which could lead to some insights.

______

<h2 id="serpapi">Using SerpApi</h2>

You can avoid all of these problems by using [SerpApi](https://serpapi.com). It's a paid API with a free plan.

The biggest difference is that it's already done for the end-user, except for the *authentification* part and you don't have to think about it either maintain it.

_____

<h2 id="links">Links</h2>

[User-Agent](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/User-Agent) • [Request Headers](https://developer.mozilla.org/en-US/docs/Glossary/Request_header) • [Response Headers](https://developer.mozilla.org/en-US/docs/Glossary/Response_header) • [List of HTTP Headers](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers) • [Types of proxies](https://smartproxy.com/what-is-a-proxy/types-of-proxies) • [Python Requests](https://docs.python-requests.org/en/master/user/quickstart/#quickstart) • [Ruby HTTParty](https://github.com/jnunemaker/httparty) • [API](https://serpapi.com/)


<h2 id="outro">Outro</h2>

If you have any questions or any suggestions, feel free to drop a comment in the comment section or via Twitter at [@serp_api](https://twitter.com/serp_api).

Yours,
Dimitry, and the rest of the SerpApi Team.