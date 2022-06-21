<h2 id='what'>What will be scraped</h2>

![image](https://user-images.githubusercontent.com/64033139/174759913-a52497b3-4e7b-450f-ba57-cde8b26abe77.png)

<h2 id='preparation'>Preparation</h2>

First, we need to create a Node.js* project and add [`npm`](https://www.npmjs.com/) packages [`cheerio`](https://www.npmjs.com/package/cheerio) to parse parts of the HTML markup, and [`axios`](https://www.npmjs.com/package/axios) to make a request to a website. To do this, in the directory with our project, open the command line and enter `npm init -y`, and then `npm i cheerio axios`.

*<span style="font-size: 15px;">If you don't have Node.js installed, you can [download it from nodejs.org](https://nodejs.org/en/) and follow the installation [documentation](https://nodejs.dev/learn/introduction-to-nodejs).</span>

<h2 id='process'>Process</h2>

[SelectorGadget Chrome extension](https://chrome.google.com/webstore/detail/selectorgadget/mhjhnkcfbdhnjickkkdbjoemdmbfginb) was used to grab CSS selectors by clicking on the desired element in the browser. If you have any struggles understanding this, we have a dedicated [Web Scraping with CSS Selectors blog post](https://serpapi.com/blog/web-scraping-with-css-selectors-using-python/) at SerpApi.
The Gif below illustrates the approach of selecting different parts of the results.

![how](https://user-images.githubusercontent.com/64033139/174762205-b5c81b51-423d-47b3-aa66-84d27de09db8.gif)

📌Note: you can get user ID from Google Scholar using my guide [How to scrape Google Scholar profiles results with Node.js](https://serpapi.com/blog/p/4ca36c41-4dda-4782-bb41-0b4562010a60/).

<h2 id='full_code'>Full code</h2>

```javascript
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

getScholarAuthorInfo().then(console.log);
```

<h3 id='code_explanation'>Code explanation</h3>

Declare constants from required libraries:

```javascript
const cheerio = require("cheerio");
const axios = require("axios");
```
        
|Code|Explanation|
|----|-----------|
|[`cheerio`](https://www.npmjs.com/package/cheerio)|library for parsing the html page and access the necessary selectors|
|[`axios`](https://www.npmjs.com/package/axios)|library for requesting the desired html document|

Next, we write in constants user ID and the necessary parameters for making a request:

```javascript
const user = "6ZiRSwQAAAAJ";

const domain = `http://scholar.google.com`;

const AXIOS_OPTIONS = {
  headers: {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36",
  },
  params: {
    user,
    hl: "en",
  },
};
```

|Code|Explanation|
|----|-----------|
|`user`|user ID from Google Scholar|
|`headers`|[HTTP headers](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers) let the client and the server pass additional information with an HTTP request or response|
|[`User-Agent`](https://developer.mozilla.org/en-US/docs/Glossary/User_agent)|is used to act as a "real" user visit. Default axios requests user-agent is `axios/0.27.2` so websites understand that it's a script that sends a request and might block it. [Check what's your user-agent](https://www.whatismybrowser.com/detect/what-is-my-user-agent/).|
|`hl`|parameter defines the language to use for the Google search|

Next, we write a function that helps us change the raw links to the correct links:

```javascript
function buildValidLink(rawLink) {
  if (!rawLink || rawLink.includes("javascript:void(0)")) return "link not available";
  if (rawLink.includes("scholar.googleusercontent")) return rawLink;
  return domain + rawLink;
}
```

We need to do this with links because they are of different types. For example, some links start with "/citations", some already have a complete and correct link, and some no links.
        
And finally a function to get the necessary information:

```javascript
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
        const pattern = /user=(?<id>[^&]+)/gm;
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
```

|Code|Explanation|
|----|-----------|
|`function ({ data })`|we received the response from axios request that have `data` key that we [destructured](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Destructuring_assignment) (this entry is equal to `function (response)` and in the next line `cheerio.load(response.data)`)|
|`.attr('href')`|gets the `href` attribute value of the html element|
|`$(el).find('.gsc_a_at')`|finds element with class name `gsc_a_at` in all child elements and their children of `el` html element|
|`.text()`|gets the raw text of html element|
|[`.trim()`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/trim)|removes whitespace from both ends of a string|
|`pattern`|a RegEx pattern for search and define author id. [See what it allows you to find](https://regex101.com/r/oxoQEj/1)|
|`link.match(pattern)[0].replace('user=', '')`|in this line, we find a substring that matches `pattern`, take `0` element from the matches array and remove "user=" part|

Now we can launch our parser. To do this enter `node YOUR_FILE_NAME` in your command line. Where `YOUR_FILE_NAME` is the name of your `.js` file.

<h2 id='output'>Output</h2>

```json
{
   "name":"Gustavo E. Scuseria",
   "photo":"https://scholar.googleusercontent.com/citations?view_op=medium_photo&user=6ZiRSwQAAAAJ&citpid=2",
   "affiliations":"Welch Professor of Chemistry, Physics & Astronomy, and Materials Science & NanoEngineering",
   "website":"http://scuseria.rice.edu/",
   "interests":[
      {
         "title":"Quantum Chemistry",
         "link":"http://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=label:quantum_chemistry"
      },
      {
         "title":"Electronic Structure",
         "link":"http://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=label:electronic_structure"
      },
      ... and other interests
   ],
   "articles":[
      {
         "title":"Gaussian",
         "link":"http://scholar.google.com/citations?view_op=view_citation&hl=en&user=6ZiRSwQAAAAJ&citation_for_view=6ZiRSwQAAAAJ:zYLM7Y9cAGgC",
         "authors":"M Frisch, GW Trucks, HB Schlegel, GE Scuseria, MA Robb, ...",
         "publication":"Inc., Wallingford, CT 200, 2009",
         "citedBy":{
            "link":"https://scholar.google.com/scholar?oi=bibs&hl=en&cites=12649774174384111814,14968720898351466124,2542640079890340298,8878124810051097364,2098631159866273549,2628790197996155063,9956613247733821950,12319774160759231510,10858305733441610093,6078020929247912320,732977129500792336,14993646544388831080,15565517274675135746,15250043469802589020,1808091898519134639,4924449844119900931,7042231487572549326,15997103006766735356,1383260141329079090,9449439637290636341,15798026778807799939,8499548159092922473,17327920478782103127,17012586779140016045,15565399274538950872,3036342632434523386,551261585751727105,149700165324054213,2578529946445560518",
            "cited":"120296"
         },
         "year":"2009"
      },
      {
         "title":"Gaussian 03, revision C. 02",
         "link":"http://scholar.google.com/citations?view_op=view_citation&hl=en&user=6ZiRSwQAAAAJ&citation_for_view=6ZiRSwQAAAAJ:oC1yQlCKEqoC",
         "authors":"MJ Frisch, GW Trucks, HB Schlegel, GE Scuseria, MA Robb, ...",
         "publication":"Gaussian, Inc., Wallingford, CT, 2004",
         "citedBy":{
            "link":"https://scholar.google.com/scholar?oi=bibs&hl=en&cites=5576070979585392002,14227769557982606857",
            "cited":"25832"
         },
         "year":"2004"
      },
      ... and other articles
   ],
   "table":{
      "citations":{
         "all":"295108",
         "since2017":"113669"
      },
      "hIndex":{
         "all":"139",
         "since2017":"76"
      },
      "i10Index":{
         "all":"552",
         "since2017":"357"
      }
   },
   "graph":[
      {
         "year":"1993",
         "citations":"771"
      },
      {
         "year":"1994",
         "citations":"782"
      },
      ... and other years
   ],
   "publicAccess":{
      "link":"http://scholar.google.com/citations?view_op=list_mandates&hl=en&user=6ZiRSwQAAAAJ",
      "available":"89 articles",
      "notAvailable":"5 articles"
   },
   "coAuthors":[
      {
         "name":"John P. Perdew",
         "link":"http://scholar.google.com/citations?user=09nv75wAAAAJ&hl=en",
         "author_id":"09nv75wAAAAJ",
         "photo":"https://scholar.googleusercontent.com/citations?view_op=small_photo&user=09nv75wAAAAJ&citpid=2",
         "affiliations":"Temple UniversityVerified email at temple.edu",
         "email":"Verified email at temple.edu"
      },
      {
         "name":"Viktor N. Staroverov",
         "link":"http://scholar.google.com/citations?user=eZqrRYEAAAAJ&hl=en",
         "author_id":"eZqrRYEAAAAJ",
         "photo":"https://scholar.googleusercontent.com/citations?view_op=small_photo&user=eZqrRYEAAAAJ&citpid=2",
         "affiliations":"Professor, The University of Western OntarioVerified email at uwo.ca",
         "email":"Verified email at uwo.ca"
      },
      ... and other co-authors
   ]
}
```

<h2 id='serp_api'>Google Scholar Author API</h2>

Alternatively, you can use the [Google Scholar Author API](https://serpapi.com/google-scholar-author-api) from SerpApi. SerpApi is a free API with 100 search per month. If you need more searches, there are paid plans.

The difference is that you won't have to write code from scratch and maintain it. You may also experience blocking from Google and changing the selected selectors. Using a ready-made solution from SerpAPI, you just need to iterate the received JSON. [Check out the playground](https://serpapi.com/playground).

First we need to install [`google-search-results-nodejs`](https://www.npmjs.com/package/google-search-results-nodejs). To do this you need to enter in your console: `npm i google-search-results-nodejs`

```javascript
require("dotenv").config();
const SerpApi = require("google-search-results-nodejs");
const search = new SerpApi.GoogleSearch(process.env.API_KEY);             //your API key from serpapi.com

const user = "6ZiRSwQAAAAJ";                                                      // the ID of the author we want to scrape

const params = {
  engine: "google_scholar_author",                                                // search engine
  author_id: user,                                                                // author ID
  hl: "en",                                                                       // Parameter defines the language to use for the Google search
};

const getScholarAuthorData = function ({ author, articles, cited_by, public_access: publicAccess, co_authors }) {
  const { name, thumbnail: photo, affiliations, website = "website not available", interests } = author;
  const { table, graph } = cited_by;
  return {
    name,
    photo,
    affiliations,
    website,
    interests:
      interests?.map((interest) => {
        const { title, link = "link not available" } = interest;
        return {
          title,
          link,
        };
      }) || "no interests",
    articles: articles?.map((article) => {
      const { title, link = "link not available", authors, publication, cited_by, year } = article;
      return {
        title,
        link,
        authors,
        publication,
        citedBy: {
          link: cited_by.link,
          cited: cited_by.value,
        },
        year,
      };
    }),
    table: {
      citations: {
        all: table[0].citations.all,
        since2017: table[0].citations.since_2017,
      },
      hIndex: {
        all: table[1].h_index.all,
        since2017: table[1].h_index.since_2017,
      },
      i10Index: {
        all: table[2].i10_index.all,
        since2017: table[2].i10_index.since_2017,
      },
    },
    graph,
    publicAccess,
    coAuthors: co_authors?.map((result) => {
      const { name, link = "link not available", thumbnail: photo, affiliations, email = "no email info", author_id } = result;
      return {
        name,
        link,
        author_id,
        photo,
        affiliations,
        email,
      };
    }),
  };
};

const getJson = () => {
  return new Promise((resolve) => {
    search.json(params, resolve);
  });
};

getJson().then(getScholarAuthorData).then(console.log);
```

<h3 id='serp_api_code_explanation'>Code explanation</h3>

Declare constants from required libraries:

```javascript
const SerpApi = require("google-search-results-nodejs");
const search = new SerpApi.GoogleSearch(API_KEY);
```

|Code|Explanation|
|----|-----------|
|`SerpApi`|SerpApi Node.js library|
|`search`|new instance of GoogleSearch class|
|`API_KEY`|your API key from [SerpApi](https://serpapi.com/manage-api-key)|

Next, we write down what we want to search and the necessary parameters for making a request:

```javascript
const user = "6ZiRSwQAAAAJ";

const params = {
  engine: "google_scholar_author",
  author_id: user,
  hl: "en",
};
```

|Code|Explanation|
|----|-----------|
|`user`|user ID from Google Scholar|
|`engine`|search engine|
|`hl`|parameter defines the language to use for the Google search|

Next, we write a callback function in which we describe what data we need from the result of our request:

```javascript
const getScholarAuthorData = function ({ author, articles, cited_by, public_access: publicAccess, co_authors }) {
  const { name, thumbnail: photo, affiliations, website = "website not available", interests } = author;
  const { table, graph } = cited_by;
  return {
    name,
    photo,
    affiliations,
    website,
    interests:
      interests?.map((interest) => {
        const { title, link = "link not available" } = interest;
        return {
          title,
          link,
        };
      }) || "no interests",
    articles: articles?.map((article) => {
      const { title, link = "link not available", authors, publication, cited_by, year } = article;
      return {
        title,
        link,
        authors,
        publication,
        citedBy: {
          link: cited_by.link,
          cited: cited_by.value,
        },
        year,
      };
    }),
    table: {
      citations: {
        all: table[0].citations.all,
        since2017: table[0].citations.since_2017,
      },
      hIndex: {
        all: table[1].h_index.all,
        since2017: table[1].h_index.since_2017,
      },
      i10Index: {
        all: table[2].i10_index.all,
        since2017: table[2].i10_index.since_2017,
      },
    },
    graph,
    publicAccess,
    coAuthors: co_authors?.map((result) => {
      const { name, link = "link not available", thumbnail: photo, affiliations, email = "no email info", author_id } = result;
      return {
        name,
        link,
        author_id,
        photo,
        affiliations,
        email,
      };
    }),
  };
};
```

|Code|Explanation|
|----|-----------|
|`author, articles, ..., co_authors`|data that we destructured from response|
|`name, thumbnail, ..., interests`|data that we destructured from `author` object|
|`thumbnail: photo`|we redefine destructured data `thumbnail` to new `photo`|
|`website = "website not available"`|we set default value `website not available` if `website` is `undefined`|

Next, we wrap the search method from the SerpApi library in a promise to further work with the search results and run it:

```javascript
const getJson = () => {
  return new Promise((resolve) => {
    search.json(params, resolve);
  })
}

getJson().then(getScholarAuthorData).then(console.log);
```

<h2 id='serp_api_output'>Output</h2>

```json
{
   "name":"Gustavo E. Scuseria",
   "photo":"https://scholar.googleusercontent.com/citations?view_op=medium_photo&user=6ZiRSwQAAAAJ&citpid=2",
   "affiliations":"Welch Professor of Chemistry, Physics & Astronomy, and Materials Science & NanoEngineering",
   "website":"http://scuseria.rice.edu/",
   "interests":[
      {
         "title":"Quantum Chemistry",
         "link":"https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=label:quantum_chemistry"
      },
      {
         "title":"Electronic Structure",
         "link":"https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=label:electronic_structure"
      },
      ... and other interests
   ],
   "articles":[
      {
         "title":"Gaussian",
         "link":"https://scholar.google.com/citations?view_op=view_citation&hl=en&user=6ZiRSwQAAAAJ&citation_for_view=6ZiRSwQAAAAJ:zYLM7Y9cAGgC",
         "authors":"M Frisch, GW Trucks, HB Schlegel, GE Scuseria, MA Robb, ...",
         "publication":"Inc., Wallingford, CT 200, 2009",
         "citedBy":{
            "link":"https://scholar.google.com/scholar?oi=bibs&hl=en&cites=12649774174384111814,14968720898351466124,2542640079890340298,8878124810051097364,2098631159866273549,2628790197996155063,9956613247733821950,12319774160759231510,10858305733441610093,6078020929247912320,732977129500792336,14993646544388831080,15565517274675135746,15250043469802589020,1808091898519134639,4924449844119900931,7042231487572549326,15997103006766735356,1383260141329079090,9449439637290636341,15798026778807799939,8499548159092922473,17327920478782103127,17012586779140016045,15565399274538950872,3036342632434523386,551261585751727105,149700165324054213,2578529946445560518",
            "cited":120296
         },
         "year":"2009"
      },
      {
         "title":"Gaussian 03, revision C. 02",
         "link":"https://scholar.google.com/citations?view_op=view_citation&hl=en&user=6ZiRSwQAAAAJ&citation_for_view=6ZiRSwQAAAAJ:oC1yQlCKEqoC",
         "authors":"MJ Frisch, GW Trucks, HB Schlegel, GE Scuseria, MA Robb, ...",
         "publication":"Gaussian, Inc., Wallingford, CT, 2004",
         "citedBy":{
            "link":"https://scholar.google.com/scholar?oi=bibs&hl=en&cites=5576070979585392002,14227769557982606857",
            "cited":25832
         },
         "year":"2004"
      },
      ... and other articles
   ],
   "table":{
      "citations":{
         "all":295108,
         "since2017":113669
      },
      "hIndex":{
         "all":139,
         "since2017":76
      },
      "i10Index":{
         "all":552,
         "since2017":357
      }
   },
   "graph":[
      {
         "year":1993,
         "citations":771
      },
      {
         "year":1994,
         "citations":782
      },
      ... and other years
   ],
   "publicAccess":{
      "link":"https://scholar.google.com/citations?view_op=list_mandates&hl=en&user=6ZiRSwQAAAAJ",
      "available":89,
      "not_available":5
   },
   "coAuthors":[
      {
         "name":"John P. Perdew",
         "link":"https://scholar.google.com/citations?user=09nv75wAAAAJ&hl=en",
         "author_id":"09nv75wAAAAJ",
         "photo":"https://scholar.googleusercontent.com/citations?view_op=small_photo&user=09nv75wAAAAJ&citpid=2",
         "affiliations":"Temple University",
         "email":"Verified email at temple.edu"
      },
      {
         "name":"Viktor N. Staroverov",
         "link":"https://scholar.google.com/citations?user=eZqrRYEAAAAJ&hl=en",
         "author_id":"eZqrRYEAAAAJ",
         "photo":"https://scholar.googleusercontent.com/citations?view_op=small_photo&user=eZqrRYEAAAAJ&citpid=2",
         "affiliations":"Professor, The University of Western Ontario",
         "email":"Verified email at uwo.ca"
      },
      ... and other co-authors
   ]
}
```

<h2 id='links'>Links</h2>

* [Code in the online IDE](https://replit.com/@MikhailZub/Google-Scholar-Author-NodeJS-SerpApi#index.js) 
* [Google Scholar API](https://serpapi.com/google-scholar-api)

If you want to see some project made with SerpApi, please write me a message.

___
<p style="text-align: center;">Join us on <a href="https://twitter.com/serp_api">Twitter</a> | <a href="https://www.youtube.com/channel/UCUgIHlYBOD3yA3yDIRhg_mg">YouTube</a></p>
<p style="text-align: center;">Add a  <a href="https://github.com/serpapi/public-roadmap/issues">Feature Request</a>💫 or a <a href="https://github.com/serpapi/public-roadmap/issues">Bug</a>🐞</p>