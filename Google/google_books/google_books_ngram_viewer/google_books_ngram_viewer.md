- <a href="#what_will_be_scraped">What will be scraped</a>
- <a href="#prerequisites">Prerequisites</a>
- <a href="#process">Process</a>
- <a href="#full_code">Full Code</a>
- <a href="#links">Links</a>
- <a href="#outro">Outro</a>

___


<h2 id="what_will_be_scraped">What will be scraped</h2>

![image](https://user-images.githubusercontent.com/78694043/153561212-19fd8869-843c-43b7-a72b-3240e219b791.png)

Comparing with the scraped data plot:

![image](https://user-images.githubusercontent.com/78694043/154284774-3bc3d8ce-63fa-48d0-a8b9-81bb875eac21.png)

<h2 id="prerequisites">Prerequisites</h2>

**Separate virtual environment**

In short, it's a thing that creates an independent set of installed libraries including different Python versions that can coexist with each
other at the same system thus preventing libraries or Python version conflicts.

If you didn't work with a virtual environment before, have a look at the
dedicated [Python virtual environments tutorial using Virtualenv and Poetry](https://serpapi.com/blog/python-virtual-environments-using-virtualenv-and-poetry/)
blog post of mine to get familiar.

📌Note: this is not a strict requirement for this blog post.

**Install libraries**:

```lang-none
pip install requests, pandas, matplotlib, matplotx
```

**Reduce the chance of being blocked**

There's a chance that a request might be blocked. Have a look
at [how to reduce the chance of being blocked while web-scraping](https://serpapi.com/blog/how-to-reduce-chance-of-being-blocked-while-web/), there are eleven methods to bypass blocks from most websites.

___


<h2 id="full_code">Full Code</h2>

```python
import requests, matplotx
import pandas as pd
import matplotlib.pyplot as plt

params = {
    "content": "Albert Einstein,Sherlock Holmes,Bear Grylls,Frankenstein,Elon Musk,Richard Branson",
    "year_start": "1800",
    "year_end": "2019"
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.87 Safari/537.36",
}

html = requests.get("https://books.google.com/ngrams/json", params=params, headers=headers, timeout=30).text
time_series = pd.read_json(html, typ="series")

year_values = list(range(int(params['year_start']), int(params['year_end']) + 1))

for series in time_series:
    plt.plot(year_values, series["timeseries"], label=series["ngram"])

plt.title("Google Books Ngram Viewer", pad=10)
matplotx.line_labels()  # https://stackoverflow.com/a/70200546/15164646

plt.xticks(list(range(int(params['year_start']), int(params['year_end']) + 1, 20)))
plt.grid(axis="y", alpha=0.3)

plt.ylabel("%", labelpad=5)
plt.xlabel(f"Year: {params['year_start']}-{params['year_end']}", labelpad=5)
plt.show()
```

Import libraries: 

```python
import requests, matplotx
import pandas as pd
import matplotlib.pyplot as plt
```

- `requests` to make a request and `matplotx` to customize plot line labels.
- `pandas` to read convert JSON string to pandas `Series` which will be passed to `matplotlib` to make a chart.
- `matplotlib` to make a time series plot.

Create search query URL parameters and request headers:

```python
# https://docs.python-requests.org/en/master/user/quickstart/#passing-parameters-in-urls
params = {
    "content": "Albert Einstein,Sherlock Holmes,Bear Grylls,Frankenstein,Elon Musk,Richard Branson",
    "year_start": "1800",
    "year_end": "2019"
}

# https://requests.readthedocs.io/en/master/user/quickstart/#custom-headers
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.87 Safari/537.36",
}
```

- `User-Agent` is used to act as a "real" user visit so websites would think that it's not a bot or a script that sends a request.
- Make sure you're using latest `User-Agent`. If using old `User-Agent`, websites might treat particular request as a bot or a script that sends a request. [Check what's your `User-Agent` at  whatismybrowser.com](https://www.whatismybrowser.com/detect/what-is-my-user-agent).

Pass search query `params`, request `header` to `requests` and `read_json()` from returned `html`:

```python
html = requests.get("https://books.google.com/ngrams/json", params=params, headers=headers, timeout=30).text
time_series = pd.read_json(html, typ="series")
```

- `"https://books.google.com/ngrams/json"` is a Google Book Ngram Viewer JSON endpoint. The only thing that is being changed in the URL is `ngrams/graph` -> `ngrams/json`. Besides, that, it accepts the same URL parameters as `ngrams/graph`.
- [`timeout=30`](https://docs.python-requests.org/en/latest/user/advanced/#timeouts) tells `requsests` to stop waiting for a response after 30 seconds.
- [`typ="series"`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_json.html) tells `pandas` to make a `series` object from the JSON string. Default is `DataFrame`.


Add year values:

```python
# 1800 - 2019
year_values = list(range(int(params['year_start']), int(params['year_end']) + 1))
```

- `list()` will create a `list` of values.
- `range()` will iterate over a range of values that comes from search query `params`, in this case, from 1800 to 2019. 
- `int()` will convert string query parameter to an integer.
- `+ 1` to get the last value as well, in this case, year 2019, otherwise the last value will be 2018.

Iterate over `time_series` data and make a `plot`:

```python
for series in time_series:
    plt.plot(year_values, series["timeseries"], label=series["ngram"])
```

- `label=label` is a line label on the time-series chart.


Add chart title, labels: 

```python
plt.title("Google Books Ngram Viewer", pad=10)
matplotx.line_labels()  # https://stackoverflow.com/a/70200546/15164646

plt.xticks(list(range(int(params['year_start']), int(params['year_end']) + 1, 20)))
plt.grid(axis="y", alpha=0.3)

plt.ylabel("%", labelpad=5)
plt.xlabel(f"Year: {params['year_start']}-{params['year_end']}", labelpad=5)
```
- `pad=10` and `labelpad=5` stands for label padding.
- `matplotx.line_labels()` will add style labels which will apper on the right side of each line.
- `plt.xticks()` is a ticks on X the axis and `range(<code>, 20)` where 20 is a step size.
- [`grid()` is a grid lines](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.grid.html), and [`alpha`](https://matplotlib.org/stable/api/_as_gen/matplotlib.artist.Artist.set_alpha.html#matplotlib.artist.Artist.set_alpha) argument defines a blending (transparency). 
- `ylabel()`/`xlabel()` stands for y-axis and x-axis label.


Show plot:

```python
plt.show()
```

![image](https://user-images.githubusercontent.com/78694043/154284774-3bc3d8ce-63fa-48d0-a8b9-81bb875eac21.png)

____

<h2 id="links">Links</h2>

- [GitHub Repository with Jupyter Notebook](https://github.com/dimitryzub/google-books-ngrams-viewer-py)

___

<h2 id="outro">Outro</h2>

If you have anything to share, any questions, suggestions, or something that isn't working correctly, feel free to drop a comment in the comment section or reach out via Twitter at [@dimitryzub](https://twitter.com/DimitryZub), or [@serp_api](https://twitter.com/serp_api).

Yours, 
Dmitriy, and the rest of SerpApi Team.

___

<p style="text-align: center;">Join us on <a href="https://www.reddit.com/r/SerpApi/">Reddit</a> | <a href="https://twitter.com/serp_api">Twitter</a> | <a href="https://www.youtube.com/channel/UCUgIHlYBOD3yA3yDIRhg_mg">YouTube</a></p>

<p style="text-align: center;">Add a  <a href="https://github.com/serpapi/public-roadmap/issues">Feature Request</a>💫 or a <a href="https://github.com/serpapi/public-roadmap/issues">Bug</a>🐞</p>