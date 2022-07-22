const withPuppeteer = require("./withPuppeteer");
const withSerpApi = require("./withSerpApi");

// withPuppeteer.getLocalPlaceInfo().then((result) => console.dir(result, { depth: null }));

withSerpApi.getResults().then((result) => console.dir(result, { depth: null }));
