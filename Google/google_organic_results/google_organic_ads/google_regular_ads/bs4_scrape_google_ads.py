from bs4 import BeautifulSoup
import requests, lxml, json

# https://docs.python-requests.org/en/master/user/quickstart/#passing-parameters-in-urls
params = {
    "q": "coffee beans buy",
    "hl": "en",
    "gl": "us"
}

# https://docs.python-requests.org/en/master/user/quickstart/#custom-headers
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.87 Safari/537.36",
}

html = requests.get("https://www.google.com/search", params=params, headers=headers)
soup = BeautifulSoup(html.text, "lxml")

ad_results = []

for index, ad_result in enumerate(soup.select(".uEierd"), start=1):
    title = ad_result.select_one(".v0nnCb span").text
    website_link = ad_result.select_one("a.sVXRqc")["data-pcu"]
    ad_link = ad_result.select_one("a.sVXRqc")["href"]
    displayed_link = ad_result.select_one(".qzEoUe").text
    tracking_link = ad_result.select_one(".v5yQqb a.sVXRqc")["data-rw"]
    snippet = ad_result.select_one(".MUxGbd div span").text
    phone = None if ad_result.select_one("span.fUamLb span") is None else ad_result.select_one("span.fUamLb span") .text

    inline_link_text = [title.text for title in ad_result.select("div.bOeY0b .XUpIGb a")]
    inline_link = [link["href"] for link in ad_result.select("div.bOeY0b .XUpIGb a")]

    ad_results.append({
        "position": index,
        "title": title,
        "phone": phone,
        "website_link": website_link,
        "displayed_link": displayed_link,
        "ad_link": ad_link,
        "tracking_link": tracking_link,
        "snippet": snippet,
        "sitelinks": [{"titles": inline_link_text, "links": inline_link}]
    })

print(json.dumps(ad_results, indent=2))