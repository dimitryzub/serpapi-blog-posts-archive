👉**Briefly about the essence**: tutorial about how to extract Google Scholar Metrics results and store them to CSV using Python.

🔨**What is required**: Understanding of loops, data structures, exception handling and basic knowledge of `CSS` selectors. `requests`, `beautifulsoup`, `lxml`, `pandas` libraries.

⏱️**How long will it take**: ~15-30 minutes to read and implement.

___

- <a href="#what_will_be_scraped">What will be scraped</a>
- <a href="#prerequisites">Prerequisites</a>
- <a href="#top_publications">Scrape Top Publications</a>
- <a href="#mandates">Scrape Public Access Mandates</a>
- <a href="#links">Links</a>
- <a href="#outro">Outro</a>

___

<h2 id="what_will_be_scraped">What will be scraped</h2>

Top publications

![what_will_be_scrpaed_2_01](https://user-images.githubusercontent.com/78694043/148908051-5ae7632d-bcfb-4732-bb8d-5b6f31638fd2.jpg)

Public access mandates 

![what_will_be_scrpaed_1_01](https://user-images.githubusercontent.com/78694043/148908042-6c0f2637-8a5f-454a-8976-fa862e661f28.jpg)

📌Note: you have an option to save CSV file, but there will be no funder link. This blog post shows how to scrape funder link as well. 

If you don't need an explanation:
- [try the code in the online IDE](https://replit.com/@DimitryZub1/Scrape-Google-Scholar-Metrics-with-Python#main.py).

____

<h2 id="prerequisites">Prerequisites</h2>

**Basic knowledge scraping with CSS selectors**

`CSS` selectors declare which part of the markup a style applies to thus allowing to extract data from matching tags and attributes.

If you haven't scraped with `CSS` selectors, there's a dedicated blog post of mine about [how to use `CSS` selectors when web-scraping](https://serpapi.com/blog/web-scraping-with-css-selectors-using-python/) that covers what it is, pros and cons, and why they're matter from a web-scraping perspective.

**Separate virtual environment**

It's a thing that creates an independent set of installed libraries including different Python versions that can coexist with each other on  the same system prevention libraries or Python version conflicts when working on multiple projects at the same time.

If you didn't work with a virtual environment before, have a look at the dedicated [Python virtual environments tutorial using Virtualenv and Poetry](https://serpapi.com/blog/python-virtual-environments-using-virtualenv-and-poetry/) blog post of mine to get familiar.

📌Note: using virtual environment is not a strict requirement.

**Libraries**:

```lang-none
pip install requests lxml beautifulsoup4 pandas
```

**Reducing the chance of being blocked**

There's a chance that a request might be blocked. Have a look at [how to reduce the chance of being blocked while web-scraping](https://serpapi.com/blog/how-to-reduce-chance-of-being-blocked-while-web/) blog of mine, there's eleven methods to bypass blocks from most websites. 

In this blog post only saving HTML locally for the test was used to prevent blocks by sending multiple requests in a short period of time.
___


<h2 id="top_publications">Scrape Google Scholar Metrics all Top Publications</h2>

```python
import requests, lxml
from bs4 import BeautifulSoup
import pandas as pd

def scrape_all_metrics_top_publications():

    params = {
        "view_op": "top_venues",  # top publications results
        "hl": "en"                # language
    }

    html = requests.get("https://scholar.google.com/citations", params=params)
    soup = BeautifulSoup(html.text, "lxml").find("table")

    df = pd.DataFrame(pd.read_html(str(soup))[0])
    df.drop(df.columns[0], axis=1, inplace=True)
    
    df.insert(loc=2,
              column="h5-index link",
              value=[f'https://scholar.google.com/{link.a["href"]}' for link in soup.select(".gsc_mvt_t+ td")])

    df.to_csv("google_scholar_metrics_top_publications.csv", index=False)

    # save to csv for a specific language
    # df.to_csv(f"google_scholar_metrics_top_publications_lang_{params['hl']}.csv", index=False)
```

Create search query parameters:

```python
params = {
    "view_op": "top_venues",  # top publications results
    "hl": "en"                # language:
                              # pt - Portuguese
                              # sp - Spanish
                              # de - German
                              # ru - Russian
                              # fr - French
                              # ja - Japanese
                              # ko - Korean
                              # pl - Polish
                              # uk - Ukrainian
                              # id - Indonesian
}
```

Pass search query `params` to request and `find()` the `<table>` via `BeautifulSoup()`:

```python
html = requests.get("https://scholar.google.com/citations", params=params)
soup = BeautifulSoup(html.text, "lxml").find("table")
```

You can scrape table data without scraping with `BeautifulSoup()` first, but you won't have an option to save links from the table using `pandas` only. Scraping table with `BeautifulSoup()` will allow you to scrape links data as well once passed to `pandas` `read_html()`.

`read_html()`, access table data `[0]` from the `soup` and create a `DataFrame`:

```python
df = pd.DataFrame(pd.read_html(str(soup))[0])
```

Drop unnecessary numeration _"Unnamed"_ column:

```python
df.drop(df.columns[0], axis=1, inplace=True)
```

- `df.columns[0]` is the first column in the table. In this case it's _"Unnamed"_ column.
- `axis=1` will delete column instead of row.
- `inplace=True` allows doing operations on existing `DataFrame` without having to reassign to a new variable.


Insert a new column and add extracted links:

```python
df.insert(loc=2,
          column="h5-index link",
          value=[f'https://scholar.google.com/{link.a["href"]}' for link in soup.select(".gsc_mvt_t+ td")])
```

- `loc=2` is the location where column will be added.
- `columns=` is your column name.
- `value=` is your extracted value.

Save `to_csv()`:

```python
df.to_csv("google_scholar_metrics_top_publications.csv", index=False)
```

`index=False` to drop default `pandas` row numbers.

Save `to_csv()` for a specific language:

```python
df.to_csv(f"google_scholar_metrics_top_publications_lang_{params['hl']}.csv", index=False)
```

`params['hl']` is the language that will be passed to search query `params`.  

____

<h2 id="mandates">Scrape Google Scholar Metrics all Public Access Mandates</h2>


```python
import requests, lxml
from bs4 import BeautifulSoup
import pandas as pd

def scrape_all_metrics_public_mandates():
    
    params = {
        "view_op": "mandates_leaderboard",  # public access mandates results
        "hl": "en"                          # language
    }

    html = requests.get("https://scholar.google.com/citations", params=params)
    soup = BeautifulSoup(html.text, "lxml").find("table")

    df = pd.DataFrame(pd.read_html(str(soup))[0])
    df.drop(df.columns[[0, 2]], axis=1, inplace=True)

    df.insert(loc=1, 
              column="Funder Link", 
              value=[link.a["href"] for link in soup.select("td.gsc_mlt_t")])

    df.to_csv("google_scholar_metrics_public_access_mandates.csv", index=False)

    # save to csv for specific language
    # df.to_csv(f"google_scholar_metrics_public_access_mandates_lang_{params['hl']}.csv", index=False)
```

Create search query parameters:

```python
params = {
    "view_op": "mandates_leaderboard",  # public access mandates results
    "hl": "en"  # or other lang: pt, sp, de, ru, fr, ja, ko, pl, uk, id
}
```

Pass search query `params`, make a request and `find()` the `<table>` via `BeautifulSoup()`:

```python
html = requests.get("https://scholar.google.com/citations", params=params)
soup = BeautifulSoup(html.text, "lxml").find("table")
```

`read_html()`,access table data `[0]` and create a `DataFrame`:

```python
df = pd.DataFrame(pd.read_html(str(soup))[0])
```

Drop two unnecessary _"Unnamed, Available:"_ columns:

```python
df.drop(df.columns[[0, 2]], axis=1, inplace=True)
```

- `df.columns[[0, 2]]` is the first and third columns in the table. In this case it's _"Unnamed, Available:"_ columns.
- `axis=1` will delete column instead of row.
- `inplace=True` allows doing operations on existing `DataFrame` without having to reassign to a new variable.

Insert a new column and add extracted links:

```python
df.insert(loc=1, 
          column="Funder Link", 
          value=[link.a["href"] for link in soup.select("td.gsc_mlt_t")])
```

- `loc=1` is the location where column will be added.
- `columns=` is your column name.
- `value=` is your extracted value.

Save `to_cs()`:

```python
df.to_csv("google_scholar_metrics_public_access_mandates.csv", index=False)
```

`index=False` to drop default `pandas` row numbers.


Save `to_csv()` for a specific language:

```python
df.to_csv(f"google_scholar_metrics_public_access_mandates_lang_{params['hl']}.csv", index=False)
```

`params['hl']` is the language that will be passed to search query `params`.


___


<h2 id="links">Links</h2>

- [Code in the online IDE](https://replit.com/@DimitryZub1/Scrape-Google-Scholar-Metrics-with-Python#main.py)

___

<h2 id="outro">Outro</h2>

If you have anything to share, any questions, suggestions, or something that isn't working correctly, feel free to drop a comment in the comment section or reach out via Twitter at [@dimitryzub](https://twitter.com/DimitryZub), or [@serp_api](https://twitter.com/serp_api).

Yours,
Dimitry, and the rest of SerpApi Team.

___

<p style="text-align: center;">Join us on <a href="https://www.reddit.com/r/SerpApi/">Reddit</a> | <a href="https://twitter.com/serp_api">Twitter</a> | <a href="https://www.youtube.com/channel/UCUgIHlYBOD3yA3yDIRhg_mg">YouTube</a></p>

<p style="text-align: center;">Add a  <a href="https://forum.serpapi.com/feature-requests">Feature Request</a>💫 or a <a href="https://forum.serpapi.com/bugs">Bug</a>🐞</p>