const withCheerio = require("./withCheerio");
const withSerpApi = require("./withSerpApi");

// withCheerio.getScholarInfo().then(console.log);

withSerpApi.getResults().then(console.log);
