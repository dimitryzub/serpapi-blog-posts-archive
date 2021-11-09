Contents: intro, imports, what will be scraped, process, code, links, outro.

### Intro
This blog post is a continuation of Google's web scraping series. Here you'll see how to scrape Product Results using Python using `beautifulsoup`, `requests`, `lxml` libraries. An alternative API solution will be shown.

### Imports
```python
import requests, lxml, json
from bs4 import BeautifulSoup
from serpapi import GoogleSearch
```

### What will be scraped
![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/hnzbrkw5qln85qp100k2.png)


### Process

1. Found a container will all data.
2. Used nested `for` loops whenever data is not extracted fully. *Note that nested `for` loops could be pain in the neck if you want to get a structured `json`, e.g. `.update()` existing `dict()`, but I could be wrong here. These words are based on my experience.*


### Code
```python
import requests, lxml
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}

response = requests.get("https://www.google.com/shopping/product/14506091995175728218?hl=en", headers=headers)
soup = BeautifulSoup(response.text, 'lxml')


def get_product_results_data():
    for page_result in soup.select('.sg-product__dpdp-c'):
        title = soup.select_one('.sh-t__title').text
        reviews = soup.select_one('.aE5Gic span').text.replace('(', '').replace(')', '')
        rating = soup.select_one('.UzThIf')['aria-label'].replace('stars', '').replace(' out of ', '.').strip()
        description = soup.select_one('.sh-ds__trunc-txt').text
        #  · = " · " dot separator
        extensions = soup.select_one('.Qo4JI').text.split(' · ')
        print(f'{title}\n{reviews}\n{rating}\n{description}\n{extensions}\n')

        for prices in page_result.select('.o4ZIje'):
            price = prices.text.replace('(', '').replace(')', '').split(' + ')[0]
            print(price)

        for review_table in page_result.select('.aALHge'):
            number_of_stars = review_table.select_one('.rOdmxf').text
            number_of_reviews = review_table.select_one('.rOdmxf').next_sibling['aria-label'].split(' ')[0]
            print(f'{number_of_stars}\n{number_of_reviews}')

        for user_review in page_result.select('.XBANlb'):
            title = user_review.select_one('.P3O8Ne').text
            rating = user_review.select_one('.UzThIf')['aria-label'].split(' ')[0]
            date = user_review.select_one('.ff3bE').text
            desc = user_review.select_one('.g1lvWe div').text
            source = user_review.select_one('.sPPcBf').text.replace('   ', ' ')
            print(f'\n{title}\n{rating}\n{date}\n{desc}\n{source}')
            print('----------------------------------------------------')

        # get link to use in another func() that will extract other reviews
        all_reviews_link = f"https://www.google.com{soup.select_one('a.internal-link.JKlKAe.Ba4zEd ')['href']}"

        return all_reviews_link


----------------------
'''
Google Pixel 4 White 64 GB, Unlocked
632
4.5
Point and shoot for the perfect photo. Capture brilliant color and control the exposure balance of different parts of your photos. Get the shot without the flash. Night Sight is now faster and easier to use it can even take photos of the Milky Way. Get more done with your voice ...
['Google', 'Pixel Family', 'Pixel 4', 'Android', '5.7 inches screen', 'Facial Recognition', '8 MP Front Camera', 'Smartphone', 'Wireless Charging', 'Unlocked']

5 star
362
4 star
90
3 star
53
2 star
34
1 star
93

Google, PLEASE bring back the fingerprint scanner!
1
November 24, 2020
I will start by saying I am usually a huge fan of all things Google. My wife and I had the original Pixel for several years and raved about them to anyone who would listen. The batteries were finally starting to fail and it was time to get new phones. We both went for the Pixel 4 thinking we would get the same great phone we had loved for years. Even though I was disappointed right away, I waited a few months to leave a review to see if I just needed to get used to it. Now, months later, I can safely say I'm disappointed. I still cannot get over the loss of the backside fingerprint scanner. The facial recognition that took its place is useless 80% of the time (it won't work if you're wearing a face mask or in low lighting), 10% of the time it unlocks my phone unintentionally ... More
Justin Thielman · Review provided by Google
'''
```



### Get more reviews
Essentially, the URL is coming from the  `get_product_results_data()` function that `return` `all_reviews_link` variable.

```python
import requests, lxml
from bs4 import BeautifulSoup
from google_get_product_results import get_product_results_data


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}


def get_all_reviews():
    response = requests.get(get_product_results_data(), headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')

    for user_review in soup.select('.z6XoBf'):
        try:
            title = user_review.select_one('.P3O8Ne').text
        except:
            title = None
        rating = user_review.select_one('.UzThIf')['aria-label'].split(' ')[0]
        date = user_review.select_one('.ff3bE').text
        desc = user_review.select_one('.g1lvWe div').text
        source = user_review.select_one('.sPPcBf').text.replace('   ', ' ')
        print(f'{title}\n{rating}\n{date}\n{desc}\n{source}')
```

### Combining two functions together:

```python
from google_get_product_results import get_product_results_data
from google_get_all_product_results_reviews import get_all_reviews

print('Product data:')
get_product_results_data()

print('All reviews:')
get_all_reviews()


------------------
'''
Product data:
Google Pixel 4 White 64 GB, Unlocked
629
4.5
Point and shoot for the perfect photo. Capture brilliant color and control the exposure balance of different parts of your photos. Get the shot without the flash. Night Sight is now faster and easier to use it can even take photos of the Milky Way. Get more done with your voice ...
['Google', 'Pixel Family', 'Pixel 4', 'Android', '5.7 inches screen', 'Facial Recognition', '8 MP Front Camera', 'Smartphone', 'Wireless Charging', 'Unlocked']

$598.95
$598.95
5 star
361
4 star
90
3 star
53
2 star
33
1 star
92

Google, PLEASE bring back the fingerprint scanner!
1
November 24, 2020
I will start by saying I am usually a huge fan of all things Google. My wife and I had the original Pixel for several years and raved about them to anyone who would listen. The batteries were finally starting to fail and it was time to get new phones. We both went for the Pixel 4 thinking we would get the same great phone we had loved for years. Even though I was disappointed right away, I waited a few months to leave a review to see if I just needed to get used to it. Now, months later, I can safely say I'm disappointed. I still cannot get over the loss of the backside fingerprint scanner. The facial recognition that took its place is useless 80% of the time (it won't work if you're wearing a face mask or in low lighting), 10% of the time it unlocks my phone unintentionally ... More
Justin Thielman · Review provided by Google
----------------------------------------------------
All reviews:
Google, PLEASE bring back the fingerprint scanner!
1
November 24, 2020
I will start by saying I am usually a huge fan of all things Google. My wife and I had the original Pixel for several years and raved about them to anyone who would listen. The batteries were finally starting to fail and it was time to get new phones. We both went for the Pixel 4 thinking we would get the same great phone we had loved for years. Even though I was disappointed right away, I waited a few months to leave a review to see if I just needed to get used to it. Now, months later, I can safely say I'm disappointed. I still cannot get over the loss of the backside fingerprint scanner. The facial recognition that took its place is useless 80% of the time (it won't work if you're wearing a face mask or in low lighting), 10% of the time it unlocks my phone unintentionally ... More
Justin Thielman · Review provided by Google
Waste of money, google removed key features just to put them in cheaper next gen phones.
1
February 3, 2021
One of the worst phones i have ever owned. Getting rid of the fingerprint scanner was a big mistake with this phone. The face unlock is such a stupid feature, and unnecessary when people already expect and like the fingerprint scan. The battery life is abysmal. My phone doesnt last even for 1 whole day with light usage. I have an iphone 8 plus for work and that phone has a great battery life even though it is much, much much older. That iphone lasts for 3 days with regular use, and a full day if i am streaming videos all day. The photos on the pixel are okay, i dont like that it applies a ton of blurring to faces. It will blue the heck out of your face to smooth everything and i dont like that. My selfies dont even look like me. And the night photos were the main draw, but ... More
sarahlikesglitter · Review provided by Google
Please Bring Back Fingerprint Scanner
3
December 28, 2020
Like another user said, face recognition is just not as good as a fingerprint scanner. With my fingerprint, I can unlock the phone whenever I'm holding it, no matter what position. With face recognition is has to be right up to my face. It's such a pain, and now that we're wearing masks all the time, it's really a problem. If there's low lighting, it also can't see me. As someone who was a fan of the Huawei Mate before the company was banned from the US, I'm glad the Pixel finally has an Ultra/Extreme Battery Saving mode. That was one of my favorite features as someone who always has low battery because I'm always on my phone. The latest update made the phone worse in my opinion. At first, the Messenger bumbles were messing up, but they fixed that. Now, every time I try ... More
Shan Howard · Review provided by Google
I wanted an upgrade but I was taken back to 2000.

...
Other reviews..
'''
```

You can go even further by applying `Selenium` that will click on *More reviews* button until there's nothing to click on in order to extract all review results.


______________________

### Using [Google Product Result API](https://serpapi.com/product-result)
SerpApi is a paid API with a free plan.

The difference I like the most is that it comes with structured `JSON` output and all you have to do is just to iterate over it.

Besides that, if you want to done things quickly, API is a way to go since you don't have to build everything from scratch by searching the right `CSS` selector or something else.

```python
import json
from serpapi import GoogleSearch

params = {
  "api_key": "YOUR_API_KEY",
  "engine": "google_product",
  "product_id": "14506091995175728218",
  "gl": "us",
  "hl": "en"
}

search = GoogleSearch(params)
results = search.get_dict()

title = results['product_results']['title']
prices = results['product_results']['prices']
reviews = results['product_results']['reviews']
rating = results['product_results']['rating']
extensions = results['product_results']['extensions']
description = results['product_results']['description']
user_reviews = results['product_results']['reviews']
reviews_results = results['reviews_results']['ratings']
print(f'{title}\n{prices}\n{reviews}\n{rating}\n{extensions}\n{description}\n{user_reviews}\n{reviews_results}')

----------------
'''
Google Pixel 4 White 64 GB, Unlocked
['$199.99', '$198.00', '$460.00']
629
3.9
['Google', 'Pixel Family', 'Pixel 4', 'Android', '5.7″', 'Facial Recognition', '8 MP front camera', 'Smartphone', 'With Wireless Charging', 'Unlocked']
Point and shoot for the perfect photo. Capture brilliant color and control the exposure balance of different parts of your photos. Get the shot without the flash. Night Sight is now faster and easier to use it can even take photos of the Milky Way. Get more done with your voice. The new Google Assistant is the easiest way to send texts, share photos, and more. A new way to control your phone. Quick Gestures let you skip songs and silence calls – just by waving your hand above the screen. End the robocalls. With Call Screen, the Google Assistant helps you proactively filter our spam before your phone ever rings.
629
[{'stars': 1, 'amount': 92}, {'stars': 2, 'amount': 33}, {'stars': 3, 'amount': 53}, {'stars': 4, 'amount': 90}, {'stars': 5, 'amount': 361}]
'''
```

You can also extract more reviews results using SerpApi by simply adding `reviews` parameter to `params` `dictionary`, e.g. `"reviews": "1"`, which by default is `0` (**OFF**) and `1` (**ON**).

![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/bhnc1bvdoa4w57hoxv59.png)


### Links
[Code in the online IDE](https://replit.com/@DimitryZub1/Scrape-Google-Shopping-Product-Result-python#main.py) • [Google Product Result API](https://serpapi.com/product-result)

### Outro
If you have any questions or something isn't working correctly or you want to write something else, feel free to drop a comment in the comment section or via Twitter at [@serp_api](https://twitter.com/serp_api).

Yours,
Dimitry, and the rest of SerpApi Team.


<img width="100%" style="width:100%" src="https://media.giphy.com/media/S2lenTmOxOAWA/giphy.gif">