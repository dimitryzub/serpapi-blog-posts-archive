Contents: intro, imports, organic result, answer box, related images, differences, links, outro.

### Intro
This blog post is a collection of examples on how to scrape certain Baidu Search Results using Python as well as using an alternative solution SerpApi that you can stack on top of each other to suits your particular needs.
### Imports
```python
from bs4 import BeautifulSoup
import requests, lxml, json
from serpapi import BaiduSearch # only for SerpApi solution
import os # only used with SerpApi to create environment for API_KEY
```
### Organic Results
```python
from bs4 import BeautifulSoup
import requests, lxml, json

headers = {
    "User-Agent":
    "Mozilla/5.0 (Linux; Android 10; HD1913) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.105 Mobile Safari/537.36 EdgA/46.1.2.5140"
}


def get_organic_results():
    html = requests.get('https://www.baidu.com/s?&tn=baidu&wd=minecraft',headers=headers)
    soup = BeautifulSoup(html.text, 'lxml')
   
    baidu_data = []
    
    for result in soup.select('.result.c-container.new-pmd'):
      title = result.select_one('.t').text
      link = result.select_one('.t').a['href']
      displayed_link = result.select_one('.c-showurl').text
      snippet = result.select_one('.c-abstract').text
      try:
        sitelink_title = result.select_one('.op-se-listen-recommend').text
      except:
        sitelink_title = None
      try:
        sitelink_link = result.select_one('.op-se-listen-recommend')['herf']
      except:
        sitelink_link = None
      
      baidu_data.append({
        'title': title,
        'link': link,
        'displayed_link': displayed_link,
        'snippet': snippet,
        'sitelinks': {'title': sitelink_title, 'link': sitelink_link},
      })
      
    print(json.dumps(baidu_data, indent=2, ensure_ascii=False))

# Part of the output:
'''
[
  {
    "title": "minecraft website - 官方网站 | Minecraft",
    "link": "http://www.baidu.com/link?url=_XTFGPU6ibzEJnDEdC4y2_WnTCHh-xaHkiR06lAOA6a",
    "displayed_link": "minecraft.net/",
    "snippet": "2021年3月3日 我的世界是一款堆方块、不断冒险的游戏。在此购买,或浏览网站了解最新消息和社区的精彩创意!",
    "sitelinks": {
      "title": null,
      "link": null
    }
  }
]
'''
```

### Using [Baidu Organic Search Results API](https://serpapi.com/baidu-organic-results)
```python
import os, json
from serpapi import BaiduSearch

def get_organic_results():
    params = {
        "engine": "baidu",
        "q": "minecraft",
        "api_key": os.getenv("API_KEY"),
    }

    search = BaiduSearch(params)
    results = search.get_dict()

    baidu_data = []

    for result in results['organic_results']:
      title = result['title']
      link = result['link']
      try:
        displayed_link = result['displayed_link']
      except:
        displayed_link = None
      try:
        snippet = result['snippet']
      except:
        snippet = None
      try:
        sitelink_title = result['rich_snippet']['sitelinks']['title']
      except:
        sitelink_title = None
      try:
        sitelink_link = result['rich_snippet']['sitelinks']['link']
      except:
        sitelink_link = None
      
      baidu_data.append({
        'title': title,
        'link': link,
        'displayed_link': displayed_link,
        'snippet': snippet,
        'sitelinks': [{'title': sitelink_title, 'link':sitelink_link}],
      })
    
    print(json.dumps(baidu_data, indent=2, ensure_ascii=False))

# Part of the output:
'''
[
  {
    "title": "minecraft website - 官方网站 | Minecraft",
    "link": "http://www.baidu.com/link?url=OD7rfRPzLty76yZJ9dimCAV2VS-QyXURXbLmjXH3wq3",
    "displayed_link": "minecraft.net/",
    "snippet": "我的世界是一款堆方块、不断冒险的游戏。在此购买,或浏览网站了解最新消息和社区的精彩创意!",
    "sitelinks": [
      {
        "title": null,
        "link": null
      }
    ]
  }
]
'''
```

### Answer Box
```python
from bs4 import BeautifulSoup
import requests, lxml, re, json

headers = {
    "User-Agent":
    "Mozilla/5.0 (Linux; Android 10; HD1913) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.105 Mobile Safari/537.36 EdgA/46.1.2.5140"
}


def get_answerbox_result():
    html = requests.get('https://www.baidu.com/s?&tn=baidu&wd=jet li',headers=headers)
    soup = BeautifulSoup(html.text, 'lxml')

    try:
      answer_box = []

      for result in soup.find_all('div', class_='c-border'):
        english_word = result.select_one('.op_dict3_marginRight').text
        # british
        british_phonetic = result.select_one('.c-color-t+ td .op_dict3_gap_small').text
        british_chinese_character = result.select_one('.c-color-t+ td .op_dict3_font14').text
        british_audio_link = result.find('a', class_='op_dict3_how_read c-gap-right-middle')['url']
        # american
        american_phonetic = result.select_one('.c-color-t~ td+ td .op_dict3_gap_small').text
        american_chinese_character = result.select_one('.c-color-t~ td+ td .op_dict3_font14').text
        american_audio_link = result.find('a', class_='op_dict3_how_read c-gap-right-middle')['url']

        defenition_notfixed = result.select_one('.c-gap-bottom-xsmall+ .op_dict3_english_result_table .op_dict_text2').text
        # removing all whitespace characters with regex since in not fixed variable they're all over the place.
        # replace('\n', '') or strip() methods doesn't helped
        defenition_fixed = re.sub(r'\s+', '', defenition_notfixed)
        
        answer_box.append({
          'english_word': english_word,
          'british': {'phonetic': british_phonetic, 'chinese_character': british_chinese_character, 'audio_link': british_audio_link},
          'american': {'phonetic': american_phonetic, 'chinese_character': american_chinese_character, 'audio_link': american_audio_link},
          'defenition': defenition_fixed,
        })

      print(json.dumps(answer_box, indent=2, ensure_ascii=False))

    except:
      print('No answer box found')

# Output:
'''
[
  {
    "english_word": "coffee",
    "british": {
      "phonetic": "[ˈkɒfi]",
      "chinese_character": "英",
      "audio_link": "https://sp0.baidu.com/-rM1hT4a2gU2pMbgoY3K/gettts?lan=uk&text=coffee&spd=2&source=alading"
    },
    "american": {
      "phonetic": "[ˈkɔːfi]",
      "chinese_character": "美",
      "audio_link": "https://sp0.baidu.com/-rM1hT4a2gU2pMbgoY3K/gettts?lan=uk&text=coffee&spd=2&source=alading"
    },
    "defenition": "(烘烤过的)咖啡豆;咖啡粉;咖啡(热饮料);一杯咖啡;"
  }
]
'''
```
### Using SerpApi Answer box
```python
import os, json
from serpapi import BaiduSearch


def get_answerbox_result():
    params = {
        "engine": "baidu",
        "q": "coffee",
        "api_key": os.getenv("API_KEY"),
    }

    search = BaiduSearch(params)
    results = search.get_dict()

    for result in results['answer_box']:
      title = result['title']
      link = result['link']
      displayed_link = result['displayed_link']
      english_word = result['english_word']
      british = result['british']
      american = result['american']
      defenitions = result['definitions'][0] # array output

      print(f'{title}\n{link}\n{displayed_link}\n{english_word}\n{british}\n{american}\n{defenitions}')

# Output:
'''
coffee - 百度翻译
http://www.baidu.com/link?url=JA5gottCkKOdztdz_enXoECH2LfUZwlDRs-ll_E7fa6TXpjY6hQzf1GzPU7gTxHkOTOTFpSm6g_6OlvRNqjjP_
fanyi.baidu.com
coffee
{'phonetic': '[ˈkɒfi]', 'chinese_character': '英', 'audio_link': 'https://sp0.baidu.com/-rM1hT4a2gU2pMbgoY3K/gettts?lan=uk&text=coffee&spd=2&source=alading'}
{'phonetic': '[ˈkɔːfi]', 'chinese_character': '美', 'audio_link': 'https://sp0.baidu.com/-rM1hT4a2gU2pMbgoY3K/gettts?lan=en&text=coffee&spd=2&source=alading'}
['n. (烘烤过的)咖啡豆; 咖啡粉; 咖啡(热饮料); 一杯咖啡;']
'''
```

### Related Images
```python
from bs4 import BeautifulSoup
import requests, lxml, re, json

headers = {
    "User-Agent":
    "Mozilla/5.0 (Linux; Android 10; HD1913) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.105 Mobile Safari/537.36 EdgA/46.1.2.5140"
}


def get_related_images_result():
    html = requests.get('https://www.baidu.com/s?&tn=baidu&wd=jet li',headers=headers)
    soup = BeautifulSoup(html.text, 'lxml')

    for related_image in soup.find_all('div', class_='op-img-address-divide-high'):
      link = related_image.a['href']
      image = related_image.a.img['src']
      print(f'{link}\n{image}\n')

# part of output:
'''
http://www.baidu.com/link?url=eSWgjIjvJxs9ihAwqPFMk0w0oeXDbwJ7Hi4mYNJzirGQ1ssl8BuLkI7GhtPPou-J2tYlh7CaMQhGC8uAStmiI7Kx2Ln8mNBobjTQ8J8elSeHIHbKy2UKJPMNB8Jv8C6JxzjRlSeOVeGhmGqg0HvT69706LMw5k7KX5V4aKLgkfTrDjYLwG1b9wRG_n4G752-MLNP_u0rJLwS0PGKAdIctA-oStoNf8efPJZmkExIpA6GZQ1-T0YyA445E9uAtWldweZwOFrZ5H-KzkT5xKW3e33kFyGrQV5Rb_li6YZ6VZ8M4K3ESwO6tzEex_eZxq_xrhRGddDw1LHTn1NmXqvsrkCEpPze5oAtsXNEaSMnSENi3q_qpTucgaWN8eDYk4ciQr42JVuv1cgrHKSf4_0dNwBhiAQB8uj6UIJFDZ-tFAIX1O2ZWQGhoBgpVm7DjVIVoVVraQx9PwZVTq80P3DhhH91U6QkSh4y1LmZJxHZVnRQ-_pZUJKircxw9ofSrgwSWNxkYo6NXwwn9ys9ggz12PHJo5IvjJRGFIlaEm1ZZHfuSfEusdI71L9RQWuSrWpxJiMqS-oqe_pSNgYxPD1PK_
https://dss0.bdstatic.com/70cFuHSh_Q1YnxGkpoWK1HF6hhy/it/u=2262600612,448000708&fm=26&gp=0.jpg
'''
```
### Using SerpApi Related Images
```python
import os, json
from serpapi import BaiduSearch


def get_related_images_result():
    params = {
        "engine": "baidu",
        "q": "jet li",
        "api_key": os.getenv("API_KEY"),
    }

    search = BaiduSearch(params)
    results = search.get_dict()
    
    for result in results['organic_results']:
      try:
        images = result['related_images']
      except:
        images = None
      print(images)

# part of the output:
'''
[{'link': 'http://www.baidu.com/link?url=YQnuO4njMj88UErWJBkGuS4aGdNiv9ZVtySw5fqiVpRTwmgJFEm_ZhCw9Zbc7U1C3Red20zd6N-FzwpURm5jDcnUsp34rhTHApNvnHuB3DlhwIu7-4BwuzlITjhSrXr0DgMBZGNt3UhgGNVTrybeZ6IPGD8Ej_oqSASrusItTQiAVlW-khcZ0A8Q1oWo6Dea_9u1gigFS30GAwBJGz4RdrnFmcyAo7AshuflPdptpcLWqx5TTYF0WjjQVVULBSRmETaEfEGIuO_YMoOKqGoc9d9d9o9QUmRClayPSf5xTppjPGYQGZmUDJ-93grTkqry63e4nXW460Lf-8ctZfnV36UTpWm-hmhXHw7pjATVT88Rmvbxo_hVLyH0dUNdapqsqTdl6YBYFA4k1JjmR5ibhDHd5tH1QuBc5XJVoG1HL-dxNjU_a3NecDeejZstG9zAr59ESZli63E8tgX1THSJ0xeY9G9VOZI-dx79kSg0pUyzctaux8jHWlh48D7qcg5sJCDh_V33kOnhTp9pbJqI3DR4r05Ma_WowxYUV87-pkMxmSnPXtK8Av6lCQgvz7tAFSmzLoPWmz5Fd_cSJ_yB7a', 'image': 'https://dss0.bdstatic.com/70cFuHSh_Q1YnxGkpoWK1HF6hhy/it/u=2262600612,448000708&fm=26&gp=0.jpg'}]
'''
```

### Differences between API and non-API solution
- fast solution and straightforward exploration.
- don't have to figure out how to grab certain elements.
- don't have to maintain the parser if things are changed in the HTML code.

### Links
Code in the [online IDE](https://replit.com/@DimitryZub1/Baidu-Search-Results-python-serpapi#main.py).
Documentation: [Baidu Organic Search Results API](https://serpapi.com/baidu-organic-results).

### Outro
If you have any questions or something isn't working correctly or you want to write something else, feel free to drop a comment in the comment section or via Twitter at [@serp_api](https://twitter.com/serp_api).

Yours,
Dimitry, and the rest of SerpApi Team.