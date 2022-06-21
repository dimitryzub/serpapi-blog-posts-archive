const cheerio = require("cheerio");
const axios = require("axios");

const user = "6ZiRSwQAAAAJ";                                       // the ID of the author we want to scrape

const domain = `http://scholar.google.com`;

const AXIOS_OPTIONS = {
  headers: {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36",
  },                                                              // adding the User-Agent header as one way to prevent the request from being blocked
  params: {
    user,
    hl: "en",                                                     // parameter defines the language to use for the Google search
  },
};

function buildValidLink(rawLink) {
  if (!rawLink || rawLink.includes("javascript:void(0)")) return "link not available";
  if (rawLink.includes("scholar.googleusercontent")) return rawLink;
  return domain + rawLink;
}

function getScholarAuthorInfo() {
  return axios.get(`${domain}/citations`, AXIOS_OPTIONS).then(function ({ data }) {
    let $ = cheerio.load(data);

    return {
      name: $("#gsc_prf_in").text().trim(),
      photo: buildValidLink($("#gsc_prf_pup-img").attr("src")),
      affiliations: $(".gsc_prf_il:nth-child(2)").text().trim(),
      website: $(".gsc_prf_ila").attr("href") || "website not available",
      interests: Array.from($("#gsc_prf_int a")).map((interest) => {
        return {
          title: $(interest).text().trim(),
          link: buildValidLink($(interest).attr("href")),
        };
      }),
      articles: Array.from($(".gsc_a_tr")).map((el) => {
        return {
          title: $(el).find(".gsc_a_at").text().trim(),
          link: buildValidLink($(el).find(".gsc_a_at").attr("href")),
          authors: $(el).find(".gs_gray:first-of-type").text().trim(),
          publication: $(el).find(".gs_gray:last-of-type").text().trim(),
          citedBy: {
            link: $(el).find(".gsc_a_ac").attr("href"),
            cited: $(el).find(".gsc_a_ac").text().trim(),
          },
          year: $(el).find(".gsc_a_h").text().trim(),
        };
      }),
      table: {
        citations: {
          all: $("#gsc_rsb_st tr:nth-child(1) td:nth-child(2)").text().trim(),
          since2017: $("#gsc_rsb_st tr:nth-child(1) td:nth-child(3)").text().trim(),
        },
        hIndex: {
          all: $("#gsc_rsb_st tr:nth-child(2) td:nth-child(2)").text().trim(),
          since2017: $("#gsc_rsb_st tr:nth-child(2) td:nth-child(3)").text().trim(),
        },
        i10Index: {
          all: $("#gsc_rsb_st tr:nth-child(3) td:nth-child(2)").text().trim(),
          since2017: $("#gsc_rsb_st tr:nth-child(3) td:nth-child(3)").text().trim(),
        },
      },
      graph: Array.from($(".gsc_md_hist_b .gsc_g_t")).map((el, i) => {
        return {
          year: $(el).text().trim(),
          citations: $(Array.from($(".gsc_md_hist_b .gsc_g_al"))[i])
            .text()
            .trim(),
        };
      }),
      publicAccess: {
        link: buildValidLink($("#gsc_lwp_mndt_lnk").attr("href")),
        available: $(Array.from($(".gsc_rsb_m_a"))[0])
          .text()
          .trim(),
        notAvailable: $(Array.from($(".gsc_rsb_m_na"))[0])
          .text()
          .trim(),
      },
      coAuthors: Array.from($("#gsc_rsb_co .gsc_rsb_aa")).map((el) => {
        const link = buildValidLink($(el).find(".gsc_rsb_a_desc a").attr("href"));
        const pattern = /user=(?<id>[^&]+)/gm;                                  //https://regex101.com/r/oxoQEj/1
        const author_id = link.match(pattern)[0].replace("user=", "");
        return {
          name: $(el).find(".gsc_rsb_a_desc a").text().trim(),
          link,
          author_id,
          photo: buildValidLink($(el).find(".gs_pp_df").attr("data-src")),
          affiliations: $(el).find(".gsc_rsb_a_ext").text().trim(),
          email: $(el).find(".gsc_rsb_a_ext2")?.text().trim() || "email not available",
        };
      }),
    };
  });
}

module.exports = { getScholarAuthorInfo };
