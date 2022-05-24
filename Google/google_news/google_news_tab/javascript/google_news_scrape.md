## What will be scraped

![What](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/afsvykjuo74n13wh1c33.png)

## Preparation

First, we need to create a Node.js project and add `npm` packages [`cheerio`](https://www.npmjs.com/package/cheerio) to parse parts of the HTML markup, and [`axios`](https://www.npmjs.com/package/axios) to make a request to a website. To do this, in the directory with our project, open the command line and enter `npm init -y`, and then `npm i cheerio axios`.

##Process
[SelectorGadget Chrome extension](https://chrome.google.com/webstore/detail/selectorgadget/mhjhnkcfbdhnjickkkdbjoemdmbfginb) was used to grab CSS selectors by clicking on the desired element in the browser. If you have any struggles understanding this, we have a dedicated [Web Scraping with CSS Selectors blog post](https://serpapi.com/blog/web-scraping-with-css-selectors-using-python/) at SerpApi.
The Gif below illustrates the approach of selecting different parts of the results.

![How](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/letec80rcxgjsnwi5t77.gif)

## Full code

```javascript
const cheerio = require("cheerio");
const axios = require("axios");

const searchString = "elon musk";                   // what we want to search
const encodedString = encodeURI(searchString);      // what we want to search for in URI encoding

const AXIOS_OPTIONS = {
    headers: {
        "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36",
    },                                                  // adding the User-Agent header as one way to prevent the request from being blocked
    params: {
        q: encodedString,                               // our encoded search string        
        tbm: "nws",                                     // parameter defines the type of search you want to do ("nws" means news)
        hl: 'en',                                       // Parameter defines the language to use for the Google search
        gl: 'us'                                        // parameter defines the country to use for the Google search
    },
};

function getNewsInfo() {
    return axios
        .get(`http://google.com/search`, AXIOS_OPTIONS)
        .then(function ({ data }) {
            let $ = cheerio.load(data);

            const pattern = /s='(?<img>[^']+)';\w+\s\w+=\['(?<id>\w+_\d+)'];/gm;
            const images = [...data.matchAll(pattern)].map(({ groups }) => ({ id: groups.id, img: groups.img.replace('\\x3d', '') }))

            const allNewsInfo = Array.from($('.WlydOe')).map((el) => {
                return {
                    link: $(el).attr('href'),
                    source: $(el).find('.CEMjEf span').text().trim(),
                    title: $(el).find('.mCBkyc').text().trim().replace('\n', ''),
                    snippet: $(el).find('.GI74Re').text().trim().replace('\n', ''),
                    image: images.find(({ id, img }) => id === $(el).find('.uhHOwf img').attr('id'))?.img || "No image",
                    date: $(el).find('.ZE0LJd span').text().trim(),
                }
            });

            return allNewsInfo;
        });
}

getNewsInfo().then(console.log);
```

### Code explanation

Declare constants from required libraries:

```javascript
const cheerio = require("cheerio");
const axios = require("axios");
```
|Code|Explanation|
|----|-----------|
|[`cheerio`](https://www.npmjs.com/package/cheerio)|library for parsing the html page and access the necessary selectors|
|[`axios`](https://www.npmjs.com/package/axios)|library for requesting the desired html document|

Next, we write in constants what we want to search for and encode our text into a URI string:

```javascript
const searchString = "elon musk";
const encodedString = encodeURI(searchString);
```

|Code|Explanation|
|----|-----------|
|`searchString`|what we want to search|
|`encodedString`|what we want to search for in [URI encoding](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/encodeURI)|

Next, we write down the necessary parameters for making a request:

```javascript
const AXIOS_OPTIONS = {
    headers: {
        "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36",
    },
    params: {
        q: encodedString,       
        tbm: "nws",
        hl: 'en',
        gl: 'us'
    },
};
```

|Code|Explanation|
|----|-----------|
|`headers`|[HTTP headers](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers) let the client and the server pass additional information with an HTTP request or response|
|[`User-Agent`](https://developer.mozilla.org/en-US/docs/Glossary/User_agent)|is used to act as a "real" user visit. Default axios requests user-agent is `axios/0.27.2` so websites understand that it's a script that sends a request and might block it. [Check what's your user-agent](https://www.whatismybrowser.com/detect/what-is-my-user-agent/).|
|`q`|encoded in URI search query|
|`tbm`|parameter defines the type of search you want to do ("nws" means news)|
|`hl`|parameter defines the language to use for the Google search|
|`gl`|parameter defines the country to use for the Google search|

And finally a function to get the necessary information:

```javascript
function getNewsInfo() {
    return axios
        .get(`http://google.com/search`, AXIOS_OPTIONS)
        .then(function ({ data }) {
            let $ = cheerio.load(data);

            const pattern = /s='(?<img>[^']+)';\w+\s\w+=\['(?<id>\w+_\d+)'];/gm;
            const images = [...data.matchAll(pattern)].map(({ groups }) => ({ id: groups.id, img: groups.img.replace('\\x3d', '') }))

            const allNewsInfo = Array.from($('.WlydOe')).map((el) => {
                return {
                    link: $(el).attr('href'),
                    source: $(el).find('.CEMjEf span').text().trim(),
                    title: $(el).find('.mCBkyc').text().trim().replace('\n', ''),
                    snippet: $(el).find('.GI74Re').text().trim().replace('\n', ''),
                    image: images.find(({ id, img }) => id === $(el).find('.uhHOwf img').attr('id'))?.img || "No image",
                    date: $(el).find('.ZE0LJd span').text().trim(),
                }
            });

            return allNewsInfo;
        });
}
```
|Code|Explanation|
|----|-----------|
|`function ({ data })`|we received the response from axios request that have `data` key that we [destructured](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Destructuring_assignment) (this entry is equal to `function (response)` and in the next line `cheerio.load(response.data)`)|
|`pattern`|a RegEx pattern for search and define full images. [See what it allows you to find](https://regex101.com/r/pMd0yx/1)|
|`images`|an array that contains the id of the `img` selector and the image itself|
|`[...data.matchAll(pattern)]`|in this code we use [spread syntax](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Spread_syntax) to create an array from an [iterator](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Iterators_and_Generators) that was returned from [matchAll method](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/matchAll) (in this case this entry is equal to `Array.from(data.matchAll(pattern))`)|
|`.replace('\\x3d', '')`|in this code we remove `\\x3d` chars from the end of the [`base64`](https://en.wikipedia.org/wiki/Base64) image format string to display image properly|
|`allNewsInfo`|an array with full info about news from page|
|`.attr('href')`|gets the `href` attribute value of the html element|
|`$(el).find('.mCBkyc')`|finds element with class name `mCBkyc` in all child elements and their children of `el` html element|
|`.text()`|gets the raw text of html element|
|[`.trim()`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/trim)|removes whitespace from both ends of a string|

Now we can launch our parser. To do this enter `node YOUR_FILE_NAME` in your command line. Where `YOUR_FILE_NAME` is the name of your `.js` file.

Outputs:

```json
[
   {
      "link":"https://www.newyorker.com/news/q-and-a/why-elon-musk-bought-twitter",
      "source":"The New Yorker",
      "title":"Why Elon Musk Bought Twitter",
      "snippet":"Portrait of Elon Musk looking off to the side. Musk, the C.E.O. of Tesla, has previously had some run-ins with the S.E.C.Source photograph by...",
      "image":"data:image/jpeg;base64,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",
      "date":"2 weeks ago"
   }, ... other results
]
```

## Google News Result API

Alternatively, you can use the [Google News Result API](https://serpapi.com/news-results) from SerpApi. SerpApi is a free API with 100 search per month. If you need more searches, there are paid plans.

The difference is that all that needs to be done is just to iterate over a ready made, structured JSON instead of coding everything from scratchmaintaining, figuring out how to bypass blocks from Google, and selecting correct selectors which could be time consuming at times. [Check out the playground](https://serpapi.com/playground).

First we need to install [`google-search-results-nodejs`](https://www.npmjs.com/package/google-search-results-nodejs). To do this you need to enter in your console: `npm i google-search-results-nodejs`


```javascript
const SerpApi = require("google-search-results-nodejs");
const search = new SerpApi.GoogleSearch(API_KEY);        //your API key from serpapi.com

const searchString = "elon musk";                        // what we want to search

const params = {
  engine: "google",                                     // search engine
  q: searchString,                                      // search query
  google_domain: "google.com",                          // google domain: google.com, google.de, google.fr
  gl: "us",                                             // parameter defines the country to use for the Google search
  hl: "en",                                             // Parameter defines the language to use for the Google search
  tbm: "nws"                                            // parameter defines the type of search you want to do ("nws" means news)
};

const getNewsData = function ({ news_results }) {
  return news_results.map((result) => {
    const { link, title, source, date, snippet, thumbnail: image = "No image" } = result;
    return {
      link,
      source,
      title: title.replace('\n', ''),
      snippet: snippet.replace('\n', ''),
      image,
      date,
    }
  })
};

const getJson = (params) => {
  return new Promise((resolve) => {
    search.json(params, resolve);
  })
}

getJson(params).then(getNewsData).then(console.log)
```

### Code explanation

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
const searchString = "elon musk";

const params = {
  engine: "google",
  q: searchString,
  google_domain: "google.com",
  gl: "us",
  hl: "en",
  tbm: "nws"
```

|Code|Explanation|
|----|-----------|
|`searchString`|what we want to search|
|`engine`|search engine|
|`q`|search query|
|`google_domain`|google domain: google.com, google.de, google.fr|
|`gl`|parameter defines the country to use for the Google search|
|`hl`|parameter defines the language to use for the Google search|
|`tbm`|parameter defines the type of search you want to do ("nws" means news)|


Next, we write a callback function in which we describe what data we need from the result of our request:

```javascript
const getNewsData = function ({ news_results }) {
  return news_results.map((result) => {
    const { link, title, source, date, snippet, thumbnail: image = "No image" } = result;
    return {
      link,
      source,
      title: title.replace('\n', ''),
      snippet: snippet.replace('\n', ''),
      image,
      date,
    }
  })
};
```

|Code|Explanation|
|----|-----------|
|`news_results`|an array that we destructured from response|
|`link, title, source, date, snippet, thumbnail`|other data that we destructured from element of news_results array|
|`thumbnail: image = "No image"`|we redefine destructured data `thumbnail` to new `image` and set default value `No image` if `thumbnail` is `undefined`|
|`replace('\n', '')`|in this code we remove [new line](https://en.wikipedia.org/wiki/Newline#In_programming_languages) symbol|

Next, we wrap the search method from the SerpApi library in a promise to further work with the search results and run it:

```javascript
const getJson = (params) => {
  return new Promise((resolve) => {
    search.json(params, resolve);
  })
}

getJson(params).then(getNewsData).then(console.log)
```

Outputs:

```json
[
   {
      "link":"https://nypost.com/2022/05/13/elon-musk-backs-gop-bid-to-strip-disney-of-mickey-mouse-copyright/",
      "source":"New York Post",
      "title":"Elon Musk backs GOP bid to strip Disney of Mickey Mouse copyright",
      "snippet":"Elon Musk appeared to voice his support for a Republican senator's efforts \n""+""to strip The Walt Disney Co. of its copyright of Mickey Mouse.",
      "image":"https://serpapi.com/searches/627e67d93c3fb22215607d9e/images/22b0f5e214e9045c6dc1c6c683cc0b1468248a0cb118e82ed3c7f8900a359195.jpeg",
      "date":"17 mins ago"
   }, ... other results
]
```

## Links
* [Code in the online IDE](https://replit.com/@MikhailZub/Google-News-Tab-scrape-NodeJS-SerpApi#index.js) 
* [Google News Result API](https://serpapi.com/news-results).


If you want to see how to do the same with using pagination or you want to see some project made with SerpApi, please write me a message.

___
<p style="text-align: center;">Join us on <a href="https://twitter.com/serp_api">Twitter</a> | <a href="https://www.youtube.com/channel/UCUgIHlYBOD3yA3yDIRhg_mg">YouTube</a></p>
<p style="text-align: center;">Add a  <a href="https://github.com/serpapi/public-roadmap/issues">Feature Request</a>💫 or a <a href="https://github.com/serpapi/public-roadmap/issues">Bug</a>🐞</p>