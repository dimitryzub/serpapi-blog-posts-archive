🔨**What is required**: Understanding of loops, data structures, exception handling. `serpapi`, `pandas`, `urllib` libraries.

⏱️**How long will it take**: ~15-30 minutes to read and implement.

___

- <a href="#what_will_be_scraped">What will be scraped</a>
- <a href="#prerequisites">Prerequisites</a>
- <a href="#process">Process</a>
  - <a href="#profile_results">Profile Results</a>
  - <a href="#author_results">Author Results</a>
  - <a href="#author_article_results">All Author Article Results</a>
  - <a href="#save_to_csv">Save to CSV</a>
- <a href="#full_code">Full Code</a>
- <a href="#links">Links</a>
- <a href="#outro">Outro</a>

___

<h2 id="what_will_be_scraped">What will be scraped</h2>

![scrape_google_scholar_profile_authors_what_will_be_scraped_02](https://user-images.githubusercontent.com/78694043/148065237-118fe14d-59d7-44d1-a79f-160b76605cd0.jpg)

____

<h2 id="prerequisites">Prerequisites</h2>

**Separate virtual environment**

In short, it's a thing that creates an independent set of installed libraries including different Python versions that can coexist with each other at the same system thus prevention libraries or Python version conflicts.

If you didn't work with a virtual environment before, have a look at the dedicated [Python virtual environments tutorial using Virtualenv and Poetry](https://serpapi.com/blog/python-virtual-environments-using-virtualenv-and-poetry/) blog post of mine to get familiar.


**Install libraries**:

```lang-none
pip install pandas, google-search-results 
```

___

<h2 id="process">Process</h2>

![scrape_google_scholar_profile_authors_process_01](https://user-images.githubusercontent.com/78694043/148172984-e090fea9-305a-46d5-b7b1-041682875fd5.jpg)



If you don't need an explanation:
- <a href="#full_code">jump to the full code section</a>,
- [grab the full code from the GitHub repository](https://github.com/dimitryzub/py-scrape-google-scholar-profile-author-to-csv),
- [try it in the online IDE](https://replit.com/@DimitryZub1/Scrape-Google-Scholar-Profile-Results-from-all-Pages#main.py).



![scrape_google_scholar_profile_authors_profile_01](https://user-images.githubusercontent.com/78694043/148173001-a72d82d6-2795-47b7-aa84-b6182c48e2f9.jpg)


<h2 id="profile_results">Scrape all Google Scholar Profile Results</h2>


```python
import os
from serpapi import GoogleSearch
from urllib.parse import urlsplit, parse_qsl
import pandas as pd

def profile_results():

    print("Extracting profile results..")

    params = {
        "api_key": os.getenv("API_KEY"),      # SerpApi API key
        "engine": "google_scholar_profiles",  # profile results search engine
        "mauthors": "blizzard",               # search query
    }
    search = GoogleSearch(params)

    profile_results_data = []

    profiles_is_present = True
    while profiles_is_present:

        profile_results = search.get_dict()

        for profile in profile_results.get("profiles", []):

            print(f'Currently extracting {profile.get("name")} with {profile.get("author_id")} ID.')

            thumbnail = profile.get("thumbnail")
            name = profile.get("name")
            link = profile.get("link")
            author_id = profile.get("author_id")
            affiliations = profile.get("affiliations")
            email = profile.get("email")
            cited_by = profile.get("cited_by")
            interests = profile.get("interests")

            profile_results_data.append({
                "thumbnail": thumbnail,
                "name": name,
                "link": link,
                "author_id": author_id,
                "email": email,
                "affiliations": affiliations,
                "cited_by": cited_by,
                "interests": interests
            })

            if "next" in profile_results["pagination"]:
                search.params_dict.update(dict(parse_qsl(urlsplit(profile_results["pagination"]["next"]).query)))
            else:
                profiles_is_present = False

    return profile_results_data
```

#### Scraping all profile results explanation

Import libraries:

```python
import os
from serpapi import GoogleSearch
from urllib.parse import urlsplit, parse_qsl
import pandas as pd
```

Pass search parameters to SerpApi and create a temp `list()`:

```python
params = {
    "api_key": os.getenv("API_KEY"),      # SerpApi API key
    "engine": "google_scholar_profiles",  # profile results search engine
    "mauthors": "blizzard",               # search query
}
search = GoogleSearch(params)

profile_results_data = []
```

Set up a `while` loop and add a `if` statement to exit the `while` loop if no pages left:

```python
profiles_is_present = True
while profiles_is_present:

    profile_results = search.get_dict()
    
    # for loop extraction here..
    
    # if next page in SerpApi pagination -> update params to new a page results.
    # if no next page -> exit the while loop.
    if "next" in profile_results.get("pagination", []):
        search.params_dict.update(dict(parse_qsl(urlsplit(profile_results.get("pagination").get("next")).query)))
    else:
        profiles_is_present = False
```

Iterate over profile results in a `for` loop:

```python
for profile in profile_results.get("profiles", []):

    print(f'Currently extracting {profile.get("name")} with {profile.get("author_id")} ID.')

    thumbnail = profile.get("thumbnail")
    name = profile.get("name")
    link = profile.get("link")
    author_id = profile.get("author_id")
    affiliations = profile.get("affiliations")
    email = profile.get("email")
    cited_by = profile.get("cited_by")
    interests = profile.get("interests")
```

Append extracted data to temporary `list` as a dictionary and `return` it:

```python
profile_results_data.append({
    "thumbnail": thumbnail,
    "name": name,
    "link": link,
    "author_id": author_id,
    "email": email,
    "affiliations": affiliations,
    "cited_by": cited_by,
    "interests": interests

return profile_results_data

# example output:
'''
Extracting profile results..
Currently extracting Adam Lobel with _xwYD2sAAAAJ ID.
... other profiles

[
  {
    "thumbnail": "https://scholar.googleusercontent.com/citations?view_op=small_photo&user=_xwYD2sAAAAJ&citpid=3",
    "name": "Adam Lobel",
    "link": "https://scholar.google.com/citations?hl=en&user=_xwYD2sAAAAJ",
    "author_id": "_xwYD2sAAAAJ",
    "email": "Verified email at AdamLobel.com",
    "affiliations": "Blizzard Entertainment",
    "cited_by": 2935,
    "interests": [
      {
        "title": "Gaming",
        "serpapi_link": "https://serpapi.com/search.json?engine=google_scholar_profiles&hl=en&mauthors=label%3Agaming",
        "link": "https://scholar.google.com/citations?hl=en&view_op=search_authors&mauthors=label:gaming"
      },
      {
        "title": "Emotion regulation",
        "serpapi_link": "https://serpapi.com/search.json?engine=google_scholar_profiles&hl=en&mauthors=label%3Aemotion_regulation",
        "link": "https://scholar.google.com/citations?hl=en&view_op=search_authors&mauthors=label:emotion_regulation"
      }
    ]
  },
  ... other profiles
]
'''
```

____

![scrape_google_scholar_profile_authors_authors_01](https://user-images.githubusercontent.com/78694043/148173012-9cda102e-571c-409c-a775-2d3551a61254.jpg)



<h2 id="author_results">Scrape Google Scholar Author Results</h2>

```python
import os
from serpapi import GoogleSearch
from google_scholar_profile_results import profile_results
from urllib.parse import urlsplit, parse_qsl
import pandas as pd

def author_results():

    print("extracting author results..")

    author_results_data = []

    for author_id in profile_results():

        print(f"Parsing {author_id['author_id']} author ID.")

        params = {
            "api_key": os.getenv("API_KEY"),      # SerpApi API key
            "engine": "google_scholar_author",    # author results search engine
            "author_id": author_id["author_id"],  # search query
            "hl": "en"
        }
        search = GoogleSearch(params)
        results = search.get_dict()

        thumbnail = results.get("author").get("thumbnail")
        name = results.get("author").get("name")
        affiliations = results.get("author").get("affiliations")
        email = results.get("author").get("email")
        website = results.get("author").get("website")
        interests = results.get("author").get("interests")

        cited_by_table = results.get("cited_by", {}).get("table")
        cited_by_graph = results.get("cited_by", {}).get("graph")

        public_access_link = results.get("public_access", {}).get("link")
        available_public_access = results.get("public_access", {}).get("available")
        not_available_public_access = results.get("public_access", {}).get("not_available")
        co_authors = results.get("co_authors")

        author_results_data.append({
          "thumbnail": thumbnail,
          "name": name,
          "affiliations": affiliations,
          "email": email,
          "website": website,
          "interests": interests,
          "cited_by_table": cited_by_table,
          "cited_by_graph": cited_by_graph,
          "public_access_link": public_access_link,
          "available_public_access": available_public_access,
          "not_available_public_access": not_available_public_access,
          "co_authors": co_authors
        })

    return author_results_data
```

#### Scraping author results explanation

Import `profile_results()` function and other libraries:

```python
import os
from serpapi import GoogleSearch
from google_scholar_profile_results import profile_results
from urllib.parse import urlsplit, parse_qsl
import pandas as pd
```

`profile_results()` will iterate over all available pages and return a dictionary including author ID result, for example `_xwYD2sAAAAJ`. 

Create temporary `list` to store extracted data:

```python
author_results_data = []
```

Iterate over extracted profiles, pass`author_id` to `author_id` search parameter:

```python
for author_id in profile_results():

    print(f"Parsing {author_id['author_id']} author ID.")

    params = {
        "api_key": os.getenv("API_KEY"),      # SerpApi API key
        "engine": "google_scholar_author",    # author results search engine
        "author_id": author_id["author_id"],  # search query: _xwYD2sAAAAJ
        "hl": "en"
    }
    search = GoogleSearch(params)
    results = search.get_dict()
```

Extract the data: 

```python
thumbnail = results.get("author").get("thumbnail")
name = results.get("author").get("name")
affiliations = results.get("author").get("affiliations")
email = results.get("author").get("email")
website = results.get("author").get("website")
interests = results.get("author").get("interests")

cited_by_table = results.get("cited_by", {}).get("table")
cited_by_graph = results.get("cited_by", {}).get("graph")

public_access_link = results.get("public_access", {}).get("link")
available_public_access = results.get("public_access", {}).get("available")
not_available_public_access = results.get("public_access", {}).get("not_available")
co_authors = results.get("co_authors")
```

Append extracted data to temporary `list` as a dictionary and `return` it:

```python
author_results_data.append({
    "thumbnail": thumbnail,
    "name": name,
    "affiliations": affiliations,
    "email": email,
    "website": website,
    "interests": interests,
    "cited_by_table": cited_by_table,
    "cited_by_graph": cited_by_graph,
    "public_access_link": public_access_link,
    "available_public_access": available_public_access,
    "not_available_public_access": not_available_public_access,
    "co_authors": co_authors
})

return author_results_data


# example output:
'''
extracting author results..
Extracting profile results..
Currently extracting Adam Lobel with _xwYD2sAAAAJ ID.
... other authors
Parsing _xwYD2sAAAAJ author ID.
... other authors

[
  {
    "thumbnail": "https://scholar.googleusercontent.com/citations?view_op=view_photo&user=_xwYD2sAAAAJ&citpid=3",
    "name": "Adam Lobel",
    "affiliations": "Blizzard Entertainment",
    "email": "Verified email at AdamLobel.com",
    "website": "https://twitter.com/GrowingUpGaming",
    "interests": [
      {
        "title": "Gaming",
        "link": "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=label:gaming",
        "serpapi_link": "https://serpapi.com/search.json?engine=google_scholar_profiles&hl=en&mauthors=label%3Agaming"
      },
      {
        "title": "Emotion regulation",
        "link": "https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=label:emotion_regulation",
        "serpapi_link": "https://serpapi.com/search.json?engine=google_scholar_profiles&hl=en&mauthors=label%3Aemotion_regulation"
      }
    ],
    "cited_by_table": [
      {
        "citations": {
          "all": 2935,
          "since_2017": 2348
        }
      },
      {
        "h_index": {
          "all": 10,
          "since_2017": 10
        }
      },
      {
        "i10_index": {
          "all": 11,
          "since_2017": 10
        }
      }
    ],
    "cited_by_graph": [
      {
        "year": 2014,
        "citations": 70
      },
      {
        "year": 2015,
        "citations": 188
      },
      {
        "year": 2016,
        "citations": 243
      },
      {
        "year": 2017,
        "citations": 342
      },
      {
        "year": 2018,
        "citations": 420
      },
      {
        "year": 2019,
        "citations": 553
      },
      {
        "year": 2020,
        "citations": 507
      },
      {
        "year": 2021,
        "citations": 504
      },
      {
        "year": 2022,
        "citations": 16
      }
    ],
    "public_access_link": "https://scholar.google.com/citations?view_op=list_mandates&hl=en&user=_xwYD2sAAAAJ",
    "available_public_access": 1,
    "not_available_public_access": 0,
    "co_authors": [
      {
        "name": "Isabela Granic",
        "link": "https://scholar.google.com/citations?user=4T5cjVIAAAAJ&hl=en",
        "serpapi_link": "https://serpapi.com/search.json?author_id=4T5cjVIAAAAJ&engine=google_scholar_author&hl=en",
        "author_id": "4T5cjVIAAAAJ",
        "affiliations": "Radboud University Nijmegen",
        "email": "Verified email at pwo.ru.nl",
        "thumbnail": "https://scholar.googleusercontent.com/citations?view_op=small_photo&user=4T5cjVIAAAAJ&citpid=4"
      },
      ... other co-authors
      }
    ]
  }
  ... other authors
]
'''
```

<h2 id="author_article_results">Scrape all Author Articles from Google Scholar</h2>

```python
import os
from serpapi import GoogleSearch
from google_scholar_profile_results import profile_results
from urllib.parse import urlsplit, parse_qsl
import pandas as pd

def all_author_articles():

    author_article_results_data = []

    for index, author_id in enumerate(profile_results(), start=1):

        print(f"Parsing {index} author with {author_id['author_id']} author ID.")

        params = {
            "api_key": os.getenv("API_KEY"),     # SerpApi API key
            "engine": "google_scholar_author",   # author results search engine
            "hl": "en",                          # language
            "sort": "pubdate",                   # sort by year
            "author_id": author_id["author_id"]  # search query
        }
        search = GoogleSearch(params)

        articles_is_present = True
        while articles_is_present:

            results = search.get_dict()

            for article in results.get("articles", []):
                title = article.get("title")
                link = article.get("link")
                citation_id = article.get("citation_id")
                authors = article.get("authors")
                publication = article.get("publication")
                cited_by_value = article.get("cited_by", {}).get("value")
                cited_by_link = article.get("cited_by", {}).get("link")
                cited_by_cites_id = article.get("cited_by", {}).get("cites_id")
                year = article.get("year")
  
                author_article_results_data.append({
                    "article_title": title,
                    "article_link": link,
                    "article_year": year,
                    "article_citation_id": citation_id,
                    "article_authors": authors,
                    "article_publication": publication,
                    "article_cited_by_value": cited_by_value,
                    "article_cited_by_link": cited_by_link,
                    "article_cited_by_cites_id": cited_by_cites_id,
                })
    
          if "next" in results.get("serpapi_pagination", []):
              search.params_dict.update(dict(parse_qsl(urlsplit(results.get("serpapi_pagination").get("next")).query)))
          else:
              articles_is_present = False

    return author_article_results_data
```

#### Scraping all author articles explanation 

Import `profile_results()` function and other libraries:

```python
import os
from serpapi import GoogleSearch
from google_scholar_profile_results import profile_results
from urllib.parse import urlsplit, parse_qsl
import pandas as pd
```

In this case `profile_results()` was used to get `author_id` as well, in order to parse author articles.

Create temporary `list` to store extracted data:
```python
author_article_results_data = []
```

Iterate over `profile_results()` and pass `author_id` to parameter search query:

```python
for index, author_id in enumerate(profile_results(), start=1):

    print(f"Parsing {index} author with {author_id['author_id']} author ID.")
  
    params = {
        "api_key": os.getenv("API_KEY"),     # SerpApi API key
        "engine": "google_scholar_author",   # author results search engine
        "hl": "en",                          # language
        "sort": "pubdate",                   # sort by year
        "author_id": author_id["author_id"]  # search query
    }
    search = GoogleSearch(params)
```

Set up a `while` loop and check `if` next page is present:

```python
articles_is_present = True
while articles_is_present:
    results = search.get_dict()
    
    # data extraction code..
    
    # if next page is present -> update previous results to new page results.
    # if next page is not present -> exit the while loop.
    if "next" in results.get("serpapi_pagination", []):
      search.params_dict.update(dict(parse_qsl(urlsplit(results.get("serpapi_pagination").get("next")).query)))
    else:
      articles_is_present = False
```

Extract data in a `for` loop:

```python
for article in results.get("articles", []):
    title = article.get("title")
    link = article.get("link")
    citation_id = article.get("citation_id")
    authors = article.get("authors")
    publication = article.get("publication")
    cited_by_value = article.get("cited_by", {}).get("value")
    cited_by_link = article.get("cited_by", {}).get("link")
    cited_by_cites_id = article.get("cited_by", {}).get("cites_id")
    year = article.get("year")
```

`Append` extracted data to temporary `list` as a dictionary:

```python
author_article_results_data.append({
    "article_title": title,
    "article_link": link,
    "article_year": year,
    "article_citation_id": citation_id,
    "article_authors": authors,
    "article_publication": publication,
    "article_cited_by_value": cited_by_value,
    "article_cited_by_link": cited_by_link,
    "article_cited_by_cites_id": cited_by_cites_id,
})
```

`Return` extracted data:

```python
return author_article_results_data
```

___

![scrape_google_scholar_profile_authors_save_to_csv_03](https://user-images.githubusercontent.com/78694043/148173050-ab105a37-2dcc-45c9-a768-120a54a49094.jpg)


<h2 id="save_to_csv">Save Google Scholar Profile and Author Results to CSV</h2>

```python
from google_scholar_profile_results import profile_results
import pandas as pd

def save_profile_results_to_csv():
    print("Waiting for profile results to save..")
    pd.DataFrame(data=profile_results()).to_csv("google_scholar_profile_results.csv", encoding="utf-8", index=False)

    print("Profile Results Saved.")

    
def save_author_result_to_csv():
    print("Waiting for author results to save..")
    pd.DataFrame(data=profile_results()).to_csv("google_scholar_author_results.csv", encoding="utf-8", index=False)

    print("Author Results Saved.")


def save_author_articles_to_csv():
    print("Waiting for author articles to save..")
    pd.DataFrame(data=profile_results()).to_csv("google_scholar_author_articles.csv", encoding="utf-8", index=False)

    print("Author Articles Saved.")
```

- `data` argument inside `DataFrame` is your data.
- `encoding='utf-8'` argument just to make sure everything will be saved correctly. I used it explicitly even thought it's a default value.
- [`index=False`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.index.html) argument to drop default `pandas` row numbers.


___

<h2 id="full_code">Full Code</h2>

```python
import os
from serpapi import GoogleSearch
from urllib.parse import urlsplit, parse_qsl
import pandas as pd


def profile_results():
    print("Extracting profile results..")

    params = {
        "api_key": os.getenv("API_KEY"),      # SerpApi API key
        "engine": "google_scholar_profiles",  # profile results search engine
        "mauthors": "blizzard",               # search query
    }
    search = GoogleSearch(params)

    profile_results_data = []

    profiles_is_present = True
    while profiles_is_present:
        profile_results = search.get_dict()

        for profile in profile_results.get("profiles", []):

            print(f'Currently extracting {profile.get("name")} with {profile.get("author_id")} ID.')

            thumbnail = profile.get("thumbnail")
            name = profile.get("name")
            link = profile.get("link")
            author_id = profile.get("author_id")
            affiliations = profile.get("affiliations")
            email = profile.get("email")
            cited_by = profile.get("cited_by")
            interests = profile.get("interests")

            profile_results_data.append({
                "thumbnail": thumbnail,
                "name": name,
                "link": link,
                "author_id": author_id,
                "email": email,
                "affiliations": affiliations,
                "cited_by": cited_by,
                "interests": interests
            })

        if "next" in profile_results.get("pagination", []):
            search.params_dict.update(dict(parse_qsl(urlsplit(profile_results.get("pagination").get("next")).query)))
        else:
            profiles_is_present = False

    return profile_results_data


def author_results():
    print("extracting author results..")

    author_results_data = []

    for author_id in profile_results():

        print(f"Parsing {author_id['author_id']} author ID.")

        params = {
            "api_key": os.getenv("API_KEY"),      # SerpApi API key
            "engine": "google_scholar_author",    # author results search engine
            "author_id": author_id["author_id"],  # search query
            "hl": "en"
        }
        search = GoogleSearch(params)
        results = search.get_dict()

        thumbnail = results.get("author").get("thumbnail")
        name = results.get("author").get("name")
        affiliations = results.get("author").get("affiliations")
        email = results.get("author").get("email")
        website = results.get("author").get("website")
        interests = results.get("author").get("interests")

        cited_by_table = results.get("cited_by", {}).get("table")
        cited_by_graph = results.get("cited_by", {}).get("graph")

        public_access_link = results.get("public_access", {}).get("link")
        available_public_access = results.get("public_access", {}).get("available")
        not_available_public_access = results.get("public_access", {}).get("not_available")
        co_authors = results.get("co_authors")

        author_results_data.append({
            "thumbnail": thumbnail,
            "name": name,
            "affiliations": affiliations,
            "email": email,
            "website": website,
            "interests": interests,
            "cited_by_table": cited_by_table,
            "cited_by_graph": cited_by_graph,
            "public_access_link": public_access_link,
            "available_public_access": available_public_access,
            "not_available_public_access": not_available_public_access,
            "co_authors": co_authors
        })

    return author_results_data


def all_author_articles():
    author_article_results_data = []

    for index, author_id in enumerate(profile_results(), start=1):

        print(f"Parsing author #{index} with {author_id['author_id']} author ID.")

        params = {
            "api_key": os.getenv("API_KEY"),     # SerpApi API key
            "engine": "google_scholar_author",   # author results search engine
            "hl": "en",                          # language
            "sort": "pubdate",                   # sort by year
            "author_id": author_id["author_id"]  # search query
        }
        search = GoogleSearch(params)

        articles_is_present = True
        while articles_is_present:
            results = search.get_dict()

            for article in results.get("articles", []):
                title = article.get("title")
                link = article.get("link")
                citation_id = article.get("citation_id")
                authors = article.get("authors")
                publication = article.get("publication")
                cited_by_value = article.get("cited_by", {}).get("value")
                cited_by_link = article.get("cited_by", {}).get("link")
                cited_by_cites_id = article.get("cited_by", {}).get("cites_id")
                year = article.get("year")

                author_article_results_data.append({
                    "article_title": title,
                    "article_link": link,
                    "article_year": year,
                    "article_citation_id": citation_id,
                    "article_authors": authors,
                    "article_publication": publication,
                    "article_cited_by_value": cited_by_value,
                    "article_cited_by_link": cited_by_link,
                    "article_cited_by_cites_id": cited_by_cites_id,
                })

            if "next" in results.get("serpapi_pagination", []):
                search.params_dict.update(dict(parse_qsl(urlsplit(results.get("serpapi_pagination").get("next")).query)))
            else:
                articles_is_present = False

    return author_article_results_data


def save_author_result_to_csv():
    print("Waiting for author results to save..")
    pd.DataFrame(data=profile_results()).to_csv("google_scholar_author_results.csv", encoding="utf-8", index=False)

    print("Author Results Saved.")


def save_author_articles_to_csv():
    print("Waiting for author articles to save..")
    pd.DataFrame(data=profile_results()).to_csv("google_scholar_author_articles.csv", encoding="utf-8", index=False)

    print("Author Articles Saved.")


def save_profile_results_to_csv():
    print("Waiting for profile results to save..")
    pd.DataFrame(data=profile_results()).to_csv("google_scholar_profile_results.csv", encoding="utf-8", index=False)

    print("Profile Results Saved.")
```

___


<h2 id="links">Links</h2>

- [GitHub repository](https://github.com/dimitryzub/py-scrape-google-scholar-profile-author-to-csv)
- [Code in the online IDE](https://replit.com/@DimitryZub1/Scrape-Google-Scholar-Profile-Results-from-all-Pages#main.py)
- [Google Scholar Profiles API](https://serpapi.com/google-scholar-profiles-api)
- [Google Scholar Author API](https://serpapi.com/google-scholar-author-api)

___

<h2 id="outro">Outro</h2>

If your goal is to extract data without the need to write a parser from scratch, figure out how to bypass blocks from search engines, how to scale it or how to extract data from JavaScript - [have a try SerpApi](https://serpapi.com/).

If you have anything to share, any questions, suggestions, or something that isn't working correctly, feel free to drop a comment in the comment section or reach out via Twitter at [@dimitryzub](https://twitter.com/DimitryZub), or [@serp_api](https://twitter.com/serp_api).

___

<p style="text-align: center;">Join us on <a href="https://www.reddit.com/r/SerpApi/">Reddit</a> | <a href="https://twitter.com/serp_api">Twitter</a> | <a href="https://www.youtube.com/channel/UCUgIHlYBOD3yA3yDIRhg_mg">YouTube</a></p>

<p style="text-align: center;">Add a  <a href="https://forum.serpapi.com/feature-requests">Feature Request</a>💫 or a <a href="https://forum.serpapi.com/bugs">Bug</a>🐞</p>