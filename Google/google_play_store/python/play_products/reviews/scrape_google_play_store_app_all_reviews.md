- <a href="#what_will_be_scraped">What will be scraped</a>
- <a href="#prerequisites">Prerequisites</a>
- <a href="#playwright">Scrape Reviews with Playwright</a>
- <a href="#links">Links</a>
- <a href="#outro">Outro</a>

___


<h2 id="what_will_be_scraped">What will be scraped</h2>

![image](https://user-images.githubusercontent.com/78694043/172108621-fbe6ddfd-6848-454d-8942-b0e80265f804.png)


<h2 id="prerequisites">Prerequisites</h2>

**Basic knowledge scraping with CSS selectors**

If you haven't scraped with CSS selectors, there's a dedicated blog post of mine about [how to use CSS selectors when web-scraping](https://serpapi.com/blog/web-scraping-with-css-selectors-using-python/) that covers what it is, pros and cons, and why they're matter from a web-scraping perspective.

**Separate virtual environment**

If you didn't work with a virtual environment before, have a look at the dedicated [Python virtual environments tutorial using Virtualenv and Poetry](https://serpapi.com/blog/python-virtual-environments-using-virtualenv-and-poetry/) blog post of mine to get familiar.

📌Note: this is not a strict requirement for this blog post.

**Install libraries**:

```lang-none
pip install playwright
```

**Reduce the chance of being blocked**

There's a chance that a request might be blocked. Have a look at [how to reduce the chance of being blocked while web-scraping](https://serpapi.com/blog/how-to-reduce-chance-of-being-blocked-while-web/), there are eleven methods to bypass blocks from most websites and some of them will be covered in this blog post.

___

<h2 id="playwright">Scrape All Reviews with Playwright</h2>

Before moving on, we need to install Playwright:

```bash
$ pip install playwright
```

Then we need to [install browser](https://playwright.dev/python/docs/browsers#download-single-browser-binary):

```bash
$ playwright install chromium

Downloading Chromium 102.0.5005.40 (playwright build v1005) - 129.7 Mb [====================] 100% 0.0s 
Chromium 102.0.5005.40 (playwright build v1005) downloaded to /home/gitpod/.cache/ms-playwright/chromium-1005
```

In my case, I'm installing only Chromium binary but [you can also install Firefox, WebKit](https://playwright.dev/python/docs/browsers).


```python
from playwright.sync_api import sync_playwright
import json, time, re

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, slow_mo=50)
    page = browser.new_page(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36', 
                            viewport={'width': 1920, 'height': 1080})
    page.goto('https://play.google.com/store/apps/details?id=com.topsecurity.android&hl=en_GB&gl=US')

    # open user reviews window
    page.locator('button.VfPpkd-LgbsSe.aLey0c', has_text='See all reviews').click()
    time.sleep(1)

    user_comments = []

    if page.query_selector('.VfPpkd-wzTsW'):

        last_height = page.evaluate("document.querySelector('.fysCi').scrollHeight;")
        page.screenshot(path='start_of_the_reviews.png', full_page=True)

        while True:
            print('Scrolling..')

            # Scroll down
            page.evaluate("document.querySelector('.fysCi').scrollTo(0, document.querySelector('.fysCi').scrollHeight);")
            time.sleep(0.5)

            current_height = page.evaluate("document.querySelector('.fysCi').scrollHeight;")
            print(f'last height = {last_height}')
            print(f'current height = {current_height}')

            if current_height == last_height:
                break
            else:
                last_height = current_height
    else:
        print('Looks like the review window does not appear.')

    print('Extracting reviews...')

    for index, comment in enumerate(page.query_selector_all('.RHo1pe'), start=1):
        user_comments.append({
            'position': index,
            'name': comment.query_selector('.X5PpBb').text_content(),
            'avatar': comment.query_selector('.gSGphe img').get_attribute('src'),
            'rating': re.search(r'\d+', comment.query_selector('.Jx4nYe .iXRFPc').get_attribute('aria-label')).group(),
            'comment_likes': comment.query_selector('[jscontroller=SWD8cc]').get_attribute('data-original-thumbs-up-count'),
            'date': comment.query_selector('.bp9Aid').text_content(),
            'comment': comment.query_selector('.h3YV2d').text_content(),
        })
        
    print(json.dumps(user_comments, indent=2, ensure_ascii=False))
    page.screenshot(path='end_of_the_reviews.png', full_page=True)

    browser.close()
```

### Code explanation

Import libraries:

```python
from playwright.sync_api import sync_playwright
import json, time, re
```

|Code|Explanation|
|----|-----------|
|`sync_playwright`| to parse data using browser automation to render JS. [`Playwright` have asynchronous API](https://playwright.dev/python/docs/intro#usage) as well using `asyncio` module.|
|`time`| to set a `sleep()` intervals between each scroll.|
|`json`| to convert Python `dict` to JSON string.|
|`re`| to match parts of string via regluar expression. In this case to extract rating digit numbers from the string.|


Lunch browser, pass arguments and open a URL: 

```python
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, slow_mo=50)
    page = browser.new_page(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36', 
                            viewport={'width': 1920, 'height': 1080})
    page.goto('https://play.google.com/store/apps/details?id=com.topsecurity.android&hl=en_GB&gl=US')
```

|Code|Explanation|
|----|-----------|
|`p.chromium.launch(headless=True, slow_mo=50)`| to [`lunch`](https://playwright.dev/python/docs/api/class-browsertype#browser-type-launch) Chromium browser instance in [`headless`](https://playwright.dev/python/docs/api/class-browsertype#browser-type-launch-option-headless) mode, and [`slow_mo`](https://playwright.dev/python/docs/api/class-browsertype#browser-type-launch-option-slow-mo) execution a bit.|
|[`browser.new_page()`](https://playwright.dev/python/docs/api/class-browser#browser-new-page)| to open a new tab with passed [`user-agent`](https://playwright.dev/python/docs/api/class-browser#browser-new-context-option-user-agent) ([what is user-agent](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/User-Agent)) and specific [`viewport`](https://playwright.dev/python/docs/api/class-browser#browser-new-context-option-viewport) parameters.|
|[`goto()`](https://playwright.dev/python/docs/api/class-page#page-goto)| to open a passed URL.|

Open all reviews: 

```python
page.locator('button.VfPpkd-LgbsSe.aLey0c', has_text='See all reviews').click()
time.sleep(1)
```

|Code|Explanation|
|----|-----------|
|[`locator()`](https://playwright.dev/python/docs/locators)| to select specifc selector that [`has_text`](https://playwright.dev/python/docs/locators#filtering-locators) `'see all reviews'` and [`click()`](https://playwright.dev/python/docs/api/class-mouse#mouse-click) on it to open.|


Create a temporary `list` to store extracted user reviews:

```python
user_comments = []
```

Check if the reviews windows opened and scroll to the end of reviews:

```python
# if reviews window is opened
if page.query_selector('.VfPpkd-wzTsW'):

    last_height = page.evaluate("document.querySelector('.fysCi').scrollHeight;") # 9267
    page.screenshot(path='start_of_the_reviews.png', full_page=True)

    while True:
        print('Scrolling..')

        # Scroll down
        page.evaluate("document.querySelector('.fysCi').scrollTo(0, document.querySelector('.fysCi').scrollHeight);")
        time.sleep(0.5)

        current_height = page.evaluate("document.querySelector('.fysCi').scrollHeight;") # 17963

        if current_height == last_height:
            break
        else:
            last_height = current_height
else:
    print('Looks like the review window does not appear.')
```

|Code|Explanation|
|----|-----------|
|`evaluate()`| to execute JavaScript in order to do DOM manipulations.|
|`time.sleep()`| to sleep for 500 milliseconds before doing another scroll.|
|`if current_height == last_height`| to check if the height after the scroll is similar to the previous height and if it's the same -> exit the loop. No height difference will mean that there was nowhere to scroll more.|

Iterate over all reviews and `append` the data to the temporary list as a dictionary:

```python
for index, comment in enumerate(page.query_selector_all('.RHo1pe'), start=1):
        user_comments.append({
            'position': index,
            'name': comment.query_selector('.X5PpBb').text_content(),
            'avatar': comment.query_selector('.gSGphe img').get_attribute('src'),
            'rating': re.search(r'\d+', comment.query_selector('.Jx4nYe .iXRFPc').get_attribute('aria-label')).group(),
            'comment_likes': comment.query_selector('[jscontroller=SWD8cc]').get_attribute('data-original-thumbs-up-count'),
            'date': comment.query_selector('.bp9Aid').text_content(),
            'comment': comment.query_selector('.h3YV2d').text_content(),
        })
```

[Print extarcted data as a JSON string](https://docs.python.org/3/library/json.html#json.dumps), take a [`screenshot`](https://playwright.dev/python/docs/screenshots#full-page-screenshots) and [`close`](https://playwright.dev/python/docs/api/class-browser#browser-close) the browser:

```python
print(json.dumps(user_comments, indent=2, ensure_ascii=False))
page.screenshot(path='end_of_the_reviews.png', full_page=True)

browser.close()
```

Outputs:

```json
[
  {
    "position": 1,
    "name": "Kevin Bauer",
    "avatar": "https://play-lh.googleusercontent.com/a/AATXAJyAb8JYXl-_si7_fWbpydfgEuuAKcvdbiGaW0OP=s32-rw-mo",
    "rating": "2",
    "comment_likes": "329",
    "date": "27 May 2022",
    "comment": "The interrupting is horrible it is messing with me about 65% of the time when iam texting and i was interrupted when i was filling out a job application twice, i had to start over both times OMG It just did it while iam filling out this remarks of my experience with bravo security app also before I go it interrupted me 3 more times, they need to do something with the programming of the app like when there hasn't been any activity for one minute, then pop in otherwise it seems to be doing ok."
  }, ... other reviews
  {
    "position": 244,
    "name": "Kay Ach",
    "avatar": "https://play-lh.googleusercontent.com/a-/AOh14GiarKPy6h0DG73hd195aEmJaVedKnr1ZTl4i6GO=s32-rw",
    "rating": "4",
    "comment_likes": "4",
    "date": "14 May 2022",
    "comment": "Ok"
  }
]
```

____

Alternatively, there's a [Google Play Product Reviews API](https://serpapi.com/google-play-product-reviews) from SerpApi which can handle all of it without using browser automation with bypassing blocks from Google, solving CAPTCHA and can handle scaling to enterprice level. It's a paid API with a free plan.

Example code to integrate:

```python

```

Outputs:

```json

```

<h2 id="links">Links</h2>

- [GitHub Gist](https://gist.github.com/dimitryzub/785cd77806346706adfbde2a89b7d2de)
- [Google Play Product Reviews API](https://serpapi.com/google-play-product-reviews)


<p style="text-align: center;">Join us on <a href="https://twitter.com/serp_api">Twitter</a> | <a href="https://www.youtube.com/channel/UCUgIHlYBOD3yA3yDIRhg_mg">YouTube</a></p>


