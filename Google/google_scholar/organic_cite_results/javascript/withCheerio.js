const cheerio = require("cheerio");
const axios = require("axios");

const searchString = "artificial intelligence";                         // what we want to search
const encodedString = encodeURI(searchString);                     // what we want to search for in URI encoding

const domain = `http://scholar.google.com`;

const AXIOS_OPTIONS = {
  headers: {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36",
  },                                                                  // adding the User-Agent header as one way to prevent the request from being blocked
  params: {
    q: encodedString,                                                 // our encoded search string
    hl: "en",                                                         // parameter defines the language to use for the Google search
  },
};

function buildValidLink(rawLink) {
  if (!rawLink || rawLink.includes("javascript:void(0)")) return "link not available";
  if (rawLink.includes("scholar.googleusercontent")) return rawLink;
  return domain + rawLink;
}

function getScholarOrganicResults() {
  return axios.get(`${domain}/scholar`, AXIOS_OPTIONS).then(function ({ data }) {
    let $ = cheerio.load(data);

    const organicResults = Array.from($(".gs_r.gs_scl")).map((el) => {
      const cited_by_rawLink = $(el).find(".gs_fl > a:nth-child(3)").attr("href");
      const related_articles_rawLink = $(el).find(".gs_fl > a:nth-child(4)").attr("href");
      const all_versions_rawLink = $(el).find(".gs_fl > a:nth-child(5)").attr("href");
      const cited_by = buildValidLink(cited_by_rawLink);
      const related_articles = buildValidLink(related_articles_rawLink);
      const all_versions = buildValidLink(all_versions_rawLink);
      return {
        title: $(el).find(".gs_rt").text().trim(),
        link: $(el).find(".gs_rt a").attr("href") || "link not available",
        publication_info: $(el).find(".gs_a").text().trim(),
        snippet: $(el).find(".gs_rs").text().trim().replace("\n", ""),
        document: $(el).find(".gs_or_ggsm a").attr("href") || "document not available",
        cited_by,
        related_articles,
        all_versions,
      };
    });
    return organicResults;
  });
}

module.exports = { getScholarOrganicResults };
