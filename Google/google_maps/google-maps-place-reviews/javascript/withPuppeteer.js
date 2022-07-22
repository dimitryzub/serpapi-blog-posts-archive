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
          localGuide: el.querySelector(".RfnDt span:first-child").style.display === "none" ? undefined : true,
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

module.exports = { getLocalPlaceReviews };
