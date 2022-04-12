- <a href="#what_will_be_scraped">What will be scraped</a>
- <a href="#prerequisites">Prerequisites</a>
- <a href="#regular_ads">Google Regular Ad Results</a>
- <a href="#shopping_ads">Google Shopping Ad Results</a>
- <a href="#links">Links</a>
- <a href="#outro">Outro</a>

___

<h2 id="what_will_be_scraped">What will be scraped</h2>

1. Google Regular Ads:

![image](https://user-images.githubusercontent.com/78694043/158805083-28ef2f59-2c5d-4489-963a-f643e3aa0cab.png)

2. Google Shopping Ads (top and right side block results):

![image](https://user-images.githubusercontent.com/78694043/158785709-2ccdc9f0-1ff1-4fc5-a8f0-ae615a396dce.png)

![image](https://user-images.githubusercontent.com/78694043/158785781-3d83d5f2-d5e7-4063-b95b-4e34ecf8c873.png)


<h2 id="prerequisites">Prerequisites</h2>

**Basic knowledge scraping with CSS selectors**

`CSS` selectors declare which part of the markup a style applies to thus allowing to extract data from matching tags and attributes.

If you haven't scraped with CSS selectors, there's a dedicated blog post of mine about [how to use CSS selectors when web-scraping](https://serpapi.com/blog/web-scraping-with-css-selectors-using-python/) that covers what it is, pros and cons, and why they're matter from a web-scraping perspective.

**Separate virtual environment**

In short, it's a thing that creates an independent set of installed libraries including different Python versions that can coexist with each other at the same system thus preventing libraries or Python version conflicts.

If you didn't work with a virtual environment before, have a look at the dedicated [Python virtual environments tutorial using Virtualenv and Poetry](https://serpapi.com/blog/python-virtual-environments-using-virtualenv-and-poetry/) blog post of mine to get familiar.

📌Note: this is not a strict requirement for this blog post.

**Install libraries**:

```lang-none
pip install requests, parsel, beautifulsoup4, lxml
```

📌Note: You don't need to install both `beautifulsoup4` and `parsel`. This blog post contains examples using both libraries. Choose the one that you feel more comfortable with.

**Reduce the chance of being blocked**

There's a chance that a request might be blocked. Have a look at [how to reduce the chance of being blocked while web-scraping](https://serpapi.com/blog/how-to-reduce-chance-of-being-blocked-while-web/), there are eleven methods to bypass blocks from most websites.

___

<h2 id="regular_ads">Google Regular Ad Results</h2>

```python
# using beautifulsoup

from bs4 import BeautifulSoup
import requests, lxml, json

params = {
    "q": "coffee beans buy",
    "hl": "en",
    "gl": "us"
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.87 Safari/537.36",
}

html = requests.get("https://www.google.com/search?", params=params, headers=headers)
soup = BeautifulSoup(html.text, "lxml")

ad_results = []

for index, ad_result in enumerate(soup.select(".uEierd"), start=1):
    title = ad_result.select_one(".v0nnCb span").text
    website_link = ad_result.select_one("a.sVXRqc")["data-pcu"]
    ad_link = ad_result.select_one("a.sVXRqc")["href"]
    displayed_link = ad_result.select_one(".qzEoUe").text
    tracking_link = ad_result.select_one(".v5yQqb a.sVXRqc")["data-rw"]
    snippet = ad_result.select_one(".MUxGbd div span").text
    phone = None if ad_result.select_one("span.fUamLb span") is None else ad_result.select_one("span.fUamLb span") .text

    inline_link_text = [title.text for title in ad_result.select("div.bOeY0b .XUpIGb a")]
    inline_link = [link["href"] for link in ad_result.select("div.bOeY0b .XUpIGb a")]

    ad_results.append({
        "position": index,
        "title": title,
        "phone": phone,
        "website_link": website_link,
        "displayed_link": displayed_link,
        "ad_link": ad_link,
        "tracking_link": tracking_link,
        "snippet": snippet,
        "sitelinks": [{"titles": inline_link_text, "links": inline_link}]
    })

print(json.dumps(ad_results, indent=2))
```

Create search query parameters and request headers:

```python
# https://docs.python-requests.org/en/master/user/quickstart/#passing-parameters-in-urls
params = {
    "q": "coffee beans buy",
    "hl": "en",
    "gl": "us"
}

# https://docs.python-requests.org/en/master/user/quickstart/#custom-headers
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.87 Safari/537.36",
}
```

Make a request, pass headers and search query parameters, create `BeautifulSoup()` object, pass HTML parser, and temporary `list` to store extracted data:

```python
html = requests.get("https://www.google.com/search", params=params, headers=headers)
selector = BeautifulSoup(html.text)

ad_results = []
```

Extract the data and `append` to the temporary `list` and `print` it to see the result:

```python
for index, ad_result in enumerate(soup.select(".uEierd"), start=1):
    title = ad_result.select_one(".v0nnCb span").text
    website_link = ad_result.select_one("a.sVXRqc")["data-pcu"]
    ad_link = ad_result.select_one("a.sVXRqc")["href"]
    displayed_link = ad_result.select_one(".qzEoUe").text
    tracking_link = ad_result.select_one(".v5yQqb a.sVXRqc")["data-rw"]
    snippet = ad_result.select_one(".MUxGbd div span").text
    phone = None if ad_result.select_one("span.fUamLb span") is None else ad_result.select_one("span.fUamLb span") .text

    inline_link_text = [title.text for title in ad_result.select("div.bOeY0b .XUpIGb a")]
    inline_link = [link["href"] for link in ad_result.select("div.bOeY0b .XUpIGb a")]

    ad_results.append({
        "position": index,
        "title": title,
        "phone": phone,
        "website_link": website_link,
        "displayed_link": displayed_link,
        "ad_link": ad_link,
        "tracking_link": tracking_link,
        "snippet": snippet,
        "sitelinks": [{"titles": inline_link_text, "links": inline_link}]
    })

print(json.dumps(ad_results, indent=2))
```

Output:

```json
[
  {
    "position": 1,
    "title": "Bluestone Lane Coffee Beans - Straight to Your Door",
    "phone": "(718) 374-6858",
    "website_link": "https://shop.bluestonelane.com/",
    "displayed_link": "https://shop.bluestonelane.com/shop-online/beans",
    "ad_link": "https://shop.bluestonelane.com/collections/coffee",
    "tracking_link": "https://www.google.com/aclk?sa=l&ai=DChcSEwiP6r3a-rv2AhUGqpYKHdQzCsgYABAEGgJ0bA&ae=2&sig=AOD64_1zlaVI5SseAcinZkdqJ8NE73vcDw&q&adurl",
    "snippet": "Save 10% On Your Weekly Coffee At Home When You Subscribe. The Perfect Pour, Straight To Your Door. Shop Bluestone Lane Coffee Beans Now! Aussie Inspired Coffee. Healthy.",
    "sitelinks": [
      {
        "titles": [
          "Download New Loyalty App",
          "Our Commitment",
          "Subscribe Today",
          "Filter Blend 12oz Coffee"
        ],
        "links": [
          "https://www.google.com/aclk?sa=l&ai=DChcSEwiP6r3a-rv2AhUGqpYKHdQzCsgYABAJGgJ0bA&ae=2&sig=AOD64_0xTS8u7xoSaM1L2zpjHW72MVf2rA&q=&ved=2ahUKEwjAorfa-rv2AhV0IqYKHV9GBogQpigoAHoECAUQBw&adurl=",
          "https://www.google.com/aclk?sa=l&ai=DChcSEwiP6r3a-rv2AhUGqpYKHdQzCsgYABAPGgJ0bA&ae=2&sig=AOD64_2iLZxTyzQIy4E-ppYcvnXR0N5NjQ&q=&ved=2ahUKEwjAorfa-rv2AhV0IqYKHV9GBogQpigoAXoECAUQCA&adurl=",
          "https://www.google.com/aclk?sa=l&ai=DChcSEwiP6r3a-rv2AhUGqpYKHdQzCsgYABAVGgJ0bA&ae=2&sig=AOD64_0EoBw_9CBqxqAOZdMI8q74-Ze_WQ&q=&ved=2ahUKEwjAorfa-rv2AhV0IqYKHV9GBogQpigoAnoECAUQCQ&adurl=",
          "https://www.google.com/aclk?sa=l&ai=DChcSEwiP6r3a-rv2AhUGqpYKHdQzCsgYABAbGgJ0bA&ae=2&sig=AOD64_2sn0YN-maincAYRdu_nANJvF83fg&q=&ved=2ahUKEwjAorfa-rv2AhV0IqYKHV9GBogQpigoA3oECAUQCg&adurl="
        ]
      }
    ]
  }, ... other results
]
```

____

```python
# using parsel

from parsel import Selector
import requests, json

params = {
    "q": "coffee beans buy",
    "hl": "en",
    "gl": "us"
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.87 Safari/537.36",
}

html = requests.get("https://www.google.com/search", params=params, headers=headers)
selector = Selector(html.text)

ad_results = []

for index, ad_result in enumerate(selector.css(".uEierd"), start=1):
    title = ad_result.css(".v0nnCb span::text").get()
    website_link = ad_result.css("a.sVXRqc::attr(data-pcu)").get()
    ad_link = ad_result.css("a.sVXRqc::attr(href)").get()
    displayed_link = ad_result.css(".qzEoUe::text").get()
    tracking_link = ad_result.css(".v5yQqb a.sVXRqc::attr(data-rw)").get()
    snippet = ad_result.css(".MUxGbd div span").xpath("normalize-space()").get()
    phone = ad_result.css("span.fUamLb span::text").get()

    inline_link_text = None if ad_result.css("div.bOeY0b .XUpIGb a::text").getall() == [] else ad_result.css("div.bOeY0b .XUpIGb a::text").getall()
    inline_link = None if ad_result.css("div.bOeY0b .XUpIGb a::attr(href)").getall() == [] else ad_result.css("div.bOeY0b .XUpIGb a::attr(href)").getall()

    ad_results.append({
        "position": index,
        "title": title,
        "phone": phone,
        "website_link": website_link,
        "displayed_link": displayed_link,
        "ad_link": ad_link,
        "tracking_link": tracking_link,
        "snippet": snippet,
        "sitelinks": [{"titles": inline_link_text, "links": inline_link}]
    })

print(json.dumps(ad_results, indent=2))
```

Create search query parameters and request headers:

```python
# https://docs.python-requests.org/en/master/user/quickstart/#passing-parameters-in-urls
params = {
    "q": "coffee beans buy",
    "hl": "en",
    "gl": "us"
}

# https://docs.python-requests.org/en/master/user/quickstart/#custom-headers
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.87 Safari/537.36",
}
```

Make a request, pass headers and search query parameters, create `Selector()` object and temporary `list` to store extracted data:

```python
html = requests.get("https://www.google.com/search", params=params, headers=headers)
selector = Selector(html.text)

ad_results = []
```

Extract the data, `append` it to the temporary `list` and `print` it to see results:

```python
for index, ad_result in enumerate(selector.css(".uEierd"), start=1):
    title = ad_result.css(".v0nnCb span::text").get()
    website_link = ad_result.css("a.sVXRqc::attr(data-pcu)").get()
    ad_link = ad_result.css("a.sVXRqc::attr(href)").get()
    displayed_link = ad_result.css(".qzEoUe::text").get()
    tracking_link = ad_result.css(".v5yQqb a.sVXRqc::attr(data-rw)").get()
    snippet = ad_result.css(".MUxGbd div span").xpath("normalize-space()").get()
    phone = ad_result.css("span.fUamLb span::text").get()

    inline_link_text = None if ad_result.css("div.bOeY0b .XUpIGb a::text").getall() == [] else ad_result.css("div.bOeY0b .XUpIGb a::text").getall()
    inline_link = None if ad_result.css("div.bOeY0b .XUpIGb a::attr(href)").getall() == [] else ad_result.css("div.bOeY0b .XUpIGb a::attr(href)").getall()

    ad_results.append({
        "position": index,
        "title": title,
        "phone": phone,
        "website_link": website_link,
        "displayed_link": displayed_link,
        "ad_link": ad_link,
        "tracking_link": tracking_link,
        "snippet": snippet,
        "sitelinks": [{"titles": inline_link_text, "links": inline_link}]
    })

print(json.dumps(ad_results, indent=2))
```

- `enumerate()` adds counter to an iterable and returns it, and `start=1` will start counting from 1, instead from 0.
- `css()` will process passed CSS selectors to manipulate XML/HTML document. It's like `select()` or `select_one()` `beautifulsoup` methods.
- `::text` and `::attr(<attribute_name>)` is a `parsel` pseudo-elements [which translates to XPath](https://github.com/scrapy/parsel/blob/f5f73d34ba787ad0c9df25de295de6e196ecd91d/parsel/selector.py#L350-L351) using [`cssselct`](https://cssselect.readthedocs.io/en/latest/index.html) under the hood.
- `xpath("normalize-space()")` will grab those blank text nodes since `/text()` will ignore blank text nodes.
- `inline_link_text` `if` statement expression will return `None` `if` selector returns a `[]`, otherwise it will return `list` of matched data. Same goes for extracting `attr(href)` attribute.
- `getall()` wll return a `list` of matches.

Output:

```json
[
  {
    "position": 1,
    "title": "Our Coffee, Your Cup - Straight to Your Door - bluestonelane.com",
    "phone": "(718) 374-6858",
    "website_link": "https://shop.bluestonelane.com/",
    "displayed_link": "https://shop.bluestonelane.com/shop-online/beans",
    "ad_link": "https://shop.bluestonelane.com/collections/coffee",
    "tracking_link": "https://www.google.com/aclk?sa=l&ai=DChcSEwjyvZ7a-7v2AhXKIWAKHbB0CPUYABADGgJ0bQ&ae=2&sig=AOD64_36gM2Qo8gyYFj6BGQ2TBWx6UchxQ&q&adurl",
    "snippet": "Brew Flagstaff At Home: Our Balanced And Approachable Drip Blend. Save 10% On Your Weekly Coffee At Home When You Subscribe. Aussie Inspired Coffee. Australian Inspired.",
    "sitelinks": [
      {
        "titles": null,
        "links": null
      }
    ]
  }, ... other results
]
```

____

<h2 id="shopping_ads">Google Shopping Ad Results</h2>

```python
# using beautiflsoup
# handles both top and right side shopping results

# if top block shopping ads appears
if soup.select_one(".commercial-unit-desktop-top"):
    for index, shopping_ad in enumerate(soup.select(".mnr-c.pla-unit"), start=1):
        title = shopping_ad.select_one(".pymv4e").text
        link = shopping_ad.select_one(".pla-unit-title-link")["href"]
        price = shopping_ad.select_one(".e10twf").text
        source = shopping_ad.select_one(".LbUacb .zPEcBd").text

        data.append({
            "position": index,
            "block_position": "top_block",
            "title": title,
            "link": link,
            "price": price,
            "source": source
            })

# if right block shopping ads appears
elif soup.select_one(".commercial-unit-desktop-rhs"):
    for index, shopping_ad in enumerate(soup.select(".mnr-c.pla-unit"), start=1):
        title = shopping_ad.select_one(".pymv4e").text
        link = shopping_ad.select_one(".pla-unit-title-link")["href"]
        price = shopping_ad.select_one(".e10twf").text
        source = shopping_ad.select_one(".LbUacb, .zPEcBd").text

        data.append({
            "position": index,
            "block_position": "right_block",
            "title": title,
            "link": link,
            "price": price,
            "source": source
            })

print(json.dumps(data, indent=2, ensure_ascii=False))
```

____

```python
# using parsel
# handles both top and right side shopping results

from parsel import Selector
import requests, json

# https://docs.python-requests.org/en/master/user/quickstart/#passing-parameters-in-urls
params = {
    "q": "graphics card buy",
    "hl": "en",
    "gl": "us"
    }

# https://docs.python-requests.org/en/master/user/quickstart/#custom-headers
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
    }

html = requests.get("https://www.google.com/search", params=params, headers=headers, timeout=30)
selector = Selector(html.text)

data = []

# if top block shopping ads appears
if selector.css(".commercial-unit-desktop-top").get():
    for index, shopping_ad in enumerate(selector.css(".mnr-c.pla-unit"), start=1):
        title = shopping_ad.css(".pymv4e::text").get()
        link = shopping_ad.css(".pla-unit-title-link::attr(href)").get()
        price = shopping_ad.css(".e10twf::text").get()
        source = shopping_ad.css(".LbUacb .zPEcBd::text").get()

        data.append({
            "position": index,
            "block_position": "top_block",
            "title": title,
            "link": link,
            "price": price,
            "source": source
            })

# if right block shopping ads appears
elif selector.css(".commercial-unit-desktop-rhs").get():
    for index, shopping_ad in enumerate(selector.css(".mnr-c.pla-unit"), start=1):
        title = shopping_ad.css(".pymv4e::text").get()
        link = shopping_ad.css(".pla-unit-title-link::attr(href)").get()
        price = shopping_ad.css(".e10twf::text").get()
        source = shopping_ad.css(".LbUacb::text, .zPEcBd::text").get()

        data.append({
            "position": index,
            "block_position": "right_block",
            "title": title,
            "link": link,
            "price": price,
            "source": source
            })

print(json.dumps(data, indent=2, ensure_ascii=False))
```

Top results output:

```json
[
  {
    "position": "top_block",
    "title": "Відеокарта Gigabyte GeForce RTX 3080 Ti Gaming OC 12288MB (GV-N308TGAMING OC-12GD)",
    "link": "https://telemart.ua/ua/products/gigabyte-geforce-rtx-3080-ti-gaming-oc-12288mb-gv-n308tgaming-oc-12gd/",
    "price": "UAH 61,999.00",
    "source": "telemart.ua"
  }, ... other results
  {
    "position": "top_block",
    "title": "Gigabyte GeForce RTX 3080 VISION OC 10G (rev. 2.0) NVIDIA 10 GB GDDR6X",
    "link": "https://www.grooves.land/gigabyte-geforce-rtx-3080-vision-10g-rev-grafikkarten-rtx-3080-gddr6x-pcie-x16-hdmi-displayport-gigabyte-hardware-electronic-pZZa1-2100509896.html?language=en&currency=EUR&_z=ua",
    "price": "UAH 38,359.03",
    "source": "Grooves.Land"
  }
]
```

Right results output:

```json
[
  {
    "position": "right_block",
    "title": "MSI GeForce RTX 2060 Ventus 12G OC NVIDIA 12 GB GDDR6",
    "link": "https://www.grooves.land/msi-geforce-rtx-2060-ventus-12gb-grafikkarte-msi-hardware-electronic-pZZa1-2100485027.html?language=en&currency=EUR&_z=ua",
    "price": "UAH 16,210.82",
    "source": "Grooves.Land"
  }, ... other results
 {
    "position": "right_block",
    "title": "RTX 3060Ti 8GB MSI VENTUS 2X 8G OCV1 LHR Hardware/Electronic",
    "link": "https://www.grooves.land/msi-geforce-rtx-3060-ventus-ocv1-lhr-grafikkarten-rtx-3060-gddr6-pcie-hdmi-displayport-msi-hardware-electronic-pZZa1-2100386549.html?language=en&currency=EUR&_z=ua",
    "price": "UAH 20,997.98",
    "source": "Grooves.Land"
  }
]
```


___

Alternatively, you can do it using [Google Ad Results API](https://serpapi.com/google-ads) from SerpApi.

While using API, there's no need to create the parser from scratch, maintain it overtime, figure out how to scale it and how to bypass blocks from search engines. [Have a try using SerpApi](https://serpapi.com/playground?q=skyrim+buy&gl=us&hl=en).

```python
# scrapes both regular and shopping ads (top, right blocks)

from serpapi import GoogleSearch
import json, os

params = {
    "api_key": os.getenv("API_KEY"),
    "engine": "google",
    "q": "buy rtx 3080",
    "gl": "us",
    "hl": "en"
}

search = GoogleSearch(params)
results = search.get_dict()

if results.get("ads", []):
    for ad in results["ads"]:
        print(json.dumps(ad, indent=2))

if results.get("shopping_results", []):
    for shopping_ad in results["shopping_results"]:
        print(json.dumps(shopping_ad, indent=2))
else:
    print("no shopping ads found.")
```

Regular ads output:

```json
{
  "position": 1,
  "block_position": "top",
  "title": "Specialty roaster coffee beans - Specialty coffee bean delivery",
  "link": "https://www.bottomless.com/",
  "displayed_link": "https://www.bottomless.com/",
  "tracking_link": "https://www.google.com/aclk?sa=l&ai=DChcSEwiolvLqiM32AhUKnLMKHaQJC-sYABACGgJxbg&ae=2&sig=AOD64_0z23Z-mc1OkEpczNz-x2yF5YLSsQ&q&adurl",
  "extensions": [
    "\u200eShop Products \u00b7 \u200eCoffee Subscription \u00b7 \u200eSend A Bottomless Gift \u00b7 \u200eCareers \u00b7 \u200ePartnerships \u00b7 \u200eGet Started \u00b7 \u200eFAQs \u00b7 \u200eBlog"
  ],
  "description": "Never have to buy coffee beans from the store again with our automated coffee delivery.",
  "sitelinks": [
    {
      "title": "Shop Products",
      "link": "https://www.google.com/aclk?sa=l&ai=DChcSEwiolvLqiM32AhUKnLMKHaQJC-sYABADGgJxbg&ae=2&sig=AOD64_0HYHHtwrsAIGomuNVmydPd7v2TUA&q=&ved=2ahUKEwjKxenqiM32AhUxq3IEHcu2CvEQpigoAHoECAQQBQ&adurl="
    },
    {
      "title": "Coffee Subscription",
      "link": "https://www.google.com/aclk?sa=l&ai=DChcSEwiolvLqiM32AhUKnLMKHaQJC-sYABAEGgJxbg&ae=2&sig=AOD64_3wLVBOmaIcctrg5eeIpXUjncI8sg&q=&ved=2ahUKEwjKxenqiM32AhUxq3IEHcu2CvEQpigoAXoECAQQBg&adurl="
    },
    {
      "title": "Send A Bottomless Gift",
      "link": "https://www.google.com/aclk?sa=l&ai=DChcSEwiolvLqiM32AhUKnLMKHaQJC-sYABAFGgJxbg&ae=2&sig=AOD64_2QwYx_VHhBAzXoagpeVSVrLlUEqg&q=&ved=2ahUKEwjKxenqiM32AhUxq3IEHcu2CvEQpigoAnoECAQQBw&adurl="
    },
    {
      "title": "Careers",
      "link": "https://www.google.com/aclk?sa=l&ai=DChcSEwiolvLqiM32AhUKnLMKHaQJC-sYABAGGgJxbg&ae=2&sig=AOD64_2hIva8QgcQLurgDS09y-cwQONJsg&q=&ved=2ahUKEwjKxenqiM32AhUxq3IEHcu2CvEQpigoA3oECAQQCA&adurl="
    },
    {
      "title": "Partnerships",
      "link": "https://www.google.com/aclk?sa=l&ai=DChcSEwiolvLqiM32AhUKnLMKHaQJC-sYABAHGgJxbg&ae=2&sig=AOD64_2GyFC-hVyKRZzNwqxuCEJo0zu4qw&q=&ved=2ahUKEwjKxenqiM32AhUxq3IEHcu2CvEQpigoBHoECAQQCQ&adurl="
    },
    {
      "title": "Get Started",
      "link": "https://www.google.com/aclk?sa=l&ai=DChcSEwiolvLqiM32AhUKnLMKHaQJC-sYABAIGgJxbg&ae=2&sig=AOD64_3Xfw361uyxsaVLWQQEwdDsSaVlNQ&q=&ved=2ahUKEwjKxenqiM32AhUxq3IEHcu2CvEQpigoBXoECAQQCg&adurl="
    },
    {
      "title": "FAQs",
      "link": "https://www.google.com/aclk?sa=l&ai=DChcSEwiolvLqiM32AhUKnLMKHaQJC-sYABAJGgJxbg&ae=2&sig=AOD64_04tmkV2h42w8JZZII5WxfD6SLqow&q=&ved=2ahUKEwjKxenqiM32AhUxq3IEHcu2CvEQpigoBnoECAQQCw&adurl="
    },
    {
      "title": "Blog",
      "link": "https://www.google.com/aclk?sa=l&ai=DChcSEwiolvLqiM32AhUKnLMKHaQJC-sYABAKGgJxbg&ae=2&sig=AOD64_3f_UEHA546-i91dlA4_u0nIWhNCQ&q=&ved=2ahUKEwjKxenqiM32AhUxq3IEHcu2CvEQpigoB3oECAQQDA&adurl="
    }
  ]
} ... other results
```

Shopping ads output:

```json
{
  "position": 1,
  "block_position": "top",
  "title": "ASUS GeForce RTX 3080 Ti TUF Gaming OC Graphics Card Chipset NVIDIA, 12GB, Windows, DisplayPort 1.4 HDMI 2.1 5, Ports 2.1 x2, 1.4 x3, Bus PCIe 4.0 x16",
  "price": "$1,949.99",
  "extracted_price": 1949.99,
  "link": "https://www.google.com/aclk?sa=l&ai=DChcSEwj-ouaTic32AhXuam8EHTWvCRsYABAFGgJqZg&ae=2&sig=AOD64_3KbwY-1-lU3sxYJrrCtTuQ4vD1QA&ctype=5&q=&ved=2ahUKEwi6ytyTic32AhXck2oFHRLuA-gQ5bgDegQIARA5&adurl=",
  "source": "B&H Photo-Vid...",
  "reviews": 139,
  "thumbnail": "https://serpapi.com/searches/62331f6c2f542e30940b588f/images/f33950a51d54d017faac86bbc552ceadcb0d642f5a3d5ea2230be8c5c62ddd9c.png"
} ... other results
```
___

<h2 id="links">Links</h2>

- [Code in the online IDE](https://replit.com/@DimitryZub1/Scrape-Google-Ads-1#main.py)
- [Google Ad Results API](https://serpapi.com/google-ads)

___

<h2 id="outro">Outro</h2>

If you have anything to share, any questions, suggestions, or something that isn't working correctly, reach out via Twitter at [@dimitryzub](https://twitter.com/DimitryZub), or [@serp_api](https://twitter.com/serp_api).

Yours,
Dmitriy, and the rest of SerpApi Team.

___

<p style="text-align: center;">Join us on <a href="https://www.reddit.com/r/SerpApi/">Reddit</a> | <a href="https://twitter.com/serp_api">Twitter</a> | <a href="https://www.youtube.com/channel/UCUgIHlYBOD3yA3yDIRhg_mg">YouTube</a></p>

<p style="text-align: center;">Add a  <a href="https://forum.serpapi.com/feature-requests">Feature Request</a>💫 or a <a href="https://forum.serpapi.com/bugs">Bug</a>🐞</p>

