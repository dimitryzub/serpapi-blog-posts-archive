- <a href="#what_will_be_scraped">What will be scraped</a>
- <a href="#fullcode">Full Code</a>
- <a href="#prerequisites">Prerequisites</a>
    - <a href="#code_explanation">Code Explanation</a>
- <a href="#links">Links</a>

<h2 id="what_will_be_scraped">What will be scraped</h2>

![image](https://user-images.githubusercontent.com/78694043/180145105-4d3a5a36-5f03-4fb1-a88f-e383f3d04632.png)


<h2 id="fullcode">Full Code</h2>

```python
import os, requests, lxml, re, json, urllib.request
from bs4 import BeautifulSoup
from serpapi import GoogleSearch

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36"
}

params = {
    "q": "mincraft wallpaper 4k", # search query
    "tbm": "isch",                # image results
    "hl": "en",                   # language of the search
    "gl": "us",                   # country where search comes from
    "ijn": "0"                    # page number
}

html = requests.get("https://www.google.com/search", params=params, headers=headers, timeout=30)
soup = BeautifulSoup(html.text, "lxml")

def get_images_with_request_headers():
    del params["ijn"]
    params["content-type"] = "image/png" # parameter that indicate the original media type

    return [img["src"] for img in soup.select("img")]

def get_suggested_search_data():
    suggested_searches = []

    all_script_tags = soup.select("script")

    # https://regex101.com/r/48UZhY/6
    matched_images = "".join(re.findall(r"AF_initDataCallback\(({key: 'ds:1'.*?)\);</script>", str(all_script_tags)))
    
    # https://kodlogs.com/34776/json-decoder-jsondecodeerror-expecting-property-name-enclosed-in-double-quotes
    # if you try to json.loads() without json.dumps it will throw an error:
    # "Expecting property name enclosed in double quotes"
    matched_images_data_fix = json.dumps(matched_images)
    matched_images_data_json = json.loads(matched_images_data_fix)

    # search for only suggested search thumbnails related
    # https://regex101.com/r/ITluak/2
    suggested_search_thumbnails = ",".join(re.findall(r'{key(.*?)\[null,\"Size\"', matched_images_data_json))

    # https://regex101.com/r/MyNLUk/1
    suggested_search_thumbnail_encoded = re.findall(r'\"(https:\/\/encrypted.*?)\"', suggested_search_thumbnails)

    for suggested_search, suggested_search_fixed_thumbnail in zip(soup.select(".PKhmud.sc-it.tzVsfd"), suggested_search_thumbnail_encoded):
        suggested_searches.append({
            "name": suggested_search.select_one(".VlHyHc").text,
            "link": f"https://www.google.com{suggested_search.a['href']}",
            # https://regex101.com/r/y51ZoC/1
            "chips": "".join(re.findall(r"&chips=(.*?)&", suggested_search.a["href"])),
            # https://stackoverflow.com/a/4004439/15164646 comment by Frédéric Hamidi
            "thumbnail": bytes(suggested_search_fixed_thumbnail, "ascii").decode("unicode-escape")
        })

    return suggested_searches

def get_original_images():

    """
    https://kodlogs.com/34776/json-decoder-jsondecodeerror-expecting-property-name-enclosed-in-double-quotes
    if you try to json.loads() without json.dumps() it will throw an error:
    "Expecting property name enclosed in double quotes"
    """

    google_images = []

    all_script_tags = soup.select("script")

    # # https://regex101.com/r/48UZhY/4
    matched_images_data = "".join(re.findall(r"AF_initDataCallback\(([^<]+)\);", str(all_script_tags)))
    
    matched_images_data_fix = json.dumps(matched_images_data)
    matched_images_data_json = json.loads(matched_images_data_fix)

    # https://regex101.com/r/pdZOnW/3
    matched_google_image_data = re.findall(r'\[\"GRID_STATE0\",null,\[\[1,\[0,\".*?\",(.*),\"All\",', matched_images_data_json)

    # https://regex101.com/r/NnRg27/1
    matched_google_images_thumbnails = ", ".join(
        re.findall(r'\[\"(https\:\/\/encrypted-tbn0\.gstatic\.com\/images\?.*?)\",\d+,\d+\]',
                   str(matched_google_image_data))).split(", ")

    thumbnails = [
        bytes(bytes(thumbnail, "ascii").decode("unicode-escape"), "ascii").decode("unicode-escape") for thumbnail in matched_google_images_thumbnails
    ]

    # removing previously matched thumbnails for easier full resolution image matches.
    removed_matched_google_images_thumbnails = re.sub(
        r'\[\"(https\:\/\/encrypted-tbn0\.gstatic\.com\/images\?.*?)\",\d+,\d+\]', "", str(matched_google_image_data))

    # https://regex101.com/r/fXjfb1/4
    # https://stackoverflow.com/a/19821774/15164646
    matched_google_full_resolution_images = re.findall(r"(?:'|,),\[\"(https:|http.*?)\",\d+,\d+\]", removed_matched_google_images_thumbnails)

    full_res_images = [
        bytes(bytes(img, "ascii").decode("unicode-escape"), "ascii").decode("unicode-escape") for img in matched_google_full_resolution_images
    ]
    
    for index, (metadata, thumbnail, original) in enumerate(zip(soup.select('.isv-r.PNCib.MSM1fd.BUooTd'), thumbnails, full_res_images), start=1):
        google_images.append({
            "title": metadata.select_one(".VFACy.kGQAp.sMi44c.lNHeqe.WGvvNb")["title"],
            "link": metadata.select_one(".VFACy.kGQAp.sMi44c.lNHeqe.WGvvNb")["href"],
            "source": metadata.select_one(".fxgdke").text,
            "thumbnail": thumbnail,
            "original": original
        })

        # Download original images
        print(f'Downloading {index} image...')
        
        opener=urllib.request.build_opener()
        opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36')]
        urllib.request.install_opener(opener)

        urllib.request.urlretrieve(original, f'Bs4_Images/original_size_img_{index}.jpg')

    return google_images
```

<h2 id="prerequisites">Prerequisites</h2>

**Install libraries**:

```lang-none
pip install requests bs4 google-search-results
```

`google-search-results` is a SerpApi API package.

**Basic knowledge scraping with CSS selectors**

CSS selectors declare which part of the markup a style applies to thus allowing to extract data from matching tags and attributes.

If you haven't scraped with CSS selectors, there's a dedicated blog post of mine
about [how to use CSS selectors when web-scraping](https://serpapi.com/blog/web-scraping-with-css-selectors-using-python/) that covers what it is, its pros and cons, and why they matter from a web-scraping perspective.

**Reduce the chance of being blocked**

There's a chance that a request might be blocked. Have a look
at [how to reduce the chance of being blocked while web-scraping](https://serpapi.com/blog/how-to-reduce-chance-of-being-blocked-while-web/), there are eleven methods to bypass blocks from most websites.

Make sure to pass [`User-Agent`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/User-Agent), because Google might block your requests eventually and you'll receive a different HTML thus empty output. 

`User-Agent` identifies the browser, its version number, and its host operating system that represents a person (browser) in a Web context that lets servers and network peers identify if it's a bot or not. And we're faking "real" user visit. [Check what is your user-agent](https://www.whatismybrowser.com/detect/what-is-my-user-agent).


<h3 id="code_explanation">Code Explanation</h3>

Import libraries:

```python
import os, requests, lxml, re, json, urllib.request
from bs4 import BeautifulSoup
from serpapi import GoogleSearch
```

| Library       | Purpose                                                            |
|---------------|--------------------------------------------------------------------|
| [`os`](https://docs.python.org/3/library/os.html)    | to return environement variable (SerpApi API key) value.                                  |
| [`requests`](https://requests.readthedocs.io/en/latest/user/quickstart/)    | to make a request to the website.                                  |
| [`lxml`](https://lxml.de/)    | to process XML/HTML documents fast.                                  |
| [`json`](https://docs.python.org/3/library/json.html)        | to convert extracted data to a JSON object.                        |
| [`re`](https://docs.python.org/3/library/re.html)          | to extract parts of the data via regular expression.               |
| [`urllib.request`](https://docs.python.org/3/library/urllib.request.html)          | to save images locally with [`urllib.request.urlretrieve`](https://docs.python.org/3/library/urllib.request.html#urllib.request.urlretrieve)               |
| [`BeautifulSoup`](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)      | is a XML/HTML scraping library. It's [used in combo with `lxml` as it faster than `html.parser`](https://www.crummy.com/software/BeautifulSoup/bs4/doc//#installing-a-parser) |


Create URL parameter and request headers:

```python
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36"
}

params = {
    "q": "mincraft wallpaper 4k", # search query
    "tbm": "isch",                # image results
    "hl": "en",                   # language of the search
    "gl": "us",                   # country where search comes from
    "ijn": "0"                    # page number
}
```

| Code                                                                      | Explanation                                           |
|------------------------------------------------------------------------------|---------------------------------------------------|
| [`params` ](https://docs.python-requests.org/en/master/user/quickstart/#passing-parameters-in-urls)                                                                      |a prettier way of passing URL parameters to a request. |
| [`user-agent`](https://developer.mozilla.org/en-US/docs/Glossary/User_agent) | to act as a "real" user request from the browser by passing it to [request headers](https://docs.python-requests.org/en/master/user/quickstart/#custom-headers). [Default `requests` user-agent is a `python-reqeusts`](https://github.com/psf/requests/blob/589c4547338b592b1fb77c65663d8aa6fbb7e38b/requests/utils.py#L808-L814) so websites might understand that it's a bot or a script and block the request to the website. [Check what's your `user-agent`](https://www.whatismybrowser.com/detect/what-is-my-user-agent). |


Make a request, pass created request parameters and headers. Pass returned HTML to `BeautifulSoup`: 

```python
html = requests.get("https://www.google.com/search", params=params, headers=headers, timeout=30)
soup = BeautifulSoup(html.text, "lxml")
```

|Code|Explanation|
|----|-----------|
|[`timeout=30`](https://docs.python-requests.org/en/master/user/quickstart/#timeouts)| to stop waiting for response after 30 seconds.|
|`Selector(text=html.text)`|where passed HTML from the response will be processed by `parsel`.|
|`html.text, "lxml"`|`html.text` will return a textual HTML data and `"lxml"` will be set as a XML/HTML processor, not the default `html.parser`|


Extracting data with request headers only, no regular expression the moment:

```python
def get_images_with_request_headers():
    params["content-type"] = "image/png" # parameter that indicate the original media type 

    return [img["src"] for img in soup.select("img")]
```

The reason why it's handy is beacuse when you try directly parse data from `img` tag and `src` attriubte, you'll get a base64 encoded URL which will be a 1x1 image placeholder. Not a particularly useful image resolution 🙂


|Code|Explanation|
|----|-----------|
|`params["content-type"]`|will create a new `dict` key `"content-type"` and assinged a `"image/png"` value which will return images.|
|`[img["src"] for img in soup.select("img")]`|will iterate over all `img` tags and extracts `src` attriubte in a [list comprehension](https://www.w3schools.com/python/python_lists_comprehension.asp) loop and returned value would be a `list` of URLs from `src` attriubte.|


Print retured data:

```lang-none
[
   "/images/branding/searchlogo/1x/googlelogo_desk_heirloom_color_150x55dp.gif",
   "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQIMPdHAO0x25OT-1uxKUw_Kh1Bct6RIDaHlL8fTqXY_qGNdAizUZGa_uI6_Q&s",
   "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSvj_A0yXqbEgcTsZ1_ckFjtTEVCxn9BFJF6EYh1MbLiWokT3EdvPo0aB3aeQ&s",
   "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcThOaMoYjrJCat0kGBaecZVz1pOXsntuvwyexmedIsR4gFXtek-3rNmBlL8fQ&s",
   "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTuUcXHuHe2qOVv_IfHmk3A8T24VeWT-qHfRrHaEUHH89MGlH8r2NJXHHZ-Yg&s",
   "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSan-UQMuDyVQI5ZEiyubOle_0q_PgXL7DpBgKq8Y2-Fuc1BM1X5MxMBiP4ag&s",
   "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQfWQp1ltZK-o_PZ1f2rRtSq0MoWx-0jLFh_y1uv8umjK4eSj6IqhqRBzCKtg&s",
   "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRn4d2zWI7_4wInrzsNntRSWcA_neicVq63ZJdiiYcsEERogyw542JmFugEc4U&s",
   "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTDtyIKB9SH1rg9U4kcrGlD_La_NCcveaOD4UX1EaXUxkW-L0DNhcsLX5obpQ&s",
   "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRg2xAc8_Wdv5Cheb9w6Xq_e7X1fV7tdUCi9F-PsbHGlaJ2dLHSfYUgPXHmIw&s",
   "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSmdAeFWxFVq7gpGtkEqq_ZzexHslYOGrHxW-IUgeOXv4CuIygDDyhaqSnPSy8&s",
   "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQHeNDVL9JbWgD8ypdDR4XTr6xY7dRgh_n2_5q8GZQuiqlk_oDCHaOC0bu0Hg&s",
   "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRa5NpjrrZl0US_8TFHdO5d3SQ4TF_dn6MvRzL4SwzB_KcemJWdPRHJtGnTOw&s",
   "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSbRM8yNQyOF4EZsYZCtu7W4mWOIVPfaGySwmyfA6eeJfMySK4clUTvdrMg-g&s",
   "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRvBJ8a7VeA8JLlqI_p4oP2fx7oXzYMVCQEPG_Pg_ez0DvAwk7-aCwM4_U7vAA&s",
   "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSHNhOWeEKm5LbrrpPBzbfve0V9YFLTYMhxwIDtxizdLQksWhsqIpoQ1UsmaA&s",
   "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRKeLIuwzSKazmbf4pUxXxosJf1yfacVk0YAmghMI9tvU1UgVeRKp1RYgxqcEY&s",
   "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ7dBADGlYdi8qGZ9EiAEqFp0V0CQlvMTbczsJShx0qwNV0aM-BKAR33bsTUTg&s",
   "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSIjBkxu1ZJH5Nl_Gnr1U24VDDXPJ8HmjQ4GltNgIr0An3sHmzKUYafNp03qA&s",
   "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS0JKR9RIPl5boovVxH9oSNPJzkIyQB1RhdoJSHyi7ScUVPM2T6I3N0r1awxQ&s",
   "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRmUMz6FrjQ8YF9Ktxz1ftVKAnNxmTs5ACqDpJ0z_4ppcYBaWWGCyfd-GZLjQ&s"
]
```


Now to the suggested search results, a thing above actual images:

```python
def get_suggested_search_data():
    """
    https://kodlogs.com/34776/json-decoder-jsondecodeerror-expecting-property-name-enclosed-in-double-quotes
    if you try to json.loads() without json.dumps it will throw an error:
    "Expecting property name enclosed in double quotes"
    """

    suggested_searches = []

    all_script_tags = soup.select("script")

    # https://regex101.com/r/48UZhY/6
    matched_images = "".join(re.findall(r"AF_initDataCallback\(({key: 'ds:1'.*?)\);</script>", str(all_script_tags)))
    
    matched_images_data_fix = json.dumps(matched_images)
    matched_images_data_json = json.loads(matched_images_data_fix)

    # search for only suggested search thumbnails related
    # https://regex101.com/r/ITluak/2
    suggested_search_thumbnails = ",".join(re.findall(r'{key(.*?)\[null,\"Size\"', matched_images_data_json))

    # https://regex101.com/r/MyNLUk/1
    suggested_search_thumbnail_encoded = re.findall(r'\"(https:\/\/encrypted.*?)\"', suggested_search_thumbnails)

    # zip() is used on puprose over zip_longest() as number of results would be identical
    for suggested_search, suggested_search_fixed_thumbnail in zip(soup.select(".PKhmud.sc-it.tzVsfd"), suggested_search_thumbnail_encoded):
        suggested_searches.append({
            "name": suggested_search.select_one(".VlHyHc").text,
            "link": f"https://www.google.com{suggested_search.a['href']}",
            # https://regex101.com/r/y51ZoC/1
            "chips": "".join(re.findall(r"&chips=(.*?)&", suggested_search.a["href"])),
            # https://stackoverflow.com/a/4004439/15164646 comment by Frédéric Hamidi
            "thumbnail": bytes(suggested_search_fixed_thumbnail, "ascii").decode("unicode-escape")
        })

    return suggested_searches
```

|Code|Explanation|
|----|-----------|
|`suggested_searches`|a temporary `list` where extracted data will be [appended](https://www.w3schools.com/python/ref_list_append.asp) at the end of the function.|
|`all_script_tags`|a variable which will hold all extracted `<script>` HTML tags from `soup.select("script")` where [`select()`](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#css-selectors) will return a list of matched `<script>` tags.|
|`matched_images`|will hold all extracted matched images data from [`re.findall()`](https://docs.python.org/3/library/re.html#re.findall) which returns an [iterator](https://docs.python.org/3/glossary.html#term-iterator). This variable is needed to extract suggested search thumbnails, image thumbnail and full resolution images.|
|`suggested_search_thumbnails` and `suggested_search_thumbnail_encoded`|parses part of inline JSON where `suggested_search_thumbnail_encoded` parses actual thubmnails from parlty parsed inline JSON data.|
|[`zip()`](https://docs.python.org/3/library/functions.html#zip)|to iterate over multiple iterables in parralel. Keep in mind that `zip` used on puprose. [`zip()` ends with the shortest iterator while `zip_longest()` iterates up to the lenght of the longest iterator](https://stackoverflow.com/a/59119827/15164646).|
|`suggested_searches.append({})`|to [`append` extracted images data to a `list`](https://www.w3schools.com/python/ref_list_append.asp) as a dictionary.|
|`select_one()`|to return one (instead of all) matched element in a loop.|
|`["href"]`|is a shortcut of accessing and [extracting HTML attributes with `BeautifulSoup`. Alternative is `get(<attribute>)`](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#attributes).|
|[`"".join()`](https://www.w3schools.com/python/ref_string_join.asp)|to join all itemes from in iterable into a string.|
|`bytes(<variable>, "ascii").decode("unicode-escape")`|to decode parsed image data.|

Printed returned data:

```json
[
  {
    "name": "ultra hd",
    "link": "https://www.google.com/search?q=minecraft+wallpaper+4k&tbm=isch&hl=en&gl=us&chips=q:minecraft+wallpaper+4k,g_1:ultra+hd:5VuluDYWa8Y%3D&sa=X&ved=2ahUKEwjshdCK0Yn5AhXrlWoFHYhyCrQQ4lYoAHoECAEQHQ",
    "chips": "q:minecraft+wallpaper+4k,g_1:ultra+hd:5VuluDYWa8Y%3D",
    "thumbnail": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcThU0xo_GeIciyaBmvE6EI46tnj0npeDAmDsLKjYlnv4tGz0eaw&usqp=CAU"
  },
  {
    "name": "epic",
    "link": "https://www.google.com/search?q=minecraft+wallpaper+4k&tbm=isch&hl=en&gl=us&chips=q:minecraft+wallpaper+4k,g_1:epic:5c56RYLjq2c%3D&sa=X&ved=2ahUKEwjshdCK0Yn5AhXrlWoFHYhyCrQQ4lYoAXoECAEQHw",
    "chips": "q:minecraft+wallpaper+4k,g_1:epic:5c56RYLjq2c%3D",
    "thumbnail": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ_bUq-7tk9FyeNSW40Yo8FRY6SOViMbUeme_ln1uMwxcTdfI6d&usqp=CAU"
  }, ... other results
]
```

Extracting original resolution images:

```python
def get_original_images():

    """
    https://kodlogs.com/34776/json-decoder-jsondecodeerror-expecting-property-name-enclosed-in-double-quotes
    if you try to json.loads() without json.dumps() it will throw an error:
    "Expecting property name enclosed in double quotes"
    """

    google_images = []

    all_script_tags = soup.select("script")

    # # https://regex101.com/r/48UZhY/4
    matched_images_data = "".join(re.findall(r"AF_initDataCallback\(([^<]+)\);", str(all_script_tags)))
    
    matched_images_data_fix = json.dumps(matched_images_data)
    matched_images_data_json = json.loads(matched_images_data_fix)

    # https://regex101.com/r/pdZOnW/3
    matched_google_image_data = re.findall(r'\[\"GRID_STATE0\",null,\[\[1,\[0,\".*?\",(.*),\"All\",', matched_images_data_json)

    # https://regex101.com/r/NnRg27/1
    matched_google_images_thumbnails = ", ".join(
        re.findall(r'\[\"(https\:\/\/encrypted-tbn0\.gstatic\.com\/images\?.*?)\",\d+,\d+\]',
                   str(matched_google_image_data))).split(", ")

    thumbnails = [
        bytes(bytes(thumbnail, "ascii").decode("unicode-escape"), "ascii").decode("unicode-escape") for thumbnail in matched_google_images_thumbnails
    ]

    # removing previously matched thumbnails for easier full resolution image matches.
    removed_matched_google_images_thumbnails = re.sub(
        r'\[\"(https\:\/\/encrypted-tbn0\.gstatic\.com\/images\?.*?)\",\d+,\d+\]', "", str(matched_google_image_data))

    # https://regex101.com/r/fXjfb1/4
    # https://stackoverflow.com/a/19821774/15164646
    matched_google_full_resolution_images = re.findall(r"(?:'|,),\[\"(https:|http.*?)\",\d+,\d+\]", removed_matched_google_images_thumbnails)

    full_res_images = [
        bytes(bytes(img, "ascii").decode("unicode-escape"), "ascii").decode("unicode-escape") for img in matched_google_full_resolution_images
    ]
    
    for index, (metadata, thumbnail, original) in enumerate(zip(soup.select(".isv-r.PNCib.MSM1fd.BUooTd"), thumbnails, full_res_images), start=1):
        google_images.append({
            "title": metadata.select_one(".VFACy.kGQAp.sMi44c.lNHeqe.WGvvNb")["title"],
            "link": metadata.select_one(".VFACy.kGQAp.sMi44c.lNHeqe.WGvvNb")["href"],
            "source": metadata.select_one(".fxgdke").text,
            "thumbnail": thumbnail,
            "original": original
        })

        # Download original images
        print(f"Downloading {index} image...")
        
        opener=urllib.request.build_opener()
        opener.addheaders=[("User-Agent","Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36")]
        urllib.request.install_opener(opener)

        urllib.request.urlretrieve(original, f"Bs4_Images/original_size_img_{index}.jpg")

    return google_images
```

The process is almost identical as extracting suggested search results except different regular expressions:

1\. Creating temporary `list` `google_images` where extracted data will be appended.

2\. Extracting `all_script_tags`.

3\. Extracting `matched_images_data` to extract thumbnails and original resolution images.

4\. Decode extracted encoded `thubmnails`:

```python
thumbnails = [
    bytes(bytes(thumbnail, "ascii").decode("unicode-escape"), "ascii").decode("unicode-escape") for thumbnail in matched_google_images_thumbnails
]

# equvalent to 
for fixed_google_image_thumbnail in matched_google_images_thumbnails:
    # https://stackoverflow.com/a/4004439/15164646 comment by Frédéric Hamidi
    google_image_thumbnail_not_fixed = bytes(fixed_google_image_thumbnail, 'ascii').decode('unicode-escape')
    # after first decoding, Unicode characters are still present. After the second iteration, they were decoded.
    google_image_thumbnail = bytes(google_image_thumbnail_not_fixed, 'ascii').decode('unicode-escape')
```

5\. Decode extracted encoded `full_res_images`:

```python
full_res_images = [
      bytes(bytes(img, "ascii").decode("unicode-escape"), "ascii").decode("unicode-escape") for img in matched_google_full_resolution_images
  ]

# equvalent to
for index, fixed_full_res_image in enumerate(matched_google_full_resolution_images):
    # https://stackoverflow.com/a/4004439/15164646 comment by Frédéric Hamidi
    original_size_img_not_fixed = bytes(fixed_full_res_image, 'ascii').decode('unicode-escape')
    original_size_img = bytes(original_size_img_not_fixed, 'ascii').decode('unicode-escape')
```

Save full resolution images locally:

```python
opener=urllib.request.build_opener()
opener.addheaders=[("User-Agent","Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36")]
urllib.request.install_opener(opener)

urllib.request.urlretrieve(original, f"Bs4_Images/original_size_img_{index}.jpg")
```

|Code|Explanation|
|----|-----------|
|[`urllib.request.build_opener()`](https://docs.python.org/3/library/urllib.request.html#urllib.request.build_opener)|manages the chaining of handlers and will automatically add headers on each request (row below).|
|`opener.addheaders[()]`|to add headers to the request.|
|[`urllib.install_opener()`](https://docs.python.org/3/library/urllib.request.html#urllib.request.install_opener)|set opener as a default global opener. Whatever that means 👀|
|[`urllib.request.urlretrieve()`](https://docs.python.org/3/library/urllib.request.html#urllib.request.urlretrieve)|to save images locally.|


Printed returned data:

```json
[
  {
    "title": "4K Minecraft Wallpapers | Background Images",
    "link": "https://wall.alphacoders.com/tag/4k-minecraft-wallpapers",
    "source": "wall.alphacoders.com",
    "thumbnail": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSJxrGh1FUsvCRNgKI4aiM8CimALQ0rHU2SDigSRl6X1c7BiWDOUMMMVCwyKtufB9SEddw&usqp=CAU",
    "original": "https://images6.alphacoders.com/108/thumb-1920-1082090.jpg"
  },
  {
    "title": "Best Minecraft Wallpaper 4k - Minecraft Tutos",
    "link": "https://minecraft-tutos.com/en/minecraft-wallpaper/",
    "source": "minecraft-tutos.com",
    "thumbnail": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTRDMguXava6khO5e5A0GQsm5v64rrJI_tYuSaJjyxWQNhTrhRWPRLLuhtPVouOUSaqzC0&usqp=CAU",
    "original": "https://minecraft-tutos.com/wp-content/uploads/2022/03/wallpaper-minecraft-alex-steve-universe.jpeg"
  }, ... other results
]
```


### Using [Google Images API](https://serpapi.com/images-results)

The main difference is that it's a quicker approach. No need to figure out regular expressions, create a parser and maintain it over time or how scale the number of requests without being blocked.

Example with pagination and mulptiple search queries:

```python
def serpapi_get_google_images():
    image_results = []
    
    for query in ["Coffee", "boat", "skyrim", "minecraft"]:
        # search query parameters
        params = {
            "engine": "google",               # search engine. Google, Bing, Yahoo, Naver, Baidu...
            "q": query,                       # search query
            "tbm": "isch",                    # image results
            "num": "100",                     # number of images per page
            "ijn": 0,                         # page number: 0 -> first page, 1 -> second...
            "api_key": os.getenv("API_KEY")   # your serpapi api key
            # other query parameters: hl (lang), gl (country), etc  
        }
    
        search = GoogleSearch(params)         # where data extraction happens
    
        images_is_present = True
        while images_is_present:
            results = search.get_dict()       # JSON -> Python dictionary
    
            # checks for "Google hasn't returned any results for this query."
            if "error" not in results:
                for image in results["images_results"]:
                    if image["original"] not in image_results:
                        image_results.append(image["original"])
                
                # update to the next page
                params["ijn"] += 1
            else:
                images_is_present = False
                print(results["error"])
    
    # -----------------------
    # Downloading images

    for index, image in enumerate(results["images_results"], start=1):
        print(f"Downloading {index} image...")
        
        opener=urllib.request.build_opener()
        opener.addheaders=[("User-Agent","Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36")]
        urllib.request.install_opener(opener)

        urllib.request.urlretrieve(image["original"], f"SerpApi_Images/original_size_img_{index}.jpg")

    print(json.dumps(image_results, indent=2))
    print(len(image_results))
```

Outputs:

```lang-none
[
  "https://i.ytimg.com/vi/ZXMgC-HuvIk/maxresdefault.jpg",
  "https://www.minecraft.net/content/dam/games/minecraft/key-art/redeem-art-minecraft-285x380.jpg",
  "https://i.ytimg.com/vi/yZ_Ppfg886A/maxresdefault.jpg",
  "https://www.minecraft.net/content/dam/games/minecraft/screenshots/1-18-2-release-header.jpg",
  "https://i.ytimg.com/vi/vdrn4ouZRvQ/maxresdefault.jpg",
  "https://cdn.shopify.com/s/files/1/0266/4841/2351/products/MCMATTEL-PLUSH-BUNDLE-Minecraft-PlushImage-1080x1080_1_1024x1024.jpg?v=1647522411",
  "https://i.ytimg.com/vi/LMCt-gSvEqU/maxresdefault.jpg",
  "https://www.minecraft.net/content/dam/community/events/cy21/minecraft-live-2021/Minecraft_Live_2021_PMP_Hero_01.jpg",
  "https://i.ytimg.com/vi/yCNUP2NAt-A/maxresdefault.jpg",
  "https://yt3.ggpht.com/WSL98T4k4vjvwzFjtIk_tQfTGu7ak0mTRiUnF1djjhevjEX4SNW9LOiY5534JKOzSYlehght0w=s540-w390-h540-c-k-c0x00ffffff-no-nd-rj",
  "https://i.ytimg.com/vi/rrl8-jOOlIA/maxresdefault.jpg",
  "https://i.ytimg.com/vi/f8LJloSamwg/maxresdefault.jpg",
  "https://i.ytimg.com/vi/IqtMhWqv_pw/maxresdefault.jpg",
  "https://i.ytimg.com/vi/076mjMOL6R8/maxresdefault.jpg",
  "https://i.ytimg.com/vi/5qrUb7a821c/maxresdefault.jpg",
  "https://i.ytimg.com/vi/HZGffLRh6a4/maxresdefault.jpg",
  "https://i.ytimg.com/vi/nFQKvjM9HCw/maxresdefault.jpg",
  "https://i.ytimg.com/vi/LK4w3PwdCWc/maxresdefault.jpg",
  "https://i.ytimg.com/vi/hySgv7XyWaM/maxresdefault.jpg",
  "https://i.ytimg.com/vi/rmkGOy7pS4I/maxresdefault.jpg",
  "https://i.ytimg.com/vi/YV-576jC1BU/maxresdefault.jpg",
  "https://i.ytimg.com/vi/YXY74kWderc/maxresdefault.jpg"
]
2349 # number of total extracted images
```



<h2 id="links">Links</h2>

- [Code in the online IDE](https://replit.com/@DimitryZub1/Scrape-and-Download-Google-Images-with-Python#bs4_original_images.py)
- [Google Images API](https://serpapi.com/images-results)
- [Github Gist](https://gist.github.com/dimitryzub/9d1c5de0613610a02e3fdc96e05e86a1)
- [Video API tutorial: Web Scraping all Google Images in Python and SerpApi](https://www.youtube.com/watch?v=QuCPV6_GT6o)


<p style="text-align: center;">Join us on <a href="https://twitter.com/serp_api">Twitter</a> | <a href="https://www.youtube.com/channel/UCUgIHlYBOD3yA3yDIRhg_mg">YouTube</a></p>

<p style="text-align: center;">Add a  <a href="https://github.com/serpapi/SerpApi/issues/">Feature Request</a>💫 or a <a href="https://github.com/serpapi/SerpApi/issues/">Bug</a>🐞</p>