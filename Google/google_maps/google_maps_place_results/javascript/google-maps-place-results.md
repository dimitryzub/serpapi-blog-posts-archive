<h2 id='what'>What will be scraped</h2>

![image](https://user-images.githubusercontent.com/64033139/179211329-c59b7cd3-c94a-42ef-93a2-245d8f44227d.png)

<h2 id='preparation'>Preparation</h2>

First, we need to create a Node.js* project and add [`npm`](https://www.npmjs.com/) packages [`puppeteer`](https://www.npmjs.com/package/puppeteer), [`puppeteer-extra`](https://www.npmjs.com/package/puppeteer-extra) and [`puppeteer-extra-plugin-stealth`](https://www.npmjs.com/package/puppeteer-extra-plugin-stealth) to control Chromium (or Chrome, or Firefox, but now we work only with Chromium which is used by default) over the [DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/) in [headless](https://developers.google.com/web/updates/2017/04/headless-chrome) or non-headless mode. 

To do this, in the directory with our project, open the command line and enter `npm init -y`, and then `npm i puppeteer puppeteer-extra puppeteer-extra-plugin-stealth`.

*<span style="font-size: 15px;">If you don't have Node.js installed, you can [download it from nodejs.org](https://nodejs.org/en/) and follow the installation [documentation](https://nodejs.dev/learn/introduction-to-nodejs).</span>

📌Note: also, you can use `puppeteer` without any extensions, but I strongly recommended use it with `puppeteer-extra` with `puppeteer-extra-plugin-stealth` to prevent website detection that you are using headless Chromium or that you are using [web driver](https://www.w3.org/TR/webdriver/). You can check it on [Chrome headless tests website](https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html). The screenshot below shows you a difference.

![stealth](https://user-images.githubusercontent.com/64033139/173014238-eb8450d7-616c-42ae-8b2f-24eeb5fd5916.png)

<h2 id='process'>Process</h2>

[SelectorGadget Chrome extension](https://chrome.google.com/webstore/detail/selectorgadget/mhjhnkcfbdhnjickkkdbjoemdmbfginb) was used to grab CSS selectors by clicking on the desired element in the browser. If you have any struggles understanding this, we have a dedicated [Web Scraping with CSS Selectors blog post](https://serpapi.com/blog/web-scraping-with-css-selectors-using-python/) at SerpApi.

The Gif below illustrates the approach of selecting different parts of the results.

![how](https://user-images.githubusercontent.com/64033139/179208512-531434b2-254f-462f-96d4-849cce54f632.gif)

<h2 id='full_code'>Full code</h2>

📌Note: to get a place URL you may use the tutorial from my [Web Scraping Google Maps Places with Nodejs](https://serpapi.com/blog/web-scraping-google-maps-places-with-nodejs/#full_code) blog post.

```javascript
const puppeteer = require("puppeteer-extra");
const StealthPlugin = require("puppeteer-extra-plugin-stealth");

puppeteer.use(StealthPlugin());

const placeUrl =
  "https://www.google.com/maps/place/Starbucks/data=!4m7!3m6!1s0x549069a98254bd17:0xb2f64f75b3edf4c3!8m2!3d47.5319688!4d-122.1942498!16s%2Fg%2F1tdfmzpb!19sChIJF71UgqlpkFQRw_Tts3VP9rI?authuser=0&hl=en&rclk=1";

async function fillPlaceInfo(page) {
  const dataFromPage = await page.evaluate(() => {
    return {
      title: document.querySelector(".DUwDvf").textContent.trim(),
      rating: document.querySelector("div.F7nice").textContent.trim(),
      reviews: document.querySelector("span.F7nice").textContent.trim().split(" ")[0],
      price: document.querySelector(".mgr77e > span:last-child > span:nth-child(2)").textContent.trim(),
      type: document.querySelector(".skqShb > div:nth-child(2)")?.textContent.replaceAll("·", "").trim(),
      description: document.querySelector(".PYvSYb")?.textContent.replaceAll("·", "").trim(),
      serviceOptions: document.querySelector(".E0DTEd")?.textContent.replaceAll("·", "").trim(),
      address: document.querySelector("button[data-item-id='address']")?.textContent.trim(), // data-item-id attribute may be different if the language is not English
      hours: Array.from(document.querySelectorAll(".OqCZI tr")).map((el) => {
        return {
          [el.querySelector("td:first-child")?.textContent.trim()]: el.querySelector("td:nth-child(2)")?.getAttribute("aria-label"),
        };
      }),
      menuLink: document.querySelector("a.CsEnBe[aria-label='Menu']")?.getAttribute["href"], // aria-label attribute may be different if the language is not English
      website: document.querySelector("a.CsEnBe[data-tooltip='Open website']")?.getAttribute("href"), // data-tooltip attribute may be different if the language is not English
      phone: document.querySelector(".RcCsl > button[data-tooltip='Copy phone number']")?.textContent.trim(), // data-tooltip attribute may be different if the language is not English
      plusCode: document.querySelector(".RcCsl > button[data-tooltip='Copy plus code']")?.textContent.trim(), // data-tooltip attribute may be different if the language is not English
      popularTimes: {
        graphResults: Array.from(document.querySelectorAll(".C7xf8b > div")).reduce((acc, el, i) => {
          let day;
          switch (i) {
            case 0:
              day = "sunday";
              break;
            case 1:
              day = "monday";
              break;
            case 2:
              day = "tuesday";
              break;
            case 3:
              day = "wednesday";
              break;
            case 4:
              day = "thursday";
              break;
            case 5:
              day = "friday";
              break;
            case 6:
              day = "saturday";
              break;
          }
          return {
            ...acc,
            [day]: Array.from(el.querySelectorAll(`:nth-child(${i + 1}) [aria-label]`)).map((el) => {
              const timeString = el.getAttribute("aria-label");
              const timeStart = timeString.indexOf("at");
              const scoreEnd = timeString.indexOf("%");
              const time = timeString.slice(timeStart + 3, -1);
              const busynessScore = timeString.slice(0, scoreEnd + 1);
              return {
                time,
                busynessScore,
              };
            }),
          };
        }, {}),
        liveHash: document.querySelector(".UgBNB")?.textContent.trim(),
      },
      images: Array.from(document.querySelectorAll(".KoY8Lc")).map((el) => {
        return {
          title: el.textContent?.trim(),
          thumbnail: el.parentElement.querySelector("img")?.getAttribute("src"),
        };
      }),
      userReviews: {
        summary: Array.from(document.querySelectorAll(".tBizfc")).map((el) => {
          return {
            snippet: el.querySelector(" .OXD3gb > div")?.textContent.replaceAll('"', "").trim(),
          };
        }),
        mostRelevant: Array.from(document.querySelectorAll(".jftiEf")).map((el) => {
          return {
            username: el.querySelector(".d4r55")?.textContent.trim(),
            rating: parseFloat(el.querySelector(".kvMYJc")?.getAttribute("aria-label")),
            description: el.querySelector(".MyEned")?.textContent.trim(),
            images: Array.from(el.querySelectorAll(".KtCyie button")).length
              ? Array.from(el.querySelectorAll(".KtCyie button")).map((el) => {
                  return {
                    thumbnail: getComputedStyle(el).backgroundImage.slice(5, -2),
                  };
                })
              : undefined,
            date: el.querySelector(".rsqaWe")?.textContent.trim(),
          };
        }),
      },
      peopleAlsoSearch: Array.from(document.querySelectorAll(".Ymd7jc")).map((el) => {
        return {
          title: el.querySelector(".GgK1If")?.textContent.trim(),
          rating: el.querySelector(".MW4etd")?.textContent.trim(),
          reviews: el.querySelector(".UY7F9")?.textContent.trim().slice(1, -1),
          type: el.querySelector("div.Q5g20")?.textContent.trim(),
          thumbnail: el.querySelector(".W7kqEc")?.getAttribute("src"),
        };
      }),
    };
  });
  return dataFromPage;
}

async function getLocalPlaceInfo() {
  const browser = await puppeteer.launch({
    headless: false,
    args: ["--no-sandbox", "--disable-setuid-sandbox"],
  });

  const page = await browser.newPage();

  await page.setDefaultNavigationTimeout(60000);
  await page.goto(placeUrl);
  await page.waitForNavigation();

  const placeInfo = await fillPlaceInfo(page);

  await page.click(".Dx2nRe");
  await page.waitForTimeout(2000);

  placeInfo.photosLink = page.url();

  const urlPattern = /!1s(?<id>[^!]+).+!3d(?<latitude>[^!]+)!4d(?<longitude>[^!]+)/gm; // https://regex101.com/r/KFE09c/1
  placeInfo.dataId = [...placeUrl.matchAll(urlPattern)].map(({ groups }) => groups.id)[0];
  const latitude = [...placeUrl.matchAll(urlPattern)].map(({ groups }) => groups.latitude)[0];
  const longitude = [...placeUrl.matchAll(urlPattern)].map(({ groups }) => groups.longitude)[0];
  placeInfo.gpsCoordinates = {
    latitude,
    longitude,
  };
  placeInfo.placeUrl = placeUrl;
  await browser.close();

  return placeInfo;
}

getLocalPlaceInfo().then((result) => console.dir(result, { depth: null }));
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

Next, we write down a function for getting place info from page:

```javascript
async function fillPlaceInfo(page) {
  const dataFromPage = await page.evaluate(() => {
    return {
      title: document.querySelector(".DUwDvf").textContent.trim(),
      rating: document.querySelector("div.F7nice").textContent.trim(),
      reviews: document.querySelector("span.F7nice").textContent.trim().split(" ")[0],
      price: document.querySelector(".mgr77e > span:last-child > span:nth-child(2)").textContent.trim(),
      type: document.querySelector(".skqShb > div:nth-child(2)")?.textContent.replaceAll("·", "").trim(),
      description: document.querySelector(".PYvSYb")?.textContent.replaceAll("·", "").trim(),
      serviceOptions: document.querySelector(".E0DTEd")?.textContent.replaceAll("·", "").trim(),
      address: document.querySelector("button[data-item-id='address']")?.textContent.trim(), // data-item-id attribute may be different if the language is not English
      hours: Array.from(document.querySelectorAll(".OqCZI tr")).map((el) => {
        return {
          [el.querySelector("td:first-child")?.textContent.trim()]: el.querySelector("td:nth-child(2)")?.getAttribute("aria-label"),
        };
      }),
      menuLink: document.querySelector("a.CsEnBe[aria-label='Menu']")?.getAttribute["href"], // aria-label attribute may be different if the language is not English
      website: document.querySelector("a.CsEnBe[data-tooltip='Open website']")?.getAttribute("href"), // data-tooltip attribute may be different if the language is not English
      phone: document.querySelector(".RcCsl > button[data-tooltip='Copy phone number']")?.textContent.trim(), // data-tooltip attribute may be different if the language is not English
      plusCode: document.querySelector(".RcCsl > button[data-tooltip='Copy plus code']")?.textContent.trim(), // data-tooltip attribute may be different if the language is not English
      popularTimes: {
        graphResults: Array.from(document.querySelectorAll(".C7xf8b > div")).reduce((acc, el, i) => {
          let day;
          switch (i) {
            case 0:
              day = "sunday";
              break;
            case 1:
              day = "monday";
              break;
            case 2:
              day = "tuesday";
              break;
            case 3:
              day = "wednesday";
              break;
            case 4:
              day = "thursday";
              break;
            case 5:
              day = "friday";
              break;
            case 6:
              day = "saturday";
              break;
          }
          return {
            ...acc,
            [day]: Array.from(el.querySelectorAll(`:nth-child(${i + 1}) [aria-label]`)).map((el) => {
              const timeString = el.getAttribute("aria-label");
              const timeStart = timeString.indexOf("at");
              const scoreEnd = timeString.indexOf("%");
              const time = timeString.slice(timeStart + 3, -1);
              const busynessScore = timeString.slice(0, scoreEnd + 1);
              return {
                time,
                busynessScore,
              };
            }),
          };
        }, {}),
        liveHash: document.querySelector(".UgBNB")?.textContent.trim(),
      },
      images: Array.from(document.querySelectorAll(".KoY8Lc")).map((el) => {
        return {
          title: el.textContent?.trim(),
          thumbnail: el.parentElement.querySelector("img")?.getAttribute("src"),
        };
      }),
      userReviews: {
        summary: Array.from(document.querySelectorAll(".tBizfc")).map((el) => {
          return {
            snippet: el.querySelector(" .OXD3gb > div")?.textContent.replaceAll('"', "").trim(),
          };
        }),
        mostRelevant: Array.from(document.querySelectorAll(".jftiEf")).map((el) => {
          return {
            username: el.querySelector(".d4r55")?.textContent.trim(),
            rating: parseFloat(el.querySelector(".kvMYJc")?.getAttribute("aria-label")),
            description: el.querySelector(".MyEned")?.textContent.trim(),
            images: Array.from(el.querySelectorAll(".KtCyie button")).length
              ? Array.from(el.querySelectorAll(".KtCyie button")).map((el) => {
                  return {
                    thumbnail: getComputedStyle(el).backgroundImage.slice(5, -2),
                  };
                })
              : undefined,
            date: el.querySelector(".rsqaWe")?.textContent.trim(),
          };
        }),
      },
      peopleAlsoSearch: Array.from(document.querySelectorAll(".Ymd7jc")).map((el) => {
        return {
          title: el.querySelector(".GgK1If")?.textContent.trim(),
          rating: el.querySelector(".MW4etd")?.textContent.trim(),
          reviews: el.querySelector(".UY7F9")?.textContent.trim().slice(1, -1),
          type: el.querySelector("div.Q5g20")?.textContent.trim(),
          thumbnail: el.querySelector(".W7kqEc")?.getAttribute("src"),
        };
      }),
    };
  });
  return dataFromPage;
}
```

|Code|Explanation|
|----|-----------|
|`page.evaluate('document.querySelector...`|runs code from the brackets in the browser console and returns the result|
|[`document.querySelector(".DUwDvf")`](https://developer.mozilla.org/en-US/docs/Web/API/Document/querySelector)|returns the first html element with selector `.DUwDvf` which is any child of the `document` html element|
|[`document.querySelectorAll(".KoY8Lc")`](https://developer.mozilla.org/en-US/docs/Web/API/Document/querySelectorAll)|returns a static [NodeList](https://developer.mozilla.org/en-US/docs/Web/API/NodeList) representing a list of the document's elements that match the css selectors with class name `KoY8Lc`|
|`.getAttribute("href")`|gets the `href` attribute value of the html element|
|`.textContent`|gets the raw text of html element|
|[`.trim()`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/trim)|removes whitespace from both ends of a string|
|`...acc`|in this code, we use [spread syntax](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Spread_syntax) to split the object which is returned from the previous iteration of the `reduce` method into elements and add them to the new returned object|
        
And finally, a function to control the browser, and get information:

```javascript
async function getLocalPlaceInfo() {
  const browser = await puppeteer.launch({
    headless: false,
    args: ["--no-sandbox", "--disable-setuid-sandbox"],
  });

  const page = await browser.newPage();

  await page.setDefaultNavigationTimeout(60000);
  await page.goto(placeUrl);
  await page.waitForNavigation();

  const placeInfo = await fillPlaceInfo(page);

  await page.click(".Dx2nRe");
  await page.waitForTimeout(2000);

  placeInfo.photosLink = page.url();

  const urlPattern = /!1s(?<id>[^!]+).+!3d(?<latitude>[^!]+)!4d(?<longitude>[^!]+)/gm; // https://regex101.com/r/KFE09c/1
  placeInfo.dataId = [...placeUrl.matchAll(urlPattern)].map(({ groups }) => groups.id)[0];
  const latitude = [...placeUrl.matchAll(urlPattern)].map(({ groups }) => groups.latitude)[0];
  const longitude = [...placeUrl.matchAll(urlPattern)].map(({ groups }) => groups.longitude)[0];
  placeInfo.gpsCoordinates = {
    latitude,
    longitude,
  };
  placeInfo.placeUrl = placeUrl;
  await browser.close();

  return placeInfo;
}

getLocalPlaceInfo().then((result) => console.dir(result, { depth: null }));
```

|Code|Explanation|
|----|-----------|
|`puppeteer.launch({options})`|this method launches a new instance of the Chromium browser with current `options`|
|`headless`|defines which mode to use: [headless](https://developers.google.com/web/updates/2017/04/headless-chrome) (by default) or non-headless|
|`args`|an array with [arguments](https://peter.sh/experiments/chromium-command-line-switches/) which is used with Chromium|
|`["--no-sandbox", "--disable-setuid-sandbox"]`|these arguments we use to allow the launch of the browser process in the [online IDE](https://replit.com/@MikhailZub/Scrape-eBay-Organic-Results-with-NodeJS-SerpApi#main.sh)|
|`browser.newPage()`|this method launches a new page|
|`page.setDefaultNavigationTimeout(60000)`|changing default (30 sec) time for waiting for selectors to 60000 ms (1 min) for slow internet connection|
|`page.goto(placeUrl)`|navigation to `placeUrl` which is defined above|
|`page.click(".Dx2nRe")`|this method emulates mouse click on the html element with the `.Dx2nRe` selector|
|`page.waitForTimeout(2000)`|waiting 2000 ms before continue|
|`page.url()`|this method returns current URL address|
|`urlPattern`|a RegEx pattern for search and define id, latitude and longitude. [See what it allows you to find](https://regex101.com/r/KFE09c/1)|
|`[...placeUrl.matchAll(urlPattern)]`|in this code we use [spread syntax](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Spread_syntax) to create an array from an [iterator](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Iterators_and_Generators) that was returned from [matchAll method](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/matchAll) (in this case this entry is equal to `Array.from(placeUrl.matchAll(urlPattern))`)|
|`browser.close()`|after all we close the browser instance|
|`console.dir(result, { depth: null })`|console method `dir` allows you to use an object with the necessary parameters to change default output options. Watch [Node.js documentation](https://nodejs.org/api/console.html#consoledirobj-options) for more info|

Now we can launch our parser. To do this enter `node YOUR_FILE_NAME` in your command line. Where `YOUR_FILE_NAME` is the name of your `.js` file.

<h2 id='output'>Output</h2>

```json
{
   "placeInfo":{
      "title":"Starbucks",
      "rating":"4.1",
      "reviews":"380",
      "price":"$$",
      "type":"Coffee shop",
      "description":"Seattle-based coffeehouse chain known for its signature roasts, light bites and WiFi availability.",
      "serviceOptions":"Dine-in    Drive-through    Delivery",
      "address":"1785 NE 44th St, Renton, WA 98056, United States",
      "hours":[
         {
            "Monday":"4:30AM to 6:30PM"
         },
         {
            "Tuesday":"4:30AM to 6:30PM"
         },
         {
            "Wednesday":"4:30AM to 6:30PM"
         },
         {
            "Thursday":"4:30AM to 6:30PM"
         },
         {
            "Friday":"4:30AM to 6:30PM"
         },
         {
            "Saturday":"4:30AM to 6:30PM"
         },
         {
            "Sunday":"4:30AM to 6:30PM"
         }
      ],
      "website":"https://www.starbucks.com/store-locator/store/10581/",
      "phone":"+1 425-226-7007",
      "plusCode":"GRJ4+Q8 Renton, Washington, USA",
      "popularTimes":{
         "graphResults":{
            "sunday":[
               {
                  "time":"3 AM",
                  "busynessScore":"0%"
               },
               {
                  "time":"4 AM",
                  "busynessScore":"4%"
               },
               {
                  "time":"5 AM",
                  "busynessScore":"12%"
               },
               {
                  "time":"6 AM",
                  "busynessScore":"26%"
               },
               {
                  "time":"7 AM",
                  "busynessScore":"47%"
               },
               {
                  "time":"8 AM",
                  "busynessScore":"68%"
               },
               {
                  "time":"9 AM",
                  "busynessScore":"83%"
               },
               {
                  "time":"10 AM",
                  "busynessScore":"86%"
               },
               {
                  "time":"11 AM",
                  "busynessScore":"78%"
               },
               {
                  "time":"12 PM",
                  "busynessScore":"66%"
               },
               {
                  "time":"1 PM",
                  "busynessScore":"57%"
               },
               {
                  "time":"2 PM",
                  "busynessScore":"50%"
               },
               {
                  "time":"3 PM",
                  "busynessScore":"42%"
               },
               {
                  "time":"4 PM",
                  "busynessScore":"31%"
               },
               {
                  "time":"5 PM",
                  "busynessScore":"20%"
               },
               {
                  "time":"6 PM",
                  "busynessScore":"10%"
               },
               {
                  "time":"7 PM",
                  "busynessScore":"0%"
               },
               {
                  "time":"8 PM",
                  "busynessScore":"0%"
               }
            ],
            ... and other days of the week
         }
      },
      "images":[
         {
            "title":"All",
            "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipM4gn5qR89yKQiYbf2v8V2Mt-u27-8xlwgzbG3J=w397-h298-k-no"
         },
         {
            "title":"Food & drink",
            "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipOBX97ObGx9e0AhlwystTXlMKC7YaIfiEXzrj_N=w527-h298-k-no"
         },
         {
            "title":"Vibe",
            "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipP2A8D2I1d1gHgtqEBNMWiHm2jb7Dtd-p76FZS_=w224-h398-k-no"
         },
         {
            "title":"By owner",
            "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipNWlgCSV9T03azM-aCjgoqHBkCTVvAUp5hV-FEW=w273-h298-k-no"
         },
         {
            "title":"Street View & 360°",
            "thumbnail":"https://streetviewpixels-pa.googleapis.com/v1/thumbnail?panoid=3vdurQ8X2FFi_HXg_NQA-A&cb_client=maps_sv.tactile.gps&w=224&h=298&yaw=105.47167&pitch=0&thumbfov=100"
         },
         {
            "title":"Videos",
            "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipN8ncHBXGgaTyw8K3zlVlKz2lns8H5CiGszE8RL=w224-h398-k-no"
         }
      ],
      "userReviews":{
         "summary":[
            {
               "snippet":"Superfast Baristas and quality service one of the better Starbucks in the area"
            },
            {
               "snippet":"Very fast service and delicious food, good prices, and food for any person"
            },
            {
               "snippet":"My wife ordered a toasted graham latte and I got a mocha."
            }
         ],
         "mostRelevant":[
            {
               "username":"Bo Wagner",
               "rating":4,
               "description":"Good service, but waiting a bit long for my drink.  Look like a trainee was making my drink. It taste different.",
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
               ],
               "date":"5 months ago"
            },
            {
               "username":"Azurina S (Zeze)",
               "rating":5,
               "description":"Super friendly and fast.  They were getting through that Drive-Thru line at record speed!! Thank you for that because I was in a serious rush!! 👍🏽",
               "images":[
                  {
                     "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipPrI2xvgjFNh2vxFmBxRJBYvw553mORZdRZYwdZ=w300-h450-p-k-no"
                  },
                  {
                     "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipPVZ4YJqXjLvL-XTFBpB0oo4lVaBdrAGv2Ohyux=w300-h450-p-k-no"
                  }
               ],
               "date":"4 months ago"
            },
            {
               
            }
         ]
      },
      "peopleAlsoSearch":[
        {
            "title":"Amoré Coffee",
            "rating":"4.6",
            "reviews":"298",
            "type":"Coffee shop",
            "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipMq632JM1h0tJTDSkQrm_igzPaL-ze_md47fKEd=w156-h114-p-k-no"
        },
        {
            "title":"Jasper's Coffee",
            "rating":"4.3",
            "reviews":"67",
            "type":"Coffee shop",
            "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipMoO4Xxc0d7sKI7O0oJmb6dc1dEl56cpp7vPNl_=w156-h114-p-k-no"
        },
        {
            "title":"Caffe Ladro Upper Queen Anne",
            "rating":"4.5",
            "reviews":"182",
            "type":"Coffee shop",
            "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipMjoCEByahsLkhIDZNHkFkWaCCKo-XoS367PVEz=w156-h114-p-k-no"
        },
        {
            "title":"Mercurys Coffee Co.",
            "rating":"4.6",
            "reviews":"990",
            "type":"Coffee shop",
            "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipMwuaCDWUjIfUPvP1WIVZpafMj0PC5mzEg_Xyo6=w156-h114-p-k-no"
        },
        {
            "title":"Firehouse Coffee",
            "rating":"4.3",
            "reviews":"228",
            "type":"Cafe",
            "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipNQAwzW79MEiZ7NBGCJszQi9cFnJGM0muZQAgCW=w156-h114-p-k-no"
        },
        {
            "title":"Starbucks",
            "rating":"3.6",
            "reviews":"28",
            "type":"Coffee shop",
            "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipNEBOwy49GnRwulGSCrpihR0IkmyvWj2gjceWPw=w156-h114-p-k-no"
        },
        {
            "title":"Starbucks",
            "rating":"3.9",
            "reviews":"17",
            "type":"Coffee shop",
            "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipPl97WrsweypI_9MGkYA2c_wCg1NlpXROBzdl7t=w156-h114-p-k-no"
        },
        {
            "title":"Starbucks",
            "rating":"4.5",
            "thumbnail":"https://lh3.googleusercontent.com/zhBcV3r4IZkSc4kOsfl2qT1ENpJj4-awQKLKheS0HoJI8ptjPEMCPZv3vhIidbZ8=w156-h114-p"
        }
      ],
      "photosLink":"https://www.google.com/maps/place/Starbucks/@47.532004,-122.1943071,3a,75y,90t/data=!3m8!1e2!3m6!1sAF1QipM4gn5qR89yKQiYbf2v8V2Mt-u27-8xlwgzbG3J!2e10!3e12!6shttps:%2F%2Flh5.googleusercontent.com%2Fp%2FAF1QipM4gn5qR89yKQiYbf2v8V2Mt-u27-8xlwgzbG3J%3Dw114-h86-k-no!7i4032!8i3024!4m5!3m4!1s0x549069a98254bd17:0xb2f64f75b3edf4c3!8m2!3d47.5319688!4d-122.1942498?authuser=0&hl=en",
      "dataId":"0x549069a98254bd17:0xb2f64f75b3edf4c3",
      "gpsCoordinates":{
         "latitude":"47.5319688",
         "longitude":"-122.1942498"
      },
      "placeUrl":"https://www.google.com/maps/place/Starbucks/data=!4m7!3m6!1s0x549069a98254bd17:0xb2f64f75b3edf4c3!8m2!3d47.5319688!4d-122.1942498!16s%2Fg%2F1tdfmzpb!19sChIJF71UgqlpkFQRw_Tts3VP9rI?authuser=0&hl=en&rclk=1"
   }
}
```

<h2 id='serp_api'>Google Maps Place Results API</h2>

Alternatively, you can use the [Google Maps Place Results API](https://serpapi.com/maps-place-results) from SerpApi. SerpApi is a free API with 100 searches per month. If you need more searches, there are paid plans.

The difference is that you won't have to write code from scratch and maintain it. You may also experience blocking from Google and changing selectors which will break the parser. Instead, you just need to iterate the structured JSON and get the data you want. [Check out the playground](https://serpapi.com/playground).

First, we need to install [`google-search-results-nodejs`](https://www.npmjs.com/package/google-search-results-nodejs). To do this you need to enter in your console: `npm i google-search-results-nodejs`

📌Note: To make our search we need the data parameter, which must be set in the next format:
```lang-none
!4m5!3m4!1s + data_id + !8m2!3d + latitude + !4d + longitude
```
[A SerpApi video tutorial about extracting `data_id`, `latitude`, and `longitude`](https://www.youtube.com/watch?v=jqoNHXiGeZA&t=23s)

```javascript
const SerpApi = require("google-search-results-nodejs");
const search = new SerpApi.GoogleSearch(process.env.API_KEY); //your API key from serpapi.com

const dataId = "0x549069a98254bd17:0xb2f64f75b3edf4c3"; // data ID parameter
const latitude = "47.5319688"; // GPS coordinates latitude
const longitude = "-122.1942498"; // GPS coordinates longitude

const params = {
  engine: "google_maps", // search engine
  type: "place", // parameter defines the type of search you want to make
  data: `!4m5!3m4!1s${dataId}!8m2!3d${latitude}!4d${longitude}`, // parameter defines a search for a specific place
};

const getJson = () => {
  return new Promise((resolve) => {
    search.json(params, resolve);
  });
};

getJson().then(({place_results}) => console.dir(place_results, { depth: null }));
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

Next, we write down the necessary parameters for making a request:

```javascript
const dataId = "0x549069a98254bd17:0xb2f64f75b3edf4c3"; // data ID parameter
const latitude = "47.5319688"; // GPS coordinates latitude
const longitude = "-122.1942498"; // GPS coordinates longitude

const params = {
  engine: "google_maps", // search engine
  type: "place", // parameter defines the type of search you want to make
  data: `!4m5!3m4!1s${dataId}!8m2!3d${latitude}!4d${longitude}`, // parameter defines a search for a specific place
};
```

|Code|Explanation|
|----|-----------|
|`dataId`|data ID parameter|
|`latitude`|GPS coordinates latitude|
|`longitude`|GPS coordinates longitude|
|`engine`|search engine|
|`type`|parameter defines the type of search you want to make|
|`data`|parameter defines a search for a specific place|

Next, we wrap the search method from the SerpApi library in a promise to further work with the search results:

```javascript
const getJson = () => {
  return new Promise((resolve) => {
    search.json(params, resolve);
  })
}
```

And finally, run the `getJson` function that gets place info and returns it:

```javascript
getJson().then(({place_results}) => console.dir(place_results, { depth: null }));
```

|Code|Explanation|
|----|-----------|
|`console.dir(result, { depth: null })`|console method `dir` allows you to use an object with the necessary parameters to change default output options. Watch [Node.js documentation](https://nodejs.org/api/console.html#consoledirobj-options) for more info|

<h2 id='serp_api_output'>Output</h2>

```json
{
   "title":"Starbucks",
   "place_id":"ChIJF71UgqlpkFQRw_Tts3VP9rI",
   "data_id":"0x549069a98254bd17:0xb2f64f75b3edf4c3",
   "data_cid":"12895581949970478275",
   "reviews_link":"https://serpapi.com/search.json?data_id=0x549069a98254bd17%3A0xb2f64f75b3edf4c3&engine=google_maps_reviews&hl=en",
   "photos_link":"https://serpapi.com/search.json?data_id=0x549069a98254bd17%3A0xb2f64f75b3edf4c3&engine=google_maps_photos&hl=en",
   "gps_coordinates":{
      "latitude":47.5319688,
      "longitude":-122.1942498
   },
   "place_id_search":"https://serpapi.com/search.json?data=%214m5%213m4%211s0x549069a98254bd17%3A0xb2f64f75b3edf4c3%218m2%213d47.5319688%214d-122.1942498&engine=google_maps&google_domain=google.com&hl=en&type=place",
   "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipM4gn5qR89yKQiYbf2v8V2Mt-u27-8xlwgzbG3J=w114-h86-k-no",
   "rating":4.1,
   "reviews":381,
   "price":"$$",
   "type":[
      "Coffee shop",
      "Breakfast restaurant",
      "Cafe",
      "Coffee store",
      "Espresso bar",
      "Internet cafe"
   ],
   "description":"Seattle-based coffeehouse chain known for its signature roasts, light bites and WiFi availability.",
   "service_options":{
      "dine_in":true,
      "drive_through":true,
      "delivery":true
   },
   "extensions":[
      {
         "highlights":[
            "Fast service",
            "Great coffee",
            "Great tea selection"
         ]
      },
      {
         "popular_for":[
            "Breakfast",
            "Lunch",
            "Solo dining",
            "Good for working on laptop"
         ]
      },
      {
         "accessibility":[
            "Wheelchair accessible entrance",
            "Wheelchair accessible restroom",
            "Wheelchair accessible seating"
         ]
      },
      {
         "offerings":[
            "Coffee",
            "Organic dishes",
            "Prepared foods",
            "Quick bite",
            "Small plates"
         ]
      },
      {
         "dining_options":[
            "Breakfast",
            "Lunch",
            "Dessert"
         ]
      },
      {
         "amenities":[
            "Good for kids",
            "Restroom",
            "Wi-Fi"
         ]
      },
      {
         "atmosphere":[
            "Casual"
         ]
      },
      {
         "crowd":[
            "Groups",
            "LGBTQ+ friendly",
            "Tourists"
         ]
      },
      {
         "payments":[
            "Debit cards",
            "NFC mobile payments"
         ]
      }
   ],
   "address":"1785 NE 44th St, Renton, WA 98056",
   "website":"https://www.starbucks.com/store-locator/store/10581/",
   "phone":"(425) 226-7007",
   "open_state":"Closed ⋅ Opens 4:30AM",
   "plus_code":"GRJ4+Q8 Renton, Washington",
   "hours":[
      {
         "tuesday":"4:30AM–6:30PM"
      },
      {
         "wednesday":"4:30AM–6:30PM"
      },
      {
         "thursday":"4:30AM–6:30PM"
      },
      {
         "friday":"4:30AM–6:30PM"
      },
      {
         "saturday":"4:30AM–6:30PM"
      },
      {
         "sunday":"4:30AM–6:30PM"
      },
      {
         "monday":"4:30AM–6:30PM"
      }
   ],
   "images":[
      {
         "title":"All",
         "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipM4gn5qR89yKQiYbf2v8V2Mt-u27-8xlwgzbG3J=w397-h298-k-no"
      },
      {
         "title":"Latest",
         "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipMyZV-ERwRWVapz0JAGKAxvRDOK0VyidtodhmC6=w224-h398-k-no"
      },
      {
         "title":"Food & drink",
         "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipOBX97ObGx9e0AhlwystTXlMKC7YaIfiEXzrj_N=w527-h298-k-no"
      },
      {
         "title":"Vibe",
         "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipP2A8D2I1d1gHgtqEBNMWiHm2jb7Dtd-p76FZS_=w224-h398-k-no"
      },
      {
         "title":"By owner",
         "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipNWlgCSV9T03azM-aCjgoqHBkCTVvAUp5hV-FEW=w273-h298-k-no"
      },
      {
         "title":"Street View & 360°",
         "thumbnail":"https://streetviewpixels-pa.googleapis.com/v1/thumbnail?panoid=3vdurQ8X2FFi_HXg_NQA-A&cb_client=maps_sv.tactile.gps&w=224&h=298&yaw=105.47167&pitch=0&thumbfov=100"
      },
      {
         "title":"Videos",
         "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipN8ncHBXGgaTyw8K3zlVlKz2lns8H5CiGszE8RL=w224-h398-k-no"
      }
   ],
   "user_reviews":{
      "summary":[
         {
            "snippet":"\"Superfast Baristas and quality service one of the better Starbucks in the area\""
         },
         {
            "snippet":"\"Very fast service and delicious food, good prices, and food for any person\""
         },
         {
            "snippet":"\"My wife ordered a toasted graham latte and I got a mocha.\""
         }
      ],
      "most_relevant":[
         {
            "username":"Bo Wagner",
            "rating":4,
            "description":"Good service, but waiting a bit long for my drink.  Look like a trainee was making my drink. It taste different.",
            "images":[
               {
                  "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipNIUP-aOWRElmfVOjnf5lJJYFiLKBaSx7MSkhg8=w150-h150-k-no-p"
               },
               {
                  "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipPcTFJIW9JAZxZ0PU0WC2U5rPnESv7OnrnSANwV=w150-h150-k-no-p"
               },
               {
                  "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipN_LkT7MCwx-oaf1yXkMnc_D-gm6HrWa7Kqoep8=w150-h150-k-no-p"
               }
            ],
            "date":"5 months ago"
         },
         {
            "username":"Azurina S (Zeze)",
            "rating":5,
            "description":"Super friendly and fast.  They were getting through that Drive-Thru line at record speed!! Thank you for that because I was in a serious rush!! 👍🏽",
            "images":[
               {
                  "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipPrI2xvgjFNh2vxFmBxRJBYvw553mORZdRZYwdZ=w150-h150-k-no-p"
               },
               {
                  "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipPVZ4YJqXjLvL-XTFBpB0oo4lVaBdrAGv2Ohyux=w150-h150-k-no-p"
               }
            ],
            "date":"4 months ago"
         },
         {
            "username":"Emile Nelson",
            "rating":5,
            "description":"This location is always very quick. I place my mobile order as I leave my driveway and my drink is complete when I arrive (about 5-8 min drive). It’s in a big parking lot so plenty 
of easy parking. The staff are friendly and the store was recently redone so it’s very clean and sleek inside.",
            "date":"a month ago"
         },
         {
            "username":"Leeanne Banghart",
            "rating":1,
            "description":"Bought a Venti flat white single shot with vanilla. The first drink tasted terrible either had too many shots or not a ristretto shot. Second drink she left out the vanilla because 
she didn’t like having to make it again.",
            "date":"a month ago"
         },
         {
            "username":"Layla Kochi",
            "rating":1,
            "description":"I come here regularly because its the closest one to me, but its far from the best spot. More than half of my drinks end up only tasting like an overpriced glass of milk.",
            "date":"2 months ago"
         },
         {
            "username":"Denis Ko",
            "rating":2,
            "description":"Tried to buy my regular Turkey sandwich and asked them to warm it up in the oven for me, they told me it’s against their policy to warm up that specific sandwich even tho I’ve been 
doing that at all other Starbucks places. Had to settle with a different sandwich.",
            "images":[
               {
                  "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipNTPaghKZbvv5aouQjzCq7no46UiiCa8IbsNmCZ=w150-h150-k-no-p"
               }
            ],
            "date":"3 years ago"
         },
         {
            "username":"Eustolio Salinas",
            "rating":4,
            "description":"Always use drive thru but staff is always pleasant and friendly",
            "date":"2 months ago"
         },
         {
            "username":"Josie B (josinator317)",
            "rating":5,
            "description":"I love the baristas here! They’re all so kind!",
            "date":"3 months ago"
         }
      ]
   },
   "people_also_search_for":[
      {
         "search_term":"Quick coffee spots",
         "local_results":[
            {
               "position":1,
               "title":"Amoré Coffee",
               "data_id":"0x0:0xc616846fe1cecea9",
               "data_cid":"14273741685062028969",
               "reviews_link":"https://serpapi.com/search.json?data_id=0x0%3A0xc616846fe1cecea9&engine=google_maps_reviews&hl=en",
               "photos_link":"https://serpapi.com/search.json?data_id=0x0%3A0xc616846fe1cecea9&engine=google_maps_photos&hl=en",
               "gps_coordinates":{
                  "latitude":47.6299705,
                  "longitude":-122.1540146
               },
               "place_id_search":"https://serpapi.com/search.json?data=%214m5%213m4%211s0x0%3A0xc616846fe1cecea9%218m2%213d47.6299705%214d-122.1540146&engine=google_maps&google_domain=google.com&hl=en&type=place",
               "rating":4.6,
               "reviews":298,
               "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipMq632JM1h0tJTDSkQrm_igzPaL-ze_md47fKEd=w156-h156-n-k-no",
               "type":[
                  "Coffee shop"
               ]
            },
            {
               "position":2,
               "title":"Jasper's Coffee",
               "data_id":"0x0:0x931128093ca032bb",
               "data_cid":"10597295418316436155",
               "reviews_link":"https://serpapi.com/search.json?data_id=0x0%3A0x931128093ca032bb&engine=google_maps_reviews&hl=en",
               "photos_link":"https://serpapi.com/search.json?data_id=0x0%3A0x931128093ca032bb&engine=google_maps_photos&hl=en",
               "gps_coordinates":{
                  "latitude":47.456427999999995,
                  "longitude":-122.2819186
               },
               "place_id_search":"https://serpapi.com/search.json?data=%214m5%213m4%211s0x0%3A0x931128093ca032bb%218m2%213d47.456427999999995%214d-122.2819186&engine=google_maps&google_domain=google.com&hl=en&type=place",
               "rating":4.3,
               "reviews":67,
               "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipMoO4Xxc0d7sKI7O0oJmb6dc1dEl56cpp7vPNl_=w156-h156-n-k-no",
               "type":[
                  "Coffee shop",
                  "Cafe",
                  "Espresso bar",
                  "Store",
                  "Tea house"
               ]
            }
         ]
      },
      {
         "search_term":"Coffee and snacks",
         "local_results":[
            {
               "position":1,
               "title":"Caffe Ladro Upper Queen Anne",
               "data_id":"0x0:0x85b7345e1cd6e440",
               "data_cid":"9635227506597880896",
               "reviews_link":"https://serpapi.com/search.json?data_id=0x0%3A0x85b7345e1cd6e440&engine=google_maps_reviews&hl=en",
               "photos_link":"https://serpapi.com/search.json?data_id=0x0%3A0x85b7345e1cd6e440&engine=google_maps_photos&hl=en",
               "gps_coordinates":{
                  "latitude":47.638656,
                  "longitude":-122.3571131
               },
               "place_id_search":"https://serpapi.com/search.json?data=%214m5%213m4%211s0x0%3A0x85b7345e1cd6e440%218m2%213d47.638656%214d-122.3571131&engine=google_maps&google_domain=google.com&hl=en&type=place",
               "rating":4.5,
               "reviews":182,
               "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipOj7WJpLwxMZN8GrE0SKaO27SGECF0uasREHYbb=w156-h156-n-k-no",
               "type":[
                  "Coffee shop",
                  "Cafe",
                  "Espresso bar",
                  "Pastries"
               ]
            },
            {
               "position":2,
               "title":"Mercurys Coffee Co.",
               "data_id":"0x0:0x930e6194f7705433",
               "data_cid":"10596514265683743795",
               "reviews_link":"https://serpapi.com/search.json?data_id=0x0%3A0x930e6194f7705433&engine=google_maps_reviews&hl=en",
               "photos_link":"https://serpapi.com/search.json?data_id=0x0%3A0x930e6194f7705433&engine=google_maps_photos&hl=en",
               "gps_coordinates":{
                  "latitude":47.679584999999996,
                  "longitude":-122.17799799999997
               },
               "place_id_search":"https://serpapi.com/search.json?data=%214m5%213m4%211s0x0%3A0x930e6194f7705433%218m2%213d47.679584999999996%214d-122.17799799999997&engine=google_maps&google_domain=google.com&hl=en&type=place",
               "rating":4.6,
               "reviews":990,
               "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipMwuaCDWUjIfUPvP1WIVZpafMj0PC5mzEg_Xyo6=w156-h156-n-k-no",
               "type":[
                  "Coffee shop",
                  "Cafe"
               ]
            },
            {
               "position":3,
               "title":"Firehouse Coffee",
               "data_id":"0x0:0xc5dc6dd78d437396",
               "data_cid":"14257391292903551894",
               "reviews_link":"https://serpapi.com/search.json?data_id=0x0%3A0xc5dc6dd78d437396&engine=google_maps_reviews&hl=en",
               "photos_link":"https://serpapi.com/search.json?data_id=0x0%3A0xc5dc6dd78d437396&engine=google_maps_photos&hl=en",
               "gps_coordinates":{
                  "latitude":47.668838799999996,
                  "longitude":-122.39146869999999
               },
               "place_id_search":"https://serpapi.com/search.json?data=%214m5%213m4%211s0x0%3A0xc5dc6dd78d437396%218m2%213d47.668838799999996%214d-122.39146869999999&engine=google_maps&google_domain=google.com&hl=en&type=place",
               "rating":4.3,
               "reviews":228,
               "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipNQAwzW79MEiZ7NBGCJszQi9cFnJGM0muZQAgCW=w156-h156-n-k-no",
               "type":[
                  "Cafe"
               ]
            }
         ]
      },
      {
         "search_term":"Other locations for Starbucks",
         "local_results":[
            {
               "position":1,
               "title":"Starbucks",
               "data_id":"0x0:0xa7f4b5d23062c474",
               "data_cid":"12102498013010904180",
               "reviews_link":"https://serpapi.com/search.json?data_id=0x0%3A0xa7f4b5d23062c474&engine=google_maps_reviews&hl=en",
               "photos_link":"https://serpapi.com/search.json?data_id=0x0%3A0xa7f4b5d23062c474&engine=google_maps_photos&hl=en",
               "gps_coordinates":{
                  "latitude":47.539502999999996,
                  "longitude":-122.1673879
               },
               "place_id_search":"https://serpapi.com/search.json?data=%214m5%213m4%211s0x0%3A0xa7f4b5d23062c474%218m2%213d47.539502999999996%214d-122.1673879&engine=google_maps&google_domain=google.com&hl=en&type=place",
               "rating":3.6,
               "reviews":28,
               "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipNEBOwy49GnRwulGSCrpihR0IkmyvWj2gjceWPw=w156-h156-n-k-no",
               "type":[
                  "Coffee shop"
               ]
            },
            {
               "position":2,
               "title":"Starbucks",
               "data_id":"0x0:0x54529b2050fa59c6",
               "data_cid":"6076089410376063430",
               "reviews_link":"https://serpapi.com/search.json?data_id=0x0%3A0x54529b2050fa59c6&engine=google_maps_reviews&hl=en",
               "photos_link":"https://serpapi.com/search.json?data_id=0x0%3A0x54529b2050fa59c6&engine=google_maps_photos&hl=en",
               "gps_coordinates":{
                  "latitude":47.538987,
                  "longitude":-122.1649229
               },
               "place_id_search":"https://serpapi.com/search.json?data=%214m5%213m4%211s0x0%3A0x54529b2050fa59c6%218m2%213d47.538987%214d-122.1649229&engine=google_maps&google_domain=google.com&hl=en&type=place",
               "rating":3.9,
               "reviews":17,
               "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipPl97WrsweypI_9MGkYA2c_wCg1NlpXROBzdl7t=w156-h156-n-k-no",
               "type":[
                  "Coffee shop"
               ]
            },
            {
               "position":3,
               "title":"",
               "data_id":"0x0:0xa5b69d736702abe0",
               "data_cid":"11940904580994477024",
               "reviews_link":"https://serpapi.com/search.json?data_id=0x0%3A0xa5b69d736702abe0&engine=google_maps_reviews&hl=en",
               "photos_link":"https://serpapi.com/search.json?data_id=0x0%3A0xa5b69d736702abe0&engine=google_maps_photos&hl=en",
               "rating":0,
               "reviews":0,
               "thumbnail":"https://lh3.googleusercontent.com/zhBcV3r4IZkSc4kOsfl2qT1ENpJj4-awQKLKheS0HoJI8ptjPEMCPZv3vhIidbZ8=w156-h156-n"
            },
            {
               "position":4,
               "title":"Starbucks",
               "data_id":"0x0:0x550b3f046f8d079b",
               "data_cid":"6128061006251624347",
               "reviews_link":"https://serpapi.com/search.json?data_id=0x0%3A0x550b3f046f8d079b&engine=google_maps_reviews&hl=en",
               "photos_link":"https://serpapi.com/search.json?data_id=0x0%3A0x550b3f046f8d079b&engine=google_maps_photos&hl=en",
               "gps_coordinates":{
                  "latitude":47.541261999999996,
                  "longitude":-122.22574100000001
               },
               "place_id_search":"https://serpapi.com/search.json?data=%214m5%213m4%211s0x0%3A0x550b3f046f8d079b%218m2%213d47.541261999999996%214d-122.22574100000001&engine=google_maps&google_domain=google.com&hl=en&type=place",
               "rating":4.5,
               "reviews":114,
               "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipMsyNpIMbnxgmioXwwnmKUrmRrmezBTz-_R5wn6=w156-h156-n-k-no",
               "type":[
                  "Coffee shop"
               ]
            }
         ]
      }
   ],
   "popular_times":{
      "graph_results":{
         "sunday":[
            {
               "time":"3 AM",
               "busyness_score":0
            },
            {
               "time":"4 AM",
               "info":"Usually not busy",
               "busyness_score":4
            },
            {
               "time":"5 AM",
               "info":"Usually not busy",
               "busyness_score":12
            },
            {
               "time":"6 AM",
               "info":"Usually not too busy",
               "busyness_score":26
            },
            {
               "time":"7 AM",
               "info":"Usually not too busy",
               "busyness_score":47
            },
            {
               "time":"8 AM",
               "info":"Usually a little busy",
               "busyness_score":68
            },
            {
               "time":"9 AM",
               "info":"Usually as busy as it gets",
               "busyness_score":83
            },
            {
               "time":"10 AM",
               "info":"Usually as busy as it gets",
               "busyness_score":86
            },
            {
               "time":"11 AM",
               "info":"Usually a little busy",
               "busyness_score":78
            },
            {
               "time":"12 PM",
               "info":"Usually a little busy",
               "busyness_score":66
            },
            {
               "time":"1 PM",
               "info":"Usually a little busy",
               "busyness_score":57
            },
            {
               "time":"2 PM",
               "info":"Usually not too busy",
               "busyness_score":50
            },
            {
               "time":"3 PM",
               "info":"Usually not too busy",
               "busyness_score":42
            },
            {
               "time":"4 PM",
               "info":"Usually not too busy",
               "busyness_score":31
            },
            {
               "time":"5 PM",
               "info":"Usually not busy",
               "busyness_score":20
            },
            {
               "time":"6 PM",
               "info":"Usually not busy",
               "busyness_score":10
            },
            {
               "time":"7 PM",
               "busyness_score":0
            },
            {
               "time":"8 PM",
               "busyness_score":0
            }
         ],
          ... and other days of the week
      },
      "live_hash":{
         "info":null,
         "time_spent":"People typically spend 10 min here"
      }
   }
}
```

<h2 id='links'>Links</h2>

* [Code in the online IDE](https://replit.com/@MikhailZub/Google-Maps-Place-NodeJS-SerpApi#index.js) 
* [Google Maps Place Results API](https://serpapi.com/maps-place-results)

If you want to see some projects made with SerpApi, please write me a message.

___
<p style="text-align: center;">Join us on <a href="https://twitter.com/serp_api">Twitter</a> | <a href="https://www.youtube.com/channel/UCUgIHlYBOD3yA3yDIRhg_mg">YouTube</a></p>
<p style="text-align: center;">Add a  <a href="https://github.com/serpapi/public-roadmap/issues">Feature Request</a>💫 or a <a href="https://github.com/serpapi/public-roadmap/issues">Bug</a>🐞</p>