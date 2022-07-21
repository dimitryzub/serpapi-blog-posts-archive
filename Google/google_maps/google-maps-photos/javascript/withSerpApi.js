require("dotenv").config();
const SerpApi = require("google-search-results-nodejs");
const search = new SerpApi.GoogleSearch(process.env.API_KEY); //your API key from serpapi.com

const dataId = "0x549069a98254bd17:0xb2f64f75b3edf4c3"; // data ID parameter

const params = {
  engine: "google_maps_photos", // search engine
  hl: "en", // parameter defines the language to use for the Google search
  data_id: dataId, // parameter defines the Google Maps data ID
};

const getJson = () => {
  return new Promise((resolve) => {
    search.json(params, resolve);
  });
};

exports.getResults = async () => {
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
