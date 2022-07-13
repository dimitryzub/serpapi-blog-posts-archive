const withPuppeteer = require("./withPuppeteer");
const withSerpApi = require("./withSerpApi");

withPuppeteer.getLocalPlacesInfo().then(console.log);

// withSerpApi.getResults().then((result) => console.dir(result, { depth: null }));
