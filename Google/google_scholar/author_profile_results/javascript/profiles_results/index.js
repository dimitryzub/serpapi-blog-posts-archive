const withCheerio = require("./withCheerio");
const withSerpApi = require("./withSerpApi");

withCheerio.startScrape().then((result) => console.dir(result, { depth: null }));

// withSerpApi.getResults().then((result) => console.dir(result, { depth: null }));
