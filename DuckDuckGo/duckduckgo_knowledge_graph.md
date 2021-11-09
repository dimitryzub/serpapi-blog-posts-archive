Contents: intro, imports, what will be scraped, process, code, links, outro.

### Intro
This blog post is a continuation of the DuckDuckGo web scraping series. Here you'll see how to scrape Knowledge Graph Results using Python with `selenium` library. An alternative API solution will be shown.

### Imports
```python
from selenium import webdriver
```

### What will be scraped
![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/k3n6noaymuql1gcvnbej.png)


### Process

Selecting title, description, facts, profiles
<img width="100%" style="width:100%" src="https://media.giphy.com/media/pYTRCF4H88nk2O6O93/giphy.gif">


### Code
```python
from selenium import webdriver

driver = webdriver.Chrome(executable_path='path/to/chromedriver.exe')

# &iax=about - expanded knowledge graph that appears after you click on arrow down icon
driver.get('https://duckduckgo.com/?q=elon musk&kl=us-en&ia=web&iax=about')


title = driver.find_element_by_css_selector('.module__title__link').text

try:
    website = driver.find_element_by_css_selector('.js-about-item-link').text
except:
    website = None

description = driver.find_element_by_css_selector('.js-about-item-abstr').text.strip()
description_link = driver.find_element_by_css_selector('.js-about-item-more-at-inline').get_attribute('href')
thumbnail = driver.find_element_by_css_selector('.module__image img').get_attribute('src')
print(f"{title}\n{website}\n{description}\n{description_link}\n{thumbnail}")

for knowledge_graph_fact in driver.find_elements_by_css_selector('.js-about-module-content .about-info-box__info-row'):
    key_element = knowledge_graph_fact.find_element_by_css_selector('.js-about-module-content .about-info-box__info-label').text.replace(':', '').strip()
    key_value = knowledge_graph_fact.find_element_by_css_selector('.js-about-module-content .about-info-box__info-value').text.strip()
    print(f"{key_element}: {key_value}\n")

for profile in driver.find_elements_by_css_selector('.js-about-profile-link'):
    profile_name = profile.get_attribute('title')
    profile_link = profile.get_attribute('href')
    profile_thumbnail = f"https://duckduckgo.com{profile.find_element_by_css_selector('.js-about-profile-link .about-profiles__img').get_attribute('src')}"
    print(f'{profile_name}\n{profile_link}\n{profile_thumbnail}\n')

driver.quit()

-----------------------------------
'''
Elon Musk
None
Elon Reeve Musk is an entrepreneur and business magnate. He is the founder, CEO, and Chief Engineer at SpaceX; early stage investor, CEO, and Product Architect of Tesla, Inc.; founder of The Boring Company; and co-founder of Neuralink and OpenAI. A centibillionaire, Musk is one of the richest people in the world. Musk was born to a Canadian mother and South African father and raised in Pretoria, South Africa. He briefly attended the University of Pretoria before moving to Canada aged 17 to attend Queen's University. He transferred to the University of Pennsylvania two years later, where he received bachelor's degrees in economics and physics. He moved to California in 1995 to attend Stanford University but decided instead to pursue a business career, co-founding the web software company Zip2 with brother Kimbal. The startup was acquired by Compaq for $307 million in 1999. Musk co-founded online bank X.com that same year, which merged with Confinity in 2000 to form PayPal.
https://en.wikipedia.org/wiki/Elon_Musk
https://duckduckgo.com/i/15945ca0.jpg
Born: Elon Reeve Musk, June 28, 1971, Pretoria, South Africa
Citizenship: South Africa (1971–present), Canada (1971–present), United States (2002–present)
Alma mater: University of Pretoria, Queen's University, University of Pennsylvania (BS and BA, 1997)
Title: Founder, CEO and Chief Engineer of SpaceX, CEO and product architect of Tesla, Inc, Founder of The Boring Company and X.com (now part of PayPal), Co-founder of Neuralink, OpenAI, and Zip2
Partner(s): Grimes (2018–present)
Children: 7
Parent(s): Maye Musk (mother)
Relatives: Tosca Musk (sister), Kimbal Musk (brother), Lyndon Rive (cousin)

Wikipedia
https://en.wikipedia.org/wiki/Elon_Musk
https://duckduckgo.comhttps://duckduckgo.com/assets/icons/thirdparty/wikipedia.svg

Twitter
https://twitter.com/elonmusk
https://duckduckgo.comhttps://duckduckgo.com/assets/icons/thirdparty/twitter.svg
...
'''
```

### Using [DuckDuckGo Knowledge Graph API](https://serpapi.com/duckduckgo-knowledge-graph)
SerpApi is a paid API with a free plan.

The main difference is that there's no need for javascript rendering which is much faster way to scrape data and spending time to create and maintain the parser.
```python
from serpapi import GoogleSearch

params = {
  "api_key": "YOUR_API_KEY",
  "engine": "duckduckgo",
  "q": "elon musk",
  "kl": "us-en"
}

search = GoogleSearch(params)
results = search.get_dict()

for key, value in results['knowledge_graph'].items():
  print(f'{key}: {value}')

-------------------------
'''
title: Elon Musk
description: Elon Reeve Musk is an entrepreneur and business magnate. He is the founder, CEO, and Chief Engineer at SpaceX; early stage investor, CEO, and Product Architect of Tesla, Inc.; founder of The Boring Company; and co-founder of Neuralink and OpenAI. A centibillionaire, Musk is one of the richest people in the world. Musk was born to a Canadian mother and South African father and raised in Pretoria, South Africa. He briefly attended the University of Pretoria before moving to Canada aged 17 to attend Queen's University. He transferred to the University of Pennsylvania two years later, where he received bachelor's degrees in economics and physics. He moved to California in 1995 to attend Stanford University but decided instead to pursue a business career, co-founding the web software company Zip2 with brother Kimbal. The startup was acquired by Compaq for $307 million in 1999. Musk co-founded online bank X.com that same year, which merged with Confinity in 2000 to form PayPal.
thumbnail: https://duckduckgo.com/i/15945ca0.jpg
facts: {'born': 'Elon Reeve Musk, June 28, 1971, Pretoria, South Africa', 'citizenship': 'South Africa (1971–present), Canada (1971–present), United States (2002–present)', 'alma_mater': "University of Pretoria, Queen's University, University of Pennsylvania (BS and BA, 1997)", 'title': 'Founder, CEO and Chief Engineer of SpaceX, CEO and product architect of Tesla, Inc, Founder of The Boring Company and X.com (now part of PayPal), Co-founder of Neuralink, OpenAI, and Zip2', 'partner_s': 'Grimes (2018–present)', 'children': '7', 'parent_s': 'Maye Musk (mother)', 'relatives': 'Tosca Musk (sister), Kimbal Musk (brother), Lyndon Rive (cousin)'}
profiles: [{'name': 'Wikipedia', 'link': 'https://en.wikipedia.org/wiki/Elon_Musk', 'thumbnail': 'https://duckduckgo.com/assets/icons/thirdparty/wikipedia.svg'}, {'name': 'Twitter profile', 'link': 'https://twitter.com/elonmusk', 'thumbnail': 'https://duckduckgo.com/assets/icons/thirdparty/twitter.svg'}, {'name': 'Instagram profile', 'link': 'https://instagram.com/elonmusk', 'thumbnail': 'https://duckduckgo.com/assets/icons/thirdparty/instagram.svg'}, {'name': 'IMDb ID', 'link': 'https://www.imdb.com/name/nm1907769', 'thumbnail': 'https://duckduckgo.com/assets/icons/thirdparty/imdb.svg'}, {'name': 'Rotten Tomatoes ID', 'link': 'https://rottentomatoes.com/celebrity/elon-musk', 'thumbnail': 'https://duckduckgo.com/assets/icons/thirdparty/rt.svg'}, {'name': 'Spotify Artist ID', 'link': 'https://open.spotify.com/artist/2WUTOhBxG2HjyKYFJrcSPB', 'thumbnail': 'https://duckduckgo.com/assets/icons/thirdparty/spotify.svg'}, {'name': 'SoundCloud ID', 'link': 'https://soundcloud.com/user-209448905', 'thumbnail': 'https://duckduckgo.com/assets/icons/thirdparty/soundcloud.svg'}, {'name': 'iTunes artist ID', 'link': 'https://itunes.apple.com/artist/1497370136', 'thumbnail': 'https://duckduckgo.com/assets/icons/thirdparty/apple.svg'}]
'''
```


### Links
[GitHub Gist](https://gist.github.com/dimitryzub/5f2dc5b63bad02bd1ed1014d49b8e7ce) • [DuckDuckGo Knowledge Graph API](https://serpapi.com/duckduckgo-knowledge-graph)


### Outro
If you have any questions or something isn't working correctly or you want to write something else, feel free to drop a comment in the comment section or via Twitter at [@serp_api](https://twitter.com/serp_api).

Yours,
Dimitry, and the rest of SerpApi Team.