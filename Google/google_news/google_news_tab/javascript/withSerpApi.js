// https://dev.to/mikhailzub/how-to-scrape-google-news-with-nodejs-3el6-temp-slug-8721582?preview=1edd6335ce816828245e9c39bcb357a0659ed993467a7d129d31619d42fd4b71c9cbbfbc9339fb350aa89fd78e72ba6564e96a3ecc83792f5396ea6d

require('dotenv').config()
const SerpApi = require("google-search-results-nodejs");
const search = new SerpApi.GoogleSearch(process.env.API_KEY);

const searchString = "elon musk";                        // what we want to search

const params = {
  engine: "google",                                     // search engine
  q: searchString,                                      // search query
  google_domain: "google.com",                          // google domain of the search
  gl: "us",                                             // parameter defines the country to use for the Google search
  hl: "en",                                             // Parameter defines the language to use for the Google search
  tbm: "nws"                                            // parameter defines the type of search you want to do ("nws" means news)
};

const getNewsData = function ({ news_results }) {
  return news_results.map((result) => {
    const { link, title, source, date, snippet, thumbnail: image = "No image" } = result;
    return {
      link,
      source,
      title: title.replace('\n', ''),
      snippet: snippet.replace('\n', ''),
      image,
      date,
    }
  })
};

const getJson = (params) => {
  return new Promise((resolve) => {
    search.json(params, resolve);
  })
}

exports.getResults = () => {
  return getJson(params).then(getNewsData)
}