- <a href="#what_will_be_scraped">What will be scraped</a>
- <a href="#prerequisites">Prerequisites</a>
    - <a href="#ticker_data">Scraping Google Finance Ticker Quote Data</a>
        - <a href="#ticker_data_explanation">Explanation on Extracting Ticker Data</a>
    - <a href="#scrape_multiple_tickers">Scrape Multiple Google Finance Tickers Quotes</a>
    - <a href="#timeseries_data">Extract Google Finance Chart Time-Series Data</a>
        - <a href="#timeseries_code">Scraping Google Finance Time-Series Data</a>
        - <a href="#timeseries_data_explanation">Explanation on Time-Series Extraction Code</a>
        - <a href="#nasdaq_rates">NASDAQ Rate Limits</a>
        - <a href="#nasdaq_resources">Additional Nasdaq API Resources</a>
- <a href="#links">Links</a>
- <a href="#outro">Outro</a>


<h2 id="what_will_be_scraped">What will be scraped</h2>

![image](https://user-images.githubusercontent.com/78694043/162904436-ba92fd3a-9e99-41b7-9487-6867de4b0bb6.png)

<h2 id="prerequisites">Prerequisites</h2>

**Basic knowledge scraping with CSS selectors**

CSS selectors declare which part of the markup a style applies to thus allowing to extract data from matching tags and attributes.

If you haven't scraped with CSS selectors, there's a dedicated blog post of mine
about [how to use CSS selectors when web-scraping](https://serpapi.com/blog/web-scraping-with-css-selectors-using-python/) that covers what it is, pros and cons, and why they matter from a web-scraping perspective.

**Separate virtual environment**

In short, it's a thing that creates an independent set of installed libraries including different Python versions that can coexist with each other in the same system thus preventing libraries or Python version conflicts.

If you didn't work with a virtual environment before, have a look at the
dedicated [Python virtual environments tutorial using Virtualenv and Poetry](https://serpapi.com/blog/python-virtual-environments-using-virtualenv-and-poetry/) blog post of mine to get a little bit more familiar.


📌Note: this is not a strict requirement for this blog post.

**Install libraries**:

```lang-none
pip install requests parsel
```

**Reduce the chance of being blocked**

There's a chance that a request might be blocked. Have a look
at [how to reduce the chance of being blocked while web-scraping](https://serpapi.com/blog/how-to-reduce-chance-of-being-blocked-while-web/), there are eleven methods to bypass blocks from most websites.

___

<h2 id="ticker_data">Scraping Google Finance Ticker Quote Data</h2>

```python
def scrape_google_finance(ticker: str):
    params = {
        "hl": "en" # language
        }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36",
        }

    html = requests.get(f"https://www.google.com/finance/quote/{ticker}", params=params, headers=headers, timeout=30)
    selector = Selector(text=html.text)
    
    # where all extracted data will be temporary located
    ticker_data = {
        "ticker_data": {},
        "about_panel": {},
        "news": {"items": []},
        "finance_perfomance": {"table": []}, 
        "people_also_search_for": {"items": []},
        "interested_in": {"items": []}
    }
    
    # current price, quote, title extraction
    ticker_data["ticker_data"]["current_price"] = selector.css(".AHmHk .fxKbKc::text").get()
    ticker_data["ticker_data"]["quote"] = selector.css(".PdOqHc::text").get().replace(" • ",":")
    ticker_data["ticker_data"]["title"] = selector.css(".zzDege::text").get()
    
    # about panel extraction
    about_panel_keys = selector.css(".gyFHrc .mfs7Fc::text").getall()
    about_panel_values = selector.css(".gyFHrc .P6K39c").xpath("normalize-space()").getall()
    
    for key, value in zip_longest(about_panel_keys, about_panel_values):
        key_value = key.lower().replace(" ", "_")
        ticker_data["about_panel"][key_value] = value
    
    # description "about" extraction
    ticker_data["about_panel"]["description"] = selector.css(".bLLb2d::text").get()
    ticker_data["about_panel"]["extensions"] = selector.css(".w2tnNd::text").getall()
    
    # news extarction
    if selector.css(".yY3Lee").get():
        for index, news in enumerate(selector.css(".yY3Lee"), start=1):
            ticker_data["news"]["items"].append({
                "position": index,
                "title": news.css(".Yfwt5::text").get(),
                "link": news.css(".z4rs2b a::attr(href)").get(),
                "source": news.css(".sfyJob::text").get(),
                "published": news.css(".Adak::text").get(),
                "thumbnail": news.css("img.Z4idke::attr(src)").get()
            })
    else: 
        ticker_data["news"]["error"] = f"No news result from a {ticker}."

    # finance perfomance table
    if selector.css(".slpEwd .roXhBd").get():
        fin_perf_col_2 = selector.css(".PFjsMe+ .yNnsfe::text").get()           # e.g. Dec 2021
        fin_perf_col_3 = selector.css(".PFjsMe~ .yNnsfe+ .yNnsfe::text").get()  # e.g. Year/year change
        
        for fin_perf in selector.css(".slpEwd .roXhBd"):
            if fin_perf.css(".J9Jhg::text , .jU4VAc::text").get():
                perf_key = fin_perf.css(".J9Jhg::text , .jU4VAc::text").get()   # e.g. Revenue, Net Income, Operating Income..
                perf_value_col_1 = fin_perf.css(".QXDnM::text").get()           # 60.3B, 26.40%..   
                perf_value_col_2 = fin_perf.css(".gEUVJe .JwB6zf::text").get()  # 2.39%, -21.22%..
                
                ticker_data["finance_perfomance"]["table"].append({
                    perf_key: {
                        fin_perf_col_2: perf_value_col_1,
                        fin_perf_col_3: perf_value_col_2
                    }
                })
    else:
        ticker_data["finance_perfomance"]["error"] = f"No 'finence perfomance table' for {ticker}."
    
    # "you may be interested in" results
    if selector.css(".HDXgAf .tOzDHb").get():
        for index, other_interests in enumerate(selector.css(".HDXgAf .tOzDHb"), start=1):
            ticker_data["interested_in"]["items"].append(discover_more_tickers(index, other_interests))
    else:
        ticker_data["interested_in"]["error"] = f"No 'you may be interested in` results for {ticker}"
    
    
    # "people also search for" results
    if selector.css(".HDXgAf+ div .tOzDHb").get():
        for index, other_tickers in enumerate(selector.css(".HDXgAf+ div .tOzDHb"), start=1):
            ticker_data["people_also_search_for"]["items"].append(discover_more_tickers(index, other_tickers))
    else:
        ticker_data["people_also_search_for"]["error"] = f"No 'people_also_search_for` in results for {ticker}"
        

    return ticker_data


def discover_more_tickers(index: int, other_data: str):
    """
    if price_change_formatted will start complaining,
    check beforehand for None values with try/except and set it to 0, in this function.
    
    however, re.search(r"\d{1}%|\d{1,10}\.\d{1,2}%" should make the job done.
    """
    return {
            "position": index,
            "ticker": other_data.css(".COaKTb::text").get(),
            "ticker_link": f'https://www.google.com/finance{other_data.attrib["href"].replace("./", "/")}',
            "title": other_data.css(".RwFyvf::text").get(),
            "price": other_data.css(".YMlKec::text").get(),
            "price_change": other_data.css("[jsname=Fe7oBc]::attr(aria-label)").get(),
            # https://regex101.com/r/BOFBlt/1
            # Up by 100.99% -> 100.99%
            "price_change_formatted": re.search(r"\d{1}%|\d{1,10}\.\d{1,2}%", other_data.css("[jsname=Fe7oBc]::attr(aria-label)").get()).group()
        }


scrape_google_finance(ticker="GOOGL:NASDAQ")
```

<h3 id="ticker_data_explanation">Explanation on Extracting Ticker Data</h3>

Import libraries:

```python
import requests, json, re
from parsel import Selector
from itertools import zip_longest # https://docs.python.org/3/library/itertools.html#itertools.zip_longest
```

| Library       | Purpose                                                            |
|---------------|--------------------------------------------------------------------|
| `requests`    | to make a request to the website.                                  |
| `json`        | to convert extracted data to a JSON object.                        |
| `re`          | to extract parts of the data via regular expression.               |
| `parsel`      | to parse data from HTML/XML documents. Similar to `BeautifulSoup`. |
| `zip_longest` | to iterate over several iterables in parallel. More on that below. |



Define a function:

```python
def scrape_google_finance(ticker: str): # ticker should be a string
    # further code...

scrape_google_finance(ticker="GOOGL:NASDAQ")
```

Create request headers and URL parameters:

```python
# https://docs.python-requests.org/en/master/user/quickstart/#passing-parameters-in-urls
params = {
    "hl": "en" # language
}

# https://docs.python-requests.org/en/master/user/quickstart/#custom-headers
# https://www.whatismybrowser.com/detect/what-is-my-user-agent
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36",
}
```

| Library                                                                      | Purpose                                           |
|------------------------------------------------------------------------------|---------------------------------------------------|
| [`params` ](https://docs.python-requests.org/en/master/user/quickstart/#passing-parameters-in-urls)                                                                      |a prettier way of passing URL parameters to a request. |
| [`user-agent`](https://developer.mozilla.org/en-US/docs/Glossary/User_agent) | to act as a "real" user request from the browser by passing it to [request headers](https://docs.python-requests.org/en/master/user/quickstart/#custom-headers). [Check what's your `user-agent`](https://www.whatismybrowser.com/detect/what-is-my-user-agent). |


Pass requests parameters and request headers, make a request and pass response to `parsel`: 

```python
html = requests.get(f"https://www.google.com/finance/quote/{ticker}", params=params, headers=headers, timeout=30)
selector = Selector(text=html.text)
```

|Code|Explanation|
|----|-----------|
|`f"https://www.google.com/finance/quote/{ticker}"`|is a [f-string](https://docs.python.org/3/tutorial/inputoutput.html#fancier-output-formatting) where `{ticker}` will be replaced by actual ticker string e.g. `"GOOGL:NASDAQ"`.|
|[`timeout=30`](https://docs.python-requests.org/en/master/user/quickstart/#timeouts)| to stop waiting for response after 30 secods.|
|`Selector(text=html.text)`|where passed HTML from the response will be processed by `parsel`.|

Create an empty dictionary structure where all the data will be filled in:

```python
# where all extracted data will be temporarily located
ticker_data = {
    "ticker_data": {},
    "about_panel": {},
    "news": {"items": []},
    "finance_perfomance": {"table": []}, 
    "people_also_search_for": {"items": []},
    "interested_in": {"items": []}
}
```

Extarcting current price, quote and title data:

```python
# current price, quote, title extraction
ticker_data["ticker_data"]["current_price"] = selector.css(".AHmHk .fxKbKc::text").get()
ticker_data["ticker_data"]["quote"] = selector.css(".PdOqHc::text").get().replace(" • ",":")
ticker_data["ticker_data"]["title"] = selector.css(".zzDege::text").get()
```

|Code|Explanation|
|----|-----------|
|`ticker_data["ticker_data"]["current_price"]`|accesses `["ticker_data"]` key and creates a new key `["current_price"]` and assigns it to whatever value would be extracted by `parsel`. Same for new `["quote"]` and `["title"]` keys.|
|`::text`|is a [`parsel` own pseudo-element support](https://github.com/scrapy/parsel/blob/90397dcd0b2c1cbb91e44f65c50f9e11628ba028/parsel/csstranslator.py#L48-L51) [which will translate every CSS query to XPath](https://github.com/scrapy/parsel/blob/90397dcd0b2c1cbb91e44f65c50f9e11628ba028/parsel/selector.py#L351-L363). In this case `::text` would become `/text()`.|
|`get()`|[to get actual data](https://github.com/scrapy/parsel/blob/90397dcd0b2c1cbb91e44f65c50f9e11628ba028/parsel/selector.py#L197-L204).|
|`replace(" • ",":")`|[to replace someting old with something new](https://docs.python.org/3/library/stdtypes.html#str.replace).|

Extracting right panel data:

```python
about_panel_keys = selector.css(".gyFHrc .mfs7Fc::text").getall()
about_panel_values = selector.css(".gyFHrc .P6K39c").xpath("normalize-space()").getall()

for key, value in zip_longest(about_panel_keys, about_panel_values):
    key_value = key.lower().replace(" ", "_")
    ticker_data["about_panel"][key_value] = value
```

|Code|Explanation|
|----|-----------|
|`getall()`|[to get all a `list` of matches](https://github.com/scrapy/parsel/blob/90397dcd0b2c1cbb91e44f65c50f9e11628ba028/parsel/selector.py#L180-L185).|
|`xpath("normalize-space()")`|[to get blank text nodes as well](https://github.com/scrapy/parsel/issues/62#issuecomment-1042309376). By default, blank text nodes will be skippet resulting not a complete output.|
|`lower()`|[to lowercase all string characters](https://docs.python.org/3/library/stdtypes.html#str.lower).|
|`zip_longest()`|[to combine multiple iterators](https://docs.python.org/3/library/itertools.html#itertools.zip_longest). Difference between [`zip()`](https://docs.python.org/3/library/functions.html#zip) and `zip_longest()` is that `zip()` ends at the shortest iterator while [`zip_longest()` iterates up to the length of the longest iterator](https://stackoverflow.com/questions/59119751/zip-and-zip-longest).|
|`[key_value]`|will dynamically add a key to a dictionary with it's own, extracted value.|

Extracting description and extensions data from the right panel:

```python
# description "about" and  extensions extraction
ticker_data["about_panel"]["description"] = selector.css(".bLLb2d::text").get()
ticker_data["about_panel"]["extensions"] = selector.css(".w2tnNd::text").getall()
```

Extracting news results:

```python
# news extarction
if selector.css(".yY3Lee").get():
    for index, news in enumerate(selector.css(".yY3Lee"), start=1):
        ticker_data["news"]["items"].append({
            "position": index,
            "title": news.css(".Yfwt5::text").get(),
            "link": news.css(".z4rs2b a::attr(href)").get(),
            "source": news.css(".sfyJob::text").get(),
            "published": news.css(".Adak::text").get(),
            "thumbnail": news.css("img.Z4idke::attr(src)").get()
        })
else: 
    ticker_data["news"]["error"] = f"No news result from a {ticker}."
```

|Code|Explanation|
|----|-----------|
|`if selector.css(".yY3Lee").get()`|to check if news results is present. No need to check `if <element> is not None`.|
|[`enumerate()`](https://docs.python.org/3/library/functions.html#enumerate)|[to add a counter to an iterable and return it](https://www.programiz.com/python-programming/methods/built-in/enumerate). `start=1` will start counting from 1, instead from the default value of 0.|
|`ticker_data["news"].append({})`|to [`append`](https://docs.python.org/3/tutorial/datastructures.html) extracted data to a `list` as dictionary.|
|`::attr(src)`|is also a `parsel` pseudo-element support to get `src` attribute from the node. Equivalent to XPath `/@src`.|
|`ticker_data["news"]["error"]`|to create a new `"error"` key and a message when the error occurs.|

Extracting Financial Perfomance table data:

```python
# finance perfomance table
# checks if finance table exists
if selector.css(".slpEwd .roXhBd").get():
    fin_perf_col_2 = selector.css(".PFjsMe+ .yNnsfe::text").get()           # e.g. Dec 2021
    fin_perf_col_3 = selector.css(".PFjsMe~ .yNnsfe+ .yNnsfe::text").get()  # e.g. Year/year change
    
    for fin_perf in selector.css(".slpEwd .roXhBd"):
        if fin_perf.css(".J9Jhg::text , .jU4VAc::text").get():
            
            """
            if fin_perf.css().get() statement is needed, otherwise first dict key and sub dict values would be None:
            
            "finance_perfomance": {
            "table": [
                {
                "null": {
                    "Dec 2021": null,
                    "Year/year change": null
                }
            }
            """             
            
            perf_key = fin_perf.css(".J9Jhg::text , .jU4VAc::text").get()   # e.g. Revenue, Net Income, Operating Income..
            perf_value_col_1 = fin_perf.css(".QXDnM::text").get()           # 60.3B, 26.40%..   
            perf_value_col_2 = fin_perf.css(".gEUVJe .JwB6zf::text").get()  # 2.39%, -21.22%..
            
            ticker_data["finance_perfomance"]["table"].append({
                perf_key: {
                    fin_perf_col_2: perf_value_col_1, # dynamically add key and value from the second (2) column
                    fin_perf_col_3: perf_value_col_2  # dynamically add key and value from the third (3) column
                }
            })
else:
    ticker_data["finance_perfomance"]["error"] = f"No 'finence perfomance table' for {ticker}."
```

Extracting you may be `"interested in"`/`"people also search for"` results:

```python
    # "you may be interested in" results
    if selector.css(".HDXgAf .tOzDHb").get():
        for index, other_interests in enumerate(selector.css(".HDXgAf .tOzDHb"), start=1):
            ticker_data["interested_in"]["items"].append(discover_more_tickers(index, other_interests))
    else:
        ticker_data["interested_in"]["error"] = f"No 'you may be interested in` results for {ticker}"
    
    
    # "people also search for" results
    if selector.css(".HDXgAf+ div .tOzDHb").get():
        for index, other_tickers in enumerate(selector.css(".HDXgAf+ div .tOzDHb"), start=1):
            ticker_data["people_also_search_for"]["items"].append(discover_more_tickers(index, other_tickers))
    else:
        ticker_data["people_also_search_for"]["error"] = f"No 'people_also_search_for` in results for {ticker}"

# ....

def discover_more_tickers(index: int, other_data: str):
    """
    if price_change_formatted will start complaining,
    check beforehand for None values with try/except or if statement and set it to 0.
    
    however, re.search(r"\d{1}%|\d{1,10}\.\d{1,2}%" should get the job done.
    """
    return {
            "position": index,
            "ticker": other_data.css(".COaKTb::text").get(),
            "ticker_link": f'https://www.google.com/finance{other_data.attrib["href"].replace("./", "/")}',
            "title": other_data.css(".RwFyvf::text").get(),
            "price": other_data.css(".YMlKec::text").get(),
            "price_change": other_data.css("[jsname=Fe7oBc]::attr(aria-label)").get(),
            # https://regex101.com/r/BOFBlt/1
            # Up by 100.99% -> 100.99%
            "price_change_formatted": re.search(r"\d{1}%|\d{1,10}\.\d{1,2}%", other_data.css("[jsname=Fe7oBc]::attr(aria-label)").get()).group()
        }
```

| Code | Explanation   |
|------|---------------|
| `discover_more_tickers()` |created function used to combine two identical code into single function. This way, code needs to be changed in one place only.|
| [`attrib["attribute_name"]`](https://github.com/scrapy/parsel/blob/90397dcd0b2c1cbb91e44f65c50f9e11628ba028/parsel/selector.py#L209-L215) |to get a node attribute.|
|`[jsname=Fe7oBc]`|is a [CSS selector that used to select elements with the specified attribute and value](https://www.w3schools.com/cssref/sel_attribute_value.asp) e.g. `[attribute=value]`.|
|` re.search()`|to match parts of the string and grab only digits and `%` values. And `group()` to return matched string by a regular expression.|


Return and print the data:

```python
# def scrape_google_finance(ticker: str):
    # ticker_data = {
    #     "ticker_data": {},
    #     "about_panel": {},
    #     "news": {"items": []},
    #     "finance_perfomance": {"table": []}, 
    #     "people_also_search_for": {"items": []},
    #     "interested_in": {"items": []}
    # }

    # extraction code...

    return ticker_data

print(json.dumps(data_1, indent=2, ensure_ascii=False))
```

Full output:

```json
{
  "ticker_data": {
    "current_price": "$2,665.75",
    "quote": "GOOGL:NASDAQ",
    "title": "Alphabet Inc Class A"
  },
  "about_panel": {
    "previous_close": "$2,717.77",
    "day_range": "$2,659.31 - $2,713.40",
    "year_range": "$2,193.62 - $3,030.93",
    "market_cap": "1.80T USD",
    "volume": "1.56M",
    "p/e_ratio": "23.76",
    "dividend_yield": "-",
    "primary_exchange": "NASDAQ",
    "ceo": "Sundar Pichai",
    "founded": "Oct 2, 2015",
    "headquarters": "Mountain View, CaliforniaUnited States",
    "website": "abc.xyz",
    "employees": "156,500",
    "description": "Alphabet Inc. is an American multinational technology conglomerate holding company headquartered in Mountain View, California. It was created through a restructuring of Google on October 2, 2015, and became the parent company of Google and several former Google subsidiaries. The two co-founders of Google remained as controlling shareholders, board members, and employees at Alphabet. Alphabet is the world's third-largest technology company by revenue and one of the world's most valuable companies. It is one of the Big Five American information technology companies, alongside Amazon, Apple, Meta and Microsoft.\nThe establishment of Alphabet Inc. was prompted by a desire to make the core Google business \"cleaner and more accountable\" while allowing greater autonomy to group companies that operate in businesses other than Internet services. Founders Larry Page and Sergey Brin announced their resignation from their executive posts in December 2019, with the CEO role to be filled by Sundar Pichai, also the CEO of Google. Page and Brin remain co-founders, employees, board members, and controlling shareholders of Alphabet Inc. ",
    "extensions": [
      "Stock",
      "US listed security",
      "US headquartered"
    ]
  },
  "news": [
    {
      "position": 1,
      "title": "Amazon Splitting Stock, Alphabet Too. Which Joins the Dow First?",
      "link": "https://www.barrons.com/articles/amazon-stock-split-dow-jones-51646912881?tesla=y",
      "source": "Barron's",
      "published": "1 month ago",
      "thumbnail": "https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcRlf6wb63KP9lMPsOheYDvvANIfevHp17lzZ-Y0d0aQO1-pRCIDX8POXGtZBQk"
    },
    {
      "position": 2,
      "title": "Alphabet's quantum tech group Sandbox spins off into an independent company",
      "link": "https://www.cnbc.com/2022/03/22/alphabets-quantum-tech-group-sandbox-spins-off-into-an-independent-company.html",
      "source": "CNBC",
      "published": "2 weeks ago",
      "thumbnail": "https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcSIyv1WZJgDvwtMW8e3RAs9ImXtTZSmo2rfmCKIASk4B_XofZfZ8AbDLAMolhk"
    },
    {
      "position": 3,
      "title": "Cash-Rich Berkshire Hathaway, Apple, and Alphabet Should Gain From Higher \nRates",
      "link": "https://www.barrons.com/articles/cash-rich-berkshire-hathaway-apple-and-alphabet-should-gain-from-higher-rates-51647614268",
      "source": "Barron's",
      "published": "3 weeks ago",
      "thumbnail": "https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcSZ6dJ9h9vXlKrWlTmHiHxlfYVbViP5DAr9a_xV4LhNUOaNS01RuPmt-5sjh4c"
    },
    {
      "position": 4,
      "title": "Amazon's Stock Split Follows Alphabet's. Here's Who's Next.",
      "link": "https://www.barrons.com/articles/amazon-stock-split-who-next-51646944161",
      "source": "Barron's",
      "published": "1 month ago",
      "thumbnail": "https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcSJGKk2i1kLT_YToKJlJnhWaaj_ujLvhhZ5Obw_suZcu_YyaDD6O_Llsm1aqt8"
    },
    {
      "position": 5,
      "title": "Amazon, Alphabet, and 8 Other Beaten-Up Growth Stocks Set to Soar",
      "link": "https://www.barrons.com/articles/amazon-stock-growth-buy-51647372422",
      "source": "Barron's",
      "published": "3 weeks ago",
      "thumbnail": "https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcTxotkd3p81U7xhmCTJ6IO0tMf_yVKv3Z40bafvtp9XCyosyB4WAuX7Qt-t7Ds"
    },
    {
      "position": 6,
      "title": "Is It Too Late to Buy Alphabet Stock?",
      "link": "https://www.fool.com/investing/2022/03/14/is-it-too-late-to-buy-alphabet-stock/",
      "source": "The Motley Fool",
      "published": "3 weeks ago",
      "thumbnail": "https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcQv5D9GFKMNUPvMd91aRvi83p12y91Oau1mh_4FBPj6LCNK3cH1vEZ3_gFU4kI"
    }
  ],
  "finance_perfomance": [
    {
      "Revenue": {
        "Dec 2021": "75.32B",
        "Year/year change": "32.39%"
      }
    },
    {
      "Net income": {
        "Dec 2021": "20.64B",
        "Year/year change": "35.56%"
      }
    },
    {
      "Diluted EPS": {
        "Dec 2021": "30.69",
        "Year/year change": "37.62%"
      }
    },
    {
      "Net profit margin": {
        "Dec 2021": "27.40%",
        "Year/year change": "2.39%"
      }
    },
    {
      "Operating income": {
        "Dec 2021": "21.88B",
        "Year/year change": "39.83%"
      }
    },
    {
      "Net change in cash": {
        "Dec 2021": "-2.77B",
        "Year/year change": "-143.78%"
      }
    },
    {
      "Cash and equivalents": {
        "Dec 2021": "20.94B",
        "Year/year change": "-20.86%"
      }
    },
    {
      "Cost of revenue": {
        "Dec 2021": "32.99B",
        "Year/year change": "26.49%"
      }
    }
  ],
  "people_also_search_for": [
    {
      "position": 1,
      "ticker": "GOOG",
      "ticker_link": "https://www.google.com/finance/quote/GOOG:NASDAQ",
      "title": "Alphabet Inc Class C",
      "price": "$2,680.21",
      "price_change": "Down by 1.80%",
      "price_change_formatted": "1.80%"
    }, ... other results
    {
      "position": 18,
      "ticker": "SQ",
      "ticker_link": "https://www.google.com/finance/quote/SQ:NYSE",
      "title": "Block Inc",
      "price": "$123.22",
      "price_change": "Down by 2.15%",
      "price_change_formatted": "2.15%"
    }
  ],
  "interested_in": [
    {
      "position": 1,
      "ticker": "Index",
      "ticker_link": "https://www.google.com/finance/quote/.INX:INDEXSP",
      "title": "S&P 500",
      "price": "4,488.28",
      "price_change": "Down by 0.27%",
      "price_change_formatted": "0.27%"
    }, ... other results
    {
      "position": 18,
      "ticker": "NFLX",
      "ticker_link": "https://www.google.com/finance/quote/NFLX:NASDAQ",
      "title": "Netflix Inc",
      "price": "$355.88",
      "price_change": "Down by 1.73%",
      "price_change_formatted": "1.73%"
    }
  ]
}
```

<h3 id="scrape_multiple_tickers">Scrape Multiple Google Finance Tickers Quotes</h3>

```python
for ticker in ["DAX:INDEXDB", "GOOGL:NASDAQ", "MSFT:NASDAQ"]:
    data = scrape_google_finance(ticker=ticker)
    print(json.dumps(data["ticker_data"], indent=2, ensure_ascii=False))
```

Outputs:

```json
{
  "current_price": "14,178.23",
  "quote": "DAX:Index",
  "title": "DAX PERFORMANCE-INDEX"
}
{
  "current_price": "$2,665.75",
  "quote": "GOOGL:NASDAQ",
  "title": "Alphabet Inc Class A"
}
{
  "current_price": "$296.97",
  "quote": "MSFT:NASDAQ",
  "title": "Microsoft Corporation"
}
```

____


<h2 id="timeseries_data">Extract Google Finance Chart Time-Series Data</h2>

Scraping time-series data is not a particularly good idea so it's better to use a dedicated API to get the job done. 

How to find which API Google uses to build time series charts?

![image](https://user-images.githubusercontent.com/78694043/162904012-fae53275-e906-4f5d-a310-65977fa55265.png)

We can confirm that Google is using NASDAQ API to get time-series data by simply checking [Nasdaq chart with the quote `GOOGL`](https://www.nasdaq.com/market-activity/stocks/googl):

![image](https://user-images.githubusercontent.com/78694043/162904167-6a22cf76-fb07-4fc5-9564-e172a249a90d.png)

In this case, I used [Nasdaq Data Link API](https://docs.data.nasdaq.com/) which has a support for [Python](https://docs.data.nasdaq.com/docs/python-installation), [R](https://docs.data.nasdaq.com/docs/r-installation) and [Excel](https://docs.data.nasdaq.com/docs/excel-installation). I believe other platforms provide Python integration as well.


I'm assuming that you have already installed a `nasdaq-data-link` package but if not here's how you can do it. If you set up a default version of Python:

```bash
# WSL
$ pip install nasdaq-data-link
```

If you don't set up a default version of Python:

```bash
# WSL
$ python3.9 -m pip install nasdaq-data-link # change python to your version: python3.X
```

Get your API key at [`data.nasdaq.com/account/profile`](https://data.nasdaq.com/account/profile):

![image](https://user-images.githubusercontent.com/78694043/162904299-1d4fee3e-be2c-48f9-b58c-f06deb223c1b.png)


Create a `.env` file to store your API key there:

```bash
touch .nasdaq_api_key # change the file name to yours 

# paste API key inside the created file
```


<h3 id="timeseries_code">Scraping Google Finance Time-Series Data</h3>

```python
import nasdaqdatalink

def nasdaq_get_timeseries_data():
    nasdaqdatalink.read_key(filename=".nasdaq_api_key")
    # print(nasdaqdatalink.ApiConfig.api_key) # prints api key from the .nasdaq_api_key file

    timeseries_data = nasdaqdatalink.get("WIKI/GOOGL", collapse="monthly") # not sure what "WIKI" stands for
    print(timeseries_data)

nasdaq_get_timeseries_data()
```

<h3 id="timeseries_data_explanation">Time-Series Extraction Code Explanation</h3>


|Code|Explanation|
|----|-----------|
|`nasdaqdatalink.read_key(filename=".nasdaq_api_key")`|[to read your API key](https://github.com/Nasdaq/data-link-python#alternative-api-key-file-location).|
|`".nasdaq_api_key"`|is your [`.env` variable](https://en.wikipedia.org/wiki/Environment_variable#Design) with secret API key. All secret variables (correct me if I'm wrong) starts with a `.` symbol to showcase it.|
|`nasdaqdatalink.ApiConfig.api_key`|to test out if your API is being recognized by the `nasdaq-data-link` package. Example output: `2adA_avd12CXauv_1zxs`|
|`nasdaqdatalink.get()`|to get the [time-series data which is dataset structure](https://github.com/Nasdaq/data-link-python#retrieving-data).|


Outputs a [`pandas`](https://pandas.pydata.org/docs/index.html) [`DataFrame` object](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html):

```lang-none
                Open     High      Low    Close      Volume  Ex-Dividend  Split Ratio    Adj. Open    Adj. High     Adj. Low   Adj. Close  Adj. Volume
Date                                                                                                                                                  
2004-08-31   102.320   103.71   102.16   102.37   4917800.0          0.0          1.0    51.318415    52.015567    51.238167    51.343492    4917800.0
2004-09-30   129.899   132.30   129.00   129.60  13758000.0          0.0          1.0    65.150614    66.354831    64.699722    65.000651   13758000.0
2004-10-31   198.870   199.95   190.60   190.64  42282600.0          0.0          1.0    99.742897   100.284569    95.595093    95.615155   42282600.0
2004-11-30   180.700   183.00   180.25   181.98  15384600.0          0.0          1.0    90.629765    91.783326    90.404069    91.271747   15384600.0
2004-12-31   199.230   199.88   192.56   192.79  15321600.0          0.0          1.0    99.923454   100.249460    96.578127    96.693484   15321600.0
...              ...      ...      ...      ...         ...          ...          ...          ...          ...          ...          ...          ...
2017-11-30  1039.940  1044.14  1030.07  1036.17   2190379.0          0.0          1.0  1039.940000  1044.140000  1030.070000  1036.170000    2190379.0
2017-12-31  1055.490  1058.05  1052.70  1053.40   1156357.0          0.0          1.0  1055.490000  1058.050000  1052.700000  1053.400000    1156357.0
2018-01-31  1183.810  1186.32  1172.10  1182.22   1643877.0          0.0          1.0  1183.810000  1186.320000  1172.100000  1182.220000    1643877.0
2018-02-28  1122.000  1127.65  1103.00  1103.92   2431023.0          0.0          1.0  1122.000000  1127.650000  1103.000000  1103.920000    2431023.0
2018-03-31  1063.900  1064.54   997.62  1006.94   2940957.0          0.0          1.0  1063.900000  1064.540000   997.620000  1006.940000    2940957.0

[164 rows x 12 columns]
```

As you can see, there are no data about the 2019-2022 years. It's because I'm using the [Free version, which is suitable for experimentation and exploration, as Nasdaq saying](https://docs.data.nasdaq.com/docs/getting-started#free-and-premium-data).


<h3 id="nasdaq_rates"><a href="https://docs.data.nasdaq.com/docs/getting-started#rate-limits">Nasdaq rate limits</a></h3>

| Authenticated users          | Premium users                |
|------------------------------|------------------------------|
| 300 calls per 10 seconds.    | -                            |
| 2,000 calls per 10 minutes.  | 5,000 calls per 10 minutes.  |
| limit  50,000 calls per day. | limit 720,000 calls per day. |


<h3 id="nasdaq_resources">Additional Nasdaq API Resources</h3>

|Resource|Explanation|
|--------|-----------|
|[Times-series parameters](https://docs.data.nasdaq.com/docs/parameters-2)|to customize (manipulate) your time-series dataset by adding additional parameters to a request. [Transformation of time-series data](https://docs.data.nasdaq.com/docs/parameters-2#transformations)|
|[Composing a request with `curl`](https://docs.data.nasdaq.com/docs/quick-start-examples-1)|to easily make a request using `curl`.|
|[Available saving formats](https://blog.data.nasdaq.com/getting-started-with-the-nasdaq-data-link-api)|to save data in `CSV`, `XML`, `JSON`|
|[Data formats](https://github.com/Nasdaq/data-link-python/blob/main/FOR_DEVELOPERS.md#data-formats)|to convert the data into available formats.|
|[Downloading in bulk](https://github.com/Nasdaq/data-link-python/blob/main/FOR_ANALYSTS.md#download-entire-database-bulk-download)|to download all the data in a database in a single call.|
|[Detailed guide on available methods](https://github.com/Nasdaq/data-link-python/blob/main/FOR_DEVELOPERS.md#detailed-method-guide---nasdaq-data-linkpython)|to understand how to use `data-link-python` package in more details.|
|[`data-link-python` on GitHub](https://github.com/Nasdaq/data-link-python)|to read full documentation.|
|[`quandl-python` on GitHub](https://github.com/quandl/quandl-python)|What `data-link-python` is using under the hood. You can find a little bit more documentation here.|

___


<h2 id="links">Links</h2>

- [Code in the online IDE](https://replit.com/@DimitryZub1/Scrape-Google-Finance-Ticker-Quote-in-Python#main.py)
- [GitHub repository](https://github.com/dimitryzub/google-finance-py/tree/main)

___

<h2 id="outro">Outro</h2>

If you have anything to share, any questions, suggestions, or something that isn't working correctly, reach out via Twitter at [@dimitryzub](https://twitter.com/DimitryZub) or [@serp_api](https://twitter.com/serp_api).

Yours, 
Dmitriy, and the rest of SerpApi Team.


<p style="text-align: center;">Join us on <a href="https://twitter.com/serp_api">Twitter</a> | <a href="https://www.youtube.com/channel/UCUgIHlYBOD3yA3yDIRhg_mg">YouTube</a></p>

<p style="text-align: center;">Add a  <a href="https://github.com/serpapi/SerpApi/issues/">Feature Request</a>💫 or a <a href="https://github.com/serpapi/SerpApi/issues/">Bug</a>🐞</p>

