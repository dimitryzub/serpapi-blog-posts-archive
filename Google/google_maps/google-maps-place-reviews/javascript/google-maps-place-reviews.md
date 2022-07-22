<h2 id='what'>What will be scraped</h2>

![image](https://user-images.githubusercontent.com/64033139/180441876-eb28584f-2516-45f5-a1f6-1c26671fb9c2.png)

<h2 id='preparation'>Preparation</h2>

First, we need to create a Node.js* project and add [`npm`](https://www.npmjs.com/) packages [`puppeteer`](https://www.npmjs.com/package/puppeteer), [`puppeteer-extra`](https://www.npmjs.com/package/puppeteer-extra) and [`puppeteer-extra-plugin-stealth`](https://www.npmjs.com/package/puppeteer-extra-plugin-stealth) to control Chromium (or Chrome, or Firefox, but now we work only with Chromium which is used by default) over the [DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/) in [headless](https://developers.google.com/web/updates/2017/04/headless-chrome) or non-headless mode. 

To do this, in the directory with our project, open the command line and enter `npm init -y`, and then `npm i puppeteer puppeteer-extra puppeteer-extra-plugin-stealth`.

*<span style="font-size: 15px;">If you don't have Node.js installed, you can [download it from nodejs.org](https://nodejs.org/en/) and follow the installation [documentation](https://nodejs.dev/learn/introduction-to-nodejs).</span>

📌Note: also, you can use `puppeteer` without any extensions, but I strongly recommended use it with `puppeteer-extra` with `puppeteer-extra-plugin-stealth` to prevent website detection that you are using headless Chromium or that you are using [web driver](https://www.w3.org/TR/webdriver/). You can check it on [Chrome headless tests website](https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html). The screenshot below shows you a difference.

![stealth](https://user-images.githubusercontent.com/64033139/173014238-eb8450d7-616c-42ae-8b2f-24eeb5fd5916.png)

<h2 id='process'>Process</h2>

[SelectorGadget Chrome extension](https://chrome.google.com/webstore/detail/selectorgadget/mhjhnkcfbdhnjickkkdbjoemdmbfginb) was used to grab CSS selectors by clicking on the desired element in the browser. If you have any struggles understanding this, we have a dedicated [Web Scraping with CSS Selectors blog post](https://serpapi.com/blog/web-scraping-with-css-selectors-using-python/) at SerpApi.

The Gif below illustrates the approach of selecting different parts of the results.

![how](https://user-images.githubusercontent.com/64033139/180442213-ddd8f019-89df-4d35-8d74-6e4293e7b159.gif)

<h2 id='full_code'>Full code</h2>

📌Note: to get a place URL you may use the tutorial from my blog post [Web Scraping Google Maps Places with Nodejs](https://serpapi.com/blog/web-scraping-google-maps-places-with-nodejs/#full_code).

```javascript
const puppeteer = require("puppeteer-extra");
const StealthPlugin = require("puppeteer-extra-plugin-stealth");

puppeteer.use(StealthPlugin());

const placeUrl =
  "https://www.google.com/maps/place/Starbucks/data=!4m7!3m6!1s0x549069a98254bd17:0xb2f64f75b3edf4c3!8m2!3d47.5319688!4d-122.1942498!16s%2Fg%2F1tdfmzpb!19sChIJF71UgqlpkFQRw_Tts3VP9rI?authuser=0&hl=en&rclk=1";

async function scrollPage(page, scrollContainer) {
  let lastHeight = await page.evaluate(`document.querySelector("${scrollContainer}").scrollHeight`);
  while (true) {
    await page.evaluate(`document.querySelector("${scrollContainer}").scrollTo(0, document.querySelector("${scrollContainer}").scrollHeight)`);
    await page.waitForTimeout(2000);
    let newHeight = await page.evaluate(`document.querySelector("${scrollContainer}").scrollHeight`);
    if (newHeight === lastHeight) {
      break;
    }
    lastHeight = newHeight;
  }
}

async function getReviewsFromPage(page) {
  const reviews = await page.evaluate(() => {
    return Array.from(document.querySelectorAll(".jftiEf")).map((el) => {
      return {
        user: {
          name: el.querySelector(".d4r55")?.textContent.trim(),
          link: el.querySelector(".WNxzHc a")?.getAttribute("href"),
          thumbnail: el.querySelector(".NBa7we")?.getAttribute("src"),
          localGuide: el.querySelector(".RfnDt span:first-child")?.style.display === "none" ? undefined : true,
          reviews: parseInt(el.querySelector(".RfnDt span:last-child")?.textContent.replace("·", "")),
        },
        rating: parseFloat(el.querySelector(".kvMYJc")?.getAttribute("aria-label")),
        date: el.querySelector(".rsqaWe")?.textContent.trim(),
        snippet: el.querySelector(".MyEned")?.textContent.trim(),
        likes: parseFloat(el.querySelector(".GBkF3d:nth-child(2)")?.getAttribute("aria-label")),
        images: Array.from(el.querySelectorAll(".KtCyie button")).length
          ? Array.from(el.querySelectorAll(".KtCyie button")).map((el) => {
              return {
                thumbnail: getComputedStyle(el).backgroundImage.slice(5, -2),
              };
            })
          : undefined,
        date: el.querySelector(".rsqaWe")?.textContent.trim(),
      };
    });
  });
  return reviews;
}

async function fillPlaceInfo(page) {
  const placeInfo = await page.evaluate(() => {
    return {
      title: document.querySelector(".DUwDvf").textContent.trim(),
      address: document.querySelector("button[data-item-id='address']")?.textContent.trim(), // data-item-id attribute may be different if the language is not English
      rating: document.querySelector("div.F7nice").textContent.trim(),
      reviews: document.querySelector("span.F7nice").textContent.trim().split(" ")[0],
    };
  });
  return placeInfo;
}

async function getLocalPlaceReviews() {
  const browser = await puppeteer.launch({
    headless: false,
    args: ["--no-sandbox", "--disable-setuid-sandbox"],
  });

  const page = await browser.newPage();

  await page.setDefaultNavigationTimeout(60000);
  await page.goto(placeUrl);
  await page.waitForSelector(".DUwDvf");

  const placeInfo = await fillPlaceInfo(page);

  await page.click(".mgr77e .DkEaL");
  await page.waitForTimeout(2000);
  await page.waitForSelector(".jftiEf");

  await scrollPage(page, '.DxyBCb');

  const reviews = await getReviewsFromPage(page);

  await browser.close();

  return { placeInfo, reviews };
}

getLocalPlaceReviews().then((result) => console.dir(result, { depth: null }));
```

<h3 id='code_explanation'>Code explanation</h3>

Declare constants from required libraries:

```javascript
const puppeteer = require("puppeteer-extra");
const StealthPlugin = require("puppeteer-extra-plugin-stealth");
```
        
|Code|Explanation|
|----|-----------|
|[`puppeteer`](https://www.npmjs.com/package/puppeteer-extra)|Chromium control library|
|[`StealthPlugin`](https://www.npmjs.com/package/puppeteer-extra-plugin-stealth)|library for prevent website detection that you are using [web driver](https://www.w3.org/TR/webdriver/)|

Next, we "say" to `puppeteer` use `StealthPlugin` and write place URL:

```javascript
puppeteer.use(StealthPlugin());

const placeUrl =
  "https://www.google.com/maps/place/Starbucks/data=!4m7!3m6!1s0x549069a98254bd17:0xb2f64f75b3edf4c3!8m2!3d47.5319688!4d-122.1942498!16s%2Fg%2F1tdfmzpb!19sChIJF71UgqlpkFQRw_Tts3VP9rI?authuser=0&hl=en&rclk=1";
```
        
Next, we write down a function for scrolling reviews container on the page:

```javascript
async function scrollPage(page, scrollContainer) {
  let lastHeight = await page.evaluate(`document.querySelector("${scrollContainer}").scrollHeight`);
  while (true) {
    await page.evaluate(`document.querySelector("${scrollContainer}").scrollTo(0, document.querySelector("${scrollContainer}").scrollHeight)`);
    await page.waitForTimeout(2000);
    let newHeight = await page.evaluate(`document.querySelector("${scrollContainer}").scrollHeight`);
    if (newHeight === lastHeight) {
      break;
    }
    lastHeight = newHeight;
  }
}
```

|Code|Explanation|
|----|-----------|
|`lastHeight`|current [scrollheight](https://developer.mozilla.org/en-US/docs/Web/API/Element/scrollHeight) of the container|
|`page.evaluate('document.querySelector...`|runs code from the brackets in the browser console and returns the result|
|`page.waitForTimeout(2000)`|waiting 2000 ms before continue|
|`newHeight`|[scrollheight](https://developer.mozilla.org/en-US/docs/Web/API/Element/scrollHeight) of the container after scroll|

Next, we write down a function for getting reviews from the page:

```javascript
async function getReviewsFromPage(page) {
  const reviews = await page.evaluate(() => {
    return Array.from(document.querySelectorAll(".jftiEf")).map((el) => {
      return {
        user: {
          name: el.querySelector(".d4r55")?.textContent.trim(),
          link: el.querySelector(".WNxzHc a")?.getAttribute("href"),
          thumbnail: el.querySelector(".NBa7we")?.getAttribute("src"),
          localGuide: el.querySelector(".RfnDt span:first-child")?.style.display === "none" ? undefined : true,
          reviews: parseInt(el.querySelector(".RfnDt span:last-child")?.textContent.replace("·", "")),
        },
        rating: parseFloat(el.querySelector(".kvMYJc")?.getAttribute("aria-label")),
        date: el.querySelector(".rsqaWe")?.textContent.trim(),
        snippet: el.querySelector(".MyEned")?.textContent.trim(),
        likes: parseFloat(el.querySelector(".GBkF3d:nth-child(2)")?.getAttribute("aria-label")),
        images: Array.from(el.querySelectorAll(".KtCyie button")).length
          ? Array.from(el.querySelectorAll(".KtCyie button")).map((el) => {
              return {
                thumbnail: getComputedStyle(el).backgroundImage.slice(5, -2),
              };
            })
          : undefined,
        date: el.querySelector(".rsqaWe")?.textContent.trim(),
      };
    });
  });
  return reviews;
}
```

|Code|Explanation|
|----|-----------|
|[`document.querySelectorAll(".jftiEf")`](https://developer.mozilla.org/en-US/docs/Web/API/Document/querySelectorAll)|returns a static [NodeList](https://developer.mozilla.org/en-US/docs/Web/API/NodeList) representing a list of the document's elements that match the css selectors with class name `jftiEf`|
|[`el.querySelector(".d4r55")`](https://developer.mozilla.org/en-US/docs/Web/API/Document/querySelector)|returns the first html element with selector `.d4r55` which is any child of the `el` html element|
|`.textContent`|gets the raw text of html element|
|[`.trim()`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/trim)|removes whitespace from both ends of a string|
|`.getAttribute("href")`|gets the `href` attribute value of the html element|
|`getComputedStyle(el).backgroundImage`|[`getComputedStyle(el)`](https://developer.mozilla.org/en-US/docs/Web/API/Window/getComputedStyle) returns an object containing the values of all CSS properties of an `el`, after applying active stylesheets, and get `backgroundImage` property|
|`.slice(5, -2)`|this method keeps everything from the 5th character from the beginning to the 2nd (inclusive) character from the end and removes the others|

Next, we write down a function for getting main place info from the page:

```javascript
async function fillPlaceInfo(page) {
  const placeInfo = await page.evaluate(() => {
    return {
      title: document.querySelector(".DUwDvf").textContent.trim(),
      address: document.querySelector("button[data-item-id='address']")?.textContent.trim(),
      rating: document.querySelector("div.F7nice").textContent.trim(),
      reviews: document.querySelector("span.F7nice").textContent.trim().split(" ")[0],
    };
  });
  return placeInfo;
}
```

And finally, a function to control the browser, and get information:

```javascript
async function getLocalPlaceReviews() {
  const browser = await puppeteer.launch({
    headless: false,
    args: ["--no-sandbox", "--disable-setuid-sandbox"],
  });

  const page = await browser.newPage();

  await page.setDefaultNavigationTimeout(60000);
  await page.goto(placeUrl);
  await page.waitForSelector(".DUwDvf");

  const placeInfo = await fillPlaceInfo(page);

  await page.click(".mgr77e .DkEaL");
  await page.waitForTimeout(2000);
  await page.waitForSelector(".jftiEf");

  await scrollPage(page, '.DxyBCb');

  const reviews = await getReviewsFromPage(page);

  await browser.close();

  return { placeInfo, reviews };
}

getLocalPlaceReviews().then((result) => console.dir(result, { depth: null }));
```

|Code|Explanation|
|----|-----------|
|`puppeteer.launch({options})`|this method launches a new instance of the Chromium browser with current `options`|
|`headless`|defines which mode to use: [headless](https://developers.google.com/web/updates/2017/04/headless-chrome) (by default) or non-headless|
|`args`|an array with [arguments](https://peter.sh/experiments/chromium-command-line-switches/) which is used with Chromium|
|`["--no-sandbox", "--disable-setuid-sandbox"]`|these arguments we use to allow the launch of the browser process in the [online IDE](https://replit.com/@MikhailZub/Scrape-eBay-Organic-Results-with-NodeJS-SerpApi#main.sh)|
|`browser.newPage()`|this method launches a new page|
|`page.setDefaultNavigationTimeout(60000)`|changing default (30 sec) time for waiting for selectors to 60000 ms (1 min) for slow internet connection|
|`page.goto(URL)`|navigation to `URL` which is defined above|
|`page.click(".Dx2nRe")`|this methods emulates mouse click on the html element with the `.Dx2nRe` selector|
|`browser.close()`|after all we close the browser instance|
|`console.dir(result, { depth: null })`|console method `dir` allows you to use an object with the necessary parameters to change default output options. Watch [Node.js documentation](https://nodejs.org/api/console.html#consoledirobj-options) for more info|

Now we can launch our parser. To do this enter `node YOUR_FILE_NAME` in your command line. Where `YOUR_FILE_NAME` is the name of your `.js` file.

<h2 id='output'>Output</h2>

```json
{
   "placeInfo":{
      "title":"Starbucks",
      "address":"1785 NE 44th St, Renton, WA 98056, United States",
      "rating":"4.1",
      "reviews":"381"
   },
   "reviews":[
      {
         "user":{
            "name":"Bo Wagner",
            "link":"https://www.google.com/maps/contrib/118325097789436047813/reviews?hl=en-US",
            "thumbnail":"https://lh3.googleusercontent.com/a/AItbvmlPWzfGuqAk1v2yewzIizLcl462BenzGnCadQWt=w36-h36-p-c0x00000000-rp-mo-ba6-br100",
            "localGuide":true,
            "reviews":442
         },
         "rating":4,
         "date":"5 months ago",
         "snippet":"Good service, but waiting a bit long for my drink.  Look like a trainee was making my drink. It taste different.",
         "likes":1,
         "images":[
            {
               "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipNIUP-aOWRElmfVOjnf5lJJYFiLKBaSx7MSkhg8=w300-h450-p-k-no"
            },
            {
               "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipPcTFJIW9JAZxZ0PU0WC2U5rPnESv7OnrnSANwV=w300-h225-p-k-no"
            },
            {
               "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipN_LkT7MCwx-oaf1yXkMnc_D-gm6HrWa7Kqoep8=w300-h225-p-k-no"
            }
         ]
      },
      {
         "user":{
            "name":"Azurina S (Zeze)",
            "link":"https://www.google.com/maps/contrib/108701024889578509779/reviews?hl=en-US",
            "thumbnail":"https://lh3.googleusercontent.com/a-/AFdZucqQsjYaAOuvBT8dMBe_BeywrjLtshpgCL3xZGp5mg=w36-h36-p-c0x00000000-rp-mo-br100",
            "reviews":7
         },
         "rating":5,
         "date":"4 months ago",
         "snippet":"Super friendly and fast.  They were getting through that Drive-Thru line at record speed!! Thank you for that because I was in a serious rush!! 👍🏽",
         "likes":1,
         "images":[
            {
               "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipPrI2xvgjFNh2vxFmBxRJBYvw553mORZdRZYwdZ=w300-h450-p-k-no"
            },
            {
               "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipPVZ4YJqXjLvL-XTFBpB0oo4lVaBdrAGv2Ohyux=w300-h450-p-k-no"
            }
         ]
      },
      ...and other reviews
   ]
}
```

<h2 id='serp_api'>Google Maps Reviews API</h2>

Alternatively, you can use the [Google Maps Reviews API](https://serpapi.com/google-maps-reviews-api) from SerpApi. SerpApi is a free API with 100 searches per month. If you need more searches, there are paid plans.

The difference is that you won't have to write code from scratch and maintain it. You may also experience blocking from Google and changing selectors which will break the parser. Instead, you just need to iterate the structured JSON and get the data you want. [Check out the playground](https://serpapi.com/playground).

First, we need to install [`google-search-results-nodejs`](https://www.npmjs.com/package/google-search-results-nodejs). To do this you need to enter in your console: `npm i google-search-results-nodejs`

📌Note: To make our search we need the `data_id` parameter. You can take it using the guide from my blog post [Web Scraping Google Maps Places with Nodejs](https://serpapi.com/blog/web-scraping-google-maps-places-with-nodejs/#serp_api).

```javascript
const SerpApi = require("google-search-results-nodejs");
const search = new SerpApi.GoogleSearch(process.env.API_KEY);     //your API key from serpapi.com

const dataId = "0x549069a98254bd17:0xb2f64f75b3edf4c3";                    // data ID parameter

const params = {
  engine: "google_maps_reviews",                                           // search engine
  hl: "en",                                                                // parameter defines the language to use for the Google search
  data_id: dataId,                                                         // parameter defines the Google Maps data ID
};

const getJson = () => {
  return new Promise((resolve) => {
    search.json(params, resolve);
  });
};

exports.getResults = async () => {
  const allReviews = {
    reviews: [],
  };
  while (true) {
    const json = await getJson();
    if (!allReviews.placeInfo) allReviews.placeInfo = json.place_info;
    if (json.reviews) {
      allReviews.reviews.push(...json.reviews);
    } else break;
    if (json.serpapi_pagination?.next_page_token) {
      params.next_page_token = json.serpapi_pagination?.next_page_token;
    } else break;
  }
  return allReviews;
};

getResults.then((result) => console.dir(result, { depth: null }));
```

<h3 id='serp_api_code_explanation'>Code explanation</h3>

Declare constants from required libraries:

```javascript
const SerpApi = require("google-search-results-nodejs");
const search = new SerpApi.GoogleSearch(API_KEY);
```

|Code|Explanation|
|----|-----------|
|`SerpApi`|SerpApi Node.js library|
|`search`|new instance of GoogleSearch class|
|`API_KEY`|your API key from [SerpApi](https://serpapi.com/manage-api-key)|

Next, we write down what we want to search and the necessary parameters for making a request:

```javascript
const dataId = "0x549069a98254bd17:0xb2f64f75b3edf4c3";

const params = {
  engine: "google_maps_reviews",
  hl: "en",
  data_id: dataId,
};
```

|Code|Explanation|
|----|-----------|
|`dataId`|data ID parameter|
|`engine`|search engine|
|`hl`|parameter defines the language to use for the Google Scholar search|

Next, we wrap the search method from the SerpApi library in a promise to further work with the search results:

```javascript
const getJson = () => {
  return new Promise((resolve) => {
    search.json(params, resolve);
  })
}
```

And finally, we declare and run the function `getResult` that gets reviews from all pages and return it:

```javascript
const getResults = async () => {
  const allReviews = {
    reviews: [],
  };
  while (true) {
    const json = await getJson();
    if (!allReviews.placeInfo) allReviews.placeInfo = json.place_info;
    if (json.reviews) {
      allReviews.reviews.push(...json.reviews);
    } else break;
    if (json.serpapi_pagination?.next_page_token) {
      params.next_page_token = json.serpapi_pagination?.next_page_token;
    } else break;
  }
  return allReviews;
};

getResults().then((result) => console.dir(result, { depth: null }))
```

|Code|Explanation|
|----|-----------|
|`allReviews`|an object with main place info and reviews from all pages|
|`allReviews.reviews.push(...json.reviews)`|in this code, we use [spread syntax](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Spread_syntax) to split the `photos` array from result that was returned from `reviews` function into elements and add them in the end of `allReviews.reviews` array|
|`console.dir(result, { depth: null })`|console method `dir` allows you to use an object with the necessary parameters to change default output options. Watch [Node.js documentation](https://nodejs.org/api/console.html#consoledirobj-options) for more info|

<h2 id='serp_api_output'>Output</h2>

```json
{
   "reviews":[
      {
         "user":{
            "name":"Bo Wagner",
            "link":"https://www.google.com/maps/contrib/118325097789436047813?hl=en-US&sa=X&ved=2ahUKEwiEpJXYzoz5AhXDVDUKHbpYCAwQvvQBegQIARBB",
            "thumbnail":"https://lh3.googleusercontent.com/a/AItbvmlPWzfGuqAk1v2yewzIizLcl462BenzGnCadQWt=s40-c-c0x00000000-cc-rp-mo-ba6-br100",
            "local_guide":true,
            "reviews":442,
            "photos":4747
         },
         "rating":4,
         "date":"5 months ago",
         "snippet":"Good service, but waiting a bit long for my drink. Look like a trainee was making my drink. It taste different.",
         "likes":1,
         "images":[
            "https://lh5.googleusercontent.com/p/AF1QipNIUP-aOWRElmfVOjnf5lJJYFiLKBaSx7MSkhg8=w100-h100-p-n-k-no",
            "https://lh5.googleusercontent.com/p/AF1QipPcTFJIW9JAZxZ0PU0WC2U5rPnESv7OnrnSANwV=w100-h100-p-n-k-no",
            "https://lh5.googleusercontent.com/p/AF1QipN_LkT7MCwx-oaf1yXkMnc_D-gm6HrWa7Kqoep8=w100-h100-p-n-k-no"
         ]
      },
      {
         "user":{
            "name":"Azurina S (Zeze)",
            "link":"https://www.google.com/maps/contrib/108701024889578509779?hl=en-US&sa=X&ved=2ahUKEwiEpJXYzoz5AhXDVDUKHbpYCAwQvvQBegQIARBb",
            "thumbnail":"https://lh3.googleusercontent.com/a-/AFdZucqQsjYaAOuvBT8dMBe_BeywrjLtshpgCL3xZGp5mg=s40-c-c0x00000000-cc-rp-mo-br100",
            "reviews":7,
            "photos":2
         },
         "rating":5,
         "date":"4 months ago",
         "snippet":"Super friendly and fast. They were getting through that Drive-Thru line at record speed!! Thank you for that because I was in a serious rush!! 👍🏽",
         "likes":1,
         "images":[
            "https://lh5.googleusercontent.com/p/AF1QipPrI2xvgjFNh2vxFmBxRJBYvw553mORZdRZYwdZ=w100-h100-p-n-k-no",
            "https://lh5.googleusercontent.com/p/AF1QipPVZ4YJqXjLvL-XTFBpB0oo4lVaBdrAGv2Ohyux=w100-h100-p-n-k-no"
         ]
      },
      ...and other reviews
   ],
   "placeInfo":{
      "title":"Starbucks",
      "address":"1785 NE 44th St, Renton, WA",
      "rating":4.1,
      "reviews":381
   }
}
```

<h2 id='links'>Links</h2>

* [Code in the online IDE](https://replit.com/@MikhailZub/Google-Maps-Reviews-NodeJS-SerpApi#index.js) 
* [Google Maps Reviews API](https://serpapi.com/google-maps-reviews-api)

If you want to see some projects made with SerpApi, please write me a message.

___
<p style="text-align: center;">Join us on <a href="https://twitter.com/serp_api">Twitter</a> | <a href="https://www.youtube.com/channel/UCUgIHlYBOD3yA3yDIRhg_mg">YouTube</a></p>
<p style="text-align: center;">Add a  <a href="https://github.com/serpapi/public-roadmap/issues">Feature Request</a>💫 or a <a href="https://github.com/serpapi/public-roadmap/issues">Bug</a>🐞</p>