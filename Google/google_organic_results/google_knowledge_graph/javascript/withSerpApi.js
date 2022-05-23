const SerpApi = require("google-search-results-nodejs");
const search = new SerpApi.GoogleSearch(process.env.API_KEY);

const searchString = "tesla";                           // what we want to search

const params = {
  engine: "google",                                     // search engine
  q: searchString,                                      // search query
  google_domain: "google.com",                          // google domain of the search
  gl: "us",                                             // parameter defines the country to use for the Google search
  hl: "en",                                             // Parameter defines the language to use for the Google search
};

const getKnowledgeGraph = function ({ knowledge_graph }) {
  const allInfo = {
    title: '',
    type: '',
    image: '',
    website: '',
    description: {},
    main: {},
    profiles: {},
    peopleAlsoSearchFor: {}
  } 
    for (const key in knowledge_graph) {
        if (key.includes('_link') || key.includes('_stick') || key === "see_results_about") {
        } else if (key === 'title') {
          allInfo.title = knowledge_graph[key]
        } else if (key === 'type') {
          allInfo.type = knowledge_graph[key]
        } else if (key === 'image') {
          allInfo.image = knowledge_graph[key]
        } else if (key === 'website') {
          allInfo.website = knowledge_graph[key]
        } else if (key === 'description') {
          allInfo.description.text = knowledge_graph[key];
        } else if (key === 'source') {
          allInfo.description.source = knowledge_graph[key].name;
          allInfo.description.link = knowledge_graph[key].link;
        } else if (key === 'profiles') {
          allInfo.profiles = knowledge_graph[key].reduce((acc, el) => {
            return { ...acc, [el.name]: el.link };
          }, {});
        } else if (key === 'people_also_search_for') {
          allInfo.peopleAlsoSearchFor = knowledge_graph[key].reduce((acc, el) => {
            return { ...acc, [el.name]: el.link };
          }, {});
        } else {
          allInfo.main = {...allInfo.main, [key]: knowledge_graph[key]}
    }
  }
  return allInfo
};

const getJson = (params) => {
  return new Promise((resolve) => {
    search.json(params, resolve);
  })
}

exports.getResults = () => {
  return getJson(params).then(getKnowledgeGraph)
}