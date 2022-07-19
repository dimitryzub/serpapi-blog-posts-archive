require("dotenv").config();
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

exports.getResults = async () => {
  const {place_results} = await getJson();
  return place_results;
};
