const withPuppeteer = require("./withPuppeteer");
const withSerpApi = require("./withSerpApi");

// withPuppeteer.getScholarAuthorInfo().then((result) => console.dir(result, { depth: null }));

withSerpApi.getResults().then((result) => console.dir(result, { depth: null }));
