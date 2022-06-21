const withCheerio = require("./withCheerio");
const withSerpApi = require("./withSerpApi");

// withCheerio.getScholarOrganicResults().then(console.log);

withSerpApi.getResults().then(console.log);
