<h2 id='what'>What will be scraped</h2>

![image](https://user-images.githubusercontent.com/64033139/178459793-d2ea82a9-2415-4dc4-b1f3-427f235a664d.png)

<h2 id='preparation'>Preparation</h2>

First, we need to create a Node.js* project and add [`npm`](https://www.npmjs.com/) packages [`puppeteer`](https://www.npmjs.com/package/puppeteer), [`puppeteer-extra`](https://www.npmjs.com/package/puppeteer-extra) and [`puppeteer-extra-plugin-stealth`](https://www.npmjs.com/package/puppeteer-extra-plugin-stealth) to control Chromium (or Chrome, or Firefox, but now we work only with Chromium which is used by default) over the [DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/) in [headless](https://developers.google.com/web/updates/2017/04/headless-chrome) or non-headless mode. 

To do this, in the directory with our project, open the command line and enter `npm init -y`, and then `npm i puppeteer puppeteer-extra puppeteer-extra-plugin-stealth`.

*<span style="font-size: 15px;">If you don't have Node.js installed, you can [download it from nodejs.org](https://nodejs.org/en/) and follow the installation [documentation](https://nodejs.dev/learn/introduction-to-nodejs).</span>

📌Note: also, you can use `puppeteer` without any extensions, but I strongly recommended use it with `puppeteer-extra` with `puppeteer-extra-plugin-stealth` to prevent website detection that you are using headless Chromium or that you are using [web driver](https://www.w3.org/TR/webdriver/). You can check it on [Chrome headless tests website](https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html). The screenshot below shows you a difference.

![stealth](https://user-images.githubusercontent.com/64033139/173014238-eb8450d7-616c-42ae-8b2f-24eeb5fd5916.png)

<h2 id='process'>Process</h2>

[SelectorGadget Chrome extension](https://chrome.google.com/webstore/detail/selectorgadget/mhjhnkcfbdhnjickkkdbjoemdmbfginb) was used to grab CSS selectors by clicking on the desired element in the browser. If you have any struggles understanding this, we have a dedicated [Web Scraping with CSS Selectors blog post](https://serpapi.com/blog/web-scraping-with-css-selectors-using-python/) at SerpApi.

The Gif below illustrates the approach of selecting different parts of the results.

![how](https://user-images.githubusercontent.com/64033139/178461319-ac26ce42-83e3-4a70-ae95-fe8f591e8b61.gif)

<h2 id='full_code'>Full code</h2>

📌Notes: 
* To make our search more relevant we need to add GPS coordinates parameter. It has to be constructed in the next sequence: `@` + `latitude` + `,` + `longitude` + `,` + `zoom`. This will form a string that looks like this: e.g. `@47.6040174,-122.1854488,11z`. The zoom parameter is optional but recommended for higher precision (it ranges from `3z`, map completely zoomed out - to `21z`, map completely zoomed in). We have a dedicated video on our YouTube channel explaining [What's and Why's about Google Maps GPS Coordinates](https://www.youtube.com/watch?v=HugsLaQR0GA&t=15s).
* Sometimes Google displays results from local places using pagination, and sometimes it loads more results as you scroll. This code works for both cases. If pagination is displayed in your case, you need to uncomment the `while` loop and internal lines in the `getLocalPlacesInfo` function.

```javascript
const puppeteer = require("puppeteer-extra");
const StealthPlugin = require("puppeteer-extra-plugin-stealth");

puppeteer.use(StealthPlugin());

const requestParams = {
  baseURL: `http://google.com`,
  query: "starbucks",                                          // what we want to search
  coordinates: "@47.6040174,-122.1854488,11z",                 // parameter defines GPS coordinates of location where you want your query to be applied
  hl: "en",                                                    // parameter defines the language to use for the Google maps search
};

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

async function fillDataFromPage(page) {
  const dataFromPage = await page.evaluate(() => {
    return Array.from(document.querySelectorAll(".bfdHYd")).map((el) => {
      const placeUrl = el.parentElement.querySelector(".hfpxzc")?.getAttribute("href");
      const urlPattern = /!1s(?<id>[^!]+).+!3d(?<latitude>[^!]+)!4d(?<longitude>[^!]+)/gm;                     // https://regex101.com/r/KFE09c/1
      const dataId = [...placeUrl.matchAll(urlPattern)].map(({ groups }) => groups.id)[0];
      const latitude = [...placeUrl.matchAll(urlPattern)].map(({ groups }) => groups.latitude)[0];
      const longitude = [...placeUrl.matchAll(urlPattern)].map(({ groups }) => groups.longitude)[0];
      return {
        title: el.querySelector(".qBF1Pd")?.textContent.trim(),
        rating: el.querySelector(".MW4etd")?.textContent.trim(),
        reviews: el.querySelector(".UY7F9")?.textContent.replace("(", "").replace(")", "").trim(),
        type: el.querySelector(".W4Efsd:last-child > .W4Efsd:nth-of-type(1) > span:first-child")?.textContent.replaceAll("·", "").trim(),
        address: el.querySelector(".W4Efsd:last-child > .W4Efsd:nth-of-type(1) > span:last-child")?.textContent.replaceAll("·", "").trim(),
        openState: el.querySelector(".W4Efsd:last-child > .W4Efsd:nth-of-type(3) > span:first-child")?.textContent.replaceAll("·", "").trim(),
        phone: el.querySelector(".W4Efsd:last-child > .W4Efsd:nth-of-type(3) > span:last-child")?.textContent.replaceAll("·", "").trim(),
        website: el.querySelector("a[data-value]")?.getAttribute("href"),
        description: el.querySelector(".W4Efsd:last-child > .W4Efsd:nth-of-type(2)")?.textContent.replace("·", "").trim(),
        serviceOptions: el.querySelector(".qty3Ue")?.textContent.replaceAll("·", "").replaceAll("  ", " ").trim(),
        gpsCoordinates: {
          latitude,
          longitude,
        },
        placeUrl,
        dataId,
      };
    });
  });
  return dataFromPage;
}

async function getLocalPlacesInfo() {
  const browser = await puppeteer.launch({
    headless: false,
    args: ["--no-sandbox", "--disable-setuid-sandbox"],
  });

  const page = await browser.newPage();

  const URL = `${requestParams.baseURL}/maps/search/${requestParams.query}/${requestParams.coordinates}?hl=${requestParams.hl}`;

  await page.setDefaultNavigationTimeout(60000);
  await page.goto(URL);

  await page.waitForNavigation();

  const scrollContainer = ".m6QErb[aria-label]";

  const localPlacesInfo = [];

  // while (true) {
    await page.waitForTimeout(2000);
    // const nextPageBtn = await page.$("#eY4Fjd:not([disabled])");
    // if (!nextPageBtn) break;
    await scrollPage(page, scrollContainer);
    localPlacesInfo.push(...(await fillDataFromPage(page)));
    // await page.click("#eY4Fjd");
  // }

  await browser.close();

  return localPlacesInfo;
}

getLocalPlacesInfo().then(console.log);
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

Next, we "say" to `puppeteer` use `StealthPlugin`:

```javascript
puppeteer.use(StealthPlugin());
```

Next, we write what we want to search and the necessary parameters for making a request:

```javascript
const requestParams = {
  baseURL: `http://google.com`,
  query: "starbucks",
  coordinates: "@47.6040174,-122.1854488,11z", 
  hl: "en", 
};
```

|Code|Explanation|
|----|-----------|
|`query`|search query|
|`coordinates`|parameter defines GPS coordinates of location where you want your query to be applied. See more on [Google Maps Help](https://support.google.com/maps/answer/18539?hl=en&co=GENIE.Platform%3DDesktop)|
|`hl`|parameter defines the language to use for the Google Maps search|
        
Next, we write down a function for scrolling places container on the page:

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

Next, we write down a function for getting places info from page:

```javascript
async function fillDataFromPage(page) {
  const dataFromPage = await page.evaluate(() => {
    return Array.from(document.querySelectorAll(".bfdHYd")).map((el) => {
      const placeUrl = el.parentElement.querySelector(".hfpxzc")?.getAttribute("href");
      const urlPattern = /!1s(?<id>[^!]+).+!3d(?<latitude>[^!]+)!4d(?<longitude>[^!]+)/gm;                     // https://regex101.com/r/KFE09c/1
      const dataId = [...placeUrl.matchAll(urlPattern)].map(({ groups }) => groups.id)[0];
      const latitude = [...placeUrl.matchAll(urlPattern)].map(({ groups }) => groups.latitude)[0];
      const longitude = [...placeUrl.matchAll(urlPattern)].map(({ groups }) => groups.longitude)[0];
      return {
        title: el.querySelector(".qBF1Pd")?.textContent.trim(),
        rating: el.querySelector(".MW4etd")?.textContent.trim(),
        reviews: el.querySelector(".UY7F9")?.textContent.replace("(", "").replace(")", "").trim(),
        type: el.querySelector(".W4Efsd:last-child > .W4Efsd:nth-of-type(1) > span:first-child")?.textContent.replaceAll("·", "").trim(),
        address: el.querySelector(".W4Efsd:last-child > .W4Efsd:nth-of-type(1) > span:last-child")?.textContent.replaceAll("·", "").trim(),
        openState: el.querySelector(".W4Efsd:last-child > .W4Efsd:nth-of-type(3) > span:first-child")?.textContent.replaceAll("·", "").trim(),
        phone: el.querySelector(".W4Efsd:last-child > .W4Efsd:nth-of-type(3) > span:last-child")?.textContent.replaceAll("·", "").trim(),
        website: el.querySelector("a[data-value]")?.getAttribute("href"),
        description: el.querySelector(".W4Efsd:last-child > .W4Efsd:nth-of-type(2)")?.textContent.replace("·", "").trim(),
        serviceOptions: el.querySelector(".qty3Ue")?.textContent.replaceAll("·", "").replaceAll("  ", " ").trim(),
        gpsCoordinates: {
          latitude,
          longitude,
        },
        placeUrl,
        dataId,
      };
    });
  });
  return dataFromPage;
}
```

|Code|Explanation|
|----|-----------|
|[`document.querySelectorAll(".bfdHYd")`](https://developer.mozilla.org/en-US/docs/Web/API/Document/querySelectorAll)|returns a static [NodeList](https://developer.mozilla.org/en-US/docs/Web/API/NodeList) representing a list of the document's elements that match the css selectors with class name `bfdHYd`|
|[`el.querySelector(".qBF1Pd")`](https://developer.mozilla.org/en-US/docs/Web/API/Document/querySelector)|returns the first html element with selector `.qBF1Pd` which is any child of the `el` html element|
|`.getAttribute("href")`|gets the `href` attribute value of the html element|
|`urlPattern`|a RegEx pattern for search and define id, latitude and longitude. [See what it allows you to find](https://regex101.com/r/KFE09c/1)|
|`[...placeUrl.matchAll(urlPattern)]`|in this code we use [spread syntax](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Spread_syntax) to create an array from an [iterator](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Iterators_and_Generators) that was returned from [matchAll method](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/matchAll) (in this case this entry is equal to `Array.from(placeUrl.matchAll(urlPattern))`)|
|`.textContent`|gets the raw text of html element|
|[`.trim()`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/trim)|removes whitespace from both ends of a string|
        
And finally, a function to control the browser, and get information:

```javascript
async function getLocalPlacesInfo() {
  const browser = await puppeteer.launch({
    headless: false,
    args: ["--no-sandbox", "--disable-setuid-sandbox"],
  });

  const page = await browser.newPage();

  const URL = `${requestParams.baseURL}/maps/search/${requestParams.query}/${requestParams.coordinates}?hl=${requestParams.hl}`;

  await page.setDefaultNavigationTimeout(60000);
  await page.goto(URL);

  await page.waitForNavigation();

  const scrollContainer = ".m6QErb[aria-label]";

  const localPlacesInfo = [];

  // while (true) {
    await page.waitForTimeout(2000);
    // const nextPageBtn = await page.$("#eY4Fjd:not([disabled])");
    // if (!nextPageBtn) break;
    await scrollPage(page, scrollContainer);
    localPlacesInfo.push(...(await fillDataFromPage(page)));
    // await page.click("#eY4Fjd");
  // }

  await browser.close();

  return localPlacesInfo;
}

getLocalPlacesInfo().then(console.log);
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
|`page.$("#eY4Fjd:not([disabled])")`|this methods finds the html element with the `#eY4Fjd:not([disabled])` selector and return it|
|`localPlacesInfo.push(...(await fillDataFromPage(page)))`|in this code, we use [spread syntax](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Spread_syntax) to split the array which is returned from the `fillDataFromPage` function into elements and add them to the end of the `localPlacesInfo` array|
|`page.click("#eY4Fjd")`|this methods emulates mouse click on the html element with the `#eY4Fjd` selector|
|`browser.close()`|after all we close the browser instance|

Now we can launch our parser. To do this enter `node YOUR_FILE_NAME` in your command line. Where `YOUR_FILE_NAME` is the name of your `.js` file.

<h2 id='output'>Output</h2>

📌Note: if you see something like `[Object]` in your console you can use `console.dir(result, { depth: null })` instead `console.log()`. Watch [Node.js documentation](https://nodejs.org/api/console.html#consoledirobj-options) for more info.

```json
[
[
   {
      "title":"Starbucks",
      "rating":"4.2",
      "reviews":"233",
      "type":"Coffee shop",
      "address":"545 Bellevue Square",
      "openState":"Closed ⋅ Opens 7AM",
      "phone":"+1 425-452-5534",
      "website":"https://www.starbucks.com/store-locator/store/18615/",
      "description":"Iconic Seattle-based coffeehouse chain",
      "serviceOptions":"Dine-in   Takeaway   No delivery",
      "gpsCoordinates":{
         "latitude":"47.617077",
         "longitude":"-122.2019599"
      },
      "placeUrl":"https://www.google.com/maps/place/Starbucks/data=!4m7!3m6!1s0x54906c8f50e36025:0x5175a46aeadfbc0f!8m2!3d47.617077!4d-122.2019599!16s%2Fg%2F1thw6fd9!19sChIJJWDjUI9skFQRD7zf6mqkdVE?authuser=0&hl=en&rclk=1",
      "dataId":"0x54906c8f50e36025:0x5175a46aeadfbc0f"
   },
   {
      "title":"Starbucks",
      "reviews":"379",
      "type":"Coffee shop",
      "address":"1785 NE 44th St",
      "openState":"Closed ⋅ Opens 4:30AM",
      "phone":"+1 425-226-7007",
      "website":"https://www.starbucks.com/store-locator/store/10581/",
      "description":"Iconic Seattle-based coffeehouse chain",
      "serviceOptions":"Dine-in   Drive-through   Delivery",
      "gpsCoordinates":{
         "latitude":"47.5319688",
         "longitude":"-122.1942498"
      },
      "placeUrl":"https://www.google.com/maps/place/Starbucks/data=!4m7!3m6!1s0x549069a98254bd17:0xb2f64f75b3edf4c3!8m2!3d47.5319688!4d-122.1942498!16s%2Fg%2F1tdfmzpb!19sChIJF71UgqlpkFQRw_Tts3VP9rI?authuser=0&hl=en&rclk=1",
      "dataId":"0x549069a98254bd17:0xb2f64f75b3edf4c3"
   },
   ...and other results
]
```

<h2 id='serp_api'>Google Scholar Author API</h2>

Alternatively, you can use the [Google Maps Local Results API](https://serpapi.com/maps-local-results) from SerpApi. SerpApi is a free API with 100 searches per month. If you need more searches, there are paid plans.

The difference is that you won't have to write code from scratch and maintain it. You may also experience blocking from Google and changing selectors which will break the parser. Instead, you just need to iterate the structured JSON and get the data you want. [Check out the playground](https://serpapi.com/playground).

First, we need to install [`google-search-results-nodejs`](https://www.npmjs.com/package/google-search-results-nodejs). To do this you need to enter in your console: `npm i google-search-results-nodejs`

📌Note: To make our search more relevant we need to add GPS coordinates parameter. It has to be constructed in the next sequence: `@` + `latitude` + `,` + `longitude` + `,` + `zoom`. This will form a string that looks like this: e.g. `@47.6040174,-122.1854488,11z`. The zoom parameter is optional but recommended for higher precision (it ranges from `3z`, map completely zoomed out - to `21z`, map completely zoomed in).

```javascript
const SerpApi = require("google-search-results-nodejs");
const search = new SerpApi.GoogleSearch(process.env.API_KEY); //your API key from serpapi.com

const searchString = "starbucks"; // what we want to search

const params = {
  engine: "google_maps", // search engine
  q: searchString, // search query
  hl: "en", // parameter defines the language to use for the Google search
  ll: "@47.6040174,-122.1854488,11z", // parameter defines GPS coordinates of location where you want your query to be applied
  type: "search", // parameter defines the type of search you want to make
};

const getJson = () => {
  return new Promise((resolve) => {
    search.json(params, resolve);
  });
};

const getResults = async () => {
  const allPlaces = [];
  while (true) {
    const json = await getJson();
    if (json.local_results) {
      allPlaces.push(...json.local_results)
    } else break;
    if (json.serpapi_pagination?.next) {
      !params.start ? (params.start = 20) : (params.start += 20);
    } else break;
  }
  return allPlaces;
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
const searchString = "starbucks";

const params = {
  engine: "google_maps",
  q: searchString,
  hl: "en",
  ll: "@47.6040174,-122.1854488,11z", // parameter defines GPS coordinates of location where you want your query to be applied
  type: "search", // parameter defines the type of search you want to make
};
```

|Code|Explanation|
|----|-----------|
|`searchString`|what we want to search|
|`engine`|search engine|
|`q`|search query|
|`hl`|parameter defines the language to use for the Google Scholar search|
|`ll`|parameter defines GPS coordinates of location where you want your query to be applied|
|`type`|parameter defines the type of search you want to make|

Next, we wrap the search method from the SerpApi library in a promise to further work with the search results:

```javascript
const getJson = () => {
  return new Promise((resolve) => {
    search.json(params, resolve);
  })
}
```

And finally, we declare and run the function `getResult` that gets places info from all pages and return it:

```javascript
const getResults = async () => {
  const allPlaces = [];
  while (true) {
    const json = await getJson();
    if (json.local_results) {
      allPlaces.push(...json.local_results)
    } else break;
    if (json.serpapi_pagination?.next) {
      !params.start ? (params.start = 20) : (params.start += 20);
    } else break;
  }
  return allPlaces;
};

getResults().then((result) => console.dir(result, { depth: null }))
```

|Code|Explanation|
|----|-----------|
|`allPlaces`|an array with all citations info from all pages|
|`allPlaces.push(...json.local_results)`|in this code, we use [spread syntax](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Spread_syntax) to split the `local_results` array from result that was returned from `getJson` function into elements and add them in the end of `allPlaces` array|
|`console.dir(result, { depth: null })`|console method `dir` allows you to use an object with the necessary parameters to change default output options. Watch [Node.js documentation](https://nodejs.org/api/console.html#consoledirobj-options) for more info|

<h2 id='serp_api_output'>Output</h2>

```json
[
   {
      "position":1,
      "title":"Starbucks",
      "place_id":"ChIJrxaZdhlBkFQRk-hWRsy4sWA",
      "data_id":"0x54904119769916af:0x60b1b8cc4656e893",
      "data_cid":"6967553286011807891",
      "reviews_link":"https://serpapi.com/search.json?data_id=0x54904119769916af%3A0x60b1b8cc4656e893&engine=google_maps_reviews&hl=en",
      "photos_link":"https://serpapi.com/search.json?data_id=0x54904119769916af%3A0x60b1b8cc4656e893&engine=google_maps_photos&hl=en",
      "gps_coordinates":{
         "latitude":47.544705,
         "longitude":-122.38743199999999
      },
      "place_id_search":"https://serpapi.com/search.json?data=%214m5%213m4%211s0x54904119769916af%3A0x60b1b8cc4656e893%218m2%213d47.544705%214d-122.38743199999999&engine=google_maps&google_domain=google.com&hl=en&start=80&type=place",
      "rating":4.2,
      "reviews":310,
      "price":"$$",
      "type":"Coffee shop",
      "address":"6501 California Ave SW, Seattle, WA 98136, United States",
      "open_state":"Closed ⋅ Opens 5AM",
      "hours":"Closed ⋅ Opens 5AM",
      "operating_hours":{
         "wednesday":"5am–5:30pm",
         "thursday":"5am–5:30pm",
         "friday":"5am–5:30pm",
         "saturday":"5am–5:30pm",
         "sunday":"5am–5:30pm",
         "monday":"5am–5:30pm",
         "tuesday":"5am–5:30pm"
      },
      "phone":"+1 206-938-6371",
      "website":"https://www.starbucks.com/store-locator/store/18390/",
      "description":"Iconic Seattle-based coffeehouse chain. Seattle-based coffeehouse chain known for its signature roasts, light bites and WiFi availability.",
      "service_options":{
         "dine_in":true,
         "drive_through":true,
         "delivery":true
      },
      "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipOSvSFJ7cD_s3pemaRs_TjEQe2_aVAy_NhUZVgN=w80-h106-k-no"
   },
   ...and other results
]
```

<h2 id='links'>Links</h2>

* [Code in the online IDE](https://replit.com/@MikhailZub/Google-Maps-Places-NodeJS-SerpApi#index.js) 
* [Google Maps Local Results API](https://serpapi.com/maps-local-results)

If you want to see some projects made with SerpApi, please write me a message.

___
<p style="text-align: center;">Join us on <a href="https://twitter.com/serp_api">Twitter</a> | <a href="https://www.youtube.com/channel/UCUgIHlYBOD3yA3yDIRhg_mg">YouTube</a></p>
<p style="text-align: center;">Add a  <a href="https://github.com/serpapi/public-roadmap/issues">Feature Request</a>💫 or a <a href="https://github.com/serpapi/public-roadmap/issues">Bug</a>🐞</p>