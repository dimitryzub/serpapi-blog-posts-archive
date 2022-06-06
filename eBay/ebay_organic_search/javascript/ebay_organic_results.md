<h2 id='what'>What will be scraped</h2>

![image](https://user-images.githubusercontent.com/64033139/171408505-80c98d88-28cb-4cae-abc0-f2d5063d9466.png)


<h2 id='preparation'>Preparation</h2>

First, we need to create a Node.js* project and add [`npm`](https://www.npmjs.com/) packages [`puppeteer`](https://www.npmjs.com/package/puppeteer), [`puppeteer-extra`](https://www.npmjs.com/package/puppeteer-extra) and [`puppeteer-extra-plugin-stealth`](https://www.npmjs.com/package/puppeteer-extra-plugin-stealth) to control Chromium (or Chrome, or Firefox, but now we work only with Chromium which is used by default) over the [DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/) in [headless](https://developers.google.com/web/updates/2017/04/headless-chrome) or full (non-headless) mode. To do this, in the directory with our project, open the command line and enter `npm init -y`, and then `npm i puppeteer puppeteer-extra puppeteer-extra-plugin-stealth`.

*<span style="font-size: 15px;">If you don't have Node.js installed, you can [download it from nodejs.org](https://nodejs.org/en/) and follow the installation [documentation](https://nodejs.dev/learn/introduction-to-nodejs).</span>

📌Note: also, you can use `puppeteer` without any extensions, but I strongly recommended use it with `puppeteer-extra` with `puppeteer-extra-plugin-stealth` to prevent website detection that you are using headless Chromium or that you are using [web driver](https://www.w3.org/TR/webdriver/). You can check it on [Chrome headless tests website](https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html). The screenshot below shows you a difference.

![stealth](https://user-images.githubusercontent.com/64033139/171674554-d6027d3e-5fb2-44fb-88c7-4492851b43ff.png)

<h2 id='process'>Process</h2>

[SelectorGadget Chrome extension](https://chrome.google.com/webstore/detail/selectorgadget/mhjhnkcfbdhnjickkkdbjoemdmbfginb) was used to grab CSS selectors by clicking on the desired element in the browser. If you have any struggles understanding this, we have a dedicated [Web Scraping with CSS Selectors blog post](https://serpapi.com/blog/web-scraping-with-css-selectors-using-python/) at SerpApi.
The Gif below illustrates the approach of selecting different parts of the results.

![how2](https://user-images.githubusercontent.com/64033139/171663382-83677c90-7a01-47c6-8924-ecd07ba7d4fc.gif)

<h2 id='full_code'>Full code</h2>

```javascript
const puppeteer = require("puppeteer-extra");
const StealthPlugin = require("puppeteer-extra-plugin-stealth");

puppeteer.use(StealthPlugin());

const searchString = "playstation";                   // what we want to search
const pagesLimit = 10;                                // limit of pages for getting info
let currentPage = 1;                                  // current page of the search

const URL = "https://www.ebay.com";

async function getPageResults(page) {
  const pageResults = await page.evaluate(function () {
    return Array.from(document.querySelectorAll("ul .s-item__wrapper")).map((el) => ({
      link: el.querySelector(".s-item__link").getAttribute("href"),
      title: el.querySelector(".s-item__title").textContent.trim(),
      condition: el.querySelector(".SECONDARY_INFO")?.textContent.trim() || "No condition data",
      price: el.querySelector(".s-item__price")?.textContent.trim() || "No price data",
      shipping: el.querySelector(".s-item__shipping")?.textContent.trim() || "No shipping data",
      thumbnail: el.querySelector(".s-item__image-img")?.getAttribute("src") || "No image",
    }));
  });
  return pageResults;
}

async function getOrganicResults() {
  const browser = await puppeteer.launch({
    headless: false,
    args: ["--no-sandbox", "--disable-setuid-sandbox"],
  });

  const page = await browser.newPage();

  await page.setDefaultNavigationTimeout(60000);
  await page.goto(URL);
  await page.waitForSelector("#gh-ac");
  await page.focus("#gh-ac");
  await page.keyboard.type(searchString);
  await page.waitForTimeout(1000);
  await page.click("#gh-btn");

  const organicResults = [];

  while (true) {
    await page.waitForSelector(".srp-results");
    const isNextPage = await page.$(".pagination__next");
    if (!isNextPage || currentPage > pagesLimit) break;
    organicResults.push(...(await getPageResults(page)));
    await page.click(".pagination__next");
    currentPage++;
  }

  await browser.close();

  return organicResults;
}

getOrganicResults().then(console.log);
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

Next, we "saying" to `puppeteer` use `StealthPlugin`:

```javascript
puppeteer.use(StealthPlugin());
```

Next, we write variables with our search parameters:

```javascript
const searchString = "playstation";
const pagesLimit = 10;
let currentPage = 1;

const URL = "https://www.ebay.com";
```

|Code|Explanation|
|----|-----------|
|`searchString`|what we want to search|
|`pagesLimit`|limit of pages for getting info|
|`currentPage`|current page of the search|

Next, we write down a function for getting information from page:

```javascript
async function getPageResults(page) {
  const pageResults = await page.evaluate(function () {
    return Array.from(document.querySelectorAll("ul .s-item__wrapper")).map((el) => ({
      link: el.querySelector(".s-item__link").getAttribute("href"),
      title: el.querySelector(".s-item__title").textContent.trim(),
      condition: el.querySelector(".SECONDARY_INFO")?.textContent.trim() || "No condition data",
      price: el.querySelector(".s-item__price")?.textContent.trim() || "No price data",
      shipping: el.querySelector(".s-item__shipping")?.textContent.trim() || "No shipping data",
      thumbnail: el.querySelector(".s-item__image-img")?.getAttribute("src") || "No image",
    }));
  });
  return pageResults;
}
```

|Code|Explanation|
|----|-----------|
|`pageResults`|an array with information about all goods from page|
|`page.evaluate(function () {`|is the Puppeteer method for injecting `function` in the page context and allows to return data directly from the browser|
|`.getAttribute("href")`|gets the `href` attribute value of the html element|
|[`.trim()`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/trim)|removes whitespace from both ends of a string|
        
And finally, a function to control the browser, change pages, and runs `getPageResults` from each page:

```javascript
async function getOrganicResults() {
  const browser = await puppeteer.launch({
    headless: false,
    args: ["--no-sandbox", "--disable-setuid-sandbox"],
  });

  const page = await browser.newPage();

  await page.setDefaultNavigationTimeout(60000);
  await page.goto(URL);
  await page.waitForSelector("#gh-ac");
  await page.focus("#gh-ac");
  await page.keyboard.type(searchString);
  await page.waitForTimeout(1000);
  await page.click("#gh-btn");

  const organicResults = [];

  while (true) {
    await page.waitForSelector(".srp-results");
    const isNextPage = await page.$(".pagination__next");
    if (!isNextPage || currentPage > pagesLimit) break;
    organicResults.push(...(await getPageResults(page)));
    await page.click(".pagination__next");
    currentPage++;
  }

  await browser.close();

  return organicResults;
}
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
|`page.waitForSelector("#gh-ac")`|stops the script and waits for the html element with the `#gh-ac` selector to load|
|`page.focus("#gh-ac")`|focus on the html element with the `#gh-ac` selector|
|`page.keyboard.type(searchString)`|this method emulates keyboard input stored in `searchString` text|
|`page.waitForTimeout(1000)`|waiting 1000 ms before continue|
|`page.click("#gh-btn")`|this methods emulates mouse click on the html element with the `#gh-btn` selector|
|`const isNextPage = await page.$(".pagination__next")`|in this line of code, we find the html element with the `.pagination__next` selector and save it in `isNextPage` constant|
|`organicResults.push(...(await getPageResults(page)))`|in this code, we use [spread syntax](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Spread_syntax) to split the array from result that was returned from `getPageResults` function into elements and add them in the end of `organicResults` array|
|`browser.close()`|after all we close the browser instance|

Now we can launch our parser. To do this enter `node YOUR_FILE_NAME` in your command line. Where `YOUR_FILE_NAME` is the name of your `.js` file.

<h2 id='output'>Output</h2>

```json
[
   {
      "link":"https://www.ebay.com/itm/324843125086?epid=4039276585&hash=item4ba228b95e:g:iygAAOSwJfFdty6D&amdata=enc%3AAQAHAAAA4BFods1e0MuxITheGVrICxhRAyEmOAtx6%2BT28euOBHuShbOsuqcQpMnhGTsxgz2hVdsgoUlbIYGe5nghV6CFsQVPDoRG%2FKhoBe2ilQMTPM%2BmcyGm8Qx%2B2DL%2BOg3UZAGCbXM0jikrzbg0zKp1PCYgcINmwxFqy7MaNP%2BnO2TMJEIK45mGxj6Ymsx2lDyuT84SMvBClalDYs9rJMZmrzQqIgyo0Kerk6Wk6F1l%2BBDyJ%2Blpe%2BmwoYqzu2FzQxAX3gAyRF0XSTyrDRu2IYXb0Kh89kbvtuq0KNyNG%2B2lZdO78M0R%7Ctkp%3ABFBMjMe8n6Vg",
      "title":"Dusk Diver Day One Edition PlayStation 4, PS4 Brand New Factory Sealed",
      "condition":"Brand New",
      "price":"$37.49",
      "shipping":"Free shipping",
      "thumbnail":"https://i.ebayimg.com/thumbs/images/g/iygAAOSwJfFdty6D/s-l225.webp"
   },
   {
      "link":"https://www.ebay.com/itm/265719188920?epid=110660824&hash=item3dde190db8:g:-oEAAOSwztpimIB~",
      "title":"Sony PlayStation with xStation installed (PS1, NTSC SCPH-5501)",
      "condition":"Pre-Owned",
      "price":"$289.99",
      "shipping":"+$13.15 shipping",
      "thumbnail":"https://i.ebayimg.com/thumbs/images/g/-oEAAOSwztpimIB~/s-l225.webp"
   },
   ...and other results
]
```

<h2 id='serp_api'>Ebay Search Engine Results API</h2>

Alternatively, you can use the [Ebay Search Engine Results API](https://serpapi.com/ebay-search-api) from SerpApi. SerpApi is a free API with 100 searches per month. If you need more searches, there are paid plans.

The difference is that you don't have to use browser control solutions (like Puppeteer) which is much more time-consuming, you also don't have to look for the right selectors that can change over time, bypass blocking from robots and maintain a solution written from scratch. Instead, you will get ready-made structured JSON. [Check out the playground](https://serpapi.com/playground).

First we need to install [`google-search-results-nodejs`](https://www.npmjs.com/package/google-search-results-nodejs). To do this you need to enter in your command line: `npm i google-search-results-nodejs`

```javascript
const SerpApi = require("google-search-results-nodejs");
const search = new SerpApi.GoogleSearch(process.env.API_KEY);     //your api key from serpapi.com

const searchString = "playstation";                                       // what we want to search
const pagesLimit = 10;                                                    // limit of pages for getting info
let currentPage = 1;                                                      // current page of the search

const params = {
  engine: "ebay",                                                         // search engine
  _nkw: searchString,                                                     // search query
  ebay_domain: "ebay.com",                                                // ebay domain of the search
  _pgn: currentPage,                                                      // page of the search
};

const getOrganicResults = ({ organic_results }) => {
  return organic_results.map((element) => {
    const { link, title, condition = "No condition data", price = "No price data", shipping = "No shipping data", thumbnail = "No image" } = element;
    return {
      link,
      title,
      condition,
      price: price && price.raw ? price.raw : `${price.from?.raw} - ${price.to?.raw}`,
      shipping,
      thumbnail,
    };
  });
};

const getJson = (params) => {
  return new Promise((resolve) => {
    search.json(params, resolve);
  });
};

const getResults = async () => {
  const organicResults = [];
  while (true) {
    if (currentPage > pagesLimit) break;
    const json = await getJson(params);
    if (json.search_information?.organic_results_state === "Fully empty") break;
    organicResults.push(...(await getOrganicResults(json)));
    currentPage++;
  }
  return organicResults;
};

getResults().then(console.log)
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
const searchString = "playstation";
const pagesLimit = 10;
let currentPage = 1;

const params = {
  engine: "ebay",
  _nkw: searchString,
  ebay_domain: "ebay.com",
  _pgn: currentPage,
};
```

|Code|Explanation|
|----|-----------|
|`searchString`|what we want to search|
|`pagesLimit`|limit of pages for getting info|
|`currentPage`|current page of the search|
|`engine`|search engine|
|`_nkw`|search query|
|`ebay_domain`|ebay domain: ebay.com, ebay.de, ebay.co.uk|
|`_pgn`|current page|

Next, we write a callback function in which we describe what data we need from the result of our request:

```javascript
const getOrganicResults = ({ organic_results }) => {
  return organic_results.map((element) => {
    const { link, title, condition = "No condition data", price = "No price data", shipping = "No shipping data", thumbnail = "No image" } = element;
    return {
      link,
      title,
      condition,
      price: price && price.raw ? price.raw : `${price.from?.raw} - ${price.to?.raw}`,
      shipping,
      thumbnail,
    };
  });
};
```

|Code|Explanation|
|----|-----------|
|`organic_results`|an array that we destructured from response|
|`link, title, condition, price, shipping, thumbnail`|other data that we destructured from element of news_results array|
|`thumbnail = "No image"`|we set default value `No image` if `thumbnail` is `undefined`|
|`price: price && price.raw ? price.raw : `${price.from?.raw} - ${price.to?.raw}``|in this line we use [ternary operator](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Conditional_Operator) to set vailid price. If we can get `price` and data with `raw` key we set it to our `price`, otherwise in `price` we set `price.from` and `price.to`|

Next, we wrap the search method from the SerpApi library in a promise to further work with the search results:

```javascript
const getJson = (params) => {
  return new Promise((resolve) => {
    search.json(params, resolve);
  })
}

getJson(params).then(getKnowledgeGraph).then(console.log)
```

And finally, we declare and run the function `getResult` that gets info from all pages between `currentPage` and `pagesLimit` and return it.

```javascript
const getResults = async () => {
  const organicResults = [];
  while (true) {
    if (currentPage > pagesLimit) break;
    const json = await getJson(params);
    if (json.search_information?.organic_results_state === "Fully empty") break;
    organicResults.push(...(await getOrganicResults(json)));
    currentPage++;
  }
  return organicResults;
};

getResults().then(console.log)
```

|Code|Explanation|
|----|-----------|
|`organicResults.push(...(await getOrganicResults(json)))`|in this code, we use [spread syntax](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Spread_syntax) to split the array from result that was returned from `getOrganicResults` function into elements and add them in the end of `organicResults` array|

<h2 id='serp_api_output'>Output</h2>

```json
[
   {
      "link":"https://www.ebay.com/itm/324950767168?hash=item4ba8933640:g:yQsAAOSwU8phwB9l",
      "title":"Sony PlayStation PS Vita OLED (PCH-1001) Firmware FW 3.60, 128GB - Ship in 1-DAY",
      "condition":"Open Box",
      "price":"$179.95",
      "shipping":"Free shipping",
      "thumbnail":"https://i.ebayimg.com/thumbs/images/g/yQsAAOSwU8phwB9l/s-l225.jpg"
   },
   {
      "link":"https://www.ebay.com/itm/393419045168?hash=item5b999a3930:g:NzYAAOSwBPNiBoAk",
      "title":"PS4 PlayStation 4 Sony Original Slim Pro 500GB 1TB 2TB Console Used Ship first",
      "condition":"Pre-Owned",
      "price":"$259.80 - $484.99",
      "shipping":"Free shipping",
      "thumbnail":"https://i.ebayimg.com/thumbs/images/g/NzYAAOSwBPNiBoAk/s-l225.jpg"
   },
   ...and other results
]
```

<h2 id='links'>Links</h2>

* [Code in the online IDE](https://replit.com/@MikhailZub/Scrape-eBay-Organic-Results-with-NodeJS-SerpApi#index.js) 
* [Ebay Search Engine Results API](https://serpapi.com/ebay-search-api)
* [Ebay Search Engine Results in SerpApi Playgrond](https://serpapi.com/playground?engine=ebay&_nkw=playstation&ebay_domain=ebay.com)

If you want to see some projects made with SerpApi, please write me a message.

___
<p style="text-align: center;">Join us on <a href="https://twitter.com/serp_api">Twitter</a> | <a href="https://www.youtube.com/channel/UCUgIHlYBOD3yA3yDIRhg_mg">YouTube</a></p>
<p style="text-align: center;">Add a  <a href="https://github.com/serpapi/public-roadmap/issues">Feature Request</a>💫 or a <a href="https://github.com/serpapi/public-roadmap/issues">Bug</a>🐞</p>