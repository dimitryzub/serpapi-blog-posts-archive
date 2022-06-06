const withPuppeteer = require("./withPuppeteer");
const withSerpApi = require("./withSerpApi");

withPuppeteer.getOrganicResults().then(console.log);

withSerpApi.getResults().then(console.log);
