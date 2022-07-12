<h2 id='what'>What will be scraped</h2>

![image](https://user-images.githubusercontent.com/64033139/177721411-4fb88604-fc7e-40e5-8068-ebc167be13c1.png)

<h2 id='preparation'>Preparation</h2>

First, we need to create a Node.js* project and add [`npm`](https://www.npmjs.com/) packages [`puppeteer`](https://www.npmjs.com/package/puppeteer), [`puppeteer-extra`](https://www.npmjs.com/package/puppeteer-extra) and [`puppeteer-extra-plugin-stealth`](https://www.npmjs.com/package/puppeteer-extra-plugin-stealth) to control Chromium (or Chrome, or Firefox, but now we work only with Chromium which is used by default) over the [DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/) in [headless](https://developers.google.com/web/updates/2017/04/headless-chrome) or non-headless mode. 

To do this, in the directory with our project, open the command line and enter `npm init -y`, and then `npm i puppeteer puppeteer-extra puppeteer-extra-plugin-stealth`.

*<span style="font-size: 15px;">If you don't have Node.js installed, you can [download it from nodejs.org](https://nodejs.org/en/) and follow the installation [documentation](https://nodejs.dev/learn/introduction-to-nodejs).</span>

📌Note: also, you can use `puppeteer` without any extensions, but I strongly recommended use it with `puppeteer-extra` with `puppeteer-extra-plugin-stealth` to prevent website detection that you are using headless Chromium or that you are using [web driver](https://www.w3.org/TR/webdriver/). You can check it on [Chrome headless tests website](https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html). The screenshot below shows you a difference.

![stealth](https://user-images.githubusercontent.com/64033139/173014238-eb8450d7-616c-42ae-8b2f-24eeb5fd5916.png)

<h2 id='process'>Process</h2>

[SelectorGadget Chrome extension](https://chrome.google.com/webstore/detail/selectorgadget/mhjhnkcfbdhnjickkkdbjoemdmbfginb) was used to grab CSS selectors by clicking on the desired element in the browser. If you have any struggles understanding this, we have a dedicated [Web Scraping with CSS Selectors blog post](https://serpapi.com/blog/web-scraping-with-css-selectors-using-python/) at SerpApi.
The Gif below illustrates the approach of selecting different parts of the results.

![how](https://user-images.githubusercontent.com/64033139/177724872-b5c97fe2-7f65-4fd6-ba63-a18991e4673c.gif)

<h2 id='full_code'>Full code</h2>

```javascript
const puppeteer = require("puppeteer-extra");
const StealthPlugin = require("puppeteer-extra-plugin-stealth");

puppeteer.use(StealthPlugin());

const requestParams = {
  q: "astronomy",                                           // what we want to search
  hl: "en",                                                 // parameter defines the language to use for the Google search
};

const domain = `http://scholar.google.com`;
const pagesLimit = Infinity;                                // limit of pages for getting info
let currentPage = 1;

async function getCitesId(page) {
  const citesId = [];
  while (true) {
    await page.waitForSelector(".gs_r.gs_scl");
    const citesIdFromPage = await page.evaluate(async () => {
      return Array.from(document.querySelectorAll(".gs_r.gs_scl")).map((el) => el.getAttribute("data-cid"));
    });
    citesId.push(...citesIdFromPage);
    const isNextPage = await page.$("#gs_n td:last-child a");
    if (!isNextPage || currentPage > pagesLimit) break;
    await page.evaluate(async () => {
      document.querySelector("#gs_n td:last-child a").click();
    });
    await page.waitForTimeout(3000);
    currentPage++;
  }
  return citesId;
}

async function fillCiteData(page) {
  const citeData = await page.evaluate(async () => {
    const citations = Array.from(document.querySelectorAll("#gs_citt tr")).map((el) => {
      return {
        title: el.querySelector("th").textContent.trim(),
        snippet: el.querySelector("td").textContent.trim(),
      };
    });
    const links = Array.from(document.querySelectorAll("#gs_citi a")).map((el) => {
      return {
        name: el.textContent.trim(),
        link: el.getAttribute("href"),
      };
    });
    return { citations, links };
  });
  return citeData;
}

async function getScholarCitesInfo() {
  const browser = await puppeteer.launch({
    headless: false,
    args: ["--no-sandbox", "--disable-setuid-sandbox"],
  });

  const page = await browser.newPage();

  const URL = `${domain}/scholar?hl=${requestParams.hl}&q=${requestParams.q}`;

  await page.setDefaultNavigationTimeout(60000);
  await page.goto(URL);
  await page.waitForSelector(".gs_r.gs_scl");
  await page.waitForTimeout(1000);

  const citesId = await getCitesId(page);
  const allCites = [];

  for (id of citesId) {
    const URL = `${domain}/scholar?q=info:${id}:scholar.google.com/&output=cite&hl=${requestParams.hl}`;
    try {
      await page.goto(URL);
      await page.waitForTimeout(2000);
      allCites.push(await fillCiteData(page));
    } catch {
      console.log("Something was wrong with getting info from ID: ", id)
    }
  }

  await browser.close();

  return allCites;
}

getScholarCitesInfo().then((result) => console.dir(result, { depth: null }));
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
  q: "astronomy",
  hl: "en",
};

const domain = `http://scholar.google.com`;
const pagesLimit = Infinity;
let currentPage = 1;
```

|Code|Explanation|
|----|-----------|
|`q`|search query|
|`hl`|parameter defines the language to use for the Google Scholar search|
|`pagesLimit`|limit of pages for getting info. If you want to limit the number of pages for getting info you need to define the last page number in this|
        
Next, we write down a function for getting citations ID from all pages:

```javascript
async function getCitesId(page) {
  const citesId = [];
  while (true) {
    await page.waitForSelector(".gs_r.gs_scl");
    const citesIdFromPage = await page.evaluate(async () => {
      return Array.from(document.querySelectorAll(".gs_r.gs_scl")).map((el) => el.getAttribute("data-cid"));
    });
    citesId.push(...citesIdFromPage);
    const isNextPage = await page.$("#gs_n td:last-child a");
    if (!isNextPage || currentPage > pagesLimit) break;
    await page.evaluate(async () => {
      document.querySelector("#gs_n td:last-child a").click();
    });
    await page.waitForTimeout(3000);
    currentPage++;
  }
  return citesId;
}
```

|Code|Explanation|
|----|-----------|
|`citesId`|an array with cite ID from the all pages|
|`page.waitForSelector(".gs_r.gs_scl")`|stops the script and waits for the html element with the `.gs_r.gs_scl` selector to load|
|`page.evaluate(async () => {`|is the Puppeteer method for injecting `function` in the page context and allows to return data directly from the browser|
|[`document.querySelectorAll(".gs_r.gs_scl")`](https://developer.mozilla.org/en-US/docs/Web/API/Document/querySelectorAll)|returns a static [NodeList](https://developer.mozilla.org/en-US/docs/Web/API/NodeList) representing a list of the document's elements that match the css selectors with class name `gs_r.gs_scl`|
|`.getAttribute("data-cid")`|gets the `data-cid` attribute value of the html element|
|`citesId.push(...citesIdFromPage)`|in this code, we use [spread syntax](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Spread_syntax) to split the `citesIdFromPage` array into elements and add them in the end of `citesId` array|
|`page.$("#gs_n td:last-child a");`|this methods finds the html element with the `#gs_n td:last-child a` selector and return it|
|[`document.querySelector(".gsc_a_at")`](https://developer.mozilla.org/en-US/docs/Web/API/Document/querySelector)|returns the first html element with selector `#gs_n td:last-child a` which is any child of the `document` html element|
|`.click()`|triggers a click event on html element|
|`page.waitForTimeout(3000)`|waiting 3000 ms before continue|

Next, we write down a function for getting citations data from page:

```javascript
async function fillCiteData(page) {
  const citeData = await page.evaluate(async () => {
    const citations = Array.from(document.querySelectorAll("#gs_citt tr")).map((el) => {
      return {
        title: el.querySelector("th").textContent.trim(),
        snippet: el.querySelector("td").textContent.trim(),
      };
    });
    const links = Array.from(document.querySelectorAll("#gs_citi a")).map((el) => {
      return {
        name: el.textContent.trim(),
        link: el.getAttribute("href"),
      };
    });
    return { citations, links };
  });
  return citeData;
}
```

|Code|Explanation|
|----|-----------|
|`.text()`|gets the raw text of html element|
|[`.trim()`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/trim)|removes whitespace from both ends of a string|
        
And finally, a function to control the browser, and get main information about the author:

```javascript
async function getScholarCitesInfo() {
  const browser = await puppeteer.launch({
    headless: false,
    args: ["--no-sandbox", "--disable-setuid-sandbox"],
  });

  const page = await browser.newPage();

  const URL = `${domain}/scholar?hl=${requestParams.hl}&q=${requestParams.q}`;

  await page.setDefaultNavigationTimeout(60000);
  await page.goto(URL);
  await page.waitForSelector(".gs_r.gs_scl");
  await page.waitForTimeout(1000);

  const citesId = await getCitesId(page);
  const allCites = [];

  for (id of citesId) {
    const URL = `${domain}/scholar?q=info:${id}:scholar.google.com/&output=cite&hl=${requestParams.hl}`;
    try {
      await page.goto(URL);
      await page.waitForTimeout(2000);
      allCites.push(await fillCiteData(page));
    } catch {
      console.log("Something was wrong with getting info from ID: ", id)
    }
  }

  await browser.close();

  return allCites;
}

getScholarCitesInfo().then((result) => console.dir(result, { depth: null }));
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
|`browser.close()`|after all we close the browser instance|
|`console.dir(result, { depth: null })`|console method `dir` allows you to use an object with the necessary parameters to change default output options. Watch [Node.js documentation](https://nodejs.org/api/console.html#consoledirobj-options) for more info|

Now we can launch our parser. To do this enter `node YOUR_FILE_NAME` in your command line. Where `YOUR_FILE_NAME` is the name of your `.js` file.

<h2 id='output'>Output</h2>

📌Note: if you see something like `[Object]` in your console you can use `console.dir(result, { depth: null })` instead `console.log()`. Watch [Node.js documentation](https://nodejs.org/api/console.html#consoledirobj-options) for more info.

```json
[
   {
      "citations":[
         {
            "title":"MLA",
            "snippet":"Feigelson, Eric D., and G. Jogesh Babu. Modern statistical methods for astronomy: with R applications. Cambridge University Press, 2012."
         },
         {
            "title":"APA",
            "snippet":"Feigelson, E. D., & Babu, G. J. (2012). Modern statistical methods for astronomy: with R applications. Cambridge University Press."
         },
         {
            "title":"Chicago",
            "snippet":"Feigelson, Eric D., and G. Jogesh Babu. Modern statistical methods for astronomy: with R applications. Cambridge University Press, 2012."
         },
         {
            "title":"Harvard",
            "snippet":"Feigelson, E.D. and Babu, G.J., 2012. Modern statistical methods for astronomy: with R applications. Cambridge University Press."
         },
         {
            "title":"Vancouver",
            "snippet":"Feigelson ED, Babu GJ. Modern statistical methods for astronomy: with R applications. Cambridge University Press; 2012 Jul 12."
         }
      ],
      "links":[
         {
            "name":"BibTeX",
            "link":"https://scholar.googleusercontent.com/scholar.bib?q=info:ec7TPNOf0BkJ:scholar.google.com/&output=citation&scisdr=CgXMI1ygEIvc-VD2gb4:AAGBfm0AAAAAYsbwmb9DmKveBMs7b13qmAh07Kz7E5wZ&scisig=AAGBfm0AAAAAYsbwmQ_qHPPtGUXxQKyT1ubTz2dZxkNs&scisf=4&ct=citation&cd=-1&hl=en"
         },
         {
            "name":"EndNote",
            "link":"https://scholar.googleusercontent.com/scholar.enw?q=info:ec7TPNOf0BkJ:scholar.google.com/&output=citation&scisdr=CgXMI1ygEIvc-VD2gb4:AAGBfm0AAAAAYsbwmb9DmKveBMs7b13qmAh07Kz7E5wZ&scisig=AAGBfm0AAAAAYsbwmQ_qHPPtGUXxQKyT1ubTz2dZxkNs&scisf=3&ct=citation&cd=-1&hl=en"
         },
         {
            "name":"RefMan",
            "link":"https://scholar.googleusercontent.com/scholar.ris?q=info:ec7TPNOf0BkJ:scholar.google.com/&output=citation&scisdr=CgXMI1ygEIvc-VD2gb4:AAGBfm0AAAAAYsbwmb9DmKveBMs7b13qmAh07Kz7E5wZ&scisig=AAGBfm0AAAAAYsbwmQ_qHPPtGUXxQKyT1ubTz2dZxkNs&scisf=2&ct=citation&cd=-1&hl=en"
         },
         {
            "name":"RefWorks",
            "link":"https://scholar.googleusercontent.com/scholar.rfw?q=info:ec7TPNOf0BkJ:scholar.google.com/&output=citation&scisdr=CgXMI1ygEIvc-VD2gb4:AAGBfm0AAAAAYsbwmb9DmKveBMs7b13qmAh07Kz7E5wZ&scisig=AAGBfm0AAAAAYsbwmQ_qHPPtGUXxQKyT1ubTz2dZxkNs&scisf=1&ct=citation&cd=-1&hl=en"
         }
      ]
   }
   ...and other results
]
```

<h2 id='serp_api'>Google Scholar Author API</h2>

Alternatively, you can use the [Google Scholar Cite API](https://serpapi.com/google-scholar-cite-api) from SerpApi. SerpApi is a free API with 100 searches per month. If you need more searches, there are paid plans.

The difference is that you won't have to write code from scratch and maintain it. You may also experience blocking from Google and changing selectors which will break the parser. Instead, you just need to iterate the structured JSON and get the data you want. [Check out the playground](https://serpapi.com/playground).

First, we need to install [`google-search-results-nodejs`](https://www.npmjs.com/package/google-search-results-nodejs). To do this you need to enter in your console: `npm i google-search-results-nodejs`

```javascript
const SerpApi = require("google-search-results-nodejs");
const search = new SerpApi.GoogleSearch(process.env.API_KEY); //your API key from serpapi.com

const searchString = "astronomy";                         // what we want to search
const pagesLimit = Infinity;                              // limit of pages for getting info
let currentPage = 1;                                      // current page of the search

const params = {
  engine: "google_scholar",                               // search engine
  q: searchString,                                        // search query
  hl: "en",                                               // Parameter defines the language to use for the Google search
};

const getJson = () => {
  return new Promise((resolve) => {
    search.json(params, resolve);
  });
};

const getResults = async () => {
  const allCites = [];
  const citesId = [];
  while (true) {
    if (currentPage > pagesLimit) break;
    const json = await getJson();
    json.organic_results.forEach((el) => {
      citesId.push(el.result_id);
    });
    if (json.pagination.next) {
      params.start ? (params.start = 10) : (params.start += 10);
    } else break;
    currentPage++;
  }
  delete params.hl;
  params.engine = "google_scholar_cite";
  for (id of citesId) {
    params.q = id;
    const { citations, links } = await getJson();
    allCites.push({ id, citations, links });
  }
  return allCites;
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
const searchString = "astronomy";
const pagesLimit = Infinity;
let currentPage = 1;

const params = {
  engine: "google_scholar",
  q: searchString,
  hl: "en",
};
```

|Code|Explanation|
|----|-----------|
|`searchString`|what we want to search|
|`pagesLimit`|limit of pages for getting info. If you want to limit the number of pages for getting info you need to define the last page number in this|
|`engine`|search engine|
|`q`|search query|
|`hl`|parameter defines the language to use for the Google Scholar search|

Next, we wrap the search method from the SerpApi library in a promise to further work with the search results:

```javascript
const getJson = () => {
  return new Promise((resolve) => {
    search.json(params, resolve);
  })
}
```

And finally, we declare and run the function `getResult` that gets all citations ID from all pages, gets all citations info and return it:

```javascript
const getResults = async () => {
  const allCites = [];
  const citesId = [];
  while (true) {
    if (currentPage > pagesLimit) break;
    const json = await getJson();
    json.organic_results.forEach((el) => {
      citesId.push(el.result_id);
    });
    if (json.pagination.next) {
      params.start ? (params.start = 10) : (params.start += 10);
    } else break;
    currentPage++;
  }
  delete params.hl;
  params.engine = "google_scholar_cite";
  for (id of citesId) {
    params.q = id;
    const { citations, links } = await getJson();
    allCites.push({ id, citations, links });
  }
  return allCites;
};

getResults().then((result) => console.dir(result, { depth: null }))
```

|Code|Explanation|
|----|-----------|
|`allCites`|an array with all citations info from all pages|
|`citesId`|an array with cite ID from all pages|
|`citations, links`|data that we destructured from the response|
|`console.dir(result, { depth: null })`|console method `dir` allows you to use an object with the necessary parameters to change default output options. Watch [Node.js documentation](https://nodejs.org/api/console.html#consoledirobj-options) for more info|

<h2 id='serp_api_output'>Output</h2>

```json
[
   {
      "id":"PkuLyccmJ74J",
      "citations":[
         {
            "title":"MLA",
            "snippet":"Zwicky, Fritz. Morphological astronomy. Springer Science & Business Media, 2012."
         },
         {
            "title":"APA",
            "snippet":"Zwicky, F. (2012). Morphological astronomy. Springer Science & Business Media."
         },
         {
            "title":"Chicago",
            "snippet":"Zwicky, Fritz. Morphological astronomy. Springer Science & Business Media, 2012."
         },
         {
            "title":"Harvard",
            "snippet":"Zwicky, F., 2012. Morphological astronomy. Springer Science & Business Media."
         },
         {
            "title":"Vancouver",
            "snippet":"Zwicky F. Morphological astronomy. Springer Science & Business Media; 2012 Dec 6."
         }
      ],
      "links":[
         {
            "name":"BibTeX",
            "link":"https://scholar.googleusercontent.com/scholar.bib?q=info:PkuLyccmJ74J:scholar.google.com/&output=citation&scisdr=CgU4uY14GAA:AAGBfm0AAAAAYsb-vkn1FCUdWV07MWHG9cBPQ2Vwxm1R&scisig=AAGBfm0AAAAAYsb-vjrBs9xBEzph-DPHmLXeLseRh7s5&scisf=4&ct=citation&cd=-1&hl=en"
         },
         {
            "name":"EndNote",
            "link":"https://scholar.googleusercontent.com/scholar.enw?q=info:PkuLyccmJ74J:scholar.google.com/&output=citation&scisdr=CgU4uY14GAA:AAGBfm0AAAAAYsb-vkn1FCUdWV07MWHG9cBPQ2Vwxm1R&scisig=AAGBfm0AAAAAYsb-vjrBs9xBEzph-DPHmLXeLseRh7s5&scisf=3&ct=citation&cd=-1&hl=en"
         },
         {
            "name":"RefMan",
            "link":"https://scholar.googleusercontent.com/scholar.ris?q=info:PkuLyccmJ74J:scholar.google.com/&output=citation&scisdr=CgU4uY14GAA:AAGBfm0AAAAAYsb-vkn1FCUdWV07MWHG9cBPQ2Vwxm1R&scisig=AAGBfm0AAAAAYsb-vjrBs9xBEzph-DPHmLXeLseRh7s5&scisf=2&ct=citation&cd=-1&hl=en"
         },
         {
            "name":"RefWorks",
            "link":"https://scholar.googleusercontent.com/scholar.rfw?q=info:PkuLyccmJ74J:scholar.google.com/&output=citation&scisdr=CgU4uY14GAA:AAGBfm0AAAAAYsb-vkn1FCUdWV07MWHG9cBPQ2Vwxm1R&scisig=AAGBfm0AAAAAYsb-vjrBs9xBEzph-DPHmLXeLseRh7s5&scisf=1&ct=citation&cd=-1&hl=en"
         }
      ]
   },
   ...and other results
]
```

<h2 id='links'>Links</h2>

* [Code in the online IDE](https://replit.com/@MikhailZub/Google-Scholar-Cite-NodeJS-SerpApi#index.js) 
* [Google Scholar Cite API](https://serpapi.com/google-scholar-cite-api)

If you want to see some projects made with SerpApi, please write me a message.

___
<p style="text-align: center;">Join us on <a href="https://twitter.com/serp_api">Twitter</a> | <a href="https://www.youtube.com/channel/UCUgIHlYBOD3yA3yDIRhg_mg">YouTube</a></p>
<p style="text-align: center;">Add a  <a href="https://github.com/serpapi/public-roadmap/issues">Feature Request</a>💫 or a <a href="https://github.com/serpapi/public-roadmap/issues">Bug</a>🐞</p>