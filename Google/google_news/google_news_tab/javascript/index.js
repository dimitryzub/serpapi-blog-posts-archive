const withCheerio = require("./withCheerio");
const withSerpApi = require("./withSerpApi");

withCheerio.getNewsInfo().then(console.log);

withSerpApi.getResults().then(console.log);
