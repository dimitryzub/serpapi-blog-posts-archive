
# TODO: check if the code is working correctly. Before results was blocked by Google.
# https://replit.com/@DimitryZub1/DimLustrousBoards#main.py


import requests, lxml, json, re
from parsel import Selector
from itertools import zip_longest

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36"
}

params = {
    "q": "gta san andreas",  # search query
    "hl": "en",  # language of the search
    "gl": "us",  # country of the search
    "num": "100",  # number of search results per page
    "tbm": "nws",  # news results
}

html = requests.get("https://www.google.com/search", headers=headers, params=params, timeout=30)
selector = Selector(text=html.text)

all_script_tags = selector.css("script::text").getall()

news_results = []
decoded_thumbnails = []

for _id in selector.css(".YEMaTe img::attr(id)"):
    # https://regex101.com/r/FZktSD/1
    thumbnails = re.findall(r"s=\'([^']+)\'\;var\s?ii\=\['{_id}'\];".format(_id=_id.get()), str(all_script_tags))

    decoded_thumbnail = [
        bytes(bytes(img, "ascii").decode("unicode-escape"), "ascii").decode("unicode-escape") for img in thumbnails
    ]

    decoded_thumbnails.append("".join(decoded_thumbnail))

for result, thumbnail_image in zip_longest(selector.css("[jsname=YKoRaf]"), decoded_thumbnails):
    news_results.append(
        {
            "title": result.css(".MBeuO::text").get(),
            "link": result.attr("href"),
            "source": result.css(".NUnG9d span::text").get(),
            "snippet": result.css(".GI74Re::text").get(),
            "date_published": result.css(".ZE0LJd span:;text").get(),
            "thumbnail": thumbnail_image
        }
    )
print(json.dumps(news_results, indent=2, ensure_ascii=False))
