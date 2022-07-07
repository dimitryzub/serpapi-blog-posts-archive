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
    await page.goto(URL);
    await page.waitForTimeout(2000);
    allCites.push(await fillCiteData(page));
  }

  await browser.close();

  return allCites;
}

module.exports = { getScholarCitesInfo };
