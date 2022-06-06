require('dotenv').config()
const SerpApi = require("google-search-results-nodejs");
const search = new SerpApi.GoogleSearch(process.env.API_KEY);     //your API key from serpapi.com

const params = {
  engine: "google_play",                                // search engine
  gl: "us",                                             // parameter defines the country to use for the Google search
  hl: "en",                                             // parameter defines the language to use for the Google search
  store: "apps"                                         // parameter defines the type of Google Play store
};

const getMainPageInfo = function ({ organic_results }) {
  return organic_results.reduce((result, category) => {
    const { title: categoryTitle, items } = category;
    const apps = items.map((app) => {
      const { title, link, rating, extansion } = app
      return {
        title,
        developer: extansion.name,
        link,
        rating,
      }
    })
    return {
      ...result, [categoryTitle]: apps
    }
  }, {})
};

const getJson = (params) => {
  return new Promise((resolve) => {
    search.json(params, resolve);
  })
}

exports.getResults = () => {
  return getJson(params).then(getMainPageInfo)
}