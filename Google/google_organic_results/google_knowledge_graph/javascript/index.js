const withCheerio = require("./withCheerio");
const withSerpApi = require("./withSerpApi");

withCheerio.getKnowledgeGraphInfo().then(console.log);

withSerpApi.getResults().then(console.log);
