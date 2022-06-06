const withCheerio = require("./withCheerio");
const withSerpApi = require("./withSerpApi");

withCheerio.getMainPageInfo().then(console.log);

withSerpApi.getResults().then(console.log);
