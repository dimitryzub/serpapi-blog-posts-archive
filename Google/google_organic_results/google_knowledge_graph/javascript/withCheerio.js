const cheerio = require("cheerio");
const axios = require("axios");

const searchString = "tesla";                                    // what we want to search
const encodedString = encodeURI(searchString);              // what we want to search for in a browser-friendly language

const domain = `http://google.com`;                             // google domain of the search

const AXIOS_OPTIONS = {
  headers: {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36",
  },                                                            // adding the User-Agent header as one way to prevent the request from being blocked
  params: {
    q: encodedString,                                           // our encoded search string
    hl: "en",                                                   // Parameter defines the language to use for the Google search
    gl: "us",                                                   // parameter defines the country to use for the Google search
  },
};

function getKnowledgeGraphInfo() {
  return axios.get(`${domain}/search`, AXIOS_OPTIONS).then(function ({ data }) {
    let $ = cheerio.load(data);

    const pattern = /s='(?<img>[^']+)';\w+\s\w+=\['(?<id>\w+_\d+)'];/gm;
    const images = [...data.matchAll(pattern)].map(({ groups }) => ({ id: groups.id, img: groups.img.replace(/\\x3d/gi, "") }));

    const allInfo = {
      title: $(".I6TXqe .qrShPb span").text().trim(),
      type: $(".I6TXqe .wwUB2c span").text().trim(),
      image: images.find(({ id }) => id === $(".I6TXqe .FZylgf img")?.attr("id")).img,
      website: $(".I6TXqe .B1uW2d").attr("href"),
      description: {
        text: $(".I6TXqe .hb8SAc span:nth-child(2)").text().trim(),
        source: $(".I6TXqe .hb8SAc span:nth-child(3) a").text().trim(),
        link: $(".I6TXqe .hb8SAc span:nth-child(3) a").attr("href"),
      },
      main: Array.from($(".I6TXqe .wDYxhc .Z1hOCe")).reduce((acc, el) => {
        const key = $(el).find(".w8qArf a").text().trim();
        return { ...acc, [key]: $(el).find(".kno-fv").text() };
      }, {}),
      profiles: Array.from($(".I6TXqe .OOijTb .fl")).reduce((acc, el) => {
        const key = $(el).find(".CtCigf").text().trim();
        return { ...acc, [key]: $(el).find("a").attr("href") };
      }, {}),
      peopleAlsoSearchFor: Array.from($(".I6TXqe .VLkRKc").closest(".UDZeY").find(".Wr0c6d")).reduce((acc, el) => {
        const key = $(el).text().trim();
        return { ...acc, [key]: domain + $(el).attr("href") };
      }, {}),
    };

    return allInfo;
  });
}

module.exports = { getKnowledgeGraphInfo };
