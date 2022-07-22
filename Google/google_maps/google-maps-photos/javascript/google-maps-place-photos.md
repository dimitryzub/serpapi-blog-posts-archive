<h2 id='what'>What will be scraped</h2>

![image](https://user-images.githubusercontent.com/64033139/180219601-87a8971d-4ced-4ed5-841b-7e1a38383694.png)

<h2 id='preparation'>Preparation</h2>

First, we need to create a Node.js* project and add [`npm`](https://www.npmjs.com/) packages [`puppeteer`](https://www.npmjs.com/package/puppeteer), [`puppeteer-extra`](https://www.npmjs.com/package/puppeteer-extra) and [`puppeteer-extra-plugin-stealth`](https://www.npmjs.com/package/puppeteer-extra-plugin-stealth) to control Chromium (or Chrome, or Firefox, but now we work only with Chromium which is used by default) over the [DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/) in [headless](https://developers.google.com/web/updates/2017/04/headless-chrome) or non-headless mode. 

To do this, in the directory with our project, open the command line and enter `npm init -y`, and then `npm i puppeteer puppeteer-extra puppeteer-extra-plugin-stealth`.

*<span style="font-size: 15px;">If you don't have Node.js installed, you can [download it from nodejs.org](https://nodejs.org/en/) and follow the installation [documentation](https://nodejs.dev/learn/introduction-to-nodejs).</span>

📌Note: also, you can use `puppeteer` without any extensions, but I strongly recommended use it with `puppeteer-extra` with `puppeteer-extra-plugin-stealth` to prevent website detection that you are using headless Chromium or that you are using [web driver](https://www.w3.org/TR/webdriver/). You can check it on [Chrome headless tests website](https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html). The screenshot below shows you a difference.

![stealth](https://user-images.githubusercontent.com/64033139/173014238-eb8450d7-616c-42ae-8b2f-24eeb5fd5916.png)

<h2 id='process'>Process</h2>

[SelectorGadget Chrome extension](https://chrome.google.com/webstore/detail/selectorgadget/mhjhnkcfbdhnjickkkdbjoemdmbfginb) was used to grab CSS selectors by clicking on the desired element in the browser. If you have any struggles understanding this, we have a dedicated [Web Scraping with CSS Selectors blog post](https://serpapi.com/blog/web-scraping-with-css-selectors-using-python/) at SerpApi.

The Gif below illustrates the approach of selecting different parts of the results.

![how](https://user-images.githubusercontent.com/64033139/180220118-69219af0-d753-4f2a-92e1-57cf32d53f49.gif)

<h2 id='full_code'>Full code</h2>

📌Note: to get a place URL you may use the tutorial from my blog post [Web Scraping Google Maps Places with Nodejs](https://serpapi.com/blog/web-scraping-google-maps-places-with-nodejs/#full_code).

```javascript
const puppeteer = require("puppeteer-extra");
const StealthPlugin = require("puppeteer-extra-plugin-stealth");

puppeteer.use(StealthPlugin());

const placeUrl =
  "https://www.google.com/maps/place/Starbucks/data=!4m7!3m6!1s0x549069a98254bd17:0xb2f64f75b3edf4c3!8m2!3d47.5319688!4d-122.1942498!16s%2Fg%2F1tdfmzpb!19sChIJF71UgqlpkFQRw_Tts3VP9rI?authuser=0&hl=en&rclk=1";

async function scrollPage(page) {
  let iterationsLength = 0;
  while (true) {
    let photosLength = await page.evaluate(() => {
      return document.querySelectorAll(".U39Pmb").length;
    });
    for (; iterationsLength < photosLength; iterationsLength++) {
      await page.waitForTimeout(200)
      await page.evaluate((iterationsLength) => {
        document.querySelectorAll(".U39Pmb")[iterationsLength].scrollIntoView()
      }, iterationsLength);
    }
    await page.waitForTimeout(5000)
    let newPhotosLength = await page.evaluate(() => {
      return document.querySelectorAll(".U39Pmb").length;
    });
    if (newPhotosLength === photosLength) break
  }
}

async function getPhotosLinks(page) {
  const photos = await page.evaluate(() => {
    return Array.from(document.querySelectorAll(".U39Pmb")).map((el) => {
      return {
        thumbnail: getComputedStyle(el).backgroundImage.slice(5, -2),
      };
    });
  });
  const scripts = await page.evaluate(() => {
    return Array.from(document.querySelectorAll("script")).map(el => el.outerHTML).join()
  })
  return {photos, scripts};
}

async function getLocalPlacePhotos() {
  const browser = await puppeteer.launch({
    headless: false,
    args: ["--no-sandbox", "--disable-setuid-sandbox"],
  });

  const page = await browser.newPage();

  await page.setDefaultNavigationTimeout(60000);
  await page.goto(placeUrl);
  await page.waitForNavigation();

  await page.click(".Dx2nRe");
  await page.waitForTimeout(2000);
  await page.waitForSelector(".U39Pmb");

  await scrollPage(page);

  const {photos, scripts} = await getPhotosLinks(page);

  await browser.close();

  const validPhotos = photos.filter((el) => el.thumbnail.includes('https://lh5.googleusercontent.com/p'))

  const photoSizePattern = /"https:\/\/lh5\.googleusercontent\.com\/p\/(?<id>[^\\]+).+?\[(?<resolution>\d{2,},\d{2,})/gm; // https://regex101.com/r/zgxNOb/2
  const fullSizeData = [...scripts.matchAll(photoSizePattern)].map(({ groups }) => ({id: groups.id, resolution: groups.resolution}));

  validPhotos.forEach(el => {
    const idPattern = /https:\/\/lh5\.googleusercontent\.com\/p\/(?<id>[^\=]+)/gm;  // https://regex101.com/r/XxS3QC/1
    const id = [...el.thumbnail.matchAll(idPattern)].map(({ groups }) => groups.id)[0];
    const resolution = fullSizeData.find((dataEl) => dataEl.id === id)?.resolution.split(',')
    if (resolution) el.image = `https://lh5.googleusercontent.com/p/${id}=w${resolution[1]}-h${resolution[0]}-k-no`
  })

  return validPhotos;
}

getLocalPlacePhotos().then(console.log);
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
        
Next, we write down a function for scrolling photo container on the page:

```javascript
async function scrollPage(page) {
  let iterationsLength = 0;
  while (true) {
    let photosLength = await page.evaluate(() => {
      return document.querySelectorAll(".U39Pmb").length;
    });
    for (; iterationsLength < photosLength; iterationsLength++) {
      await page.waitForTimeout(200)
      await page.evaluate((iterationsLength) => {
        document.querySelectorAll(".U39Pmb")[iterationsLength].scrollIntoView()
      }, iterationsLength);
    }
    await page.waitForTimeout(5000)
    let newPhotosLength = await page.evaluate(() => {
      return document.querySelectorAll(".U39Pmb").length;
    });
    if (newPhotosLength === photosLength) break
  }
}
```

|Code|Explanation|
|----|-----------|
|`photosLength`|amount of photos on the page before scrolling|
|`page.evaluate(`|runs code from the brackets in the browser console and returns the result|
|[`document.querySelectorAll(".U39Pmb")`](https://developer.mozilla.org/en-US/docs/Web/API/Document/querySelectorAll)|returns a static [NodeList](https://developer.mozilla.org/en-US/docs/Web/API/NodeList) representing a list of the document's elements that match the css selectors with class name `U39Pmb`|
|`page.waitForTimeout(200)`|waiting 200 ms before continue|
|`newPhotosLength`|amount of photos on the page after scrolling|

Next, we write down a function for getting thumbnails links from the page:

```javascript
async function getPhotosLinks(page) {
  const photos = await page.evaluate(() => {
    return Array.from(document.querySelectorAll(".U39Pmb")).map((el) => {
      return {
        thumbnail: getComputedStyle(el).backgroundImage.slice(5, -2),
      };
    });
  });
  const scripts = await page.evaluate(() => {
    return Array.from(document.querySelectorAll("script")).map(el => el.outerHTML).join()
  })
  return {photos, scripts};
}
```

|Code|Explanation|
|----|-----------|
|`getComputedStyle(el).backgroundImage`|[`getComputedStyle(el)`](https://developer.mozilla.org/en-US/docs/Web/API/Window/getComputedStyle) returns an object containing the values of all CSS properties of an `el`, after applying active stylesheets, and get `backgroundImage` property|
|`.slice(5, -2)`|this method keeps everything from the 5th character from the beginning to the 2nd (inclusive) character from the end and removes the others|
        
And finally, a function to control the browser, and get information:

```javascript
async function getLocalPlacePhotos() {
  const browser = await puppeteer.launch({
    headless: false,
    args: ["--no-sandbox", "--disable-setuid-sandbox"],
  });

  const page = await browser.newPage();

  await page.setDefaultNavigationTimeout(60000);
  await page.goto(placeUrl);
  await page.waitForNavigation();

  await page.click(".Dx2nRe");
  await page.waitForTimeout(2000);
  await page.waitForSelector(".U39Pmb");

  await scrollPage(page);

  const {photos, scripts} = await getPhotosLinks(page);

  await browser.close();

  const validPhotos = photos.filter((el) => el.thumbnail.includes('https://lh5.googleusercontent.com/p'))

  const photoSizePattern = /"https:\/\/lh5\.googleusercontent\.com\/p\/(?<id>[^\\]+).+?\[(?<resolution>\d{2,},\d{2,})/gm; // https://regex101.com/r/zgxNOb/2
  const fullSizeData = [...scripts.matchAll(photoSizePattern)].map(({ groups }) => ({id: groups.id, resolution: groups.resolution}));

  validPhotos.forEach(el => {
    const idPattern = /https:\/\/lh5\.googleusercontent\.com\/p\/(?<id>[^\=]+)/gm;  // https://regex101.com/r/XxS3QC/1
    const id = [...el.thumbnail.matchAll(idPattern)].map(({ groups }) => groups.id)[0];
    const resolution = fullSizeData.find((dataEl) => dataEl.id === id)?.resolution.split(',')
    if (resolution) el.image = `https://lh5.googleusercontent.com/p/${id}=w${resolution[1]}-h${resolution[0]}-k-no`
  })

  return validPhotos;
}

getLocalPlacePhotos().then(console.log);
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
|`photoSizePattern`|a RegEx pattern for search and define id. [See what it allows you to find](https://regex101.com/r/zgxNOb/2)|
|`[...scripts.matchAll(photoSizePattern)]`|in this code we use [spread syntax](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Spread_syntax) to create an array from an [iterator](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Iterators_and_Generators) that was returned from [matchAll method](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/matchAll) (in this case this entry is equal to `Array.from(scripts.matchAll(photoSizePattern))`)|
|`idPattern`|a RegEx pattern for search and define id and full image resolution. [See what it allows you to find](https://regex101.com/r/XxS3QC/1)|

Now we can launch our parser. To do this enter `node YOUR_FILE_NAME` in your command line. Where `YOUR_FILE_NAME` is the name of your `.js` file.

<h2 id='output'>Output</h2>

📌Note: I'm showing you the full output on purpose because not all full image links are available on the page. If I find a solution in the future, I'll update this post.

```json
[
   {
      "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipM4gn5qR89yKQiYbf2v8V2Mt-u27-8xlwgzbG3J=w203-h152-k-no",
      "image":"https://lh5.googleusercontent.com/p/AF1QipM4gn5qR89yKQiYbf2v8V2Mt-u27-8xlwgzbG3J=w3024-h4032-k-no"
   },
   {
      "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipOBX97ObGx9e0AhlwystTXlMKC7YaIfiEXzrj_N=w203-h114-k-no",
      "image":"https://lh5.googleusercontent.com/p/AF1QipOBX97ObGx9e0AhlwystTXlMKC7YaIfiEXzrj_N=w289-h512-k-no"
   },
   {
      "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipM8KZ731HUrAb6Ow6b6tvaaG1SZibLWHlUG0B7I=w203-h270-k-no",
      "image":"https://lh5.googleusercontent.com/p/AF1QipM8KZ731HUrAb6Ow6b6tvaaG1SZibLWHlUG0B7I=w4032-h3024-k-no"
   },
   {
      "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipNGkMDnc3haeI6zEkJHTaYO3NL7kQU08HDDj-Bg=w203-h152-k-no",
      "image":"https://lh5.googleusercontent.com/p/AF1QipNGkMDnc3haeI6zEkJHTaYO3NL7kQU08HDDj-Bg=w3120-h4160-k-no"
   },
   {
      "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipNWlgCSV9T03azM-aCjgoqHBkCTVvAUp5hV-FEW=w203-h220-k-no",
      "image":"https://lh5.googleusercontent.com/p/AF1QipNWlgCSV9T03azM-aCjgoqHBkCTVvAUp5hV-FEW=w546-h502-k-no"
   },
   {
      "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipNl409pGQ2GeJ4UGLoCEFE2tYP7KyAFABGYtCqW=w203-h184-k-no"
   },
   {
      "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipMzdzL2c833XHkjyKCAZA_oIpG7sWzev14BIZqY=w203-h203-k-no"
   },
   {
      "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipOXC7UsM4ytw-Qdo9BqQPgdu7hpOFkrb8oeXXcD=w203-h152-k-no"
   },
   {
      "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipPQRAYxiLusjrzSeqS8mc23V5u_fv26RobHwvpL=w205-h100-k-no"
   },
   {
      "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipP27I9yad0JARrUosmPe2Cl8rrf5FfLI9u3ZsLe=w203-h152-k-no"
   },
   {
      "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipP2A8D2I1d1gHgtqEBNMWiHm2jb7Dtd-p76FZS_=w203-h360-k-no",
      "image":"https://lh5.googleusercontent.com/p/AF1QipP2A8D2I1d1gHgtqEBNMWiHm2jb7Dtd-p76FZS_=w1920-h1080-k-no"
   },
   {
      "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipOCI7c9c2HSYM18cjd52ITmt2S-pkysyGoXAaEy=w203-h152-k-no"
   },
   {
      "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipNspVD1U4OKrDH5ZYVYwbazgE5amUtTRh54soV-=w203-h270-k-no"
   },
   {
      "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipNZeKVSAkS5IJtH_HTYenfFSrz6pgSwp4aM-1qv=w203-h164-k-no"
   },
   {
      "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipMoV7jsVrAVqTWWS3Qs7ouAJfPoi8MBIW0aOm_z=w203-h270-k-no"
   },
   {
      "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipNGOf2IWJ3Dmk_MLbhlcHAoMracP-o81WAre-51=w203-h270-k-no"
   },
   {
      "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipOn4frZ--0ZzrbAdDQoRPrtSZO5auLIVz76ju0H=w203-h152-k-no"
   },
   {
      "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipN_LkT7MCwx-oaf1yXkMnc_D-gm6HrWa7Kqoep8=w203-h270-k-no",
      "image":"https://lh5.googleusercontent.com/p/AF1QipN_LkT7MCwx-oaf1yXkMnc_D-gm6HrWa7Kqoep8=w3024-h4032-k-no"
   },
   {
      "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipNTPaghKZbvv5aouQjzCq7no46UiiCa8IbsNmCZ=w203-h270-k-no",
      "image":"https://lh5.googleusercontent.com/p/AF1QipNTPaghKZbvv5aouQjzCq7no46UiiCa8IbsNmCZ=w3024-h4032-k-no"
   },
   {
      "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipMXpF0BcYK9v4_AqjXWj1R_OHT3opK5y8h3lwxG=w203-h270-k-no"
   },
   {
      "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipMYK-cBn6_JUYTVbPkvAFTnb_cxWYI4B8aBDwGV=w203-h152-k-no"
   },
   {
      "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipPcTFJIW9JAZxZ0PU0WC2U5rPnESv7OnrnSANwV=w203-h270-k-no",
      "image":"https://lh5.googleusercontent.com/p/AF1QipPcTFJIW9JAZxZ0PU0WC2U5rPnESv7OnrnSANwV=w3024-h4032-k-no"
   },
   {
      "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipOk5SXZXLYdZrliZhbEB-fuzpwX4AIiiIjC7Ehi=w203-h114-k-no"
   },
   {
      "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipN8ncHBXGgaTyw8K3zlVlKz2lns8H5CiGszE8RL=w203-h360-k-no",
      "image":"https://lh5.googleusercontent.com/p/AF1QipN8ncHBXGgaTyw8K3zlVlKz2lns8H5CiGszE8RL=w1920-h1080-k-no"
   },
   {
      "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipMpGGf0g2dlvO0o9gaz_KJW3lIJpLOEHHOprabC=w203-h152-k-no"
   },
   {
      "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipNPGlc3kl2VVWxVoaVarj767h12q9Dn5dDMpLY6=w203-h360-k-no"
   },
   {
      "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipOFr1BaDsgzpJZ75-keeWMcucSsY9ooOc2eYbg3=w203-h262-k-no"
   },
   {
      "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipPmujcLdxq_1ykKBzaBVMFDsvUNa7qlujezz6kP=w203-h360-k-no"
   },
   {
      "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipNKcskE9z5R_qZRvE9OmfC-XFtqDotXM_dynsyH=w203-h270-k-no"
   },
   {
      "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipOOBmi7BSryS_eU-DTAj5C5vR0CEqlSp-LvbxwB=w203-h152-k-no"
   },
   {
      "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipMENxPMlida3xNw7aOFPdw5UysR8KvDwPMbYZs4=w203-h203-k-no"
   },
   {
      "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipMek3ZenfuNiPxPO5N9xQ2sd-ZmrPJAEbwJiIsZ=w203-h114-k-no"
   },
   {
      "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipOS9SWb1Me927ABd1G6Ykf0emdLVxodfIucaEYz=w203-h152-k-no"
   },
   {
      "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipNXrAp9R2-kA0XuDooVR7_ep_jL-zLN8CziOyBU=w203-h152-k-no"
   },
   {
      "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipOL-FC0pQMTTS2uMjL39BgwZHKtlxC7g4QFztBI=w203-h360-k-no"
   },
   {
      "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipOnmfuOu_9FFp3Ee0-zLFNFmrM6wU2O9PZK4Zm0=w203-h152-k-no"
   },
   {
      "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipOrktO0O66qVKhpxWh02BHe2jxJZgtAZB34c_nJ=w203-h270-k-no"
   },
   {
      "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipMLKR4zHY3bEzI1EUnRB8j5ku1MeDI7xv7UNgAR=w203-h360-k-no"
   },
   {
      "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipPgiZFDf_Xyje716A6MMAPQs_XF8yvVq_BtxQZc=w203-h152-k-no"
   },
   {
      "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipMZ_dmYNhLoOGp57DYCQa3Q_XWDae84e4Hdf1rj=w203-h152-k-no"
   },
   {
      "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipMJiZA1oAjzFuU4fBbp_ihe4UPSSpq5T1sXfufA=w203-h152-k-no"
   },
   {
      "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipNIUP-aOWRElmfVOjnf5lJJYFiLKBaSx7MSkhg8=w203-h270-k-no",
      "image":"https://lh5.googleusercontent.com/p/AF1QipNIUP-aOWRElmfVOjnf5lJJYFiLKBaSx7MSkhg8=w3024-h4032-k-no"
   },
   {
      "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipNolq_OR7cT2d3ayKRLkl2mb9s-mv0mqAJPLHX1=w203-h270-k-no"
   },
   {
      "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipOuAg_x3ITU1I32KiWZGBzgwQAU4UXf4GB5Z9PS=w203-h270-k-no"
   },
   {
      "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipMtjVGORN2eq-6kIjCrkW3biGo3cMVazFNBfz2r=w203-h152-k-no"
   },
   {
      "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipNsjaDdvAQrRboCbdVmcRA83c6DUBZ4YZvTDa8d=w203-h270-k-no"
   }
]
```

<h2 id='serp_api'>Google Maps Photos API</h2>

Alternatively, you can use the [Google Maps Photos API](https://serpapi.com/google-maps-photos-api) from SerpApi. SerpApi is a free API with 100 searches per month. If you need more searches, there are paid plans.

The difference is that you can get all full image links and you won't have to write code from scratch and maintain it. You may also experience blocking from Google and changing selectors which will break the parser. Instead, you just need to iterate the structured JSON and get the data you want. [Check out the playground](https://serpapi.com/playground).

First, we need to install [`google-search-results-nodejs`](https://www.npmjs.com/package/google-search-results-nodejs). To do this you need to enter in your console: `npm i google-search-results-nodejs`

📌Note: To make our search we need the `data_id` parameter. You can take it using the guide from my blog post [Web Scraping Google Maps Places with Nodejs](https://serpapi.com/blog/web-scraping-google-maps-places-with-nodejs/#serp_api).

```javascript
const SerpApi = require("google-search-results-nodejs");
const search = new SerpApi.GoogleSearch(process.env.API_KEY);     //your API key from serpapi.com

const dataId = "0x549069a98254bd17:0xb2f64f75b3edf4c3";           // data ID parameter

const params = {
  engine: "google_maps_photos",                                   // search engine
  hl: "en",                                                       // parameter defines the language to use for the Google search
  data_id: dataId,                                                // parameter defines the Google Maps data ID
};

const getJson = () => {
  return new Promise((resolve) => {
    search.json(params, resolve);
  });
};

const getResults = async () => {
  const allPhotos = [];
  while (true) {
    const json = await getJson();
    if (json.photos) {
      allPhotos.push(...json.photos);
    } else break;
    if (json.serpapi_pagination?.next_page_token) {
      params.next_page_token = json.serpapi_pagination?.next_page_token;
    } else break;
  }
  return allPhotos;
};

getResults.then(console.log);
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
  engine: "google_maps_photos", // search engine
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

And finally, we declare and run the function `getResult` that gets photo links from all pages and return it:

```javascript
const getResults = async () => {
  const allPhotos = [];
  while (true) {
    const json = await getJson();
    if (json.photos) {
      allPhotos.push(...json.photos);
    } else break;
    if (json.serpapi_pagination?.next_page_token) {
      params.next_page_token = json.serpapi_pagination?.next_page_token;
    } else break;
  }
  return allPhotos;
};

getResults().then(console.log)
```

|Code|Explanation|
|----|-----------|
|`allPhotos`|an array with photo links from all pages|
|`allPhotos.push(...json.photos)`|in this code, we use [spread syntax](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Spread_syntax) to split the `photos` array from result that was returned from `getJson` function into elements and add them in the end of `allPhotos` array|

<h2 id='serp_api_output'>Output</h2>

```json
[
   {
      "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipM4gn5qR89yKQiYbf2v8V2Mt-u27-8xlwgzbG3J=w203-h152-k-no",
      "image":"https://lh5.googleusercontent.com/p/AF1QipM4gn5qR89yKQiYbf2v8V2Mt-u27-8xlwgzbG3J=w4032-h3024-k-no"
   },
   {
      "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipOBX97ObGx9e0AhlwystTXlMKC7YaIfiEXzrj_N=w203-h114-k-no",
      "image":"https://lh5.googleusercontent.com/p/AF1QipOBX97ObGx9e0AhlwystTXlMKC7YaIfiEXzrj_N=w512-h289-k-no"
   },
   {
      "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipM8KZ731HUrAb6Ow6b6tvaaG1SZibLWHlUG0B7I=w203-h270-k-no",
      "image":"https://lh5.googleusercontent.com/p/AF1QipM8KZ731HUrAb6Ow6b6tvaaG1SZibLWHlUG0B7I=w3024-h4032-k-no"
   },
   {
      "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipNGkMDnc3haeI6zEkJHTaYO3NL7kQU08HDDj-Bg=w203-h152-k-no",
      "image":"https://lh5.googleusercontent.com/p/AF1QipNGkMDnc3haeI6zEkJHTaYO3NL7kQU08HDDj-Bg=w4160-h3120-k-no"
   },
   {
      "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipNWlgCSV9T03azM-aCjgoqHBkCTVvAUp5hV-FEW=w203-h220-k-no",
      "image":"https://lh5.googleusercontent.com/p/AF1QipNWlgCSV9T03azM-aCjgoqHBkCTVvAUp5hV-FEW=w502-h546-k-no"
   },
   {
      "thumbnail":"https://lh5.googleusercontent.com/p/AF1QipNl409pGQ2GeJ4UGLoCEFE2tYP7KyAFABGYtCqW=w203-h184-k-no",
      "image":"https://lh5.googleusercontent.com/p/AF1QipNl409pGQ2GeJ4UGLoCEFE2tYP7KyAFABGYtCqW=w732-h664-k-no"
   },
   ...and other results
]
```

<h2 id='links'>Links</h2>

* [Code in the online IDE](https://replit.com/@MikhailZub/Google-Maps-Photos-NodeJS-SerpApi#index.js) 
* [Google Maps Photos API](https://serpapi.com/google-maps-photos-api)

If you want to see some projects made with SerpApi, please write me a message.

___
<p style="text-align: center;">Join us on <a href="https://twitter.com/serp_api">Twitter</a> | <a href="https://www.youtube.com/channel/UCUgIHlYBOD3yA3yDIRhg_mg">YouTube</a></p>
<p style="text-align: center;">Add a  <a href="https://github.com/serpapi/public-roadmap/issues">Feature Request</a>💫 or a <a href="https://github.com/serpapi/public-roadmap/issues">Bug</a>🐞</p>