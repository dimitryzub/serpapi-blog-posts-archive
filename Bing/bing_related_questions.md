Contents: intro, imports, what will be scraped, process, code, links, outro.

### Intro
This blog post is a continuation of Bing's web scraping series. Here will be shown how to scrape Related Questions from Bing search results using Python.

### Imports
```python
from bs4 import BeautifulSoup
import requests
import lxml
from serpapi import GoogleSearch
import os # for creating environment variable
```

### What will be scraped
![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/d0j72cjfmwruh3qke5er.png)


### Process
Everything below was done using [SelectorGadget](https://selectorgadget.com/) Chrome extension.

Selecting container `CSS` selector with needed data
<img width="100%" style="width:100%" src="https://media.giphy.com/media/uEURj8oJmUYIh0hTcq/giphy.gif">

Selecting question `CSS` selector
<img width="100%" style="width:100%" src="https://media.giphy.com/media/Rymj1LZGBaHqMWPfEv/giphy.gif">

Selecting snippet `CSS` selector
<img width="100%" style="width:100%" src="https://media.giphy.com/media/NqMRz990vxUZ4spVXW/giphy.gif">

Selecting title `CSS` selector
<img width="100%" style="width:100%" src="https://media.giphy.com/media/9A5xXLDTnHWRZrYxT7/giphy.gif">

Selecting title URL `CSS` selector
<img width="100%" style="width:100%" src="https://media.giphy.com/media/UBb7XPDQfbTb7ZdYZN/giphy.gif">

Selecting displayed URL `CSS` selector
<img width="100%" style="width:100%" src="https://media.giphy.com/media/Rymj1LZGBaHqMWPfEv/giphy.gif">

### Code
```python
from bs4 import BeautifulSoup
import requests, lxml

headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}

html = requests.get('https://www.bing.com/search?q=lion king&hl=en', headers=headers)
soup = BeautifulSoup(html.content, 'lxml')

for related_question in soup.select('#relatedQnAListDisplay .df_topAlAs'):
    question = related_question.select_one('.b_1linetrunc').text
    snippet = related_question.select_one('.rwrl_padref').text
    title = related_question.select_one('#relatedQnAListDisplay .b_algo p').text
    link = related_question.select_one('#relatedQnAListDisplay .b_algo a')['href']
    displayed_link = related_question.select_one('#relatedQnAListDisplay cite').text
    print(f'{question}\n{snippet}\n{title}\n{link}\n{displayed_link}\n')

# part of the output:
'''
What kind of game is The Lion King?
Jump on top of giraffe’s head and eat bugs in this awesome classic platformer game. The Lion King is a classic 1994 platformer video game based on the multi-award winning animated film of the same name. The game takes place after the death of Simba’s father where Simba was told a lie and forced to hide.
The Lion King - Play Game Online - ArcadeSpot.com
https://arcadespot.com/game/the-lion-king/
arcadespot.com/game/the-lion-king/
'''
```

### Using [Bing Related Questions API](https://serpapi.com/bing-related-questions)
SerpApi is a paid API with a free trial of 5,000 searches.

```python
from serpapi import GoogleSearch

params = {
    "api_key": "YOUR_API_KEY",
    "engine": "bing",
    "q": "lion king"
}

search = GoogleSearch(params)
results = search.get_dict()

for result in results['related_questions']:
    question = result['question']
    snippet = result['snippet']
    title = result['title']
    link = result['link']
    displayed_link = result['displayed_link']
    print(f'{question}\n{title}\n{link}\n{displayed_link}\n{snippet}\n')

# part of the output:
'''
Is the Lion King a circle of life?
Disney THE LION KING | Award-Winning Best Musical
https://www.lionking.com/
www.lionking.com/
Circle of Life in 360 - Experience THE LION KING like never before - WATCH IT NOW Quite Simply, Stunning. -TimeOut New York A Deeply Felt Celebration of Life.
'''
```

### Links
[Code in the online IDE](https://replit.com/@DimitryZub1/Bing-Scrape-Organic-Search-Results-Python-SerpApi#bs4_results/get_related_questions.py) • [Bing Related Questions API](https://serpapi.com/bing-related-questions)

### Outro
If you have any questions or something isn't working correctly or you want to write something else, feel free to drop a comment in the comment section or via Twitter at [@serp_api](https://twitter.com/serp_api).

Yours,
Dimitry, and the rest of SerpApi Team.