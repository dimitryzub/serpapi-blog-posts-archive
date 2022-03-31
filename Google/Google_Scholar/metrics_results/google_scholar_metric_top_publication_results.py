import requests, lxml
from bs4 import BeautifulSoup
import pandas as pd

def scrape_all_metrics_top_publications():

    params = {
        "view_op": "top_venues",  # top publications results
        "hl": "en"                # language
        }

    html = requests.get("https://scholar.google.com/citations", params=params)
    soup = BeautifulSoup(html.text, "lxml").find("table")

    df = pd.DataFrame(pd.read_html(str(soup))[0])
    df.drop(df.columns[0], axis=1, inplace=True)

    df.insert(loc=2,
              column="h5-index link",
              value=[f'https://scholar.google.com/{link.a["href"]}' for link in soup.select(".gsc_mvt_t+ td")])

    df.to_csv("google_scholar_metrics_top_publications.csv", index=False)

    # save to csv for a specific language
    # df.to_csv(f"google_scholar_metrics_top_publications_lang_{params['hl']}.csv", index=False)