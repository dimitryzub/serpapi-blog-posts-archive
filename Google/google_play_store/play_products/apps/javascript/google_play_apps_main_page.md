<h2>What will be scraped</h2>

![what-2](https://serpapi.com/blog/content/images/2022/05/what-2.png)

<h2>Preparation</h2>

First, we need to create a Node.js project and add `npm` packages [`cheerio`](https://www.npmjs.com/package/cheerio) to parse parts of the HTML markup, and [`axios`](https://www.npmjs.com/package/axios) to make a request to a website. To do this, in the directory with our project, open the command line and enter `npm init -y`, and then `npm i cheerio axios`.

<h2>Process</h2>

[SelectorGadget Chrome extension](https://chrome.google.com/webstore/detail/selectorgadget/mhjhnkcfbdhnjickkkdbjoemdmbfginb) was used to grab CSS selectors.
The Gif below illustrates the approach of selecting different parts of the results.

![how-1](https://serpapi.com/blog/content/images/2022/05/how-1.gif)

<h2>Full code</h2>

```javascript
const cheerio = require("cheerio");
const axios = require("axios");

const AXIOS_OPTIONS = {
    headers: {
        "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36",
    },                                                  // adding the User-Agent header as one way to prevent the request from being blocked
    params: {
        hl: 'en',                                       // Parameter defines the language to use for the Google search
        gl: 'us'                                        // parameter defines the country to use for the Google search
    },
};

function getMainPageInfo() {
    return axios
        .get(`https://play.google.com/store/apps`, AXIOS_OPTIONS)
        .then(function ({ data }) {
            let $ = cheerio.load(data);

            const mainPageInfo = Array.from($('.Ktdaqe')).reduce((result, block) => {
                const categoryTitle = $(block).find('.sv0AUd').text().trim()
                const apps = Array.from($(block).find('.WHE7ib')).map((app) => {
                    return {
                        title: $(app).find('.WsMG1c').text().trim(),
                        developer: $(app).find('.b8cIId .KoLSrc').text().trim(),
                        link: `https://play.google.com${$(app).find('.b8cIId a').attr('href')}`,
                        rating: parseFloat($(app).find('.pf5lIe > div').attr('aria-label').slice(6, 9)),
                    }
                })
                return {
                    ...result, [categoryTitle]: apps
                }

            }, {})

            return mainPageInfo;
        });
}

getMainPageInfo().then(console.log)
```

<h3>Code explanation</h3>

Declare constants from required libraries:

```javascript
const cheerio = require("cheerio");
const axios = require("axios");
```

|Code|Explanation|
|----|-----------|
|[`cheerio`](https://www.npmjs.com/package/cheerio)|library for parsing the html page and access the necessary selectors|
|[`axios`](https://www.npmjs.com/package/axios)|library for requesting the desired html document|

Next, we write down the necessary parameters for making a request:

```javascript
const AXIOS_OPTIONS = {
    headers: {
        "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36",
    },
    params: {
        hl: 'en',
        gl: 'us'
    },
};
```

|Code|Explanation|
|----|-----------|
|`headers`|[HTTP headers](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers) let the client and the server pass additional information with an HTTP request or response|
|[`User-Agent`](https://developer.mozilla.org/en-US/docs/Glossary/User_agent)|is used to act as a "real" user visit. Default axios requests user-agent is `axios/0.27.2` so websites understand that it's a script that sends a request and might block it. [Check what's your user-agent](https://www.whatismybrowser.com/detect/what-is-my-user-agent/).|
|`hl`|parameter defines the language to use for the Google search|
|`gl`|parameter defines the country to use for the Google search|

And finally a function to get the necessary information:

```javascript
function getMainPageInfo() {
    return axios
        .get(`https://play.google.com/store/apps`, AXIOS_OPTIONS)
        .then(function ({ data }) {
            let $ = cheerio.load(data);

            const mainPageInfo = Array.from($('.Ktdaqe')).reduce((result, block) => {
                const categoryTitle = $(block).find('.sv0AUd').text().trim()
                const apps = Array.from($(block).find('.WHE7ib')).map((app) => {
                    return {
                        title: $(app).find('.WsMG1c').text().trim(),
                        developer: $(app).find('.b8cIId .KoLSrc').text().trim(),
                        link: `https://play.google.com${$(app).find('.b8cIId a').attr('href')}`,
                        rating: parseFloat($(app).find('.pf5lIe > div').attr('aria-label').slice(6, 9)),
                    }
                })
                return {
                    ...result, [categoryTitle]: apps
                }

            }, {})

            return mainPageInfo;
        });
}
```

|Code|Explanation|
|----|-----------|
|`function ({ data })`|we received the response from axios request that have `data` key that we [destructured](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Destructuring_assignment) (this entry is equal to `function (response)` and in the next line `cheerio.load(response.data)`)|
|`mainPageInfo`|an object with categories arrays that contains info about apps from page|
|`apps`|an array that contains all displayed apps in current category|
|`.attr('href')`|gets the `href` attribute value of the html element|
|`$(block).find('.sv0AUd')`|finds element with class name `sv0AUd` in all child elements and their children of `block` html element|
|`.text()`|gets the raw text of html element|
|[`.trim()`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/trim)|removes whitespace from both ends of a string|
|`{...result, [categoryTitle]: apps}`|in this code we use [spread syntax](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Spread_syntax) to create an object from result that was returned from previous reduce call and add to this object new item with key `categoryTitle` and value `apps`|

Now we can launch our parser. To do this enter `node YOUR_FILE_NAME` in your command line. Where `YOUR_FILE_NAME` is the name of your `.js` file.

<h2>Output</h2>

```json
{
   "Popular apps & games":[
      {
         "title":"Netflix",
         "developer":"Netflix, Inc.",
         "link":"https://play.google.com/store/apps/details?id=com.netflix.mediaclient",
         "rating":4.5
      },
      {
         "title":"TikTok",
         "developer":"TikTok Pte. Ltd.",
         "link":"https://play.google.com/store/apps/details?id=com.zhiliaoapp.musically",
         "rating":4.5
      },
      {
         "title":"Instagram",
         "developer":"Instagram",
         "link":"https://play.google.com/store/apps/details?id=com.instagram.android",
         "rating":4
      }
      ... and other results
   ]
}
```

<h2>Google Play Store API</h2>

Alternatively, you can use the [Google Play Store API](https://serpapi.com/google-play-api) from SerpApi. SerpApi is a free API with 100 search per month. If you need more searches, there are paid plans.

The difference is that all that needs to be done is just to iterate over a ready made, structured JSON instead of coding everything from scratch maintaining, figuring out how to bypass blocks from Google, and selecting correct selectors which could be time consuming at times. [Check out the playground](https://serpapi.com/playground).


First we need to install [`google-search-results-nodejs`](https://www.npmjs.com/package/google-search-results-nodejs). To do this you need to enter in your console: `npm i google-search-results-nodejs`


```javascript
const SerpApi = require("google-search-results-nodejs");
const search = new SerpApi.GoogleSearch(process.env.API_KEY);     //your API key from serpapi.com

const params = {
  engine: "google_play",                                // search engine
  gl: "us",                                             // parameter defines the country to use for the Google search
  hl: "en",                                             // parameter defines the language to use for the Google search
  store: "apps"                                         // parameter defines the type of Google Play store
};

const getMainPageInfo = function ({ organic_results }) {
  return organic_results.reduce((result, category) => {
    const { title: categoryTitle, items } = category;
    const apps = items.map((app) => {
      const { title, link, rating, extansion } = app
      return {
        title,
        developer: extansion.name,
        link,
        rating,
      }
    })
    return {
      ...result, [categoryTitle]: apps
    }
  }, {})
};

const getJson = (params) => {
  return new Promise((resolve) => {
    search.json(params, resolve);
  })
}

getJson(params).then(getMainPageInfo).then(console.log)
```

<h3>Code explanation</h3>

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

Next, we write down the necessary parameters for making a request:

```javascript
const params = {
  engine: "google_play",
  gl: "us",
  hl: "en",
  store: "apps"
};
```

|Code|Explanation|
|----|-----------|
|`engine`|search engine|
|`gl`|parameter defines the country to use for the Google search|
|`hl`|parameter defines the language to use for the Google search|
|`store`|parameter defines the type of Google Play store|

Next, we write a callback function in which we describe what data we need from the result of our request:

```javascript
const getMainPageInfo = function ({ organic_results }) {
  return organic_results.reduce((result, category) => {
    const { title: categoryTitle, items } = category;
    const apps = items.map((app) => {
      const { title, link, rating, extansion } = app
      return {
        title,
        developer: extansion.name,
        link,
        rating,
      }
    })
    return {
      ...result, [categoryTitle]: apps
    }
  }, {})
};
```

|Code|Explanation|
|----|-----------|
|`organic_results`|an array that we destructured from response|
|`title, items`|other data that we destructured from element of `organic_results` array|
|`title: categoryTitle`|we redefine destructured data `title` to new `categoryTitle`|
|`title, link, rating, extansion`|other data that we destructured from element of `items` array|
|`{...result, [categoryTitle]: apps}`|in this code we use [spread syntax](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Spread_syntax) to create an object from result that was returned from previous reduce call and add to this object new item with key `categoryTitle` and value `apps`|

Next, we wrap the search method from the SerpApi library in a promise to further work with the search results and run it:

```javascript
const getJson = (params) => {
  return new Promise((resolve) => {
    search.json(params, resolve);
  })
}

getJson(params).then(getNewsData).then(console.log)
```

<h2>Output:</h2>

```json
{
   "Popular apps & games":[
      {
         "title":"Netflix",
         "developer":"Netflix, Inc.",
         "link":"https://play.google.com/store/apps/details?id=com.netflix.mediaclient",
         "rating":4.5
      },
      {
         "title":"TikTok",
         "developer":"TikTok Pte. Ltd.",
         "link":"https://play.google.com/store/apps/details?id=com.zhiliaoapp.musically",
         "rating":4.5
      },
      {
         "title":"Instagram",
         "developer":"Instagram",
         "link":"https://play.google.com/store/apps/details?id=com.instagram.android",
         "rating":4
      },
      ... and other results
   ]
}
```

<h2>Links</h2>

* [Code in the online IDE](https://replit.com/@MikhailZub/Google-Play-Apps-scrape-NodeJS-SerpApi#index.js) 
* [Google Play Store API](https://serpapi.com/google-play-api)
* [SerpApi Playground](https://serpapi.com/playground?engine=google_play&gl=us&hl=en&store=apps)


If you want to see some project made with SerpApi, please write me a message.

___
<p style="text-align: center;">Join us on <a href="https://twitter.com/serp_api">Twitter</a> | <a href="https://www.youtube.com/channel/UCUgIHlYBOD3yA3yDIRhg_mg">YouTube</a></p>
<p style="text-align: center;">Add a  <a href="https://github.com/serpapi/public-roadmap/issues">Feature Request</a>💫 or a <a href="https://github.com/serpapi/public-roadmap/issues">Bug</a>🐞</p>