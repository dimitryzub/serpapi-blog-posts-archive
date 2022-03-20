- <a href="#intro">Intro</a>
- <a href="#what_will_be_scraped">What will be scraped</a>
- <a href="#prerequisites">Prerequisites</a>
- <a href="#playwright">Scrape Reviews with Playwright</a>
- <a href="#links">Links</a>
- <a href="#outro">Outro</a>

___

<h2 id="intro">Intro</h2>

This blog post a continuation of the [Scrape Google Play Store App in Python](https://serpapi.com/blog/scrape-google-play-store-app-in-python/) blog post that demonstrates actual examples of scraping all user reviews data using:
- easy method using a modern browser automation [`playwright`](https://playwright.dev/python/) if you don't want to deal with regex but slower.
- a bit advanced method using `beautifulsoup` and regex which is a lot faster than browser automation.

<h2 id="what_will_be_scraped">What will be scraped</h2>

![image](https://user-images.githubusercontent.com/78694043/151364153-680ee179-50e0-43a1-82cb-47737a2c4fc6.png)

If you don't need an explanation, [grab the full code from the GitHub repository](Link). 

<h2 id="prerequisites">Prerequisites</h2>

**Basic knowledge scraping with CSS selectors**

`CSS` selectors declare which part of the markup a style applies to thus allowing to extract data from matching tags and attributes.

If you haven't scraped with `CSS` selectors, there's a dedicated blog post of mine about [how to use `CSS` selectors when web-scraping](https://serpapi.com/blog/web-scraping-with-css-selectors-using-python/) that covers what it is, pros and cons, and why they're matter from a web-scraping perspective.

**Separate virtual environment**

In short, it's a thing that creates an independent set of installed libraries including different Python versions that can coexist with each other at the same system thus prevention libraries or Python version conflicts.

If you didn't work with a virtual environment before, have a look at the dedicated [Python virtual environments tutorial using Virtualenv and Poetry](https://serpapi.com/blog/python-virtual-environments-using-virtualenv-and-poetry/) blog post of mine to get familiar.

📌Note: this is not a strict requirement for this blog post.

**Install libraries**:

```lang-none
pip install requests
pip install lxml 
pip install beautifulsoup4
```

**Reduce the chance of being blocked**

There's a chance that a request might be blocked. Have a look at [how to reduce the chance of being blocked while web-scraping](https://serpapi.com/blog/how-to-reduce-chance-of-being-blocked-while-web/), there are eleven methods to bypass blocks from most websites and some of them will be covered in this blog post.

___

<h2 id="playwright">Scrape Reviews with Playwright</h2>

```python
import time, json
from playwright.sync_api import sync_playwright


def run(playwright):
    page = playwright.chromium.launch(headless=False).new_page()
    page.goto("https://play.google.com/store/apps/details?id=com.instantbrands.app&gl=US&showAllReviews=true")

    reached_end = False
    last_height = page.evaluate("() => document.body.scrollHeight")  # scrollHeight: 5879

    while not reached_end:
        if page.query_selector('.RveJvd'):
            page.query_selector('.RveJvd').click(force=True)
            time.sleep(2)
        else:
            page.keyboard.press("End")
            time.sleep(2)

        new_height = page.evaluate("() => document.body.scrollHeight")
        if new_height == last_height:
            reached_end = True
        else:
            last_height = new_height

    app_user_comments = []

    for comment in page.query_selector_all(".zc7KVe"):
        user_name = comment.query_selector(".X43Kjb").inner_text()

        try:
            user_avatar = comment.query_selector(".vDSMeb.bAhLNe img").get_attribute("src")
        except: user_avatar = None

        try:
            user_comment = comment.query_selector("[jsname=fbQN7e]").inner_text()
        except: user_comment = None

        try:
            comment_likes = comment.query_selector(".jUL89d.y92BAb").inner_text()
        except: comment_likes = None

        try:
            app_rating = comment.query_selector(".pf5lIe div[role=img]").get_attribute("aria-label").split(" ")[1]
        except: app_rating = None

        try:
            comment_date = comment.query_selector(".p2TkOb").inner_text()
        except: comment_date = None

        if user_name and user_avatar and user_comment and comment_likes and app_rating and comment_date not in app_user_comments and not None:
            app_user_comments.append({
                "user_name": user_name,
                "user_avatar": user_avatar,
                "user_comment": user_comment,
                "comment_likes": comment_likes,
                "app_rating": app_rating,
                "comment_date": comment_date
            })

    print(json.dumps(app_user_comments, indent=2))

    page.close()


with sync_playwright() as playwright:
    run(playwright)


# example output:
'''
[
  {
    "user_name": "Amber Yates",
    "user_avatar": "https://play-lh.googleusercontent.com/a/AATXAJw1oo6qIWrfLa1W_HVIVYS9qm7DSWuw2PY43QKC=w48-h48-n-rw-mo",
    "user_comment": "Great app to use when starting out with an instant pot or for a seasoned user. You can search for recipes based on a title or ingredient and then you can just click the shopping cart on the ingredient list and it will copy it to your notes/grocery list with the amount needed for each ingredient, love that part. Really great app. Only draw back, it needs to be updated to include the instant pot unit with the air fryer lid but you can adjust and figure it out once comfortable with your unit.",
    "comment_likes": "17",
    "app_rating": "5",
    "comment_date": "January 2, 2022"
  },
  {
    "user_name": "F C Alvarez",
    "user_avatar": "https://play-lh.googleusercontent.com/a/AATXAJzYnoQ4rI3wXGLmDJrCfbFN79YS7ZqFUmgb4yZc=w48-h48-n-rw-mo",
    "user_comment": "Real split pea soup!! Many recipes to choose from but the one by Jeffrey Eisner had the ingredients I like to use. It was an absolute cinch to make the first time I ever used the pot. Recipe tells you how long to do something then gives you an alarm to notify you when to move on to the next step with the option of increasing/decreasing the amount of time for each step. It's a pleasant sounding alarm. It was absolutely accurate for each step. How good can it get...? Thank you. \ud83d\ude01",
    "comment_likes": "7",
    "app_rating": "5",
    "comment_date": "January 5, 2022"
  } other comments
]
'''
```

#### `Playwright` code explanation

Import libraries:

```python
import time, json
from playwright.sync_api import sync_playwright
```

- `time` to set a `sleep()` intervals between each scroll.
- `json` just for pretty printing.
- `sync_playwright` for synchronous API. [`playwright` have asynchronous API](https://playwright.dev/python/docs/intro#usage) as well using `asyncio` module.

Declare a function: 

```python
def run(playwright):
    # further code..
```

Initialize `playwright`, connect to `chromium`, `launch()` a browser `new_page()` and make a request: 

```python
page = playwright.chromium.launch(headless=False).new_page()
page.goto("https://play.google.com/store/apps/details?id=com.instantbrands.app&gl=US&showAllReviews=true")
```

- [`playwright.chromium`is a connection to the Chromium](https://playwright.dev/python/docs/api/class-playwright#playwright-chromium) browser instance.
- [`launch()` will launch the browser](https://playwright.dev/python/docs/api/class-browsertype#browser-type-launch), and `headless` argument will run it in headless mode. Default is `True`.  
- [`new_page()` creates a new page in a new browser context](https://playwright.dev/python/docs/api/class-browser#browser-new-page).
- `page.goto("URL")` will make a request to provided website.

Scroll to the bottom of the page:

```python
reached_end = False
last_height = page.evaluate("() => document.body.scrollHeight")  # scrollHeight: 5879

while not reached_end:
    print(page.locator('.RveJvd').is_visible())  # just to see in the console that something is going on

    if page.query_selector('.RveJvd'):
        page.query_selector('.RveJvd').click(force=True)
        time.sleep(2)
    else:
        page.keyboard.press("End")
        time.sleep(2)

    new_height = page.evaluate("() => document.body.scrollHeight")
    if new_height == last_height:
        reached_end = True
    else:
        last_height = new_height
```

- `page.evaluate("() => document.body.scrollHeight")` will run a JavaScript code that will measurement of the height of the HTML `<body>`.
- `if page.query_selector('.RveJvd')` is visible it will `force` `click()` on the "Show More" button that could appear at random moment.
  - `else` it will make a `keaboard` `press()` "End" button if the "Show More" button is not present.
- `time.sleep(2)` will stop code execution for 2 seconds.
- Then it will measure a `new_height` after the scroll running the same measurement JavaScript code.
- Finally, it will check `if new_height == last_height`, and if so, exit the `while` loop by setting `reached_end` to `True`. 
  - `else` set the `last_height` to `new_height` and run the iteration again.


Create a temporary `list`:
```python
app_user_comments = []
```

Iterate over all results after the `while` loop is done:

```python
for comment in page.query_selector_all(".zc7KVe"):
    user_name = comment.query_selector(".X43Kjb").inner_text()

    try:
        user_avatar = comment.query_selector(".vDSMeb.bAhLNe img").get_attribute("src")
    except: user_avatar = None

    try:
        user_comment = comment.query_selector("[jsname=fbQN7e]").inner_text()
    except: user_comment = None

    try:
        comment_likes = comment.query_selector(".jUL89d.y92BAb").inner_text()
    except: comment_likes = None

    try:
        app_rating = comment.query_selector(".pf5lIe div[role=img]").get_attribute("aria-label").split(" ")[1]  # Rated 5 stars out of five stars -> 5
    except: app_rating = None

    try:
        comment_date = comment.query_selector(".p2TkOb").inner_text()
    except: comment_date = None
```

Check `if` duplicates and `None` are not present and `append` to temporary `list` as a `dict`: 

```python
if user_name and user_avatar and user_comment and comment_likes and app_rating and comment_date not in app_user_comments and not None:
    app_user_comments.append({
        "user_name": user_name,
        "user_avatar": user_avatar,
        "user_comment": user_comment,
        "comment_likes": comment_likes,
        "app_rating": app_rating,
        "comment_date": comment_date
    })
```

Print the data:

```python
print(json.dumps(app_user_comments, indent=2))
```

Close the browser instance:

```python
page.close()
```

Run your code using context manager:

```python
with sync_playwright() as playwright:
    run(playwright)
```


___


<h2 id="links">Links</h2>

- [GitHub Repository]()

___

<h2 id="outro">Outro</h2>

If you have anything to share, any questions, suggestions, or something that isn't working correctly, reach out via Twitter at [@dimitryzub](https://twitter.com/DimitryZub), or [@serp_api](https://twitter.com/serp_api).

Yours,
Dmitriy, and the rest of SerpApi Team.


<p style="text-align: center;">Join us on <a href="https://www.reddit.com/r/SerpApi/">Reddit</a> | <a href="https://twitter.com/serp_api">Twitter</a> | <a href="https://www.youtube.com/channel/UCUgIHlYBOD3yA3yDIRhg_mg">YouTube</a></p>


