Contents: intro, imports, what will be scraped, process, code, links, outro.

### Intro
This blog post is a continuation of Google's web scraping series. This post сontains code example without handling different Knowledge Graph layouts. It scrapes the one you'll see on the screenshot below.

### Imports
```python
import requests
import lxml
from bs4 import BeautifulSoup
from serpapi import GoogleSearch
```

### What will be scraped
![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/ktyho1k5seuwz3lfizud.png)

### Process
[SelectorGadget Chrome extension](https://selectorgadget.com) was used to grab `CSS` selectors.
The Gif below illustrates the approach of selecting different parts of the knowledge graph.

<img width="100%" style="width:100%" src="https://media.giphy.com/media/J6BlehCEBl9MUnHqoa/giphy.gif">


### Code
```python
from bs4 import BeautifulSoup
import requests, lxml

headers = {
    'User-agent':
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
        "Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}


def get_knowledge_graph():
    html = requests.get('https://www.google.com/search?q=dell&hl=en', headers=headers)
    soup = BeautifulSoup(html.text, 'lxml')

    title = soup.select_one('#rhs .mfMhoc span').text
    subtitle = soup.select_one('.wwUB2c span').text
    try:
        snippet = soup.select_one('.zsYMMe+ span').text
    except:
        snippet = None

    print(f"{title}\n{subtitle}\n{snippet}\n")

    for result in soup.select(".rVusze"):
        key_element = result.select_one(".w8qArf").text
        if result.select_one(".kno-fv"):
            value_element = result.select_one(".kno-fv").text.replace(": ", "")
        else:
            value_element = None
        key_link = f'https://www.google.com{result.select_one(".w8qArf a")["href"]}'
        try:
            key_value_link = f'https://www.google.com{result.select_one(".kno-fv a")["href"]}'
        except:
            key_value_link = None

        print(f"{key_element}{value_element}\nkey_link: {key_link}\nkey_value_link: {key_value_link}")


get_knowledge_graph()

------------
'''
Dell
Computer company
Dell is an American multinational computer technology company that develops, sells, repairs, and supports computers and related products and services, and is owned by its parent company of Dell Technologies.

Headquarters: Round Rock, Texas, United States
key_link: https://www.google.com/search?hl=en&q=dell+headquarters&stick=H4sIAAAAAAAAAOPgE-LQz9U3KKi0TNLSyk620s8vSk_My6xKLMnMz0PhWGWkJqYUliYWlaQWFS9iFUxJzclRQBYDAPbbwDtMAAAA&sa=X&ved=2ahUKEwjqsaWohsHxAhWO_rsIHYe9ALUQ6BMoADAregQIPRAC
key_value_link: https://www.google.com/search?hl=en&q=Round+Rock&stick=H4sIAAAAAAAAAOPgE-LQz9U3KKi0TFLiBLEMjfOScrS0spOt9POL0hPzMqsSSzLz81A4VhmpiSmFpYlFJalFxYtYuYLyS_NSFILyk7N3sDICAIJH2ApTAAAA&sa=X&ved=2ahUKEwjqsaWohsHxAhWO_rsIHYe9ALUQmxMoATAregQIPRAD
...
'''
```

### Using [Google Knowledge Graph API](https://serpapi.com/knowledge-graph)
SerpApi is a paid API with a free trial of 5,000 searches.
```python
from serpapi import GoogleSearch

params = {
    "api_key": "YOUR_API_KEY",
    "engine": "google",
    "q": "dell",
    "hl": "en",
}

search = GoogleSearch(params)
results = search.get_dict()

for key, value in results['knowledge_graph'].items():
  print(f'{key}: {value}')

---------
'''
title: Dell
type: Computer company
image: https://serpapi.com/searches/60df1de78b7ed2c811fc9402/images/5bcb8cde2f058371f30ec817e8e77f6830f7905f186ec931.png
website: http://www.dell.com/
description: Dell is an American multinational computer technology company that develops, sells, repairs, and supports computers and related products and services, and is owned by its parent company of Dell Technologies.
source: {'name': 'Wikipedia', 'link': 'https://en.wikipedia.org/wiki/Dell'}
customer_service: 1 (800) 624-9897
customer_service_chat: Online Chat
technical_support: 1 (800) 999-3355
headquarters: Round Rock, TX
parent_organization: Dell Technologies
subsidiaries: Alienware, Dell Corp ltd, Dell EMC, Dell Canada Inc, MORE
profiles: [{'name': 'Twitter', 'link': 'https://twitter.com/Dell', 'image': 'https://serpapi.com/searches/60df1de78b7ed2c811fc9402/images/5bcb8cde2f058371f30ec817e8e77f682bbb185dfebaeedb08588701cca810fb3643f16dd97f5671.png'}, {'name': 'YouTube', 'link': 'https://www.youtube.com/channel/UC01FW5V9UVohbPtqKSmXX-w', 'image': 'https://serpapi.com/searches/60df1de78b7ed2c811fc9402/images/5bcb8cde2f058371f30ec817e8e77f682bbb185dfebaeedbeb7382739a1a71fe73f0268752fdc2f4.png'}, {'name': 'Facebook', 'link': 'https://www.facebook.com/Dell', 'image': 'https://serpapi.com/searches/60df1de78b7ed2c811fc9402/images/5bcb8cde2f058371f30ec817e8e77f682bbb185dfebaeedb98264af15d9b5f8cde97aa47652da0e9.png'}, {'name': 'Instagram', 'link': 'https://www.instagram.com/dell', 'image': 'https://serpapi.com/searches/60df1de78b7ed2c811fc9402/images/5bcb8cde2f058371f30ec817e8e77f682bbb185dfebaeedba26760f1c6e7e705304a8fc921a9f0c2.png'}]
people_also_search_for: [{'name': 'Main Line Information Systems', 'extensions': ['Computer store'], 'link': 'https://www.google.com#', 'image': 'https://serpapi.com/searches/60df1de78b7ed2c811fc9402/images/5bcb8cde2f058371f30ec817e8e77f682da45e72c1616e2c8b7a6946cc49a64ca785965e5c02954e7ef17cfffc507685.png'}]
people_also_search_for_link: https://www.google.com/search?hl=en&q=Dell&stick=H4sIAAAAAAAAAONgFuLQz9U3KKi0TFKCs7RkspOt9JNKizPzUouL9TOLi0tTi6yKM1NSyxMrixexsrik5uTsYGUEACBytqo-AAAA&sa=X&ved=2ahUKEwi478nwx8TxAhVXSzABHTmeBssQMSgAMEF6BAhLEAE
people_also_search_for_stick: H4sIAAAAAAAAAONgFuLQz9U3KKi0TFKCs7RkspOt9JNKizPzUouL9TOLi0tTi6yKM1NSyxMrixexsrik5uTsYGUEACBytqo-AAAA
'''
```

### Links
[Code in the online IDE](https://replit.com/@DimitryZub1/Scrape-Google-Search-Knowledge-Graph-python-serpapi#bs4_result.py) • [Google Knowledge Graph API](https://serpapi.com/knowledge-graph)

### Outro
If you have any questions or something isn't working correctly or you want to write something else, feel free to drop a comment in the comment section or via Twitter at [@serp_api](https://twitter.com/serp_api).

Yours,
Dimitry, and the rest of SerpApi Team.