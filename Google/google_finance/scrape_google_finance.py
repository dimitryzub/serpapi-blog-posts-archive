from parsel import Selector
import requests, json, os
import pandas as pd


def scrape_google_finance(ticker: str):

    params = {
        # time window for time-series chart data: 1 day, 5 days, 1-6 month, 5 years
        "window": "1D"  # 1D, 5D, 1M, 6M, YTD (Year to date), 1Y, 5Y, MAX
    }

    # https://docs.python-requests.org/en/master/user/quickstart/#custom-headers
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.87 Safari/537.36",
    }

    html = requests.get(f"https://www.google.com/finance/quote/{ticker}?", headers=headers, params=params)
    selector = Selector(html.text)

    time = selector.css(".ygUjEc::text").get().split(" · ")[0]
    ticker_name = selector.css(".PdOqHc::text").get()
    title = selector.css(".zzDege::text").get()
    current_price = selector.css(".fxKbKc::text").get()
    percent_change = selector.css(".enJeMd .NydbP.VOXKNe.tnNmPe::attr(aria-label)").get()
    # price_change_today = selector.css(".P2Luy.Ebnabc.ZYVHBb::text").get()

    print(title, ticker_name, title, current_price, sep="\n")

    for news in selector.css(".yY3Lee"):
        news_title = news.css(".Yfwt5::text").get()
        news_link = news.xpath('*//img[@class="Z4idke"]/../@href').get()  # /.. refers to the parent node
        news_title = news.css(".Z4idke::attr(src)").get()
        news_date = news.css(".Adak::text").get()
        news_published_at = news.css(".sfyJob::text").get().split(" · ")[0]

    for knowledge_graph in selector.css(".gyFHrc"):
        graph_key = knowledge_graph.css(".mfs7Fc::text").get()
        graph_value = knowledge_graph.css(".P6K39c").xpath("normalize-space()").get()

        # print(graph_key, graph_value, end="\n")

    for table in selector.css(".slpEwd .roXhBd"):
        left = table.css(".J9Jhg").xpath("normalize-space()").get()
        center = table.css(".QXDnM::text").get()
        right = table.css(".gEUVJe").xpath("normalize-space()").get()
        # print(left, center, right)



scrape_google_finance(ticker="TSLA:NASDAQ")
