const SerpApi = require("google-search-results-nodejs");
const search = new SerpApi.GoogleSearch(process.env.API_KEY);         //your API key from serpapi.com

const searchString = "artificial intelligence";                       // what we want to search

const params = {
  engine: "google_scholar",                                           // search engine
  q: searchString,                                                    // search query
  hl: "en",                                                           // Parameter defines the language to use for the Google search
};

const getScholarData = function ({ organic_results }) {
  return organic_results.map((result) => {
    const { title, link = "link not available", snippet, publication_info, inline_links, resources } = result;
    return {
      title,
      link,
      publication_info: publication_info?.summary,
      snippet,
      document: resources?.map((el) => el.link)[0] || "document not available",
      cited_by: inline_links?.cited_by?.link || "link not available",
      related_articles: inline_links?.related_pages_link || "link not available",
      all_versions: inline_links?.versions?.link || "link not available",
    };
  });
};

const getJson = (params) => {
  return new Promise((resolve) => {
    search.json(params, resolve);
  });
};

exports.getResults = () => {
  return getJson(params).then(getScholarData);
};
