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

module.exports = { getOrganicResults };
