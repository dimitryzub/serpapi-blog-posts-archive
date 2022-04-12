👉**Briefly about the essence**: showcase how to extract Google Scholar Case Law results and save it to CSV using `pandas` and `serpapi` library.

🔨**What is required**: understanding of loops, data structures, exception handling. `serpapi`, `pandas`, `urllib` libraries.

⏱️**How long will it take**: ~10-20 minutes to read and implement.

___

- <a href="#intro">Intro</a>
- <a href="#what_will_be_scraped">What will be scraped</a>
- <a href="#prerequisites">Prerequisites</a>
- <a href="#process">Process</a>
  - <a href="#full_code">Scrape and Save Case Law results</a>
- <a href="#links">Links</a>
- <a href="#outro">Outro</a>

___

<h2 id="intro">Intro</h2>

This tutorial-demo blog post will show and guide you through the process of scraping Google Scholar Case Law results from all available pages based on the given search query using SerpApi [`google-search-results` library](https://pypi.org/project/google-search-results/).

<h2 id="what_will_be_scraped">What will be scraped</h2>


![scrape_google_scholar_case_law_what_will_be_scraped_01](https://user-images.githubusercontent.com/78694043/148174521-697e4c31-25bc-47da-883b-0f5176fd7b58.jpg)

<h2 id="prerequisites">Prerequisites</h2>

**Separate virtual environment**

If you didn't work with a virtual environment before, have a look at the dedicated [Python virtual environments tutorial using Virtualenv and Poetry](https://serpapi.com/blog/python-virtual-environments-using-virtualenv-and-poetry/) blog post of mine to get familiar.

In short, it's a thing that creates an independent set of installed libraries including different Python versions that can coexist with each other at the same system thus prevention libraries or Python version conflicts.

**Install libraries**:

```lang-none
pip install pandas
pip install google-search-results  
```

___

<h2 id="process">Process</h2>

If you don't need an explanation, [try it in the online IDE](https://replit.com/@DimitryZub1/Scrape-Google-Scholar-Case-Law-Results-to-CSV#main.py).


<h2 id="full_code">Scrape and save Google Scholar Case Law results to CSV</h2>

```python
import os
from serpapi import GoogleSearch
from urllib.parse import urlsplit, parse_qsl
import pandas as pd

def case_law_results():

    print("Extracting case law results..")

    params = {
        "api_key": os.getenv("API_KEY"),  # SerpApi API key
        "engine": "google_scholar",       # Google Scholar search results
        "q": "minecraft education ",      # search query
        "hl": "en",                       # language
        "start": "0",                     # first page
        "as_sdt": "6"                     # case law results. Wierd, huh? Try without it.
    }
    search = GoogleSearch(params)

    case_law_results_data = []

    loop_is_true = True
    while loop_is_true:
      results = search.get_dict()

      print(f"Currently extracting page №{results['serpapi_pagination']['current']}..")

      for result in results["organic_results"]:
        title = result["title"]
        publication_info_summary = result["publication_info"]["summary"]
        result_id = result["result_id"]
        link = result["link"]
        result_type = result.get("type")
        snippet = result["snippet"]

        try:
          file_title = result["resources"][0]["title"]
        except: file_title = None

        try:
          file_link = result["resources"][0]["link"]
        except: file_link = None

        try:
          file_format = result["resources"][0]["file_format"]
        except: file_format = None

        cited_by_count = result.get("inline_links", {}).get("cited_by", {}).get("total", {})
        cited_by_id = result.get("inline_links", {}).get("cited_by", {}).get("cites_id", {})
        cited_by_link = result.get("inline_links", {}).get("cited_by", {}).get("link", {})
        total_versions = result.get("inline_links", {}).get("versions", {}).get("total", {})
        all_versions_link = result.get("inline_links", {}).get("versions", {}).get("link", {})
        all_versions_id = result.get("inline_links", {}).get("versions", {}).get("cluster_id", {})

        case_law_results_data.append({
          "page_number": results['serpapi_pagination']['current'],
          "position": result["position"] + 1,
          "result_type": result_type,
          "title": title,
          "link": link,
          "result_id": result_id,
          "publication_info_summary": publication_info_summary,
          "snippet": snippet,
          "cited_by_count": cited_by_count,
          "cited_by_link": cited_by_link,
          "cited_by_id": cited_by_id,
          "total_versions": total_versions,
          "all_versions_link": all_versions_link,
          "all_versions_id": all_versions_id,
          "file_format": file_format,
          "file_title": file_title,
          "file_link": file_link,
        })

        if "next" in results["serpapi_pagination"]:
          search.params_dict.update(dict(parse_qsl(urlsplit(results["serpapi_pagination"]["next"]).query)))
        else:
          loop_is_true = False

    return case_law_results_data


def save_case_law_results_to_csv():
    print("Waiting for case law results to save..")
    pd.DataFrame(data=case_law_results()).to_csv("google_scholar_case_law_results.csv", encoding="utf-8", index=False)

    print("Case Law Results Saved.")
```

#### Scrape and save case law results explanation process

Import libraries:

```python
import os
from serpapi import GoogleSearch
from urllib.parse import urlsplit, parse_qsl
import pandas as pd
```

- `pandas` will be used to easily save extracted data to CSV file.
- `urllib` will be used in the pagination process.
- `os` is used to return the value of the SerpApi API key environment variable.

Create, pass search parameters to SerpApi and create a temporary `list()` to store extracted data:

```python
params = {
    "api_key": os.getenv("API_KEY"),  # SerpApi API key
    "engine": "google_scholar",       # Google Scholar search results
    "q": "minecraft education ",      # search query
    "hl": "en",                       # language
    "start": "0",                     # first page
    "as_sdt": "6"                     # case law results
}
search = GoogleSearch(params)

case_law_results_data = []
```

`as_sdt` is used to determine and filter which Court(s) are targeted in an API call. Refer to [supported SerpApi Google Scholar Courts](https://serpapi.com/google-scholar-courts) or [select courts on Google Scholar](https://scholar.google.com/scholar_courts?q=blizzard&hl=en&as_sdt=2006) and pass it to `as_sdt` parameter.

Note: if you want to search results for Missouri Court Of Appeals, `as_sdt` parameter would become `as_sdt=4,204`. Pay attention to `4,`, without it, article results will appear instead.

Set up a `while` loop, add an `if` statement to be able to exit the loop:

```python
loop_is_true = True
while loop_is_true:
    results = search.get_dict()

    # extraction code here... 

    # if next page is present -> update previous results to new page results.
    # if next page is not present -> exit the while loop.
    if "next" in results["serpapi_pagination"]:
        search.params_dict.update(dict(parse_qsl(urlsplit(results["serpapi_pagination"]["next"]).query)))
    else:
        loop_is_true = False
```

`search.params_dict.update()` will split next page URL in parts and pass updated search param values to `GoogleSearch(search)` as a dictionary.   

Extract results in a `for` loop and handle exceptions:

```python
for result in results["organic_results"]:
    title = result["title"]
    publication_info_summary = result["publication_info"]["summary"]
    result_id = result["result_id"]
    link = result["link"]
    result_type = result.get("type")
    snippet = result["snippet"]
  
    try:
      file_title = result["resources"][0]["title"]
    except: file_title = None
  
    try:
      file_link = result["resources"][0]["link"]
    except: file_link = None
  
    try:
      file_format = result["resources"][0]["file_format"]
    except: file_format = None
  
    # if something is None it will return an empty {} dict()
    cited_by_count = result.get("inline_links", {}).get("cited_by", {}).get("total", {})
    cited_by_id = result.get("inline_links", {}).get("cited_by", {}).get("cites_id", {})
    cited_by_link = result.get("inline_links", {}).get("cited_by", {}).get("link", {})
    total_versions = result.get("inline_links", {}).get("versions", {}).get("total", {})
    all_versions_link = result.get("inline_links", {}).get("versions", {}).get("link", {})
    all_versions_id = result.get("inline_links", {}).get("versions", {}).get("cluster_id", {})
```

Append results to temporary `list()` as a dictionary `{}`:

```python
case_law_results_data.append({
    "page_number": results['serpapi_pagination']['current'],
    "position": position + 1,
    "result_type": result_type,
    "title": title,
    "link": link,
    "result_id": result_id,
    "publication_info_summary": publication_info_summary,
    "snippet": snippet,
    "cited_by_count": cited_by_count,
    "cited_by_link": cited_by_link,
    "cited_by_id": cited_by_id,
    "total_versions": total_versions,
    "all_versions_link": all_versions_link,
    "all_versions_id": all_versions_id,
    "file_format": file_format,
    "file_title": file_title,
    "file_link": file_link,
})
```

`Return` extracted data:

```python
return case_law_results_data
```

Save returned `case_law_results()` data `to_csv()`:

```python
pd.DataFrame(data=case_law_results()).to_csv("google_scholar_case_law_results.csv", encoding="utf-8", index=False)
```

- `data` argument inside `DataFrame` is your data.
- `encoding='utf-8'` argument just to make sure everything will be saved correctly. I used it explicitly even thought it's a default value.
- [`index=False`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.index.html) argument to drop default `pandas` row numbers.


____

<h2 id="links">Links</h2>

- [Code in the online IDE](https://replit.com/@DimitryZub1/Scrape-Google-Scholar-Case-Law-Results-to-CSV#main.py)
- [Google Scholar Organic Results API](https://serpapi.com/google-scholar-organic-results)
- [SerpApi supported Google Scholar Courts](https://serpapi.com/google-scholar-courts)
- [List of Google Scholar Courts](https://scholar.google.com/scholar_courts?q=blizzard&hl=en&as_sdt=2006)
___

<h2 id="outro">Outro</h2>

If you have anything to share, any questions, suggestions, or something that isn't working correctly, reach out via Twitter at [@dimitryzub](https://twitter.com/DimitryZub), or [@serp_api](https://twitter.com/serp_api).

Yours,
Dimitry, and the rest of SerpApi Team.

___

<p style="text-align: center;">Join us on <a href="https://www.reddit.com/r/SerpApi/">Reddit</a> | <a href="https://twitter.com/serp_api">Twitter</a> | <a href="https://www.youtube.com/channel/UCUgIHlYBOD3yA3yDIRhg_mg">YouTube</a></p>

<p style="text-align: center;">Add a  <a href="https://forum.serpapi.com/feature-requests">Feature Request</a>💫 or a <a href="https://forum.serpapi.com/bugs">Bug</a>🐞</p>