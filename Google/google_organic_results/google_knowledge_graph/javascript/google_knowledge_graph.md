<h2 id='what'>What will be scraped</h2>

![what-3](https://serpapi.com/blog/content/images/2022/05/what-3.png)

<h2 id='preparation'>Preparation</h2>

First, we need to create a Node.js* project and add [`npm`](https://www.npmjs.com/) packages [`cheerio`](https://www.npmjs.com/package/cheerio) to parse parts of the HTML markup, and [`axios`](https://www.npmjs.com/package/axios) to make a request to a website. To do this, in the directory with our project, open the command line and enter `npm init -y`, and then `npm i cheerio axios`.

*<span style="font-size: 15px;">If you don't have Node.js installed, you can download it from [here](https://nodejs.org/en/) and follow the installation [documentation](https://nodejs.dev/learn/introduction-to-nodejs).</span>

<h2 id='process'>Process</h2>

[SelectorGadget Chrome extension](https://chrome.google.com/webstore/detail/selectorgadget/mhjhnkcfbdhnjickkkdbjoemdmbfginb) was used to grab CSS selectors by clicking on the desired element in the browser. If you have any struggles understanding this, we have a dedicated [Web Scraping with CSS Selectors blog post](https://serpapi.com/blog/web-scraping-with-css-selectors-using-python/) at SerpApi.
The Gif below illustrates the approach of selecting different parts of the results.

![how-2](https://serpapi.com/blog/content/images/2022/05/how-2.gif)

<h2 id='full_code'>Full code</h2>

```javascript
const cheerio = require("cheerio");
const axios = require("axios");

const searchString = "tesla";                                    // what we want to search
    const encodedString = encodeURI(searchString);              // what we want to search for in URI encoding

const domain = `http://google.com`;                             // google domain of the search

const AXIOS_OPTIONS = {
  headers: {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36",
  },                                                            // adding the User-Agent header as one way to prevent the request from being blocked
  params: {
    q: encodedString,                                           // our encoded search string
    hl: "en",                                                   // Parameter defines the language to use for the Google search
    gl: "us",                                                   // parameter defines the country to use for the Google search
  },
};

function getKnowledgeGraphInfo() {
  return axios.get(`${domain}/search`, AXIOS_OPTIONS).then(function ({ data }) {
    let $ = cheerio.load(data);

    const pattern = /s='(?<img>[^']+)';\w+\s\w+=\['(?<id>\w+_\d+)'];/gm;
    const images = [...data.matchAll(pattern)].map(({ groups }) => ({ id: groups.id, img: groups.img.replace(/\\x3d/gi, "") }));

    const allInfo = {
      title: $(".I6TXqe .qrShPb span").text().trim(),
      type: $(".I6TXqe .wwUB2c span").text().trim(),
      image: images.find(({ id }) => id === $(".I6TXqe .FZylgf img").attr("id"))?.img,
      website: $(".I6TXqe .B1uW2d").attr("href"),
      description: {
        text: $(".I6TXqe .hb8SAc span:nth-child(2)").text().trim(),
        source: $(".I6TXqe .hb8SAc span:nth-child(3) a").text().trim(),
        link: $(".I6TXqe .hb8SAc span:nth-child(3) a").attr("href"),
      },
      main: Array.from($(".I6TXqe .wDYxhc .Z1hOCe")).reduce((acc, el) => {
        const key = $(el).find(".w8qArf a").text().trim();
        return { ...acc, [key]: $(el).find(".kno-fv").text() };
      }, {}),
      profiles: Array.from($(".I6TXqe .OOijTb .fl")).reduce((acc, el) => {
        const key = $(el).find(".CtCigf").text().trim();
        return { ...acc, [key]: $(el).find("a").attr("href") };
      }, {}),
      peopleAlsoSearchFor: Array.from($(".I6TXqe .VLkRKc").closest(".UDZeY").find(".Wr0c6d")).reduce((acc, el) => {
        const key = $(el).text().trim();
        return { ...acc, [key]: domain + $(el).attr("href") };
      }, {}),
    };

    return allInfo;
  });
}

getKnowledgeGraphInfo().then(console.log);
```

<h3 id='code_explanation'>Code explanation</h3>

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
const searchString = "tesla";
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
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36",
  },
  params: {
    q: encodedString,
    hl: "en",
    gl: "us",
  },
};
```

|Code|Explanation|
|----|-----------|
|`headers`|[HTTP headers](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers) let the client and the server pass additional information with an HTTP request or response|
|[`User-Agent`](https://developer.mozilla.org/en-US/docs/Glossary/User_agent)|is used to act as a "real" user visit. Default axios requests user-agent is `axios/0.27.2` so websites understand that it's a script that sends a request and might block it. [Check what's your user-agent](https://www.whatismybrowser.com/detect/what-is-my-user-agent/).|
|`q`|encoded in URI search query|
|`hl`|parameter defines the language to use for the Google search|
|`gl`|parameter defines the country to use for the Google search|
        
And finally a function to get the necessary information:

```javascript
function getKnowledgeGraphInfo() {
  return axios.get(`${domain}/search`, AXIOS_OPTIONS).then(function ({ data }) {
    let $ = cheerio.load(data);

    const pattern = /s='(?<img>[^']+)';\w+\s\w+=\['(?<id>\w+_\d+)'];/gm;
    const images = [...data.matchAll(pattern)].map(({ groups }) => ({ id: groups.id, img: groups.img.replace(/\\x3d/gi, "") }));

    const allInfo = {
      title: $(".I6TXqe .qrShPb span").text().trim(),
      type: $(".I6TXqe .wwUB2c span").text().trim(),
      image: images.find(({ id }) => id === $(".I6TXqe .FZylgf img")?.attr("id")).img,
      website: $(".I6TXqe .B1uW2d").attr("href"),
      description: {
        text: $(".I6TXqe .hb8SAc span:nth-child(2)").text().trim(),
        source: $(".I6TXqe .hb8SAc span:nth-child(3) a").text().trim(),
        link: $(".I6TXqe .hb8SAc span:nth-child(3) a").attr("href"),
      },
      main: Array.from($(".I6TXqe .wDYxhc .Z1hOCe")).reduce((acc, el) => {
        const key = $(el).find(".w8qArf a").text().trim();
        return { ...acc, [key]: $(el).find(".kno-fv").text() };
      }, {}),
      profiles: Array.from($(".I6TXqe .OOijTb .fl")).reduce((acc, el) => {
        const key = $(el).find(".CtCigf").text().trim();
        return { ...acc, [key]: $(el).find("a").attr("href") };
      }, {}),
      peopleAlsoSearchFor: Array.from($(".I6TXqe .VLkRKc").closest(".UDZeY").find(".Wr0c6d")).reduce((acc, el) => {
        const key = $(el).text().trim();
        return { ...acc, [key]: domain + $(el).attr("href") };
      }, {}),
    };

    return allInfo;
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
|`allInfo`|an object with full info from page|
|`{ id }`|`id` that we destructured from images array element to compare it with `id` attribute from html element|
|`.attr('href')`|gets the `href` attribute value of the html element|
|`$(el).find('.kno-fv')`|finds element with class name `kno-fv` in all child elements and their children of `el` html element|
|`$(".I6TXqe .VLkRKc").closest(".UDZeY")`|finds the nearest parent element with class name `UDZeY` in elements with class name `I6TXqe` that have elements with class names `VLkRKc`|
|`.text()`|gets the raw text of html element|
|[`.trim()`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/trim)|removes whitespace from both ends of a string|
|`{...acc, [key]: $(el).find(".kno-fv").text()}`|in this code we use [spread syntax](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Spread_syntax) to create an object from result that was returned from previous reduce call and add to this object new item with key `key` and the value from html element|

Now we can launch our parser. To do this enter `node YOUR_FILE_NAME` in your command line. Where `YOUR_FILE_NAME` is the name of your `.js` file.

<h2 id='output'>Output</h2>

```json
{
  "title": "Tesla, Inc.",
  "type": "Automotive company",
  "image": "data:image/png;base64,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",
  "website": "http://www.tesla.com/",
  "description": {
    "text": "Tesla, Inc. is an American automotive and clean energy company based in Austin, Texas. Tesla designs and manufactures electric vehicles, battery energy storage from home to grid-scale, solar panels and solar roof tiles, and related products and services.",
    "source": "Wikipedia",
    "link": "https://en.wikipedia.org/wiki/Tesla,_Inc."
  },
  "main": {
    "Customer service chat": "Online Chat",
    "Stock price": "TSLA (NASDAQ) $663.90 -45.52 (-6.42%)May 20, 4:00 PM EDT - Disclaimer",
    "Customer service": "1 (888) 518-3752",
    "Sales": "1 (650) 681-5100",
    "Founded": "July 1, 2003, San Carlos, CA",
    "Headquarters": "Austin, TX",
    "Founders": "Elon Musk, Martin Eberhard, JB Straubel, Marc Tarpenning, Ian Wright"
  },
  "profiles": {
    "Twitter": "https://twitter.com/Tesla",
    "Instagram": "https://www.instagram.com/teslamotors",
    "LinkedIn": "https://www.linkedin.com/company/tesla-motors",
    "YouTube": "https://www.youtube.com/user/TeslaMotors",
    "Facebook": "https://www.facebook.com/electriceverywhere/"
  },
  "peopleAlsoSearchFor": {
    "Rivian": "http://google.com/search?hl=en&gl=us&q=Rivian&si=AC1wQDBgv4q3A2ojf086TvVgL6tTfKEZW2vrlR3V2uQ-r4wcbsReC3ET6H2gzOSJ83emah_DqBM87DBklcE_mqoTL6cnz4FB1PMxbYfHDHyZdLCyx8zARIwys088KWe7WiklQlXZK_a7dUf-yHR9rfskLPg5guGpehAFTM3fd3hWpBPW5dczKTfsYPqr14le6A9ntskIhEz3TcTFs-NfV-pYomsgg4TqTCwEZ2q78gSuQ2k7lCmM2RK7N6D_QrOJII8refqi1sQCnF5fSz2dpVnhex28ek6DZBQAIBWnfpqfBT0TR8mmzQY%3D&sa=X&ved=2ahUKEwi24_rLyfX3AhVVK80KHf-fDDoQxA16BAhiEAU",
    "Porsche": "http://google.com/search?hl=en&gl=us&q=Porsche&si=AC1wQDCwN61-ebmuwbQCO5QCrgOvEq5bkWeIzJ5JczItzAKNdRDXvnuw4L4VhlFx9HJV6OqmqtHAqzPbjVJQTwLot5VNg5xzaaCA4jSgbzJaVgihv2J3-LIDNlX1WqL91VSm_FeZk82jX-bHWYKn10Fi0s1BJzHTawI0qAtv96gwjDkx7V_htiR2kxFVzA7AQ4cQCw3CJ6Ip1UkJtRCk5CfuKq3PhLki8BfCXnAWXVPJ7q8ySkdC74wGOae908caHajpT8We8-UmIUtPdHFJCOecopicrNqwbDKyCtQFvP-2Q5CY5uyu2DA%3D&sa=X&ved=2ahUKEwi24_rLyfX3AhVVK80KHf-fDDoQxA16BAhiEAc",
    "NIO": "http://google.com/search?hl=en&gl=us&q=NIO&si=AC1wQDAXKblb4YtxZaDquKpQ5Js55CVph8NS1FIwBhgs6qyyHkehlU67aH1NSQuNhCW8DVAYZPw0DpddMm6wTKTN_Bvaze-B5FZFuI7smOYC3exZRBqB1hk0qKg9Kiv1fQ59L8TBbBAU8OOK0XFI4nAnmzy7G1NxHWMC_rq2hInqckB6GzyuGbsYEFixmX3yYpjCk9nUgVi_bvFQ-uWAdGaEZEaX-TpmPVtqjgcckC13fXyJMz-b8twpo4MntcWGbO06ceNB2YD9IvnaliU-XIfwHtOZc2pEhvax5L1V4cNA2sXlCyiTCx0%3D&sa=X&ved=2ahUKEwi24_rLyfX3AhVVK80KHf-fDDoQxA16BAhiEAk",
    "Sunrun": "http://google.com/search?hl=en&gl=us&q=Sunrun&si=AC1wQDBgv4q3A2ojf086TvVgL6tTfKEZW2vrlR3V2uQ-r4wcbmSu5nhquKqWlG2lGADH9r4kgGmXn4Lx085H40Gw8Qkq5MAMrE_2zOdeGSFnxbNwaYps0-scCzFFuAgxHXGMOmaKcxEYHFbpyU29GQaUYPgTlYfFkN9MHAcmUOFQVoDAAuPOSgbHN3qoHZP7jZiqoHw74zfkgeYScjelV-aWW1jx8mBj4pStMhjKSwEoLlri5O63Di9LXMX9LIAasThnFWea1p-jMKTqh4GUWrQXSjXOMFRGAgS_uBO7Fkfe0-vXKOx77A0%3D&sa=X&ved=2ahUKEwi24_rLyfX3AhVVK80KHf-fDDoQxA16BAhiEAs"
  }
}
```

<h2 id='serp_api'>Google Knowledge Graph API</h2>

Alternatively, you can use the [Google Knowledge Graph API](https://serpapi.com/knowledge-graph) from SerpApi. SerpApi is a free API with 100 search per month. If you need more searches, there are paid plans.

The difference is that all that needs to be done is just to iterate over a ready made, structured JSON instead of coding everything from scratch, maintaining, figuring out how to bypass blocks from Google, and selecting correct selectors which could be time consuming at times. [Check out the playground](https://serpapi.com/playground).

First we need to install [`google-search-results-nodejs`](https://www.npmjs.com/package/google-search-results-nodejs). To do this you need to enter in your console: `npm i google-search-results-nodejs`

```javascript
const SerpApi = require("google-search-results-nodejs");
const search = new SerpApi.GoogleSearch(process.env.API_KEY);

const searchString = "tesla";                           // what we want to search

const params = {
  engine: "google",                                     // search engine
  q: searchString,                                      // search query
  google_domain: "google.com",                          // google domain of the search
  gl: "us",                                             // parameter defines the country to use for the Google search
  hl: "en",                                             // Parameter defines the language to use for the Google search
};

const getKnowledgeGraph = function ({ knowledge_graph }) {
  const allInfo = {
    title: '',
    type: '',
    image: '',
    website: '',
    description: {},
    main: {},
    profiles: {},
    peopleAlsoSearchFor: {}
  } 
    for (const key in knowledge_graph) {
        if (key.includes('_link') || key.includes('_stick') || key === "see_results_about") {
        } else if (key === 'title') {
          allInfo.title = knowledge_graph[key]
        } else if (key === 'type') {
          allInfo.type = knowledge_graph[key]
        } else if (key === 'image') {
          allInfo.image = knowledge_graph[key]
        } else if (key === 'website') {
          allInfo.website = knowledge_graph[key]
        } else if (key === 'description') {
          allInfo.description.text = knowledge_graph[key];
        } else if (key === 'source') {
          allInfo.description.source = knowledge_graph[key].name;
          allInfo.description.link = knowledge_graph[key].link;
        } else if (key === 'profiles') {
          allInfo.profiles = knowledge_graph[key].reduce((acc, el) => {
            return { ...acc, [el.name]: el.link };
          }, {});
        } else if (key === 'people_also_search_for') {
          allInfo.peopleAlsoSearchFor = knowledge_graph[key].reduce((acc, el) => {
            return { ...acc, [el.name]: el.link };
          }, {});
        } else {
          allInfo.main = {...allInfo.main, [key]: knowledge_graph[key]}
    }
  }
  return allInfo
};

const getJson = (params) => {
  return new Promise((resolve) => {
    search.json(params, resolve);
  })
}

getJson(params).then(getKnowledgeGraph).then(console.log)
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
const searchString = "tesla";

const params = {
  engine: "google",
  q: searchString,
  google_domain: "google.com",
  gl: "us",
  hl: "en",
};
```

|Code|Explanation|
|----|-----------|
|`searchString`|what we want to search|
|`engine`|search engine|
|`q`|search query|
|`google_domain`|google domain: google.com, google.de, google.fr|
|`gl`|parameter defines the country to use for the Google search|
|`hl`|parameter defines the language to use for the Google search|

Next, we write a callback function in which we describe what data we need from the result of our request:

```javascript
const getKnowledgeGraph = function ({ knowledge_graph }) {
  const allInfo = {
    title: '',
    type: '',
    image: '',
    website: '',
    description: {},
    main: {},
    profiles: {},
    peopleAlsoSearchFor: {}
  } 
    for (const key in knowledge_graph) {
        if (key.includes('_link') || key.includes('_stick') || key === "see_results_about") {
        } else if (key === 'title') {
          allInfo.title = knowledge_graph[key]
        } else if (key === 'type') {
          allInfo.type = knowledge_graph[key]
        } else if (key === 'image') {
          allInfo.image = knowledge_graph[key]
        } else if (key === 'website') {
          allInfo.website = knowledge_graph[key]
        } else if (key === 'description') {
          allInfo.description.text = knowledge_graph[key];
        } else if (key === 'source') {
          allInfo.description.source = knowledge_graph[key].name;
          allInfo.description.link = knowledge_graph[key].link;
        } else if (key === 'profiles') {
          allInfo.profiles = knowledge_graph[key].reduce((acc, el) => {
            return { ...acc, [el.name]: el.link };
          }, {});
        } else if (key === 'people_also_search_for') {
          allInfo.peopleAlsoSearchFor = knowledge_graph[key].reduce((acc, el) => {
            return { ...acc, [el.name]: el.link };
          }, {});
        } else {
          allInfo.main = {...allInfo.main, [key]: knowledge_graph[key]}
    }
  }
  return allInfo
};
```

|Code|Explanation|
|----|-----------|
|`knowledge_graph`|an array that we destructured from response|
|`{...acc, [el.name]: el.link}`|in this code we use [spread syntax](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Spread_syntax) to create an object from result that was returned from previous reduce call and add to this object new item with key `el.name` and value `el.link`|

Next, we wrap the search method from the SerpApi library in a promise to further work with the search results and run it:

```javascript
const getJson = (params) => {
  return new Promise((resolve) => {
    search.json(params, resolve);
  })
}

getJson(params).then(getKnowledgeGraph).then(console.log)
```

<h2 id='serp_api_output'>Output</h2>

```json
{
  "title": "Tesla, Inc.",
  "type": "Automotive company",
  "image": "https://serpapi.com/searches/628b8735c9de453fe70b510f/images/1a7dfb07b83eed4f02ee96a98be925e974d4df171887903d.png",
  "website": "http://www.tesla.com/",
  "description": {
    "text": "Tesla, Inc. is an American automotive and clean energy company based in Austin, Texas. Tesla designs and manufactures electric vehicles, battery energy storage from home to grid-scale, solar panels and solar roof tiles, and related products and services.",
    "source": "Wikipedia",
    "link": "https://en.wikipedia.org/wiki/Tesla,_Inc."
  },
  "main": {
    "customer_service_chat": "Online Chat",
    "stock_price": "TSLA (NASDAQ) $663.90 0.00 (0.00%)May 20, 4 - 00 PM EDT - Disclaimer",
    "customer_service": "1 (888) 518-3752",
    "sales": "1 (650) 681-5100",
    "founded": "July 1, 2003, San Carlos, CA",
    "headquarters": "Austin, TX",
    "founders": "Elon Musk, Martin Eberhard, JB Straubel, Marc Tarpenning, Ian Wright",
    "latest_models": [
      {
        "name": "2022 Tesla Model 3",
        "link": "https://www.google.com/search?gl=us&hl=en&q=2022+Tesla+Model+3&stick=H4sIAAAAAAAAAONgFuLUz9U3SCmyNEhR4tVP1zc0LEoxyzUwLqvQEnbOzy1IzKsMyffNT0nNiUxNLCpexCpkZGBkpBCSWpyTqAAWVzDewcoIAL7IDD1JAAAA&sa=X&ved=2ahUKEwjSlIW_2PX3AhVIgnIEHZbWC48QxA16BAhbEAQ",
        "serpapi_link": "https://serpapi.com/search.json?device=desktop&engine=google&gl=us&google_domain=google.com&hl=en&q=2022+Tesla+Model+3&stick=H4sIAAAAAAAAAONgFuLUz9U3SCmyNEhR4tVP1zc0LEoxyzUwLqvQEnbOzy1IzKsMyffNT0nNiUxNLCpexCpkZGBkpBCSWpyTqAAWVzDewcoIAL7IDD1JAAAA",
        "image": "https://serpapi.com/searches/628b8735c9de453fe70b510f/images/1a7dfb07b83eed4f02ee96a98be925e99c59f5f2d71c9ea5561e55bdf61e24cadcb4829328a89a90.jpeg"
      },
      {
        "name": "2022 Tesla Model Y",
        "link": "https://www.google.com/search?gl=us&hl=en&q=2022+Tesla+Model+Y&stick=H4sIAAAAAAAAAONgFuLUz9U3SCmyNEhR4tVP1zc0LEqxrCgptCzWEnbOzy1IzKsMyffNT0nNiUxNLCpexCpkZGBkpBCSWpyTqAAWV4jcwcoIAPfknH5JAAAA&sa=X&ved=2ahUKEwjSlIW_2PX3AhVIgnIEHZbWC48QxA16BAhbEAY",
        "serpapi_link": "https://serpapi.com/search.json?device=desktop&engine=google&gl=us&google_domain=google.com&hl=en&q=2022+Tesla+Model+Y&stick=H4sIAAAAAAAAAONgFuLUz9U3SCmyNEhR4tVP1zc0LEqxrCgptCzWEnbOzy1IzKsMyffNT0nNiUxNLCpexCpkZGBkpBCSWpyTqAAWV4jcwcoIAPfknH5JAAAA",
        "image": "https://serpapi.com/searches/628b8735c9de453fe70b510f/images/1a7dfb07b83eed4f02ee96a98be925e99c59f5f2d71c9ea50307ca9e270b1cba5b983d776f28ce53.jpeg"
      },
      {
        "name": "2022 Tesla Model S",
        "link": "https://www.google.com/search?gl=us&hl=en&q=2022+Tesla+Model+S&stick=H4sIAAAAAAAAAONgFuLUz9U3SCmyNEhR4tVP1zc0LIovN0sqLE_XEnbOzy1IzKsMyffNT0nNiUxNLCpexCpkZGBkpBCSWpyTqAAWVwjewcoIANpU_c1JAAAA&sa=X&ved=2ahUKEwjSlIW_2PX3AhVIgnIEHZbWC48QxA16BAhbEAg",
        "serpapi_link": "https://serpapi.com/search.json?device=desktop&engine=google&gl=us&google_domain=google.com&hl=en&q=2022+Tesla+Model+S&stick=H4sIAAAAAAAAAONgFuLUz9U3SCmyNEhR4tVP1zc0LIovN0sqLE_XEnbOzy1IzKsMyffNT0nNiUxNLCpexCpkZGBkpBCSWpyTqAAWVwjewcoIANpU_c1JAAAA",
        "image": "https://serpapi.com/searches/628b8735c9de453fe70b510f/images/1a7dfb07b83eed4f02ee96a98be925e99c59f5f2d71c9ea5c9f47ee764fde2f1e79caf855134005d.jpeg"
      },
      {
        "name": "2022 Tesla Model X",
        "link": "https://www.google.com/search?gl=us&hl=en&q=2022+Tesla+Model+X&stick=H4sIAAAAAAAAAONgFuLUz9U3SCmyNEhR4tVP1zc0LEqxKDMtN0_SEnbOzy1IzKsMyffNT0nNiUxNLCpexCpkZGBkpBCSWpyTqAAWV4jYwcoIAFWdvepJAAAA&sa=X&ved=2ahUKEwjSlIW_2PX3AhVIgnIEHZbWC48QxA16BAhbEAo",
        "serpapi_link": "https://serpapi.com/search.json?device=desktop&engine=google&gl=us&google_domain=google.com&hl=en&q=2022+Tesla+Model+X&stick=H4sIAAAAAAAAAONgFuLUz9U3SCmyNEhR4tVP1zc0LEqxKDMtN0_SEnbOzy1IzKsMyffNT0nNiUxNLCpexCpkZGBkpBCSWpyTqAAWV4jYwcoIAFWdvepJAAAA",
        "image": "https://serpapi.com/searches/628b8735c9de453fe70b510f/images/1a7dfb07b83eed4f02ee96a98be925e99c59f5f2d71c9ea5f246cc054e2a0060fbff0bd16f3567fb.jpeg"
      }
    ]
  },
  "profiles": {
    "Twitter": "https://twitter.com/Tesla",
    "LinkedIn": "https://www.linkedin.com/company/tesla-motors",
    "Instagram": "https://www.instagram.com/teslamotors",
    "YouTube": "https://www.youtube.com/user/TeslaMotors",
    "Facebook": "https://www.facebook.com/electriceverywhere/"
  },
  "peopleAlsoSearchFor": {
    "Rivian": "https://www.google.com/search?gl=us&hl=en&q=Rivian&si=AC1wQDBgv4q3A2ojf086TvVgL6tTfKEZW2vrlR3V2uQ-r4wcbsReC3ET6H2gzOSJ83emah_DqBM87DBklcE_mqoTL6cnz4FB1PMxbYfHDHyZdLCyx8zARIwys088KWe7WiklQlXZK_a7dUf-yHR9rfskLPg5guGpehAFTM3fd3hWpBPW5dczKTfsYPqr14le6A9ntskIhEz3TcTFs-NfV-pYomsgg4TqTCwEZ2q78gSuQ2k7lCmM2RK7N6D_QrOJII8refqi1sQCnF5fSz2dpVnhex28ek6DZBQAIBWnfpqfBT0TR8mmzQY%3D&sa=X&ved=2ahUKEwjSlIW_2PX3AhVIgnIEHZbWC48QxA16BAhcEAU",
    "Porsche": "https://www.google.com/search?gl=us&hl=en&q=Porsche&si=AC1wQDCwN61-ebmuwbQCO5QCrgOvEq5bkWeIzJ5JczItzAKNdRDXvnuw4L4VhlFx9HJV6OqmqtHAqzPbjVJQTwLot5VNg5xzaaCA4jSgbzJaVgihv2J3-LIDNlX1WqL91VSm_FeZk82jX-bHWYKn10Fi0s1BJzHTawI0qAtv96gwjDkx7V_htiR2kxFVzA7AQ4cQCw3CJ6Ip1UkJtRCk5CfuKq3PhLki8BfCXnAWXVPJ7q8ySkdC74wGOae908caHajpT8We8-UmIUtPdHFJCOecopicrNqwbDKyCtQFvP-2Q5CY5uyu2DA%3D&sa=X&ved=2ahUKEwjSlIW_2PX3AhVIgnIEHZbWC48QxA16BAhcEAc",
    "NIO": "https://www.google.com/search?gl=us&hl=en&q=NIO&si=AC1wQDAXKblb4YtxZaDquKpQ5Js55CVph8NS1FIwBhgs6qyyHkehlU67aH1NSQuNhCW8DVAYZPw0DpddMm6wTKTN_Bvaze-B5FZFuI7smOYC3exZRBqB1hk0qKg9Kiv1fQ59L8TBbBAU8OOK0XFI4nAnmzy7G1NxHWMC_rq2hInqckB6GzyuGbsYEFixmX3yYpjCk9nUgVi_bvFQ-uWAdGaEZEaX-TpmPVtqjgcckC13fXyJMz-b8twpo4MntcWGbO06ceNB2YD9IvnaliU-XIfwHtOZc2pEhvax5L1V4cNA2sXlCyiTCx0%3D&sa=X&ved=2ahUKEwjSlIW_2PX3AhVIgnIEHZbWC48QxA16BAhcEAk",
    "Sunrun": "https://www.google.com/search?gl=us&hl=en&q=Sunrun&si=AC1wQDBgv4q3A2ojf086TvVgL6tTfKEZW2vrlR3V2uQ-r4wcbmSu5nhquKqWlG2lGADH9r4kgGmXn4Lx085H40Gw8Qkq5MAMrE_2zOdeGSFnxbNwaYps0-scCzFFuAgxHXGMOmaKcxEYHFbpyU29GQaUYPgTlYfFkN9MHAcmUOFQVoDAAuPOSgbHN3qoHZP7jZiqoHw74zfkgeYScjelV-aWW1jx8mBj4pStMhjKSwEoLlri5O63Di9LXMX9LIAasThnFWea1p-jMKTqh4GUWrQXSjXOMFRGAgS_uBO7Fkfe0-vXKOx77A0%3D&sa=X&ved=2ahUKEwjSlIW_2PX3AhVIgnIEHZbWC48QxA16BAhcEAs"
  }
}
```

<h2 id='links'>Links</h2>

* [Code in the online IDE](https://replit.com/@MikhailZub/Google-Search-Knowledge-Graph-scrape-NodeJS-SerpApi#index.js) 
* [Google Knowledge Graph API](https://serpapi.com/knowledge-graph)

If you want to see some project made with SerpApi, please write me a message.

___
<p style="text-align: center;">Join us on <a href="https://twitter.com/serp_api">Twitter</a> | <a href="https://www.youtube.com/channel/UCUgIHlYBOD3yA3yDIRhg_mg">YouTube</a></p>
<p style="text-align: center;">Add a  <a href="https://github.com/serpapi/public-roadmap/issues">Feature Request</a>💫 or a <a href="https://github.com/serpapi/public-roadmap/issues">Bug</a>🐞</p>