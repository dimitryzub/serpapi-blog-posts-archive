const puppeteer = require("puppeteer-extra");
const StealthPlugin = require("puppeteer-extra-plugin-stealth");

puppeteer.use(StealthPlugin());

const requestParams = {
  user: "6ZiRSwQAAAAJ",                              // the ID of the author we want to scrape
  hl: "en",                                          // parameter defines the language to use for the Google search
};

const domain = `http://scholar.google.com`;

async function getArticles(page) {
  while (true) {
    await page.waitForSelector("#gsc_bpf_more");
    const isNextPage = await page.$("#gsc_bpf_more:not([disabled])");
    if (!isNextPage) break;
    await page.click("#gsc_bpf_more");
    await page.waitForTimeout(5000);
  }
  return await page.evaluate(async () => {
    const articles = document.querySelectorAll(".gsc_a_tr");
    const articleInfo = [];
    for (const el of articles) {
      articleInfo.push({
        title: el.querySelector(".gsc_a_at").textContent.trim(),
        link: await window.buildValidLink(el.querySelector(".gsc_a_at").getAttribute("href")),
        authors: el.querySelector(".gs_gray:first-of-type").textContent.trim(),
        publication: el.querySelector(".gs_gray:last-of-type").textContent.trim(),
        citedBy: {
          link: el.querySelector(".gsc_a_ac").getAttribute("href"),
          cited: el.querySelector(".gsc_a_ac").textContent.trim(),
        },
        year: el.querySelector(".gsc_a_h").textContent.trim(),
      });
    }
    return articleInfo;
  });
}

async function getScholarAuthorInfo() {
  const browser = await puppeteer.launch({
    headless: false,
    args: ["--no-sandbox", "--disable-setuid-sandbox"],
  });

  const page = await browser.newPage();

  const URL = `${domain}/citations?hl=${requestParams.hl}&user=${requestParams.user}`;

  await page.setDefaultNavigationTimeout(60000);
  await page.goto(URL);
  await page.waitForSelector(".gsc_a_tr");
  await page.waitForTimeout(1000);

  await page.exposeFunction("buildValidLink", (rawLink) => {
    if (!rawLink || rawLink.includes("javascript:void(0)")) return "link not available";
    if (rawLink.includes("scholar.googleusercontent")) return rawLink;
    return domain + rawLink;
  });

  const articles = await getArticles(page);

  const scholarAuthorInfo = await page.evaluate(async (articles) => {
    const interests = [];
    const interstsSelectors = document.querySelectorAll("#gsc_prf_int a");
    for (const interest of interstsSelectors) {
      interests.push({
        title: interest.textContent.trim(),
        link: await window.buildValidLink(interest.getAttribute("href")),
      });
    }

    const coAuthors = [];
    const coAuthorsSelectors = document.querySelectorAll("#gsc_rsb_co .gsc_rsb_aa");
    for (const coAuthor of coAuthorsSelectors) {
      const link = await window.buildValidLink(coAuthor.querySelector(".gsc_rsb_a_desc a").getAttribute("href"));
      const authorIdPattern = /user=(?<id>[^&]+)/gm;                            //https://regex101.com/r/oxoQEj/1
      const authorId = link.match(authorIdPattern)[0].replace("user=", "");
      coAuthors.push({
        name: coAuthor.querySelector(".gsc_rsb_a_desc a").textContent.trim(),
        link,
        authorId,
        photo: await window.buildValidLink(coAuthor.querySelector(".gs_pp_df").getAttribute("data-src")),
        affiliations: coAuthor.querySelector(".gsc_rsb_a_ext").textContent.trim(),
        email: coAuthor.querySelector(".gsc_rsb_a_ext2")?.textContent.trim() || "email not available",
      });
    }

    return {
      name: document.querySelector("#gsc_prf_in").textContent.trim(),
      photo: await window.buildValidLink(document.querySelector("#gsc_prf_pup-img").getAttribute("src")),
      affiliations: document.querySelector(".gsc_prf_il:nth-child(2)").textContent.trim(),
      website: document.querySelector(".gsc_prf_ila").getAttribute("href") || "website not available",
      interests,
      articles,
      table: {
        citations: {
          all: document.querySelector("#gsc_rsb_st tr:nth-child(1) td:nth-child(2)").textContent.trim(),
          since2017: document.querySelector("#gsc_rsb_st tr:nth-child(1) td:nth-child(3)").textContent.trim(),
        },
        hIndex: {
          all: document.querySelector("#gsc_rsb_st tr:nth-child(2) td:nth-child(2)").textContent.trim(),
          since2017: document.querySelector("#gsc_rsb_st tr:nth-child(2) td:nth-child(3)").textContent.trim(),
        },
        i10Index: {
          all: document.querySelector("#gsc_rsb_st tr:nth-child(3) td:nth-child(2)").textContent.trim(),
          since2017: document.querySelector("#gsc_rsb_st tr:nth-child(3) td:nth-child(3)").textContent.trim(),
        },
      },
      graph: Array.from(document.querySelectorAll(".gsc_md_hist_b .gsc_g_t")).map((el, i) => {
        return {
          year: el.textContent.trim(),
          citations: document.querySelectorAll(".gsc_md_hist_b .gsc_g_al")[i].textContent.trim(),
        };
      }),
      publicAccess: {
        link: await window.buildValidLink(document.querySelector("#gsc_lwp_mndt_lnk").getAttribute("href")),
        available: document.querySelectorAll(".gsc_rsb_m_a")[0].textContent.trim(),
        notAvailable: document.querySelectorAll(".gsc_rsb_m_na")[0].textContent.trim(),
      },
      coAuthors,
    };
  }, articles);

  await browser.close();

  return scholarAuthorInfo;
}

module.exports = { getScholarAuthorInfo };
