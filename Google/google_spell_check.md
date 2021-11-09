Contents: intro, imports, what will be scraped, process, code, links, outro.

### Intro
This blog post is a continuation of Google's web scraping series. Here you'll see examples of how you can scrape Google Spell Check with Python. An alternative API solution will be shown.


### Imports
```python
from bs4 import BeautifulSoup
import requests, lxml
from serpapi import GoogleSearch
```

### What will be scraped
![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/bh5xqgj7mubu7z6wu29w.png)


### Process
Selecting `CSS` selector that support autocompletion on all languages
<img width="100%" style="width:100%" src="https://media.giphy.com/media/5H32C40aVuWPJeGnT1/giphy.gif">

Process of using SerpApi from the playground search query to the final output
<img width="100%" style="width:100%" src="https://media.giphy.com/media/La93jnCuKdhZlU6G2f/giphy.gif">


### Code
```python
from bs4 import BeautifulSoup
import requests, lxml

headers = {
    'User-agent':
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}

params = {
  'q': 'fush ro dah',
  'hl': 'en',
  'gl': 'us',
}

html = requests.get('https://www.google.com/search?q=', headers=headers, params=params).text
soup = BeautifulSoup(html, 'lxml')

corrected_word = soup.select_one('a.gL9Hy').text
corrected_word_link = f"https://www.google.com{soup.select_one('a.gL9Hy')['href']}"
search_instead_for = soup.select_one('a.spell_orig').text
search_instead_for_link = f"https://www.google.com{soup.select_one('a.spell_orig')['href']}"
print(f'{corrected_word}\n{corrected_word_link}\nSearch instead: {search_instead_for}\n{search_instead_for_link}')

-------
'''
fus ro dah
https://www.google.com/search?hl=en&gl=us&q=fus+ro+dah&spell=1&sa=X&ved=2ahUKEwiIwb3ykMzxAhVWSzABHQtlDeMQkeECKAB6BAgBEDA
Search instead: fush ro dah
https://www.google.com/search?hl=en&gl=us&q=fush+ro+dah&nfpr=1&sa=X&ved=2ahUKEwiIwb3ykMzxAhVWSzABHQtlDeMQvgUoAXoECAEQMQ
'''
```

### Using [Google Spell Check API](https://serpapi.com/spell-check)
SerpApi is a paid API with a free trial of 5,000 searches.



```python
from serpapi import GoogleSearch
import os

params = {
  "api_key": os.environ["API_KEY"],
  "engine": "google",
  "q": "fus ro dish",
  "gl": "us",
  "hl": "en"
}

search = GoogleSearch(params)
results = search.get_dict()

print(results['search_information']['organic_results_state'])
print(results['search_information']['spelling_fix'])

--------
'''
Some results for exact spelling but showing fixed spelling
fus ro dah
'''
```


### Links
[Code in the online IDE](https://replit.com/@DimitryZub1/Google-Search-Scrape-Spell-Check-python-serpapi#bs4_result.py) • [Google Spell Check API](https://serpapi.com/spell-check)

### Outro
If you have any questions or something isn't working correctly or you want to write something else, feel free to drop a comment in the comment section or via Twitter at [@serp_api](https://twitter.com/serp_api).

Yours,
Dimitry, and the rest of SerpApi Team