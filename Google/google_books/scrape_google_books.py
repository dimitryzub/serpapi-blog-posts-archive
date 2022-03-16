from parsel import Selector
import requests, json, re

params = {
    "q": "richard branson",
    "tbm": "bks",
    "gl": "us",
    "hl": "en"
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.87 Safari/537.36",
}

html = requests.get("https://www.google.com/search", params=params, headers=headers, timeout=30)
selector = Selector(text=html.text)

books_results = []

# https://regex101.com/r/mapBs4/1
book_thumbnails = re.findall(r"s=\\'data:image/jpg;base64,(.*?)\\'", str(selector.css("script").getall()), re.DOTALL)

for book_thumbnail, book_result in zip(book_thumbnails, selector.css(".Yr5TG")):
    title = book_result.css(".DKV0Md::text").get()
    link = book_result.css(".bHexk a::attr(href)").get()
    displayed_link = book_result.css(".tjvcx::text").get()
    snippet = book_result.css(".cmlJmd span::text").get()
    author = book_result.css(".fl span::text").get()
    author_link = f'https://www.google.com/search{book_result.css(".N96wpd .fl::attr(href)").get()}'
    date_published = book_result.css(".fl+ span::text").get()
    preview_link = book_result.css(".R1n8Q a.yKioRe:nth-child(1)::attr(href)").get()
    more_editions_link = book_result.css(".R1n8Q a.yKioRe:nth-child(2)::attr(href)").get()

    books_results.append({
        "title": title,
        "link": link,
        "displayed_link": displayed_link,
        "snippet": snippet,
        "author": author,
        "author_link": author_link,
        "date_published": date_published,
        "preview_link": preview_link,
        "more_editions_link": f"https://www.google.com{more_editions_link}" if more_editions_link is not None else None,
        "thumbnail": bytes(bytes(book_thumbnail, "ascii").decode("unicode-escape"), "ascii").decode("unicode-escape")
    })
