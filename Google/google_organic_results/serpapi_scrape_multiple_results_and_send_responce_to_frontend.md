👉**Briefly about the essence**: Run SerpApi `google-search-results-nodejs` client for N given keywords, store its values, and send a response to React frontend.

🔨**What is required**: [`google-search-results-nodejs`](https://www.npmjs.com/package/google-search-results-nodejs) , [`express`](https://www.npmjs.com/package/express).

___
- <a href="#what_will_be_scraped">What will be scraped</a>
- <a href="#prerequisites">Prerequisites</a>
- <a href="#process">Process</a>
- <a href="#extraction_code">Extraction Code</a>
- <a href="#front_end_code">Front-End Code</a>
- <a href="#links">Links</a>
- <a href="#outro">Outro</a>

___

<h2 id="prerequisites">Prerequisites</h2>

**Install libraries**:

```lang-none
$ npm install google-search-results-nodejs
$ npm install express 
```

___


<h2 id="extraction_code">Extraction Code</h2>

```js
const express = require("express");
const { GoogleSearch } = require("google-search-results-nodejs");
const search = new GoogleSearch(process.env.API_KEY);

const app = express();

app.set('json spaces', 2)
app.use(express.json());

// Set routes
app.get("/", (req, res) => {
  res.send("Make a request to /search?q=coffee&q=cake");
});

app.get("/search", (req, res) => {
  // The number of queries should be limited in a real application
  // but it's ommitted here in favor of simplicity
  const queries = Array.from(req.query.q);

  makeSearches(queries).then((results) => {
    res.send(results);
  });
});

// API

// Workaround to make it work with Promises
// https://github.com/serpapi/google-search-results-nodejs/issues/4
function promisifiedGetJson(params) {
  return new Promise((resolve, reject) => {
    try {
      search.json(params, resolve);
    } catch (e) {
      reject(e);
    }
  });
}

function makeSearches(queries) {
  const promises = queries.map((q) => {
    const params = {
      q,
      location: "Austin, TX",
    };

    return promisifiedGetJson(params);
  });

  return Promise.all(promises);
};

// Start server

app.listen(3000, () => {
  console.log(`Server is running on port: 3000`);
});
```

### Explanation

Make N requests:

```js
function promisifiedGetJson(params) {
  return new Promise((resolve, reject) => {
    try {
      search.json(params, resolve);
    } catch (e) {
      reject(e);
    }
  });
}
```

Note: At the moment, `google-search-results-nodejs` doesn't have a Promise API so [the workaround to make it work with Promises](https://github.com/serpapi/google-search-results-nodejs/issues/4) is required. With callback API it's also possible, but it requires the usage of [`Array#reduce`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/Reduce).

With the Promise API, a list of keywords will be mapped into an `array` of Promises:

```js
function makeSearches(queries) {
  const promises = queries.map((q) => {
    const params = {
      q,
      location: "Austin, TX",
    };

    return promisifiedGetJson(params);
  });

  return Promise.all(promises);
};
```

Make an API action (route) and return the response:

```js
app.get("/search", (req, res) => {
  // The number of queries should be limited in a real application
  // but it's ommitted here in favor of simplicity
  const queries = Array.from(req.query.q);

  makeSearches(queries).then((results) => {
    res.send(results);
  });
});
```

- `const queries` gets `array` of query parameters.
- `makeSearches()` make a call for each query and returns a results from SerpApi.


Testing simple request and response:

```
$ curl -s 'https://mern-serpapi-nodejs.serpapi.repl.co/search?q=stackoverflow&q=github&q=deno' | jq -r '.[].search_metadata'
{
  "id": "61fad426607393485726c241",
  "status": "Success",
  "json_endpoint": "https://serpapi.com/searches/582d9fcdfd66a739/61fad426607393485726c241.json",
  "created_at": "2022-02-02 18:57:42 UTC",
  "processed_at": "2022-02-02 18:57:42 UTC",
  "google_url": "https://www.google.com/search?q=stackoverflow&oq=stackoverflow&uule=w+CAIQICIdQXVzdGluLFRYLFRleGFzLFVuaXRlZCBTdGF0ZXM&sourceid=chrome&ie=UTF-8",
  "raw_html_file": "https://serpapi.com/searches/582d9fcdfd66a739/61fad426607393485726c241.html",
  "total_time_taken": 0.66
}
{
  "id": "61fad42617f923aa08188dfc",
  "status": "Success",
  "json_endpoint": "https://serpapi.com/searches/667255ede060a7ae/61fad42617f923aa08188dfc.json",
  "created_at": "2022-02-02 18:57:42 UTC",
  "processed_at": "2022-02-02 18:57:42 UTC",
  "google_url": "https://www.google.com/search?q=github&oq=github&uule=w+CAIQICIdQXVzdGluLFRYLFRleGFzLFVuaXRlZCBTdGF0ZXM&sourceid=chrome&ie=UTF-8",
  "raw_html_file": "https://serpapi.com/searches/667255ede060a7ae/61fad42617f923aa08188dfc.html",
  "total_time_taken": 0.96
}
{
  "id": "61fad4261baebbb454181a3a",
  "status": "Success",
  "json_endpoint": "https://serpapi.com/searches/ae665860b250fd5f/61fad4261baebbb454181a3a.json",
  "created_at": "2022-02-02 18:57:42 UTC",
  "processed_at": "2022-02-02 18:57:42 UTC",
  "google_url": "https://www.google.com/search?q=deno&oq=deno&uule=w+CAIQICIdQXVzdGluLFRYLFRleGFzLFVuaXRlZCBTdGF0ZXM&sourceid=chrome&ie=UTF-8",
  "raw_html_file": "https://serpapi.com/searches/ae665860b250fd5f/61fad4261baebbb454181a3a.html",
  "total_time_taken": 0.61
}
```

____

<h2 id="front_end_code">Front-End Code</h2>

Both of projects are deployed to [Vercel](https://vercel.com/). [Next.js](https://nextjs.org/) app is simpler because that's the value proposition of Next.js. 

- [Next.js app repository](https://github.com/ilyazub/nextjs-serpapi). Preview: [nextjs-serpapi.vercel.app](https://nextjs-serpapi.vercel.app/)
- [Express.js app repository](https://github.com/ilyazub/express-react-serpapi). Preview: [https://express-react-serpapi.vercel.app](https://express-react-serpapi.vercel.app/)

Note: Express.js app has SSR in development mode only. It uses Vite to render React components on the server. Next.js app have SSR in dev and prod.

Demo example:

![image](https://user-images.githubusercontent.com/78694043/155529826-7b351d42-89e3-44b8-bfe9-585f3b041f58.png)

![image](https://user-images.githubusercontent.com/78694043/155529753-005fcaf3-4c01-4342-8ec5-27c69f5dc10e.png)


React component for both cases:

```js
// App.jsx

import React from "react";
import ReactDOM from "react-dom";

import React, { useState } from "react";
import { SearchResults } from "./SearchResults";

export function App() {
  const [q, setQ] = useState("coffee, cats");
  const [searchResults, setSearchResults] = useState([]);
  const [isLoading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  function handleFormSubmit(event) {
    event.preventDefault();

    const params = new URLSearchParams({
      q,
    });

    setLoading(true);
    fetch(`/api/search?${params}`)
      .then((res) => res.json())
      .then(
        (results) => {
          setSearchResults(results);
          setLoading(false);
          setError(null);
        },
        (error) => {
          setError(error);
        }
      );
  }

  function handleQChange(event) {
    event.preventDefault();
    setQ(event.target.value);
  }

  return (
    <>
      <h1>SerpApi example in MERN stack</h1>

      <form action="/api/search" method="get" onSubmit={handleFormSubmit}>
        <label>
          <label>Queries (separated by comma):</label>&nbsp;
          <input name="q" value={q} placeholder={q} onChange={handleQChange} />
          <br />
          <input
            type="submit"
            value={isLoading ? "Loading..." : "Search"}
            disabled={isLoading} />
        </label>
      </form>

      <br />

      <SearchResults
        results={searchResults}
        isLoading={isLoading}
        error={error} />
    </>
  );
}

ReactDOM.hydrate(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById("root")
);
```


`SearchResults.jsx`:

```js
function SearchResults({ results, isLoading, error }) {
  if (isLoading)
    return (
      <p>
        Loading...
      </p>
    );

  if (!results || results.length === 0) {
    return <p>Click &quot;Search&quot; &uarr; to continue.</p>;
  }

  if (error) return <p>Error: {error}</p>;

  return (
    <section>
      <h3>Search results ({results.length})</h3>
      <ul>{results.map(r => (<li key={r.search_metadata.id}>{r.search_metadata.id}</li>))}</ul>
    </section>
  );
}
```

___

<h2 id="links">Links</h2>

- [Code in the online IDE](https://replit.com/@serpapi/mern-serpapi-nodejs)
- [google-search-results-nodejs](https://www.npmjs.com/package/google-search-results-nodejs)
- [Next.js app GitHub repository](https://github.com/ilyazub/nextjs-serpapi)
- [Express.js app GitHub repository](https://github.com/ilyazub/express-react-serpapi)
___

<h2 id="outro">Outro</h2>

If you have any questions, reach out via Twitter at [@ilyazub_](https://twitter.com/ilyazub_), or [@serp_api](https://twitter.com/serp_api).

___

<p style="text-align: center;">Join us on <a href="https://www.reddit.com/r/SerpApi/">Reddit</a> | <a href="https://twitter.com/serp_api">Twitter</a> | <a href="https://www.youtube.com/channel/UCUgIHlYBOD3yA3yDIRhg_mg">YouTube</a></p>

<p style="text-align: center;">Add a  <a href="https://forum.serpapi.com/feature-requests">Feature Request</a>💫 or a <a href="https://forum.serpapi.com/bugs">Bug</a>🐞</p>

