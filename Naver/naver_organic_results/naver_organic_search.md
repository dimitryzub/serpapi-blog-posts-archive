This blog post will show how to scrape website position rank, title, link, displayed link, and a snippet from Naver Organic Results using Python.

> This blog is suited for users with little web scraping experience.

If you're already familiar with my blog post writing style, then you can <a href="#what_will_be_scraped">jump to *what will be scraped* section</a> since the *Intro*, *Prerequisites*, and *Import* sections are, for the most part, boilerplate part.

___

- <a href="#naver">What is Naver Search</a>
- <a href="#intro">Intro</a>
    - <a href="#prerequisites">Prerequisites</a>
    - <a href="#imports">Imports</a>
- <a href="#what_will_be_scraped">What will be scraped</a>
    - <a href="#process">Process</a>
- <a href="#code">Code</a>
- <a href="#links">Links</a>
- <a href="#outro">Outro</a>


<h2 id="naver">What is Naver Search</h2>

I already answered this in my first blog about scraping [Naver News results](http://), there you can find information about what Naver Search is.

<h3 id="intro">Intro</h3>

This blog post is a continuation of the Naver web scraping series. Here you'll see how to scrape Naver Organic Results with Python using `beautifulsoup`, `requests`, `lxml` libraries.

> Note: This blog post shows how to extract data that is being shown on the <a href="#what_will_be_scraped">screenshot</a>, and don't cover different layout handling (unless said otherwise).

<h3 id="prerequisites">Prerequisites</h3>

```python
pip install requests
pip install lxml 
pip install beautifulsoup4
```

Make sure to have a basic knowledge of Python, have a basic idea of the libraries mentioned above (*except API*), and have a basic understanding of  `CSS` selectors because you'll see mostly usage of `select()`/`select_one()` `beautifulsoup` methods that accept `CSS` selectors.  [`CSS` selectors reference](https://www.w3schools.com/cssref/css_selectors.asp) for a better understanding, or train on a few examples via [CSS Diner](https://flukeout.github.io/).

Usually, I'm using the [SelectorGadget](https://selectorgadget.com/) extension to grab `CSS` selectors by clicking on the desired element in the browser.

However, if SelectorGadget can't get the desired element, I use the Elements tab via Dev Tools (*F12 on a keyboard*) to locate and grab `CSS` selector(s) or other HTML elements, either by `.class` or `#id` or both, or by `.class`/`#id` and `attribute` `.class[attribute=attribute_name]`.

To test if the selector extracts correct data you can place those `CSS` selector(s) in SelectorGadget window, or via Dev Tools Console tab using [`$$(".CSS_SELECTOR(s)")`](https://developer.chrome.com/docs/devtools/console/utilities/#querySelectorAll-function) which is equivalent to [`document.querySelectorAll()`](https://developer.mozilla.org/en-US/docs/Web/API/Document/querySelectorAll) to see if the correct elements are selected.

<h3 id="imports">Imports</h3>

```python
import requests, lxml
from bs4 import BeautifulSoup
```

<h3 id="what_will_be_scraped">What will be scraped</h3>

![What will be scraped from Naver Organic Results](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/c5nu4lm6czznndpkq6gf.png)

___

<h3 id="process">Process</h3>

If you don't need an explanation, jump to the <a href="#code">code section</a>.

We need to take three steps to make:
1. Save HTML locally to test everything before making a lot of direct requests.
2. Pick `CSS` selectors for all the needed data.
3. Extract the data.

#### Save HTML to test the parser locally

Saving HTML locally prevents blocking or banning IP address, especially when a bunch of requests needs to be made to the same website in order to test the code.

A normal user won't do 100+ requests in a very short period of time, and don't do the same thing over and over again (*pattern*) as scripts do, so websites might tag this behavior as unusual and block IP address for some period (*might be written in the response: `requests.get("URL").text`*) or ban permanently.

```python
import requests

headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}

params = {
    "query": "bruce lee",
    "where": "web"        # theres's also a "nexearch" param that will produce different results
}

def save_naver_organic_results():
    html = requests.get("https://search.naver.com/search.naver", params=params, headers=headers).text

    # replacing every space to underline (_) so bruce lee will become bruce_lee 
    query = params['query'].replace(" ", "_")

    with open(f"{query}_naver_organic_results.html", mode="w") as file:
        file.write(html)
```

#### Now, what's happening here

##### Import `requests` library

```python
import requests
```

#### Add [`user-agent`](https://developer.mozilla.org/en-US/docs/Glossary/User_agent) and [query parameters](https://docs.python-requests.org/en/master/user/quickstart/#passing-parameters-in-urls)

```python
headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}

# query parameters
params = {
    "query": "bruce lee",
    "where": "web"
}
```

I tend to pass query parameters to `requests.get(params=params)` instead of leaving them in the URL. I find it more readable, for example, let's look at the exact same URL:

```python
params = {
    "where": "web",
    "sm": "top_hty",
    "fbm": "1",
    "ie": "utf8",
    "query": "bruce+lee"
}
requests.get("https://search.naver.com/search.naver", params=params)

# VS 

requests.get("https://search.naver.com/search.naver?where=web&sm=top_hty&fbm=1&ie=utf8&query=bruce+lee")  # Press F.
```

What about `user-agent`, it's needed to act as a "real" user visit otherwise the request might be denied. You can read more about in my other blog post about [how to reduce the chance of being blocked while web scraping search engines](https://serpapi.com/blog/how-to-reduce-chance-of-being-blocked-while-web-scraping-search-engines/).

____

### Pick and test `CSS` selectors

Selecting container (`CSS` selector that wraps all needed data), title, link, displayed link, and a snippet.

![gif](https://media.giphy.com/media/v3QEncXnG2YSHLPm5O/giphy.gif)

The GIF above translates to this code snippet:

```python
for result in soup.select(".total_wrap"):
    title = result.select_one(".total_tit").text.strip()
    link = result.select_one(".total_tit .link_tit")["href"]
    displayed_link = result.select_one(".total_source").text.strip()
    snippet = result.select_one(".dsc_txt").text
```

____

### Extract data

```python
import lxml, json
from bs4 import BeautifulSoup


def extract_local_html_naver_organic_results():
    with open("bruce_lee_naver_organic_results.html", mode="r") as html_file:
        html = html_file.read()
        soup = BeautifulSoup(html, "lxml")

        data = []

        for index, result in enumerate(soup.select(".total_wrap")):
            title = result.select_one(".total_tit").text.strip()
            link = result.select_one(".total_tit .link_tit")["href"]
            displayed_link = result.select_one(".total_source").text.strip()
            snippet = result.select_one(".dsc_txt").text

            data.append({
                "position": index + 1, # starts from 1, not from 0
                "title": title,
                "link": link,
                "displayed_link": displayed_link,
                "snippet": snippet
            })

        print(json.dumps(data, indent=2, ensure_ascii=False))
```

#### Now let's break down the extraction part

##### Import `bs4`, `lxml`, `json` libraries

```python
import lxml, json
from bs4 import BeautifulSoup
```

##### Open saved HTML file, read it and pass it to `BeautifulSoup()` object and assign `lxml` as an HTML parser

```python
with open("bruce_lee_naver_organic_results.html", mode="r") as html_file:
    html = html_file.read()
    soup = BeautifulSoup(html, "lxml")
```

##### Create temporary `list()` to store extracted data

```python
data = []
```

##### Iterate and append as a [dictionary](https://www.w3schools.com/python/python_dictionaries.asp) to temporary `list()`

Since we also need to get an index (*rank position*), we can use  [`enumerate()`](https://docs.python.org/3/library/functions.html#enumerate) method which adds a counter to an iterable and returns it. [More examples](https://www.programiz.com/python-programming/methods/built-in/enumerate).

Example:

```python
grocery = ["bread", "milk", "butter"]  # iterable

for index, item in enumerate(grocery):
  print(f"{index} {item}\n")
  
'''
0 bread
1 milk
2 butter
'''
```


Actual code:

```python
# in our case iterable is soup.select() since it returns an iterable as well
for index, result in enumerate(soup.select(".total_wrap")):
    title = result.select_one(".total_tit").text.strip()
    link = result.select_one(".total_tit .link_tit")["href"]
    displayed_link = result.select_one(".total_source").text.strip()
    snippet = result.select_one(".dsc_txt").text

    data.append({
        "position": index + 1,  # starts from 1, not from 0
        "title": title,
        "link": link,
        "displayed_link": displayed_link,
        "snippet": snippet
    })
```

___
<h3 id="code">Full Code</h3>

Now when combining all functions together, we'll get four (4) functions:

- The first function saves HTML locally.
- The second function opens local HTML and calls a parser function.
- The third function makes an actual request and calls a parser function.
- The fourth function is a parser that's being called by the second and third functions.

> Note: first and second fucntion could be skipped if you don't really want to do that but take in mind possible consequences that was <a href="#process">mentioned above</a>.

```python
import requests
import lxml, json
from bs4 import BeautifulSoup

headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}

params = {
    "query": "bruce lee",  # search query
    "where": "web"         # nexearch will produce different results
}


# function that saves HTML locally
def save_naver_organic_results():
    html = requests.get("https://search.naver.com/search.naver", params=params, headers=headers).text

    # replacing every spaces so bruce lee will become bruce_lee 
    query = params['query'].replace(" ", "_")

    with open(f"{query}_naver_organic_results.html", mode="w") as file:
        file.write(html)


# fucntion that opens local HTML and calls a parser function
def extract_naver_organic_results_from_html():
    with open("bruce_lee_naver_organic_results.html", mode="r") as html_file:
        html = html_file.read()

        # calls naver_organic_results_parser() function to parse the page
        data = naver_organic_results_parser(html)

        print(json.dumps(data, indent=2, ensure_ascii=False))


# function that make an actual request and calls a parser function
def extract_naver_organic_results_from_url():
    html = requests.get("https://search.naver.com/search.naver", params=params, headers=headers)

    # calls naver_organic_results_parser() function to parse the page
    data = naver_organic_results_parser(html)

    print(json.dumps(data, indent=2, ensure_ascii=False))


# parser that's being called by 2-3 functions
def naver_organic_results_parser(html):
    soup = BeautifulSoup(html.text, "lxml")

    data = []

    for index, result in enumerate(soup.select(".total_wrap")):
        title = result.select_one(".total_tit").text.strip()
        link = result.select_one(".total_tit .link_tit")["href"]
        displayed_link = result.select_one(".total_source").text.strip()
        snippet = result.select_one(".dsc_txt").text

        data.append({
            "position": index + 1, # starts from 1, not from 0
            "title": title,
            "link": link,
            "displayed_link": displayed_link,
            "snippet": snippet
        })

    return data
```

___

### Using [Naver Web Organic Results API](https://serpapi.com/naver-web-organic-results)

Alternatively, you can achieve the same results by using SerpApi. [SerpApi](https://serpapi.com/) is a paid API with a free plan.

The difference is that there's no need to create the parser from scratch, trying to pick the correct `CSS` selectors and don't get pissed off when certain selectors don't work as you expected, plus there's no need to maintain the parser over time if something in the HTML will be changed and on the next run the script will blow up with an error 💥

Additionally, there's no need to bypass blocks from Google (*or other search engines*), understanding how to scale requests volume because it's already happening under the hood for the end-users with appropriate plans. Have a try in the [playground](https://serpapi.com/playground?q=fus%20ro%20dah).

Install SerpApi library
```
pip install google-search-results
```

Example code to integrate:

```python
from serpapi import GoogleSearch
import os, json


def serpapi_get_naver_organic_results():
    params = {
        "api_key": os.getenv("API_KEY"),
        "engine": "naver",     # search engine (Google, Bing, DuckDuckGo..)
        "query": "Bruce Lee",  # search query
        "where": "web"
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    data = []

    for result in results["organic_results"]:

        data.append({
            "position": result["position"],
            "title": result["title"],
            "link": result["link"],
            "displayed_link": result["displayed_link"],
            "snippet": result["snippet"]
        })

    print(json.dumps(data, indent=2, ensure_ascii=False))
```

#### Let's see what is happening here

##### Import `serpapi`, [`os`](https://docs.python.org/3/library/os.html), `json` libraries

```python
from serpapi import GoogleSearch
import os, json
```

##### Pass search parameters as a dictionary

```python
params = {
    "api_key": os.getenv("API_KEY"),
    "engine": "naver",                # search engine (Google, Bing, DuckDuckGo..)
    "query": "Bruce Lee",             # search query
    "where": "web"                    # filter to extract data from organic results
}
```

##### Data extraction
This is happening under the hood so you don't have to think about these two lines of code.

```python
search = GoogleSearch(params) # data extraction
results = search.get_dict()   # structured JSON which is being called later
```

##### Create a `list()` to temporary store the data

```python
data = []
```

##### Iterate and `append()` extracted data to a `list()` as a dictionary

```python
for result in results["organic_results"]:

    data.append({
        "position": result["position"],
        "title": result["title"],
        "link": result["link"],
        "displayed_link": result["displayed_link"],
        "snippet": result["snippet"]
    })
```

##### Print added data

```python
print(json.dumps(data, indent=2, ensure_ascii=False))
    
    
# ----------------
# part of the output
'''
[
  {
    "position": 1,
    "title": "Bruce Lee",
    "link": "https://brucelee.com/",
    "displayed_link": "brucelee.com",
    "snippet": "New Podcast Episode: #402 Flowing with Dustin Nguyen Watch + Listen to Episode “Your inspiration continues to guide us toward our personal liberation.” - Bruce Lee - More Podcast Episodes HBO Announces Order For Season 3 of Warrior! WARRIOR Seasons 1 & 2 Streaming Now on HBO & HBO Max “Warrior is still the best show you’re"
  }
  # other results..
]
'''
```

If you need more information about the plans, it was explained earlier by SerpApi team member Justin O'Hara in his [breakdown of SerpApi’s subscriptions](https://medium.com/serpapi/breakdown-of-serpapis-subscriptions-39213e52a952) blog post (*information is the same except you don't have to login to the SerpApi website*).

___

<h3 id="links">Links</h3>

- [Code in the Online IDE (Replit)](https://replit.com/@DimitryZub1/Scrape-Naver-Organic-Results#main.py)
- [Naver Web Organic Results API](https://serpapi.com/naver-web-organic-results)
- [SelectorGadget](https://selectorgadget.com/)
- [`CSS` Dinner](https://flukeout.github.io/)
- [`CSS` Selectors Reference](https://www.w3schools.com/cssref/css_selectors.asp)


<h3 id="outro">Outro</h3>

If you have anything to share, any questions, suggestions, or something that isn't working correctly, feel free to drop a comment in the comment section or via Twitter at [@dimitryzub](https://twitter.com/DimitryZub), or [@serp_api](https://twitter.com/serp_api).

Yours,
Dimitry, and the rest of SerpApi Team.

___

<p style="text-align: center;">Join us on <a href="https://www.reddit.com/r/SerpApi/">Reddit</a> | <a href="https://twitter.com/serp_api">Twitter</a> | <a href="https://www.youtube.com/channel/UCUgIHlYBOD3yA3yDIRhg_mg">YouTube</a> </p>