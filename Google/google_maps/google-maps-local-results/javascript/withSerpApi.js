require("dotenv").config();
const SerpApi = require("google-search-results-nodejs");
const search = new SerpApi.GoogleSearch(process.env.API_KEY); //your API key from serpapi.com

const searchString = "starbucks"; // what we want to search

const params = {
  engine: "google_maps", // search engine
  q: searchString, // search query
  hl: "en", // parameter defines the language to use for the Google search
  ll: "@47.6040174,-122.1854488,11z", // parameter defines GPS coordinates of location where you want your query to be applied
  type: "search", // parameter defines the type of search you want to make
};

const getJson = () => {
  return new Promise((resolve) => {
    search.json(params, resolve);
  });
};

exports.getResults = async () => {
  const allPlaces = [];
  while (true) {
    const json = await getJson();
    if (json.local_results) {
      allPlaces.push(...json.local_results)
    } else break;
    if (json.serpapi_pagination?.next) {
      !params.start ? (params.start = 20) : (params.start += 20);
    } else break;
  }
  return allPlaces;
};
