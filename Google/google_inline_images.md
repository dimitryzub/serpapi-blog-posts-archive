Contents: intro, imports, what will be scraped, process, code, links, outro.

### Intro
This blog post is a continuation of Google's web scraping series. Here you'll see how to scrape Inline Images using Python with `beautifulsoup`, `requests`, `lxml`, `re`, `base64`, `BytesIO`, `PIL` libraries. An alternative API solution will be shown.

*Note: This blog post assumes that you're familiar with `beautifulsoup`, `requests` libraries and a basic understanding of regular expressions.*

### Imports
```python
import requests, lxml, re, base64
from bs4 import BeautifulSoup 
from io import BytesIO # for decoding base64 image
from PIL import Image # for saving decoded image
from serpapi import GoogleSearch # alternative API solution
```

### What will be scraped
![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/kujso55bf527efx7xvh3.png)



### Process

Selecting container, link, and where photo being used.
<img width="100%" style="width:100%" src="https://media.giphy.com/media/usKeWP3kWNGbCZP71u/giphy.gif">

**Extracting thumbnail**
To extract thumbnail, we need to look at `<img>` tag with `id` `dimg_XX` (*XX - some number*).

If you open source code (Ctrl + U) and try to find `dimg_36` (*or other digits depending on the HTML code*) you'll see that there are **2** occurrences that will be found, and one of them will be somewhere in the `<script>` tags, that's what we need.

In order to extract thumbnails we need to use `regex` to get them from the `<script>` tags, because if you would parse data from a `src` attribute, the output you would get will be like this: `data:image/gif;base64,R0lGODlhAQABAIAAAP///////yH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==` which is [`base64`](https://en.wikipedia.org/wiki/Base64) encoded picture.
![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/2c2jbhgxgehykbbxg3xc.png)

*More about this topic could be found on [Developer Mozilla](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/Data_URIs#syntax)*

______


The regular expression is extremely simple:
```lang-none
s='data:image/jpeg;base64,(.*?)';
```

Regular Expression explanation:
1. looking for `s='data:image/jpeg;base64,`
2. creating a capture group `(.*?)` which will grab everything, and ending with `';` symbols.
3. only the <u>capture group</u> will be extracted without other parts.

*Screenshot to illustrate what is being captured by a regular expression which you can find [here](https://regex101.com/r/L3IZXe/4/)*:
![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/tdbij16a0p3d8j7ckzzr.png)



After that, the decoded base64 string can be saved using `PIL` module. More can be found on [StackOverFlow answer](https://stackoverflow.com/a/6966225/15164646).

### Code
```python
import requests, lxml, re, urllib.parse, base64
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}

params = {
    "q": "minecraft shareds photo",
    "sourceid": "chrome",
}

html = requests.get("https://www.google.com/search", params=params, headers=headers)
soup = BeautifulSoup(html.text, 'lxml')

for result in soup.select('div[jsname=dTDiAc]'):
    link = f"https://www.google.com{result.a['href']}"
    being_used_on = result['data-lpage']
    print(f'Link: {link}\nBeing used on: {being_used_on}\n')

# finding all script (<script>) tags
script_img_tags = soup.find_all('script')

# https://regex101.com/r/L3IZXe/4
img_matches = re.findall(r"s='data:image/jpeg;base64,(.*?)';", str(script_img_tags))

for index, image in enumerate(img_matches):
    try:
        # https://stackoverflow.com/a/6966225/15164646
        final_image = Image.open(BytesIO(base64.b64decode(str(image))))

        # https://www.educative.io/edpresso/absolute-vs-relative-path
        # https://stackoverflow.com/a/31434485/15164646
        final_image.save(f'your/absolute_or_relative/path/inline_image_{index}.jpg', 'JPEG')
    except:
        pass

------------------
# part of the output:
'''
Link: https://www.google.com/search?q=minecraft+shaders+photo&tbm=isch&source=iu&ictx=1&fir=1DCWjzl0od3bFM%252Cc4Qd0ZKVFnHrsM%252C_&vet=1&usg=AI4_-kTAvknTGktfEC1K8ciH7Ot7GsAFkA&sa=X&ved=2ahUKEwiAiaDV6_HxAhVBeawKHfbtDCIQ9QF6BAgWEAE#imgrc=1DCWjzl0od3bFM
Being used on: https://pixabay.com/illustrations/minecraft-shader-minecraft-wallpaper-1970876/

Link: https://www.google.com/search?q=minecraft+shaders+photo&tbm=isch&source=iu&ictx=1&fir=bwVoAE4HTl8GXM%252Cz3y5GvasoN8hFM%252C_&vet=1&usg=AI4_-kRfUHjrz711om99elb_i3GwJuTBnw&sa=X&ved=2ahUKEwiAiaDV6_HxAhVBeawKHfbtDCIQ9QF6BAgVEAE#imgrc=bwVoAE4HTl8GXM
Being used on: https://www.pcgamesn.com/minecraft/minecraft-shaders-best-graphics-mods
...
'''
```

Saved images in the background:
![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/8tgz4m605zsus6atvb3r.png)


GIF to illustrate the output:
<img width="100%" style="width:100%" src="https://media.giphy.com/media/Pgdu72pyzDPmQZvLwF/giphy.gif">


### Using [Google Inline Images API](https://serpapi.com/google-inline-images)
SerpApi is a paid API with a free  trial of 5,000 searches.

The biggest difference is that you don't have to figure out from where to parse certain elements in order to get a proper image size since it's already done for the end-user. Other than that, there's no need to maintaining the parser or finding ways if your script request gets blocked.

```python
import json
from serpapi import GoogleSearch

params = {
  "api_key": "YOUR_API_KEY",
  "engine": "google",
  "q": "minecraft shaders photo",
  "hl": "en",
}

search = GoogleSearch(params)
results = search.get_dict()

print(json.dumps(results['inline_images'], indent=2, ensure_ascii=False))

------------------------
'''
[
  {
    "link": "/search?q=minecraft+shaders+photo&hl=en&tbm=isch&source=iu&ictx=1&fir=bwVoAE4HTl8GXM%252Cz3y5GvasoN8hFM%252C_&vet=1&usg=AI4_-kRfUHjrz711om99elb_i3GwJuTBnw&sa=X&ved=2ahUKEwit6Jq38PHxAhUkSTABHfJyCn8Q9QF6BAgWEAE#imgrc=bwVoAE4HTl8GXM",
    "thumbnail": "https://serpapi.com/searches/60f6e03895bf92b91f6fb3d6/images/9cce8031b6aba2675322296c8d247839d434db3be723a5fec2f933d8b4bd4d1e.jpeg"
  }
]
...
'''
```


### Links
[Code in the online IDE](https://replit.com/@DimitryZub1/Scrape-Google-Inline-Images-python#bs4_result.py) • [Google Inline Images API](https://serpapi.com/google-inline-images)


### Outro
If you have any questions or something isn't working correctly or you want to write something else, feel free to drop a comment in the comment section or via Twitter at [@serp_api](https://twitter.com/serp_api).

Yours,
Dimitry, and the rest of SerpApi Team.