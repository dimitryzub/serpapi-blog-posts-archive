const cheerio = require("cheerio");
const axios = require("axios");

const AXIOS_OPTIONS = {
    headers: {
        "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36",
    },                                                  // adding the User-Agent header as one way to prevent the request from being blocked
    params: {
        hl: 'en',                                       // Parameter defines the language to use for the Google search
        gl: 'us'                                        // parameter defines the country to use for the Google search
    },
};

function getMainPageInfo() {
    return axios
        .get(`https://play.google.com/store/apps`, AXIOS_OPTIONS)
        .then(function ({ data }) {
            let $ = cheerio.load(data);

            const mainPageInfo = Array.from($('.Ktdaqe')).reduce((result, block) => {
                const categoryTitle = $(block).find('.sv0AUd').text().trim()
                const apps = Array.from($(block).find('.WHE7ib')).map((app) => {
                    return {
                        title: $(app).find('.WsMG1c').text().trim(),
                        developer: $(app).find('.b8cIId .KoLSrc').text().trim(),
                        link: `https://play.google.com${$(app).find('.b8cIId a').attr('href')}`,
                        rating: parseFloat($(app).find('.pf5lIe > div').attr('aria-label').slice(6, 9)),
                    }
                })
                return {
                    ...result, [categoryTitle]: apps
                }

            }, {})

            return mainPageInfo;
        });
}

module.exports = { getMainPageInfo }

