Contents: intro, imports, what will be scraped, process, code, links, outro.

### Intro
This blog post is a continuation of Google's web scraping series. Here you'll see how to scrape Google Shopping both **inline** and **regular** Results using Python with `beautifulsoup`, `requests`, `lxml` libraries. An alternative API solution will be shown.

### Imports
```python
import requests, json
from bs4 import BeautifulSoup
from serpapi import GoogleSearch
```

### What will be scraped
Inline shopping results
![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/umcbgjegar4802kgjdrr.png)

Shopping results
![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/j5u2hojl5xfgwktu5yeo.png)


### Process

Grabbing selectors for inline shopping results: **title, link, price, source.**
<img width="100%" style="width:100%" src="https://media.giphy.com/media/E6oEBtW2roAHcVNfPZ/giphy.gif">


Grabbing selectors for shopping results: **title, product link, price, rating, reviews, shipping, source.**
<img width="100%" style="width:100%" src="https://media.giphy.com/media/gaDH6ivLX2CTHDuk8S/giphy.gif">



### Code
```python
import requests, json
from bs4 import BeautifulSoup

headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}

params = {"q": "dji", "hl": "en", 'gl': 'us', 'tbm': 'shop'}

response = requests.get("https://www.google.com/search",
                        params=params,
                        headers=headers)
soup = BeautifulSoup(response.text, 'lxml')
# list with two dict() combined
shopping_data = []
inline_results_dict = {}
shopping_results_dict = {}

for inline_result in soup.select('.sh-np__click-target'):
    inline_shopping_title = inline_result.select_one('.sh-np__product-title').text
    inline_shopping_link = f"https://google.com{inline_result['href']}"
    inline_shopping_price = inline_result.select_one('b').text
    inline_shopping_source = inline_result.select_one('.E5ocAb').text.strip()

    inline_results_dict.update({
        'inline_shopping_results': [{
            'title': inline_shopping_title,
            'link': inline_shopping_link,
            'price': inline_shopping_price,
            'source': inline_shopping_source,
        }]
    })

    shopping_data.append(dict(inline_results_dict))

for shopping_result in soup.select('.sh-dgr__content'):
    title = shopping_result.select_one('.Lq5OHe.eaGTj h4').text
    product_link = f"https://www.google.com{shopping_result.select_one('.Lq5OHe.eaGTj')['href']}"
    source = shopping_result.select_one('.IuHnof').text
    price = shopping_result.select_one('span.kHxwFf span').text

    try:
        rating = shopping_result.select_one('.Rsc7Yb').text
    except:
        rating = None

    try:
        reviews = shopping_result.select_one('.Rsc7Yb').next_sibling.next_sibling
    except:
        reviews = None

    try:
        delivery = shopping_result.select_one('.vEjMR').text
    except:
        delivery = None



    shopping_results_dict.update({
        'shopping_results': [{
            'title': title,
            'link': product_link,
            'source': source,
            'price': price,
            'rating': rating,
            'reviews': reviews,
            'delivery': delivery,
        }]
    })

    shopping_data.append(dict(shopping_results_dict))

print(json.dumps(shopping_data, indent=2, ensure_ascii=False))


------------------
'''
[
  {
    "inline_shopping_results": [
      {
        "title": "DJI Robomaster EP Core Set",
        "link": "https://google.com/aclk?sa=l&ai=DChcSEwiA5sOD5M7xAhVK5bMKHb7uBLYYABB1GgJxbg&sig=AOD64_2tNnUWw9pyzkSr97_tzDvR4JAAIg&ctype=5&q=&ved=0ahUKEwiru7-D5M7xAhXvc98KHW0JCqwQ9A4IvA4&adurl=",
        "price": "UAH 35,746.45",
        "source": "Ipartner.com.ua"
      }
    ]
  }
...
  {
    "shopping_results": [
      {
        "title": "Квадрокоптер DJI Mavic Pro Fly More Combo",
        "link": "https://www.google.com/aclk?sa=L&ai=DChcSEwiA5sOD5M7xAhVK5bMKHb7uBLYYABBjGgJxbg&sig=AOD64_3ZqWu0lVn-pO2uVyVpt_FdAAP6kw&ctype=5&q=&ved=0ahUKEwiru7-D5M7xAhXvc98KHW0JCqwQ2CkIsg0&adurl=",
        "source": "estore.ua",
        "price": "UAH 41,169.00",
        "rating": "4.7",
        "reviews": "3,136",
        "delivery": "Free delivery"
      }
    ]
  }
]
'''
```

### Using [Google Shopping Results API](https://serpapi.com/shopping-results)
SerpApi is a paid API with a free  trial of 5,000 searches.

The difference is that API provides faster access to the data without the need to spent hour or more on selecting the right selectors, or figuring out why something doesn't work as it should since it's already done for the end-user.

Besides that, there's no need to maintain the parser or find ways to bypass blockings.

```python
import json
from serpapi import GoogleSearch

params = {
  "api_key": "YOUR_API_KEY",
  "engine": "google",
  "q": "dji",
  "gl": "us",
  "hl": "en",
  "tbm": "shop"
}

search = GoogleSearch(params)
results = search.get_dict()

for inline_result in results['inline_shopping_results']:
    print(json.dumps(inline_result, indent=2, ensure_ascii=False))

for shopping_result in results['shopping_results']:
    print(json.dumps(shopping_result, indent=2, ensure_ascii=False))


------------------
'''
{
  "position": 1,
  "block_position": "top",
  "title": "DJI Matrice 300 RTK with Shield Plus",
  "price": "$13,699.00",
  "extracted_price": 13699.0,
  "link": "https://www.google.com/aclk?sa=l&ai=DChcSEwiE17mSxM7xAhWUPq0GHWR_AMgYABAEGgJwdg&sig=AOD64_3mxrBECj5jvbdMUWLJ-9mZ5GchbA&ctype=5&q=&ved=0ahUKEwjpn7WSxM7xAhVYrJ4KHQA0D98Qww8IuAw&adurl=",
  "source": "Fizuas.com",
  "shipping": "Free shipping",
  "thumbnail": "https://encrypted-tbn2.gstatic.com/shopping?q=tbn:ANd9GcQ8cOKlp6AtvvYljsvIhQIVAZGaeUkS8bD-4yLwJPMBCLRftVpixT3EPxERlGqmFzmx2XR5JuQ&usqp=CAE"
}
...
{
  "position": 1,
  "title": "DJI Mavic Mini Drone4.73,896More bundle options",
  "link": "https://www.google.com/aclk?sa=L&ai=DChcSEwiE17mSxM7xAhWUPq0GHWR_AMgYABBDGgJwdg&sig=AOD64_2IVw0ttMIJrTJR3pBfTdSd80AHZw&ctype=5&q=&ved=0ahUKEwjpn7WSxM7xAhVYrJ4KHQA0D98Qg-UECJoN&adurl=",
  "product_link": "https://google.com/shopping/product/12874362854466218272",
  "product_id": "12874362854466218272",
  "serpapi_product_api": "https://serpapi.com/search.json?device=desktop&engine=google_product&gl=us&google_domain=google.com&hl=en&product_id=12874362854466218272",
  "source": "DJI Official Store",
  "price": "$399.00",
  "extracted_price": 399.0,
  "rating": 4.7,
  "reviews": 3896,
  "thumbnail": "https://serpapi.com/searches/60e458293bea7b1ac05878f1/images/00173ffeb117302f2aa068fa440fafbb9e57cc52314814cadc7c872ea696a9d4.jpeg"
}
'''
```


### Links
[Code in the online IDE](https://replit.com/@DimitryZub1/Scrape-Google-Shopping-pythonserpapi#main.py) • [Google Shopping Results API](https://serpapi.com/shopping-results)

### Outro
If you have any questions or something isn't working correctly or you want to write something else, feel free to drop a comment in the comment section or via Twitter at [@serp_api](https://twitter.com/serp_api).

Yours,
Dimitry, and the rest of SerpApi Team.

<img width="100%" style="width:100%" src="https://media.giphy.com/media/xUA7bcuTndaPQ6jtew/giphy.gif">