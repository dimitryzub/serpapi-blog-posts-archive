const SerpApi = require("google-search-results-nodejs");
const search = new SerpApi.GoogleSearch(process.env.API_KEY);                     //your API key from serpapi.com

const user = "6ZiRSwQAAAAJ";                                                      // the ID of the author we want to scrape

const params = {
  engine: "google_scholar_author",                                                // search engine
  author_id: user,                                                                // author ID
  hl: "en",                                                                       // Parameter defines the language to use for the Google search
};

const getScholarAuthorData = function ({ author, articles, cited_by, public_access: publicAccess, co_authors }) {
  const { name, thumbnail: photo, affiliations, website = "website not available", interests } = author;
  const { table, graph } = cited_by;
  return {
    name,
    photo,
    affiliations,
    website,
    interests:
      interests?.map((interest) => {
        const { title, link = "link not available" } = interest;
        return {
          title,
          link,
        };
      }) || "no interests",
    articles: articles?.map((article) => {
      const { title, link = "link not available", authors, publication, cited_by, year } = article;
      return {
        title,
        link,
        authors,
        publication,
        citedBy: {
          link: cited_by.link,
          cited: cited_by.value,
        },
        year,
      };
    }),
    table: {
      citations: {
        all: table[0].citations.all,
        since2017: table[0].citations.since_2017,
      },
      hIndex: {
        all: table[1].h_index.all,
        since2017: table[1].h_index.since_2017,
      },
      i10Index: {
        all: table[2].i10_index.all,
        since2017: table[2].i10_index.since_2017,
      },
    },
    graph,
    publicAccess,
    coAuthors: co_authors?.map((result) => {
      const { name, link = "link not available", thumbnail: photo, affiliations, email = "no email info", author_id } = result;
      return {
        name,
        link,
        author_id,
        photo,
        affiliations,
        email,
      };
    }),
  };
};

const getJson = () => {
  return new Promise((resolve) => {
    search.json(params, resolve);
  });
};

exports.getResults = () => {
  return getJson().then(getScholarAuthorData);
};
