require("dotenv").config();
const SerpApi = require("google-search-results-nodejs");
const search = new SerpApi.GoogleSearch(process.env.API_KEY); //your API key from serpapi.com

const searchString = "astronomy"; // what we want to search
const pagesLimit = Infinity; // limit of pages for getting info
let currentPage = 1; // current page of the search

const params = {
  engine: "google_scholar", // search engine
  q: searchString, // search query
  hl: "en", // Parameter defines the language to use for the Google search
};

const getJson = () => {
  return new Promise((resolve) => {
    search.json(params, resolve);
  });
};

exports.getResults = async () => {
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
