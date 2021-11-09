Contents: intro, organic results, ads, related searches, people also ask, local results, conclusion, code in online IDE, outro.

### Intro
This blog post is a collection of examples that you can overlay one on top of each other to get a more comprehensive program.

After each first block of code in each section, an alternative API solution will be shown.

The following blocks of code are using these imports:
```python
from bs4 import BeautifulSoup
import requests
import lxml
import os # used for creating an environment variable
from selenium import webdriver
import time # used only with selenium
from serpapi import GoogleSearch
```

[SelectorGadget](https://selectorgadget.com) Chrome extension was used to visually grab CSS selectors from the page.

I used [`find()`](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#find), [`find_all()`](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#find-all) in combination with [`select_one()`](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#css-selectors), [`select()`](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#css-selectors) `beautifulsoup` methods to find certain elements of the page.
**Why use one over another?** In my case, when it was difficult to grab certain element using SelectorGadget (CSS selector/`select()`, `select_one()`) I was switching to finding this element using inspector tool from Chrome Dev Tools (`find()`, `find_all()`).


### Organic Results
The two following blocks of code shows how to scrape Organic Search Results (title, snippet, link, displayed link) from Yahoo Search.
```python
from bs4 import BeautifulSoup
import requests, lxml

headers = {
    'User-agent':
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}

def get_organic_results():

    html = requests.get('https://search.yahoo.com/search?p=playstation 5',headers=headers, ).text
    soup = BeautifulSoup(html, 'lxml')

    for result in soup.find_all('div', class_='layoutMiddle'):
      title = result.find('h3', class_='title tc d-ib w-100p').text
      link = result.find('h3', class_='title tc d-ib w-100p').a['href']
      displayed_link = result.select_one('.compTitle div').text
      snippet = result.find('div',class_='compText aAbs').text

      print(f'{title}\n{snippet}\n{link}\n{displayed_link}\n')

# Part of the output:
'''
PlayStation 5 Back In Stock? - Free Where To Buy Guide
Beat the crowds and be first in line when PlayStation 5 comes back in stock. Our bots scan around the clock so you get alerted as soon as PS5 is available anywhere. 
https://r.search.yahoo.com/cbclk2/dWU9NDJCNUIxODQ4RjNENDMxMyZ1dD0xNjIyODE4MDM5MTE0JnVvPTgzNjMxNzI0NTI0MTM5Jmx0PTImcz0xJmVzPWNfekExc2tHUFNfOGt2Unh6UGFXWmp0ZHE2Vk1XLkZSalE4cGtDQldXRWZpVVhqWg--/RV=2/RE=1622846839/RO=10/RU=https%3a%2f%2fwww.bing.com%2faclick%3fld%3de8uGR7IulG1dkBBGL2En9GDzVUCUzZnmzCFwnACGNKW5ky0imFrUuouhwunLcTAtVbOEJxhVT-CmRU8s1ZTSlUbejj9J6Wl_8AXnBCmLSRdgE2UAD2sjARuT_z3EIWCSCFoIKIVGteIMBV2eiRFusfONPnqPM2sdOmdQpojDmsL68QCB5wnGcuERKQXMZjKaKrY0yy6A%26u%3daHR0cHMlM2ElMmYlMmZ3d3cucG9wY2FydC5jb20lMmZwczUlM2Z1dG1fbWVkaXVtJTNkY3BjJTI2dXRtX3NvdXJjZSUzZGJpbmclMjZ1dG1fY2FtcGFpZ24lM2Q0MTAxODQ1MTclMjZ1dG1fY29udGVudCUzZDEzMzgxMDYyODc5MTI2MTUlMjZ1dG1fdGVybSUzZHBsYXlzdGF0aW9uJTI1MjA1ZSUyNm1zY2xraWQlM2RjNjNkZmY3ZTVjNTAxYTgzNTliMTlmYzQ2MGE3Yjk2Nw%26rlid%3dc63dff7e5c501a8359b19fc460a7b967/RK=2/RS=nNTmP3k80tkq348j4IFNcQ8fWXg-;_ylt=AwrEwhX3PLpg67UACyJXNyoA;_ylu=Y29sbwNiZjEEcG9zAzEEdnRpZAMEc2VjA292LXRvcA--?IG=0ac4c2152e0a49878b00000000617c99
www.popcart.com › playstation-5 › where-to-buy
'''
```
#### Using [Yahoo! Organic Results API](https://serpapi.com/yahoo-organic-results)
```python
from serpapi import GoogleSearch
import os

def get_organic_results():
    params = {
      "api_key": os.getenv("API_KEY"),
      "engine": "yahoo",
      "p": "playstation 5",
      "vl": "lang_en",
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    for result in results['organic_results']:
      title = result['title']
      link = result['link']
      displayed_link = result['displayed_link']
      snippet = result['snippet']

      print(f'{title}\n{link}\n{displayed_link}\n{snippet}\n')

# Part of the output:
'''
PlayStation®5 | Play Has No Limits | PlayStation
https://www.playstation.com/en-us/ps5/
www.playstation.com › en-us › ps5
Up to 120fps with 120Hz output. Enjoy smooth and fluid high frame rate gameplay at up to 120fps for compatible games, with support for 120Hz output on 4K displays. HDR technology. With an HDR TV, supported PS5 games display an unbelievably vibrant and lifelike range of colors.
'''
```

### Ads
The two following blocks of code will show how to scrape expanded and inline ads (title, link) from Yahoo Search.
```python
from bs4 import BeautifulSoup
import requests, lxml

headers = {
    'User-agent':
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}

def get_ad_results():

    html = requests.get('https://search.yahoo.com/search?p=playstation 5',headers=headers, ).text
    soup = BeautifulSoup(html, 'lxml')

    # Ad results
    # Expanded ads
    for expanded_ad in soup.select('.mt-16'):
      title = expanded_ad.select_one('.lh-1_2x').text
      snippet = expanded_ad.select_one('.tc p').text
      ad_link_expanded = expanded_ad.select_one('.lh-1_2x')['href']

      print(f'{title}\n{snippet}\n{ad_link_expanded}\n')

    # Inline ads
    # There're will be "Cached" word that needs to be filtered.
    for inline_ad in soup.select('#main .txt a'):
      title = inline_ad.text
      link = inline_ad['href']
      print(f'{title}\n{link}\n')

# Part of the outputs:
'''
# expanded ads
Where to Buy
Find a Store Near You.
https://r.search.yahoo.com/cbclk2/dWU9M0FFREI5NkJGRDYzNDMyQyZ1dD0xNjIyODIyMzMzNDA0JnVvPTgzNjMxNzI0NTI0MTM5Jmx0PTImcz0xJmVzPUhQTGp5cHNHUFMuajB6aFM5SllHdTJpbG9hTmZjNzR0MEhYMkZucjduYTlMX1BZRlJRLS0-/RV=2/RE=1622851133/RO=10/RU=https%3a%2f%2fwww.bing.com%2faclick%3fld%3de8YrSoIz-nRZudtLaFx9aD4TVUCUwQo4mySwkxUEsrgOmixDG7udYwkESfskHe4zBIXVDs4xZVswMY9sRBMl7spIar_FTPANeWUa3YWYenoPjrPEOqdpvo7S5LUhwJHvNSk3AV_hgr4sCTscj3lxOWIbE9UPFsvu8mnbPUb-B_NnVKFhAdR_pzvBsrKKdFUkWbWQncmw%26u%3daHR0cHMlM2ElMmYlMmYlMmZwb3BjYXJ0LmNvbSUyZndoZXJlLXRvLWJ1eQ%26rlid%3d0f0136027ed31a04a71a56b8336e4df1/RK=2/RS=yag1ozDlBqohVlMpZDFJW..9qXQ-;_ylt=AwrEzee9TbpgqzAAFuZXNyoA;_ylu=Y29sbwNiZjEEcG9zAzEEdnRpZAMEc2VjA292LXRvcA--?IG=0ac4cde79aca491b8e00000000372b28


# inline ads
Amazon Deals
https://r.search.yahoo.com/cbclk2/dWU9MEY0OTU1RjU1RThDNDE2RSZ1dD0xNjIyODIyNDA3ODkzJnVvPTg0MTgxNDY2MjkxNDQ2Jmx0PTImcz0xJmVzPUhTclhncm9HUFNfMHoxNjBFMG1XWjcuYTZUOFZqRkU5SkxnSlZpQjJneHJWUl9TYw--/RV=2/RE=1622851208/RO=10/RU=https%3a%2f%2fwww.bing.com%2faclick%3fld%3de8XuYlMDs0ZCMfjfyf80GAtTVUCUz_wzwCEv4tj1E0nkEZ1gBXvZZqXHo02JspkeQs5oo4-7Wk2hLGeyxCOmIXKunU1nfbkm2-ZUodgtWvZxJm_kqZFLIk4fV3OslvLOGgaHK2KO6ZQxIBeI2q6Ag9lrRGt_f_z8EqSTFT_1Y1-c2cCXnOB84sciwgSEqYUTe-ktTf8g%26u%3daHR0cHMlM2ElMmYlMmZ3d3cuYW1hem9uLmNvbSUyZmdwJTJmZ29sZGJveCUyZiUzZnJlZiUzZHBkX3NsXzd2NGppMWVpZzVfZSUyNnRhZyUzZG1oMGItMjAlMjZ0YWclM2RtaDBiLTIwJTI2cmVmJTNkcGRfc2xfMXBvcGtseTJnYV9lJTI2YWRncnBpZCUzZDEzNDY5MDIzMTI2MzAwNDclMjZodmFkaWQlM2Q4NDE4MTQ2NjI5MTQ0NiUyNmh2bmV0dyUzZG8lMjZodnFtdCUzZGUlMjZodmJtdCUzZGJlJTI2aHZkZXYlM2RjJTI2aHZsb2NpbnQlM2QlMjZodmxvY3BoeSUzZDcyODkwJTI2aHZ0YXJnaWQlM2Rrd2QtODQxODE3NDk1MTU2MDMlM2Fsb2MtMTkwJTI2aHlkYWRjciUzZDI2NTgzXzk5NzE2Mjk%26rlid%3d4eba8ce1bc521860d28dec5bf25a063c/RK=2/RS=Eqiwbq76SQfsn_fJaV_ZD0U_EuM-;_ylt=AwrJ7JMHTrpgpSsAMiFXNyoA;_ylu=Y29sbwNiZjEEcG9zAzMEdnRpZAMEc2VjA292LWJvdHRvbQ--?IG=0ac9ec938dd84b0bbc0000000097c771
'''
```
#### Using [Yahoo! Ad Results API](https://serpapi.com/yahoo-ad-results)
```python
from serpapi import GoogleSearch
import os

def get_ad_results():
    params = {
      "api_key": os.getenv("API_KEY"),
      "engine": "yahoo",
      "p": "playstation 5",
      "vl": "lang_en",
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    for result in results['ads_results']:
      position = result['block_position']
      title = result['title']
      link = result['link']
      displayed_link = result['displayed_link']
      snippet = result['snippet']

      print(f'{position}\n{title}\n{snippet}\n{link}\n{displayed_link}\n')

    try:
      for expanded_inline_ad in results['sitelinks']:
        expanded_ad_title = expanded_inline_ad['expanded']['title']
        expanded_ad_link = expanded_inline_ad['expanded']['link']
        inline_ad_title = expanded_inline_ad['inline']['title']
        inline_ad_link = expanded_inline_ad['inline']['link']

        print(f'{expanded_ad_title}\n{expanded_ad_link}\n{inline_ad_title}\n{inline_ad_link}\n')
    except:
      pass

# Part of the output:
'''
top
PlayStation 5 Back In Stock? - Free Where To Buy Guide
popcart.com has been visited by 10K+ users in the past month
Beat the crowds and be first in line when PlayStation 5 comes back in stock. Our bots scan around the clock so you get alerted as soon as PS5 is available anywhere.
https://www.bing.com/aclick?ld=e8lKHkAzVpUFPApzOoQE60dzVUCUzAgbiG-ejwmFRySxyiF7Zk7RloM5RbVSQW1LDCNEoX23yHU7ttutTsdg3mMN_hev78H-6BspAwTLAipijncf4A04YxbI4U0G1RB-NbYATEJ6INlYJ6EuNhsSkyK1j1TvKBZy4f2v-Kh9wuSDE3yb4oVXHk9XgmKRtWuqpmPJ9rVQ&u=aHR0cHMlM2ElMmYlMmZ3d3cucG9wY2FydC5jb20lMmZwczUlM2Z1dG1fbWVkaXVtJTNkY3BjJTI2dXRtX3NvdXJjZSUzZGJpbmclMjZ1dG1fY2FtcGFpZ24lM2Q0MTAxODQ1MTclMjZ1dG1fY29udGVudCUzZDEzMzgxMDYyODc5MTI2MTUlMjZ1dG1fdGVybSUzZHBsYXlzdGF0aW9uJTI1MjA1ZSUyNm1zY2xraWQlM2QwZDM2ZjI1NjJiYWYxNjg1OTM1NDkyZWM2NjhiNzg3Yw&rlid=0d36f2562baf1685935492ec668b787c
www.popcart.com › playstation-5 › where-to-buy
'''
```
### Related Searches
The two following blocks of code will show how to scrape related searches (top and bottom) from Yahoo Search.
```python
from bs4 import BeautifulSoup
import requests, lxml

headers = {
    'User-agent':
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}

def get_related_searches():

    html = requests.get('https://search.yahoo.com/search?p=playstation 5',headers=headers, ).text
    soup = BeautifulSoup(html, 'lxml')
    
    # Top related searches
    # Locating element and splitting by ":" delimiter so that Also try: playstation 5 restock, playstation 5 console became playstation 5 restock, playstation 5 console and then splitting by "," to remove commas.
    result = soup.find('ol',class_='cardReg searchTop').text.split(':')[1].split(',')
    top_related_saearches = ''.join(result) # or ''.join(f'{result}\n')
    print('Top searches:')
    print(top_related_saearches)

    # Bottom related searches
    print('Bottom searches:')
    for result in soup.select('.pl-18'):
      print(result.text)

# Output:
'''
Top searches:
 playstation 5 restock playstation 5 console
Bottom searches:
playstation 5 restock
playstation 5 pre-order
playstation 5 console
playstation 5 gamestop
playstation 5 for sale
playstation 5 release date
sony playstation 5
xbox series x
'''
```
#### Using [Yahoo! Related Searches API](https://serpapi.com/yahoo-related-searches)
```python
from serpapi import GoogleSearch
import os

def get_related_searches():
    params = {
      "api_key": os.getenv("API_KEY"),
      "engine": "yahoo",
      "p": "playstation 5",
      "vl": "lang_en",
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    
    # Top related searches
    for top_result in results['related_searches']['top']:
        top_query = top_result['query']
        top_query_link = top_result['link']
        print('Top related search:')
        print(f'{top_query}\n{top_query_link}\n')

    # Bottom related searches
    for bottom_result in results['related_searches']['bottom']:
      bottom_query = bottom_result['query']
      bottom_query_link = bottom_result['link']
      print('Bottom related search:')
      print(f'{bottom_query}\n{bottom_query_link}\n')

# Part of the output:
'''
Top related search:
playstation 5 restock
https://search.yahoo.com/search;_ylt=AwrEzerWaLpgI3oAERtXNyoA;_ylu=Y29sbwNiZjEEcG9zAzEEdnRpZAMEc2VjA3JlbA--?p=playstation+5+restock&ei=UTF-8&fl=1&vl=lang_en&fr2=p%3As%2Cv%3Aw%2Cm%3Ars-top

Bottom related search:
playstation 5 restock
https://search.yahoo.com/search;_ylt=AwrEzerWaLpgI3oAeRtXNyoA;_ylu=Y29sbwNiZjEEcG9zAzEEdnRpZAMEc2VjA3JlbC1ib3Q-?p=playstation+5+restock&ei=UTF-8&fl=1&vl=lang_en&fr2=p%3As%2Cv%3Aw%2Cm%3Ars-bottom
'''
```
### People Also Ask using Selenium
The two following blocks of code will show how to scrape People Also Ask (question, snippet, reference link, more result) from Yahoo Search.
```python
from selenium import webdriver
import time

def get_people_also_ask():

    driver = webdriver.Chrome()
    driver.get("https://search.yahoo.com/search?p=playstation 5")

    # Just to print titles
    # for result in driver.find_elements_by_css_selector(".bingrelqa"):
    #     print(result.text)

    # Buffer for page to load. 
    time.sleep(1)
    # Clicks on every arrow
    for arrow_down in driver.find_elements_by_css_selector(".outl-no"):
        # Arrow click
        arrow_down.click()
        # Waits for 1 sec until next click
        time.sleep(1)

    # Container that pops up after clicked on every drop-down arrow
    for container in driver.find_elements_by_css_selector('#web .mt-0'):
        question = container.find_element_by_css_selector('.lh-17.va-top').text
        snippet = container.find_element_by_css_selector('#web .d-b').text
        reference_link = container.find_element_by_css_selector('.pt-10 a').get_attribute('href')
        more_results_link = container.find_element_by_css_selector('.fz-s a').get_attribute('href')

        print(f'{question}\n{snippet}\n{reference_link}\n{more_results_link}\n')
    driver.quit()
```
#### Using [Yahoo! Related Questions API](https://serpapi.com/yahoo-related-questions)
```python
from serpapi import GoogleSearch
import os

def get_related_questions():
    params = {
      "api_key": os.getenv("API_KEY"),
      "engine": "yahoo",
      "p": "best pc",
      "vl": "lang_en",
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    for result in results['related_questions']:
      question = result['question']
      title = result['title']
      link = result['link']
      displayed_link = result['displayed_link']
      more_results_link = result['more_results_link']
      snippet = result['snippet']

      print(f'{question}\n{title}\n{snippet}\n{link}\n{displayed_link}\n{more_results_link}\n')

# Part of the output:
'''
Who makes the best desktop PC?
Who Makes the Best Top Rated Desktop Computers
Dell makes the top rated desktop computers. However, who makes the best desktop computer will always be up for debate. All manufacturers make some lemons.
https://r.search.yahoo.com/_ylt=Awr9CWrjarpgALwAyzpXNyoA;_ylu=Y29sbwNncTEEcG9zAzIEdnRpZAMEc2VjA3Nj/RV=2/RE=1622858596/RO=10/RU=https%3a%2f%2fwww.brighthub.com%2fcomputing%2fhardware%2farticles%2f64052.aspx/RK=2/RS=pl7UaIH7A8lyQEI_O.RQU3Ks_tc-
www.brighthub.com/computing/hardware/articles/64052.aspx
https://search.yahoo.com/search;_ylt=Awr9CWrjarpgALwAzDpXNyoA;_ylu=Y29sbwNncTEEcG9zAzIEdnRpZAMEc2VjA3Nj?ei=UTF-8&fl=1&vl=lang_en&p=Who+makes+the+best+desktop+PC%3F&fr2=
'''
```
### Local Results (map preview)
The two following blocks of code will show how to scrape Local Results (title, link, type, if the place verified or not, link, price, hours, rating, reviews, address, phone, website link) from Yahoo Search.
```python
from bs4 import BeautifulSoup
import requests, lxml

headers = {
    'User-agent':
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}

def get_local_pack_results():

    html = requests.get('https://search.yahoo.com/search?p=manhattan beach coffee shops',headers=headers, ).text
    soup = BeautifulSoup(html, 'lxml')

    for result in soup.find_all('div', class_='info col'):
      # Deleting numbers e.g. "1. Blabla", "2. best coffee shop", "3. Best PC shop"
      result.find('span', class_='sn fc-26th').decompose()
      # Checks if place is verified or not by checking Green check mark
      if result.select_one('.icon-verified-10-green') is not None:
        print('Verified')
      else:
        print('Not verified')
      title = result.find('div', class_='titlewrapper').text
      title_search_link = result.find('div',class_='titlewrapper').a['href']
      place_type = result.select_one('.meta .bb-child').text
      try:
        price = result.select_one('.lcl-prcrate').text
      except:
        price = None
      reviews = result.select_one('.ml-2').text.split(' ')[0]
      try:
        hours = result.select_one('.isclosed').text
      except:
        hours = None
      address = result.find('span', class_='addr').text
      phone = result.select_one('.hoo .separator+ span').text
      website_link = result.select_one('.imgbox a')['href']

      print(f'{title}\n{title_search_link}\n{place_type}\n{price}\n{reviews}\n{hours}\n{address}\n{phone}\n{website_link}\n')

# Part of the output:
'''
Not verified
Two Guns Espresso - Manhattan Beach
https://search.yahoo.com/local/s;_ylt=A0geK.ItbLpgUN0AQeFXNyoA;_ylu=Y29sbwNiZjEEcG9zAzEEdnRpZAMEc2VjA3Nj?p=manhattan+beach+coffee+shops&selectedId=98602458
Coffee House
$$
1018
None
350 N Sepulveda Blvd, Ste 7, Manhattan Beach, CA
(310) 318-2537
https://r.search.yahoo.com/_ylt=A0geK.ItbLpgUN0AQ.FXNyoA;_ylu=Y29sbwNiZjEEcG9zAzEEdnRpZAMEc2VjA3Nj/RV=2/RE=1622858926/RO=10/RU=https%3a%2f%2fwww.twogunsespresso.com%2f/RK=2/RS=InLKtMhaXFbOCAt8vLSVsdosd_M-
'''
```
#### Using [Yahoo! Local Pack API](https://serpapi.com/yahoo-local-pack)
```python
from serpapi import GoogleSearch
import os

def get_local_pack_results():
    params = {
      "api_key": os.getenv("API_KEY"),
      "engine": "yahoo",
      "p": "manhattan beach coffee shops",
      "vl": "lang_en",
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    for result in results['local_results']['places']:
        title = result['title']
        place_type = result['type']
        try:
          price = result['price']
        except:
          price = None
        try:
          hours = result['hours']
        except:
          hours = None
        rating = result['rating']
        reviews = result['reviews']
        address = result['address']
        phone = result['phone']
        website_link = result['links']['website']
        # If you  need to know GPS coordinates
        try:
          latitude = result['gps_coordinates']['latitude']
        except:
          latitude = None
        try:
          longitude = result['gps_coordinates']['longitude']
        except:
          longitude = None

        print(f'{title}\n{place_type}\n{price}\n{hours}\n{rating}\n{reviews}\n{address}\n{phone}\n{website_link}\n{latitude}\n{longitude}\n')

# Part of the output:
'''
Two Guns Espresso - Manhattan Beach
Coffee House
$$
Open
4.5
1018
350 N Sepulveda Blvd, Ste 7, Manhattan Beach, CA
(310) 318-2537
https://www.twogunsespresso.com/
33.88137
-118.39572%3B
'''
```

### Conclusion
The process for the most of the time is straightforward in both cases using own solution or using third-party API. There're a few differences using API:
* It does the same thing except you don't have to figure out how to avoid blocking and maintain a parser, and in most cases it more compact and gives a JSON output for the user.

* You don't have to figure out how to scrape complex Javascript-driven websites, how to solve CAPTCHA, or finding proxies, if they're needed.

### Code in online IDE
You can test everything in the online IDE [here](https://replit.com/@DimitryZub1/Scrape-Yahoo-Python-SerpApi#main.py).

### Outro
If you have any questions or something isn't working correctly or you want to write something else, feel free to drop a comment in the comment section or via Twitter at [@serp_api](https://twitter.com/serp_api).

Yours,
Dimitry, and the rest of SerpApi Team.