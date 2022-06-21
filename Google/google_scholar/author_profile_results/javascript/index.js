const withCheerio = require("./withCheerio");
const withSerpApi = require("./withSerpApi");

withCheerio.startScrape().then(console.log);

// withSerpApi.getResults().then(console.log);
