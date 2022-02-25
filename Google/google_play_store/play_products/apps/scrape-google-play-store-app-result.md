- <a href="#what_will_be_scraped">What will be scraped</a>
- <a href="#prerequisites">Prerequisites</a>
- <a href="#full_code">Full Code</a>
  - <a href="#code_explanation">Code Explanation</a>
- <a href="#links">Links</a>
- <a href="#outro">Outro</a>

___

<h2 id="intro">Intro</h2>



You can use official the Google Play Developer API which has a default limit of [200,000 requests per day](https://developers.google.com/android-publisher/quotas#:~:text=The%20Google%20Play%20Developer%20API,of%20the%20Google%20Cloud%20Console.), [60 requests per hour for retrieving the list of reviews and individual reviews](https://developers.google.com/android-publisher/reply-to-reviews#retrieving_reviews), which is roughly [1 request every 2 minutes](https://stackoverflow.com/a/55241419/15164646). 

You can use a complete third-party Google Play Store App scraping solution for [Python `google-play-scraper`](https://github.com/JoMingyu/google-play-scraper) without any external dependencies, and [JavaScript `google-play-scraper`](https://github.com/facundoolano/google-play-scraper). Third-party solutions are usually used to break the quota limit.

You don't really need to read this post unless you need a step-by-step explanation without using browser automation such as `playwright` and `selenium` since you can see what Python [`google-play-scraper` `regex` solution is](https://github.com/JoMingyu/google-play-scraper/blob/4936a95ccf8c6de9b3d9cc85e98fbb9bb652352a/google_play_scraper/constants/regex.py#L4), [how it scrapes app results](https://github.com/JoMingyu/google-play-scraper/blob/master/google_play_scraper/features/app.py), and [how it scrapes review results](https://github.com/JoMingyu/google-play-scraper/blob/master/google_play_scraper/features/reviews.py).  

This blog post is meant to give an idea and actual step-by-step examples of how to scrape Google Play Store App using `beautifulsoup` and regular expressions.

<h2 id="what_will_be_scraped">What will be scraped</h2>


![image](https://user-images.githubusercontent.com/78694043/150628666-d9a11726-b25d-4fba-9fa2-110a7f4b8bcf.png)


![image](https://user-images.githubusercontent.com/78694043/150628848-89c0eaed-e1a8-4920-9cbe-c2acd3d21efc.png)


<h2 id="prerequisites">Prerequisites</h2>


**Separate virtual environment**

In short, it's a thing that creates an independent set of installed libraries including different Python versions that can coexist with each other at the same system thus prevention libraries or Python version conflicts.

If you didn't work with a virtual environment before, have a look at the dedicated [Python virtual environments tutorial using Virtualenv and Poetry](https://serpapi.com/blog/python-virtual-environments-using-virtualenv-and-poetry/) blog post of mine to get familiar.

📌Note: this is not a strict requirement for this blog post.

**Install libraries**:

```lang-none
pip install requests lxml beautifulsoup4
```

**Reduce the chance of being blocked**

There's a chance that a request might be blocked. Have a look at [how to reduce the chance of being blocked while web-scraping](https://serpapi.com/blog/how-to-reduce-chance-of-being-blocked-while-web/), there are eleven methods to bypass blocks from most websites. Only `user-agent`, which is the easiest method, was covered in this blog post. 

___


<h2 id="full_code">Full Code</h2>

```python
from bs4 import BeautifulSoup
import requests, lxml, re, json
from datetime import datetime

# user-agent headers to act as a "real" user visit
headers = {
    "user-agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
}

# search query params
params = {
    "id": "com.nintendo.zara",  # app name
    "gl": "RU"  # country
}


def scrape_google_store_app():
    html = requests.get("https://play.google.com/store/apps/details", params=params, headers=headers, timeout=10).text
    soup = BeautifulSoup(html, "lxml")

    # where all app data will be stored
    app_data = []

    # <script> position is not changing that's why [12] index being selected. Other <script> tags position are changing.
    # [12] index is a basic app information
    # https://regex101.com/r/DrK0ih/1
    basic_app_info = json.loads(re.findall(r"<script nonce=\".*\" type=\"application/ld\+json\">(.*?)</script>",
                                           str(soup.select("script")[12]), re.DOTALL)[0])

    app_name = basic_app_info["name"]
    app_type = basic_app_info["@type"]
    app_url = basic_app_info["url"]
    app_description = basic_app_info["description"].replace("\n", "")  # replace new line character to nothing
    app_category = basic_app_info["applicationCategory"]
    app_operating_system = basic_app_info["operatingSystem"]
    app_main_thumbnail = basic_app_info["image"]

    app_content_rating = basic_app_info["contentRating"]
    app_rating = round(float(basic_app_info["aggregateRating"]["ratingValue"]), 1)  # 4.287856 -> 4.3
    app_reviews = basic_app_info["aggregateRating"]["ratingCount"]

    app_author = basic_app_info["author"]["name"]
    app_author_url = basic_app_info["author"]["url"]

    # https://regex101.com/r/VX8E7U/1
    app_images_data = re.findall(r",\[\d{3,4},\d{3,4}\],.*?(https.*?)\"", str(soup.select("script")))
    # delete duplicates from app_images_data
    app_images = [item for item in app_images_data if app_images_data.count(item) == 1]

    # User comments
    app_user_comments = []

    # https://regex101.com/r/SrP5DS/1
    app_user_reviews_data = re.findall(r"(\[\"gp.*?);</script>",
                                       str(soup.select("script")), re.DOTALL)

    for review in app_user_reviews_data:
        # https://regex101.com/r/M24tiM/1
        user_name = re.findall(r"\"gp:.*?\",\s?\[\"(.*?)\",", str(review))
        # https://regex101.com/r/TGgR45/1
        user_avatar = [avatar.replace('"', "") for avatar in re.findall(r"\"gp:.*?\"(https.*?\")", str(review))]

        # replace single/double quotes at the start/end of a string
        # https://regex101.com/r/iHPOrI/1
        user_comments = [comment.replace('"', "").replace("'", "") for comment in
                        re.findall(r"gp:.*?https:.*?]]],\s?\d+?,.*?,\s?(.*?),\s?\[\d+,", str(review))]

        # comment utc timestamp
        # use datetime.utcfromtimestamp(int(date)).date() to have only a date
        user_comment_date = [str(datetime.utcfromtimestamp(int(date))) for date in re.findall(r"\[(\d+),", str(review))]

        # https://regex101.com/r/GrbH9A/1
        user_comment_id = [ids.replace('"', "") for ids in re.findall(r"\[\"(gp.*?),", str(review))]
        # https://regex101.com/r/jRaaQg/1
        user_comment_likes = re.findall(r",?\d+\],?(\d+),?", str(review))
        # https://regex101.com/r/Z7vFqa/1
        user_comment_app_rating = re.findall(r"\"gp.*?https.*?\],(.*?)?,", str(review))

        for name, avatar, comment, date, comment_id, likes, user_app_rating in zip(user_name,
                                                                                   user_avatar,
                                                                                   user_comments,
                                                                                   user_comment_date,
                                                                                   user_comment_id,
                                                                                   user_comment_likes,
                                                                                   user_comment_app_rating):
            app_user_comments.append({
                "user_name": name,
                "user_avatar": avatar,
                "comment": comment,
                "user_app_rating": user_app_rating,
                "user__comment_likes": likes,
                "user_comment_published_at": date,
                "user_comment_id": comment_id
            })

        app_data.append({
            "app_name": app_name,
            "app_type": app_type,
            "app_url": app_url,
            "app_main_thumbnail": app_main_thumbnail,
            "app_description": app_description,
            "app_content_rating": app_content_rating,
            "app_category": app_category,
            "app_operating_system": app_operating_system,
            "app_rating": app_rating,
            "app_reviews": app_reviews,
            "app_author": app_author,
            "app_author_url": app_author_url,
            "app_screenshots": app_images
        })

        return {"app_data": app_data, "app_user_comments": app_user_comments}


print(json.dumps(scrape_google_store_app(), indent=2))

# output:

{
  "app_data": [
    {
      "app_name": "Super Mario Run",
      "app_type": "SoftwareApplication",
      "app_url": "https://play.google.com/store/apps/details/Super_Mario_Run?id=com.nintendo.zara&hl=en_US&gl=US",
      "app_main_thumbnail": "https://play-lh.googleusercontent.com/5LIMaa7WTNy34bzdFhBETa2MRj7mFJZWb8gCn_uyxQkUvFx_uOFCeQjcK16c6WpBA3E",
      "app_description": "A new kind of Mario game that you can play with one hand.You control Mario by tapping as he constantly runs forward. You time your taps to pull off stylish jumps, midair spins, and wall jumps to gather coins and reach the goal!Super Mario Run can be downloaded for free and after you purchase the game, you will be able to play all the modes with no additional payment required. You can try out all four modes before purchase: World Tour, Toad Rally, Remix 10, and Kingdom Builder.\u25a0World TourRun and jump with style to rescue Princess Peach from Bowser\u2019s clutches! Travel through plains, caverns, ghost houses, airships, castles, and more.Clear the 24 exciting courses to rescue Princess Peach from Bowser, waiting in his castle at the end. There are many ways to enjoy the courses, such as collecting the 3 different types of colored coins or by competing for the highest score against your friends. You can try courses 1-1 to 1-4 for free.After rescuing Princess Peach, a nine-course special world, World Star, will appear.\u25a0Remix 10Some of the shortest Super Mario Run courses you'll ever play!This mode is Super Mario Run in bite-sized bursts! You'll play through 10 short courses one after the other, with the courses changing each time you play. Daisy is lost somewhere in Remix 10, so try to clear as many courses as you can to find her!\u25a0Toad RallyShow off Mario\u2019s stylish moves, compete against your friends, and challenge people from all over the world.In this challenge mode, the competition differs each time you play.Compete against the stylish moves of other players for the highest score as you gather coins and get cheered on by a crowd of Toads. Fill the gauge with stylish moves to enter Coin Rush Mode to get more coins. If you win the rally, the cheering Toads will come live in your kingdom, and your kingdom will grow. \u25a0Kingdom BuilderGather coins and Toads to build your very own kingdom.Combine different buildings and decorations to create your own unique kingdom. There are over 100 kinds of items in Kingdom Builder mode. If you get more Toads in Toad Rally, the number of buildings and decorations available will increase. With the help of the friendly Toads you can gradually build up your kingdom.\u25a0What You Can Do After Purchasing All Worlds\u30fb All courses in World Tour are playableWhy not try out the bigger challenges and thrills available in all courses?\u30fb Easier to get Rally TicketsIt's easier to get Rally Tickets that are needed to play Remix 10 and Toad Rally. You can collect them in Kingdom Builder through Bonus Game Houses and ? Blocks, by collecting colored coins in World Tour, and more.\u30fb More playable charactersIf you rescue Princess Peach by completing course 6-4 and build homes for Luigi, Yoshi, and Toadette in Kingdom Builder mode, you can get them to join your adventures as playable characters. They play differently than Mario, so why not put their special characteristics to good use in World Tour and Toad Rally?\u30fb More courses in Toad RallyThe types of courses available in Toad Rally will increase to seven different types of courses, expanding the fun! Along with the new additions, Purple and Yellow Toads may also come to cheer for you.\u30fb More buildings and decorations in Kingdom BuilderThe types of buildings available will increase, so you'll be able to make your kingdom even more lively. You can also place Rainbow Bridges to expand your kingdom.\u30fb Play Remix 10 without having to waitYou can play Remix 10 continuously, without having to wait between each game.*Internet connectivity required to play. Data charges may apply. May contain advertisements.",
      "app_content_rating": "Everyone",
      "app_category": "GAME_ACTION",
      "app_operating_system": "ANDROID",
      "app_rating": 3.9,
      "app_reviews": "1615781",
      "app_author": "Nintendo Co., Ltd.",
      "app_author_url": "https://supermariorun.com/",
      "app_screenshots": [
        "https://play-lh.googleusercontent.com/dcv6Z-pr3MsSvxYh_UiwvJem8fktDUsvvkPREnPaHYienbhT31bZ2nUqHqGpM1jdal8",
        "https://play-lh.googleusercontent.com/SVYZCU-xg-nvaBeJ-rz6rHSSDp20AK-5AQPfYwI38nV8hPzFHEqIgFpc3LET-Dmu-Q",
        "https://play-lh.googleusercontent.com/Nne-dalTl8DJ9iius5oOLmFe-4DnvZocgf92l8LTV0ldr9JVQ2BgeW_Bbjb5nkVngrQ",
        "https://play-lh.googleusercontent.com/yIqljB_Jph_T_ITmVFTpmDV0LKXVHWmsyLOVyEuSjL2794nAhTBaoeZDpTZZLahyRsE",
        "https://play-lh.googleusercontent.com/5HdGRlNsBvHTNLo-vIsmRLR8Tr9degRfFtungX59APFaz8OwxTnR_gnHOkHfAjhLse7e",
        "https://play-lh.googleusercontent.com/bPhRpYiSMGKwO9jkjJk1raR7cJjMgPcUFeHyTg_I8rM7_6GYIO9bQm6xRcS4Q2qr6mRx",
        "https://play-lh.googleusercontent.com/7DOCBRsIE5KncQ0AzSA9nSnnBh0u0u804NAgux992BhJllLKGNXkMbVFWH5pwRwHUg",
        "https://play-lh.googleusercontent.com/PCaFxQba_CvC2pi2N9Wuu814srQOUmrW42mh-ZPCbk_xSDw3ubBX7vOQeY6qh3Id3YE",
        "https://play-lh.googleusercontent.com/fQne-6_Le-sWScYDSRL9QdG-I2hWxMbe2QbDOzEsyu3xbEsAb_f5raRrc6GUNAHBoQ",
        "https://play-lh.googleusercontent.com/ql7LENlEZaTq2NaPuB-esEPDXM2hs1knlLa2rWOI3uNuQ77hnC1lLKNJrZi9XKZFb4I",
        "https://play-lh.googleusercontent.com/UIHgekhfttfNCkd5qCJNaz2_hPn67fOkv40_5rDjf5xot-QhsDCo2AInl9036huUtCwf",
        "https://play-lh.googleusercontent.com/7iH7-GjfS_8JOoO7Q33JhOMnFMK-O8k7jP0MUI75mYALK0kQsMsHpHtIJidBZR46sfU",
        "https://play-lh.googleusercontent.com/czt-uL-Xx4fUgzj_JbNA--RJ3xsXtjAxMK7Q_wFZdoMM6nL_g-4S5bxxX3Di3QTCwgw",
        "https://play-lh.googleusercontent.com/e5HMIP0FW9MCoAEGYzji9JsrvyovpZ3StHiIANughp3dovUxdv_eHiYT5bMz38bowOI",
        "https://play-lh.googleusercontent.com/nv2BP1glvMWX11mHC8GWlh_UPa096_DFOKwLZW4DlQQsrek55pY2lHr29tGwf2FEXHM",
        "https://play-lh.googleusercontent.com/xwWDr_Ib6dcOr0H0OTZkHupwSrpBoNFM6AXNzNO27_RpX_BRoZtKIULKEkigX8ETOKI",
        "https://play-lh.googleusercontent.com/AxHkW996UZvDE21HTkGtQPU8JiQLzNxp7yLoQiSCN29Y54kZYvf9aWoR6EzAlnoACQ",
        "https://play-lh.googleusercontent.com/xFouF73v1_c5kS-mnvQdhKwl_6v3oEaLebsZ2inlJqIeF2eenXjUrUPJsjSdeAd41w",
        "https://play-lh.googleusercontent.com/a1pta2nnq6f_b9uV0adiD9Z1VVQrxSfX315fIQqgKDcy8Ji0BRC1H7z8iGnvZZaeg80",
        "https://play-lh.googleusercontent.com/SDAFLzC8i4skDJ2EcsEkXidcAJCql5YCZI76eQB15fVaD0j-ojxyxea00klquLVtNAw",
        "https://play-lh.googleusercontent.com/H7BcVUoygPu8f7oIs2dm7g5_vVt9N9878f-rGd0ACd-muaDEOK2774okryFfsXv9FaI",
        "https://play-lh.googleusercontent.com/5LIMaa7WTNy34bzdFhBETa2MRj7mFJZWb8gCn_uyxQkUvFx_uOFCeQjcK16c6WpBA3E",
        "https://play-lh.googleusercontent.com/DGQjTn_Hp32i88g2YrbjrCwl0mqCPCzDjTwMkECh3wXyTv4y6zECR5VNbAH_At89jGgSJDQuSKsPSB-wVQ",
        "https://play-lh.googleusercontent.com/pzvdI66OFjncahvxJN714Tu5pHUJ_nJK--vg0tv5cpgaGNvjfwsxC-SKxoQh9_n_wEcCdSQF9FeuZeI"
      ]
    }
  ],
  "app_user_comments": [
    {
      "user_name": "Misha t",
      "user_avatar": "https://play-lh.googleusercontent.com/a/AATXAJxvYKOfPVaqDZg0FOUjJOV-W3qR6r_cMAz0XMgU\\u003dmo",
      "comment": "Fun game, but it does not warns you that only World 1 (out of 6) is free, others are behind paywall. Dont spend your time if you want full game for free",
      "user_app_rating": "1",
      "user__comment_likes": "9",
      "user_comment_published_at": "2021-09-07 19:01:46",
      "user_comment_id": "gp:AOqpTOFb_Fc_r33sWOwoSN8Zq4DDV7C9xuPTLUatfAplVowAb0NJbym2jv3j2DHBjT1o89y4z4vNZPblN60png"
    },
    {
      "user_name": "Dangan Carlo",
      "user_avatar": "https://play-lh.googleusercontent.com/a-/AOh14GiC291ZXTKihUQukmruZDx2MJjb5-tMmeCC7Ag3KQ",
      "comment": "The game is fun but you have to pay for the World 1 Boss Fight or do some challenges, and after that the rest of the game needs to be purchased. 10 dollars is too much for a game that can be beat under an hour and especially if its a mobile game. I doubt youll take down the 10 dollar price tag but itd be nice if you could.",
      "user_app_rating": "3",
      "user__comment_likes": "316",
      "user_comment_published_at": "2022-01-04 22:31:34",
      "user_comment_id": "gp:AOqpTOHLIo3dK33ItsiFuHzWadDIbu25RfHoTp8SGcZJTlY3BWMJk4X7FtJwABPSaq2tOd-LEo_3h7qnXOroJg"
    }
    {
      "user_name": "Marcus Hughes",
      "user_avatar": "https://play-lh.googleusercontent.com/a-/AOh14Gisjmr1druQ7QamKHqg0N9qq5ahGmaMQNhS2a35jw",
      "comment": "Amazing! Only one thing would make this game better.... ENDLESS MODE! It would be VERY awesome if you created an endless mode where you can endlessly repeat the same stage, only it gets more difficult as you progress, such as new enemies/obstacles, but its one stage.... Preferably itd be cool if every stage had this.",
      "user_app_rating": "5",
      "user__comment_likes": "193",
      "user_comment_published_at": "2022-01-09 19:36:23",
      "user_comment_id": "gp:AOqpTOEgyCt_NTr2otrPyb2w-l3j8xmROvlkx-xeadRCV2aAt1X9HOwXG7v2f1S0K5vvBM2d3JcY2qAvhSJ80Q"
    }, # OTHER USER COMMENTS
  ]
}
```

<h2 id="code_explanation">Code explanation</h2>

Import libraries:

```python
from bs4 import BeautifulSoup
import requests, lxml, re, json
from datetime import datetime
```

- `BeautifulSoup`, `lxml` to parse HTML.
- `requests` to make a request to a website.
- `re` to match parts of the HTML where needed data is located via regular expression.
- `json` to convert parsed data from JSON to Python dictionary, and for pretty printing.
- `datetime` to convert UTC timestamp to human-readable date format.


Create `global` request headers, and search query `params`:  

```python
# user-agent headers to act as a "real" user visit
headers = {
    "user-agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
}

# search query params
params = {
    "id": "com.nintendo.zara",  # app name
    "gl": "RU"  # country
}
```

- [`user-agent`](https://developer.mozilla.org/en-US/docs/Glossary/User_agent) is used to pretend that it's a real user visit from an actual browser so websites will assume that it's not a bot that send a request.

Pass `params`, `headers` to a request:  

```python
html = requests.get("https://play.google.com/store/apps/details", params=params, headers=headers, timeout=10).text
```

- `timeout` argument will tell `request` to stop waiting for a response after 10 seconds.

Create a `BeautifulSoup` object from returned HTML, pass HTML parser which in this case is `lxml`:

```python
soup = BeautifulSoup(html, "lxml")
```

Create a temporary `list()` to store extracted app data:
```python
app_data = []
```

Match basic app information via regular expression: 

```python
# https://regex101.com/r/DrK0ih/1
basic_app_info = json.loads(re.findall(r"<script nonce=\".*\" type=\"application/ld\+json\">(.*?)</script>",
                                       str(soup.select("script")[12]), re.DOTALL)[0])
```

- `re.findall()` will find all matched patterns in the HTML. Follow commented link to better understand what regular expression is matching.
- `(.*?)` is a regex capture group `(...)`, and `.*?` is a pattern to capture everything.
- `str(soup.select("script")[12])` is the second `re.findall()` argument which:
  - tells `soup` to grab all found `script` tags,
  - then grab only `[12]` index from returned `<script>` tags, 
  - convert it to a `string` so `re` module could process it.
- `re.DOTALL` will [tell `re` to match everything, including newlines](https://docs.python.org/3/library/re.html#re.DOTALL).
- `re.findall()[0]` will access first index from the returned `list` of matches which is the only match in this case and used to convert the `type` from `list` to `str`.
- `json.loads()` will convert parsed JSON to Python dictionary.

Access parsed JSON converted to dictionary data:   

```python
app_name = basic_app_info["name"]
app_type = basic_app_info["@type"]
app_url = basic_app_info["url"]
app_description = basic_app_info["description"].replace("\n", "")  # replace new line character with nothing
app_category = basic_app_info["applicationCategory"]
app_operating_system = basic_app_info["operatingSystem"]
app_main_thumbnail = basic_app_info["image"]

app_content_rating = basic_app_info["contentRating"]
app_rating = round(float(basic_app_info["aggregateRating"]["ratingValue"]), 1)  # 4.287856 -> 4.3
app_reviews = basic_app_info["aggregateRating"]["ratingCount"]

app_author = basic_app_info["author"]["name"]
app_author_url = basic_app_info["author"]["url"]
```

Match app screenshots data via regular expression:

```python
# https://regex101.com/r/VX8E7U/1
# Follow the link to better understand what regular expression is matching.
app_images_data = re.findall(r",\[\d{3,4},\d{3,4}\],.*?(https.*?)\"", str(soup.select("script")))
```

Iterate over matched images and filter duplicates from matched data:

```python
app_images = [item for item in app_images_data if app_images_data.count(item) == 1]
```

- `if app_images_data.count(item) == 1`:
  - `count(item)` returns the number of occurrences of the value, link in this case.
  - If link appears _exactly_ 1 time, it will be added to the list, if more than 1 time it will be skipped.

📌Note: [`count()` function is not advisable for filtering elements from the same iterator](https://www.journaldev.com/32742/python-remove-duplicates-from-list) because it can lead to unwanted results. 

Keep in mind that this is an example, there're multiple ways of filtering duplicates and use the one in which you are sure. In this case `count()` method filters from 71 to 23 links:

```python
app_images_data = re.findall(r",\[\d{3,4},\d{3,4}\],.*?(https.*?)\"", str(soup.select("script")))

app_images_not_filtered = [item for item in app_images_data]
app_images_filtered = [item for item in app_images_data if app_images_data.count(item) == 1]

print(len(app_images_not_filtered))
print(app_images_not_filtered)

print(len(app_images_filtered))
print(app_images_filtered)

'''
71
['https://play-lh.googleusercontent.com/dcv6Z-pr3MsSvxYh_UiwvJem8fktDUsvvkPREnPaHYienbhT31bZ2nUqHqGpM1jdal8', 'https://play-lh.googleusercontent.com/SVYZCU-xg-nvaBeJ-rz6rHSSDp20AK-5AQPfYwI38nV8hPzFHEqIgFpc3LET-Dmu-Q', 'https://play-lh.googleusercontent.com/Nne-dalTl8DJ9iius5oOLmFe-4DnvZocgf92l8LTV0ldr9JVQ2BgeW_Bbjb5nkVngrQ', 'https://play-lh.googleusercontent.com/yIqljB_Jph_T_ITmVFTpmDV0LKXVHWmsyLOVyEuSjL2794nAhTBaoeZDpTZZLahyRsE', 'https://play-lh.googleusercontent.com/5HdGRlNsBvHTNLo-vIsmRLR8Tr9degRfFtungX59APFaz8OwxTnR_gnHOkHfAjhLse7e', 'https://play-lh.googleusercontent.com/bPhRpYiSMGKwO9jkjJk1raR7cJjMgPcUFeHyTg_I8rM7_6GYIO9bQm6xRcS4Q2qr6mRx', 'https://play-lh.googleusercontent.com/7DOCBRsIE5KncQ0AzSA9nSnnBh0u0u804NAgux992BhJllLKGNXkMbVFWH5pwRwHUg', 'https://play-lh.googleusercontent.com/PCaFxQba_CvC2pi2N9Wuu814srQOUmrW42mh-ZPCbk_xSDw3ubBX7vOQeY6qh3Id3YE', 'https://play-lh.googleusercontent.com/fQne-6_Le-sWScYDSRL9QdG-I2hWxMbe2QbDOzEsyu3xbEsAb_f5raRrc6GUNAHBoQ', 'https://play-lh.googleusercontent.com/ql7LENlEZaTq2NaPuB-esEPDXM2hs1knlLa2rWOI3uNuQ77hnC1lLKNJrZi9XKZFb4I', 'https://play-lh.googleusercontent.com/UIHgekhfttfNCkd5qCJNaz2_hPn67fOkv40_5rDjf5xot-QhsDCo2AInl9036huUtCwf', 'https://play-lh.googleusercontent.com/7iH7-GjfS_8JOoO7Q33JhOMnFMK-O8k7jP0MUI75mYALK0kQsMsHpHtIJidBZR46sfU', 'https://play-lh.googleusercontent.com/czt-uL-Xx4fUgzj_JbNA--RJ3xsXtjAxMK7Q_wFZdoMM6nL_g-4S5bxxX3Di3QTCwgw', 'https://play-lh.googleusercontent.com/e5HMIP0FW9MCoAEGYzji9JsrvyovpZ3StHiIANughp3dovUxdv_eHiYT5bMz38bowOI', 'https://play-lh.googleusercontent.com/nv2BP1glvMWX11mHC8GWlh_UPa096_DFOKwLZW4DlQQsrek55pY2lHr29tGwf2FEXHM', 'https://play-lh.googleusercontent.com/xwWDr_Ib6dcOr0H0OTZkHupwSrpBoNFM6AXNzNO27_RpX_BRoZtKIULKEkigX8ETOKI', 'https://play-lh.googleusercontent.com/AxHkW996UZvDE21HTkGtQPU8JiQLzNxp7yLoQiSCN29Y54kZYvf9aWoR6EzAlnoACQ', 'https://play-lh.googleusercontent.com/xFouF73v1_c5kS-mnvQdhKwl_6v3oEaLebsZ2inlJqIeF2eenXjUrUPJsjSdeAd41w', 'https://play-lh.googleusercontent.com/a1pta2nnq6f_b9uV0adiD9Z1VVQrxSfX315fIQqgKDcy8Ji0BRC1H7z8iGnvZZaeg80', 'https://play-lh.googleusercontent.com/SDAFLzC8i4skDJ2EcsEkXidcAJCql5YCZI76eQB15fVaD0j-ojxyxea00klquLVtNAw', 'https://play-lh.googleusercontent.com/H7BcVUoygPu8f7oIs2dm7g5_vVt9N9878f-rGd0ACd-muaDEOK2774okryFfsXv9FaI', 'https://play-lh.googleusercontent.com/5LIMaa7WTNy34bzdFhBETa2MRj7mFJZWb8gCn_uyxQkUvFx_uOFCeQjcK16c6WpBA3E', 'https://play-lh.googleusercontent.com/iTZtyWYr4T-slu1nifgRqEhtMLmxcNagc2rDAyiWntDQWCVLlGR7rDvx0uK6z-zLujwv', 'https://play-lh.googleusercontent.com/iTZtyWYr4T-slu1nifgRqEhtMLmxcNagc2rDAyiWntDQWCVLlGR7rDvx0uK6z-zLujwv', 'https://play-lh.googleusercontent.com/EbEX3AN4FC4pu3lsElAHCiksluOVU8OgkgtWC43-wmm_aHVq2D65FmEM97bPexilUAvlAY5_4ARH8Tb3RxQ', 'https://play-lh.googleusercontent.com/_re6mcALPaqotePA0WkgYeOQ6TighHRUS62FRmREPEhyZPdGM3QmRjcSpiMt6Pz1O-WZyvEIy4mtGHj9zw', 'https://play-lh.googleusercontent.com/SI2XoFyY35xzlMz3cZdTH7SSxMDfJTJjKNtbso33YIyYknmxJnBLrfLPJ131gz3O259sB9gP9dcmSvRNFw', 'https://play-lh.googleusercontent.com/SI2XoFyY35xzlMz3cZdTH7SSxMDfJTJjKNtbso33YIyYknmxJnBLrfLPJ131gz3O259sB9gP9dcmSvRNFw', 'https://play-lh.googleusercontent.com/pzvdI66OFjncahvxJN714Tu5pHUJ_nJK--vg0tv5cpgaGNvjfwsxC-SKxoQh9_n_wEcCdSQF9FeuZeI', 'https://play-lh.googleusercontent.com/EbEX3AN4FC4pu3lsElAHCiksluOVU8OgkgtWC43-wmm_aHVq2D65FmEM97bPexilUAvlAY5_4ARH8Tb3RxQ', 'https://play-lh.googleusercontent.com/_re6mcALPaqotePA0WkgYeOQ6TighHRUS62FRmREPEhyZPdGM3QmRjcSpiMt6Pz1O-WZyvEIy4mtGHj9zw', 'https://play-lh.googleusercontent.com/_re6mcALPaqotePA0WkgYeOQ6TighHRUS62FRmREPEhyZPdGM3QmRjcSpiMt6Pz1O-WZyvEIy4mtGHj9zw', 'https://play-lh.googleusercontent.com/z6aS2wnyp16KA9CFEep7HvZd2DmwRfoR9NWm9oHWRw-tuXLE_CPbnb1OL39-a456EgA', 'https://play-lh.googleusercontent.com/z6aS2wnyp16KA9CFEep7HvZd2DmwRfoR9NWm9oHWRw-tuXLE_CPbnb1OL39-a456EgA', 'https://play-lh.googleusercontent.com/z6aS2wnyp16KA9CFEep7HvZd2DmwRfoR9NWm9oHWRw-tuXLE_CPbnb1OL39-a456EgA', 'https://play-lh.googleusercontent.com/kMnXlmzr3b8Tbzs_xDy3vq12fnZ6PM4LVlxPlFMKf_VZVkk1v7xeAUpJxW6iYab9m_w', 'https://play-lh.googleusercontent.com/kMnXlmzr3b8Tbzs_xDy3vq12fnZ6PM4LVlxPlFMKf_VZVkk1v7xeAUpJxW6iYab9m_w', 'https://play-lh.googleusercontent.com/kMnXlmzr3b8Tbzs_xDy3vq12fnZ6PM4LVlxPlFMKf_VZVkk1v7xeAUpJxW6iYab9m_w', 'https://play-lh.googleusercontent.com/5BFo6FvdAn0c10xiDKO_GZMtHmn-4qxHTtF6rarC162rCNqnA7jub30CYWmzC_DZ1l4', 'https://play-lh.googleusercontent.com/5BFo6FvdAn0c10xiDKO_GZMtHmn-4qxHTtF6rarC162rCNqnA7jub30CYWmzC_DZ1l4', 'https://play-lh.googleusercontent.com/5BFo6FvdAn0c10xiDKO_GZMtHmn-4qxHTtF6rarC162rCNqnA7jub30CYWmzC_DZ1l4', 'https://play-lh.googleusercontent.com/9EYrR6ilBWJFLt_LE_QniHZjdYlG9on6PzTOqR9tBf3SKiWU4lIDOXq-kXrrSKyyEg', 'https://play-lh.googleusercontent.com/9EYrR6ilBWJFLt_LE_QniHZjdYlG9on6PzTOqR9tBf3SKiWU4lIDOXq-kXrrSKyyEg', 'https://play-lh.googleusercontent.com/9EYrR6ilBWJFLt_LE_QniHZjdYlG9on6PzTOqR9tBf3SKiWU4lIDOXq-kXrrSKyyEg', 'https://play-lh.googleusercontent.com/pyJ4VUsm75cc800LalWMZupRMG7o-JictgTeSIUKni2Hn2ncR4m22hgV_LhTahsRt0U', 'https://play-lh.googleusercontent.com/pyJ4VUsm75cc800LalWMZupRMG7o-JictgTeSIUKni2Hn2ncR4m22hgV_LhTahsRt0U', 'https://play-lh.googleusercontent.com/pyJ4VUsm75cc800LalWMZupRMG7o-JictgTeSIUKni2Hn2ncR4m22hgV_LhTahsRt0U', 'https://play-lh.googleusercontent.com/z6aS2wnyp16KA9CFEep7HvZd2DmwRfoR9NWm9oHWRw-tuXLE_CPbnb1OL39-a456EgA', 'https://play-lh.googleusercontent.com/z6aS2wnyp16KA9CFEep7HvZd2DmwRfoR9NWm9oHWRw-tuXLE_CPbnb1OL39-a456EgA', 'https://play-lh.googleusercontent.com/z6aS2wnyp16KA9CFEep7HvZd2DmwRfoR9NWm9oHWRw-tuXLE_CPbnb1OL39-a456EgA', 'https://play-lh.googleusercontent.com/H8AjtJR4LviiM3M8dg1BrS7_XzHBziG91Cn-udo8w44fRPo5mwj6NL683JBJQslpnZOY', 'https://play-lh.googleusercontent.com/H8AjtJR4LviiM3M8dg1BrS7_XzHBziG91Cn-udo8w44fRPo5mwj6NL683JBJQslpnZOY', 'https://play-lh.googleusercontent.com/H8AjtJR4LviiM3M8dg1BrS7_XzHBziG91Cn-udo8w44fRPo5mwj6NL683JBJQslpnZOY', 'https://play-lh.googleusercontent.com/DGP09C5sfjxaawTV0JUIFTDKJ0579kmss59AkjHzvz6ry6FSjTzjHGO8GiB3BwglPI5g', 'https://play-lh.googleusercontent.com/DGP09C5sfjxaawTV0JUIFTDKJ0579kmss59AkjHzvz6ry6FSjTzjHGO8GiB3BwglPI5g', 'https://play-lh.googleusercontent.com/DGP09C5sfjxaawTV0JUIFTDKJ0579kmss59AkjHzvz6ry6FSjTzjHGO8GiB3BwglPI5g', 'https://play-lh.googleusercontent.com/tUB0fBVdN0pLn_wpfKRETC3jcraaYc7nFEDCOFsE7SUK0WCKpUWO0k3pOi-x-bPkIAo', 'https://play-lh.googleusercontent.com/tUB0fBVdN0pLn_wpfKRETC3jcraaYc7nFEDCOFsE7SUK0WCKpUWO0k3pOi-x-bPkIAo', 'https://play-lh.googleusercontent.com/tUB0fBVdN0pLn_wpfKRETC3jcraaYc7nFEDCOFsE7SUK0WCKpUWO0k3pOi-x-bPkIAo', 'https://play-lh.googleusercontent.com/z6aS2wnyp16KA9CFEep7HvZd2DmwRfoR9NWm9oHWRw-tuXLE_CPbnb1OL39-a456EgA', 'https://play-lh.googleusercontent.com/z6aS2wnyp16KA9CFEep7HvZd2DmwRfoR9NWm9oHWRw-tuXLE_CPbnb1OL39-a456EgA', 'https://play-lh.googleusercontent.com/z6aS2wnyp16KA9CFEep7HvZd2DmwRfoR9NWm9oHWRw-tuXLE_CPbnb1OL39-a456EgA', 'https://play-lh.googleusercontent.com/H8AjtJR4LviiM3M8dg1BrS7_XzHBziG91Cn-udo8w44fRPo5mwj6NL683JBJQslpnZOY', 'https://play-lh.googleusercontent.com/H8AjtJR4LviiM3M8dg1BrS7_XzHBziG91Cn-udo8w44fRPo5mwj6NL683JBJQslpnZOY', 'https://play-lh.googleusercontent.com/H8AjtJR4LviiM3M8dg1BrS7_XzHBziG91Cn-udo8w44fRPo5mwj6NL683JBJQslpnZOY', 'https://play-lh.googleusercontent.com/DGP09C5sfjxaawTV0JUIFTDKJ0579kmss59AkjHzvz6ry6FSjTzjHGO8GiB3BwglPI5g', 'https://play-lh.googleusercontent.com/DGP09C5sfjxaawTV0JUIFTDKJ0579kmss59AkjHzvz6ry6FSjTzjHGO8GiB3BwglPI5g', 'https://play-lh.googleusercontent.com/DGP09C5sfjxaawTV0JUIFTDKJ0579kmss59AkjHzvz6ry6FSjTzjHGO8GiB3BwglPI5g', 'https://play-lh.googleusercontent.com/tUB0fBVdN0pLn_wpfKRETC3jcraaYc7nFEDCOFsE7SUK0WCKpUWO0k3pOi-x-bPkIAo', 'https://play-lh.googleusercontent.com/tUB0fBVdN0pLn_wpfKRETC3jcraaYc7nFEDCOFsE7SUK0WCKpUWO0k3pOi-x-bPkIAo', 'https://play-lh.googleusercontent.com/tUB0fBVdN0pLn_wpfKRETC3jcraaYc7nFEDCOFsE7SUK0WCKpUWO0k3pOi-x-bPkIAo']
23
['https://play-lh.googleusercontent.com/dcv6Z-pr3MsSvxYh_UiwvJem8fktDUsvvkPREnPaHYienbhT31bZ2nUqHqGpM1jdal8', 'https://play-lh.googleusercontent.com/SVYZCU-xg-nvaBeJ-rz6rHSSDp20AK-5AQPfYwI38nV8hPzFHEqIgFpc3LET-Dmu-Q', 'https://play-lh.googleusercontent.com/Nne-dalTl8DJ9iius5oOLmFe-4DnvZocgf92l8LTV0ldr9JVQ2BgeW_Bbjb5nkVngrQ', 'https://play-lh.googleusercontent.com/yIqljB_Jph_T_ITmVFTpmDV0LKXVHWmsyLOVyEuSjL2794nAhTBaoeZDpTZZLahyRsE', 'https://play-lh.googleusercontent.com/5HdGRlNsBvHTNLo-vIsmRLR8Tr9degRfFtungX59APFaz8OwxTnR_gnHOkHfAjhLse7e', 'https://play-lh.googleusercontent.com/bPhRpYiSMGKwO9jkjJk1raR7cJjMgPcUFeHyTg_I8rM7_6GYIO9bQm6xRcS4Q2qr6mRx', 'https://play-lh.googleusercontent.com/7DOCBRsIE5KncQ0AzSA9nSnnBh0u0u804NAgux992BhJllLKGNXkMbVFWH5pwRwHUg', 'https://play-lh.googleusercontent.com/PCaFxQba_CvC2pi2N9Wuu814srQOUmrW42mh-ZPCbk_xSDw3ubBX7vOQeY6qh3Id3YE', 'https://play-lh.googleusercontent.com/fQne-6_Le-sWScYDSRL9QdG-I2hWxMbe2QbDOzEsyu3xbEsAb_f5raRrc6GUNAHBoQ', 'https://play-lh.googleusercontent.com/ql7LENlEZaTq2NaPuB-esEPDXM2hs1knlLa2rWOI3uNuQ77hnC1lLKNJrZi9XKZFb4I', 'https://play-lh.googleusercontent.com/UIHgekhfttfNCkd5qCJNaz2_hPn67fOkv40_5rDjf5xot-QhsDCo2AInl9036huUtCwf', 'https://play-lh.googleusercontent.com/7iH7-GjfS_8JOoO7Q33JhOMnFMK-O8k7jP0MUI75mYALK0kQsMsHpHtIJidBZR46sfU', 'https://play-lh.googleusercontent.com/czt-uL-Xx4fUgzj_JbNA--RJ3xsXtjAxMK7Q_wFZdoMM6nL_g-4S5bxxX3Di3QTCwgw', 'https://play-lh.googleusercontent.com/e5HMIP0FW9MCoAEGYzji9JsrvyovpZ3StHiIANughp3dovUxdv_eHiYT5bMz38bowOI', 'https://play-lh.googleusercontent.com/nv2BP1glvMWX11mHC8GWlh_UPa096_DFOKwLZW4DlQQsrek55pY2lHr29tGwf2FEXHM', 'https://play-lh.googleusercontent.com/xwWDr_Ib6dcOr0H0OTZkHupwSrpBoNFM6AXNzNO27_RpX_BRoZtKIULKEkigX8ETOKI', 'https://play-lh.googleusercontent.com/AxHkW996UZvDE21HTkGtQPU8JiQLzNxp7yLoQiSCN29Y54kZYvf9aWoR6EzAlnoACQ', 'https://play-lh.googleusercontent.com/xFouF73v1_c5kS-mnvQdhKwl_6v3oEaLebsZ2inlJqIeF2eenXjUrUPJsjSdeAd41w', 'https://play-lh.googleusercontent.com/a1pta2nnq6f_b9uV0adiD9Z1VVQrxSfX315fIQqgKDcy8Ji0BRC1H7z8iGnvZZaeg80', 'https://play-lh.googleusercontent.com/SDAFLzC8i4skDJ2EcsEkXidcAJCql5YCZI76eQB15fVaD0j-ojxyxea00klquLVtNAw', 'https://play-lh.googleusercontent.com/H7BcVUoygPu8f7oIs2dm7g5_vVt9N9878f-rGd0ACd-muaDEOK2774okryFfsXv9FaI', 'https://play-lh.googleusercontent.com/5LIMaa7WTNy34bzdFhBETa2MRj7mFJZWb8gCn_uyxQkUvFx_uOFCeQjcK16c6WpBA3E', 'https://play-lh.googleusercontent.com/pzvdI66OFjncahvxJN714Tu5pHUJ_nJK--vg0tv5cpgaGNvjfwsxC-SKxoQh9_n_wEcCdSQF9FeuZeI']
'''
```

Create temporary `list()` for user comments data:

```python
app_user_comments = []
```

Match user comments data using regular expression:

```python
# https://regex101.com/r/SrP5DS/1
# # Follow the link to better understand what regular expression is matching.
app_user_reviews_data = re.findall(r"(\[\"gp.*?);</script>",
                                   str(soup.select("script")), re.DOTALL)
```

- `re.DOTALL` will [tell `re` to match everything including newlines](https://docs.python.org/3/library/re.html#re.DOTALL).

Iterate over `app_user_reviews_data` to extract all available reviews and match appropriate data with a regular expression:

```python
# Follow the links to better understand what regular expressions are matching.

for review in app_user_reviews_data:
    # https://regex101.com/r/M24tiM/1
    user_name = re.findall(r"\"gp:.*?\",\s?\[\"(.*?)\",", str(review))
    
    # https://regex101.com/r/TGgR45/1
    user_avatar = [avatar.replace('"', "") for avatar in re.findall(r"\"gp:.*?\"(https.*?\")", str(review))]

    # replace single/double quotes at the start/end of a string
    # https://regex101.com/r/iHPOrI/1
    user_comment = [comment.replace('"', "").replace("'", "") for comment in
                    re.findall(r"gp:.*?https:.*?]]],\s?\d+?,.*?,\s?(.*?),\s?\[\d+,", str(review))]

    # comment utc timestamp
    # use datetime.utcfromtimestamp(int(date)).date() to have only a date: 2022-01-09
    user_comment_date = [str(datetime.utcfromtimestamp(int(date))) for date in re.findall(r"\[(\d+),", str(review))]

    # https://regex101.com/r/GrbH9A/1
    user_comment_id = [ids.replace('"', "") for ids in re.findall(r"\[\"(gp.*?),", str(review))]
    
    # https://regex101.com/r/jRaaQg/1
    user_comment_likes = re.findall(r",?\d+\],?(\d+),?", str(review))
    
    # https://regex101.com/r/Z7vFqa/1
    user_comment_app_rating = re.findall(r"\"gp.*?https.*?\],(.*?)?,", str(review))
```

Create another `for` loop to iterate over all user comments data in a parallel:

```python
for name, avatar, comment, date, comment_id, likes, user_app_rating in zip(user_name,
                                                                           user_avatar,
                                                                           user_comment,
                                                                           user_comment_date,
                                                                           user_comment_id,
                                                                           user_comment_likes,
                                                                           user_comment_app_rating):
```

- `zip()` [takes iterables, aggregates them  in a tuple and returns it](https://docs.python.org/3/library/functions.html#zip).
In this case, number of each value will identical for all, for example if there's 30 names there will be also 30 comment id's or comment date and so on. 


Append user comments data to temporary `list`:

```python
# for name, ... in zip(...) is here

app_user_comments.append({
    "user_name": name,
    "user_avatar": avatar,
    "comment": comment,
    "user_app_rating": user_app_rating,
    "user__comment_likes": likes,
    "user_comment_published_at": date,
    "user_comment_id": comment_id
})
```

Append app information data to temporary `list`:

```python
app_data.append({
    "app_name": app_name,
    "app_type": app_type,
    "app_url": app_url,
    "app_main_thumbnail": app_main_thumbnail,
    "app_description": app_description,
    "app_content_rating": app_content_rating,
    "app_category": app_category,
    "app_operating_system": app_operating_system,
    "app_rating": app_rating,
    "app_reviews": app_reviews,
    "app_author": app_author,
    "app_author_url": app_author_url,
    "app_screenshots": app_images
})
```

Return app and user comments data as a `dict`:

```python
return {"app_data": app_data, "app_user_comments": app_user_comments}
```

Example of accessing extracted user comments data:

```python
for review in scrape_google_store_app()["app_user_comments"]:
    print(review["user_name"],
          review["user_avatar"],
          review["comment"],
          review["user_app_rating"],
          review["user_comment_likes"], sep='\n')

# part of the output (in this case 40 commnets in total):
'''
Misha t
https://play-lh.googleusercontent.com/a/AATXAJxvYKOfPVaqDZg0FOUjJOV-W3qR6r_cMAz0XMgU\u003dmo
Fun game, but it does not warns you that only World 1 (out of 6) is free, others are behind paywall. Dont spend your time if you want full game for free
1
9
Dangan Carlo
https://play-lh.googleusercontent.com/a-/AOh14GiC291ZXTKihUQukmruZDx2MJjb5-tMmeCC7Ag3KQ
The game is fun but you have to pay for the World 1 Boss Fight or do some challenges, and after that the rest of the game needs to be purchased. 10 dollars is too much for a game that can be beat under an hour and especially if its a mobile game. I doubt youll take down the 10 dollar price tag but itd be nice if you could.
3
316
Marcus Hughes
https://play-lh.googleusercontent.com/a-/AOh14Gisjmr1druQ7QamKHqg0N9qq5ahGmaMQNhS2a35jw
Amazing! Only one thing would make this game better.... ENDLESS MODE! It would be VERY awesome if you created an endless mode where you can endlessly repeat the same stage, only it gets more difficult as you progress, such as new enemies/obstacles, but its one stage.... Preferably itd be cool if every stage had this.
5
193
'''
```

___


<h2 id="links">Links</h2>

- [Code in the online IDE](https://replit.com/@DimitryZub1/Scrape-Google-Play-Store-App-info-and-reviews#main.py)
- [GitHub repository](https://github.com/dimitryzub/scrape-google-play-store-app)
- [Python google-play-scraper](https://github.com/JoMingyu/google-play-scraper)
- [JavaScript google-play-scraper](https://github.com/facundoolano/google-play-scraper)

___

<h2 id="outro">Outro</h2>

With such scraper you can build a dataset for app competitors, apps in a certain category, most downloaded/rated apps or any other useful analysis.

If you have anything to share, any questions, suggestions, or something that isn't working correctly, reach out via Twitter at [@dimitryzub](https://twitter.com/DimitryZub), or [@serp_api](https://twitter.com/serp_api).

Yours,
Dmitriy, and the rest of SerpApi Team.

<p style="text-align: center;">Join us on <a href="https://www.reddit.com/r/SerpApi/">Reddit</a> | <a href="https://twitter.com/serp_api">Twitter</a> | <a href="https://www.youtube.com/channel/UCUgIHlYBOD3yA3yDIRhg_mg">YouTube</a></p>