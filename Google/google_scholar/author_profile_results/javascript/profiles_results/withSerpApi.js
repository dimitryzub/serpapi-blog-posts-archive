require("dotenv").config();
const SerpApi = require("google-search-results-nodejs");
const search = new SerpApi.GoogleSearch(process.env.API_KEY); //your API key from serpapi.com

const searchString = "astronomy";                         // what we want to search
const pagesLimit = 5;                                     // limit of pages for getting info
let currentPage = 1;                                      // current page of the search

const params = {
  engine: "google_scholar_profiles",                      // search engine
  mauthors: searchString,                                 // search query
  hl: "en",                                               // Parameter defines the language to use for the Google search
};

const getScholarProfilesData = function ({ profiles }) {
  return profiles.map((result) => {
    const { name, link = "link not available", author_id, thumbnail, affiliations, email = "no email info", cited_by, interests } = result;
    return {
      name,
      link,
      author_id,
      photo: thumbnail,
      affiliations,
      email,
      cited_by,
      interests:
        interests?.map((interest) => {
          const { title, link = "link not available" } = interest;
          return {
            title,
            link,
          };
        }) || "no interests",
    };
  });
};

const getJson = (params) => {
  return new Promise((resolve) => {
    search.json(params, resolve);
  });
};

exports.getResults = async () => {
  const profilesResults = [];
  let nextPageToken;
  while (true) {
    if (currentPage > pagesLimit) break;
    const json = await getJson(params);
    nextPageToken = json.pagination.next_page_token;
    params.after_author = nextPageToken;
    profilesResults.push(...(await getScholarProfilesData(json)));
    if (!nextPageToken) break;
    currentPage++;
  }
  return profilesResults;
};
