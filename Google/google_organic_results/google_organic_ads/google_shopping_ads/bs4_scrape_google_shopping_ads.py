from bs4 import BeautifulSoup
import requests, lxml, json

# https://docs.python-requests.org/en/master/user/quickstart/#passing-parameters-in-urls
params = {
    "q": "rtx 3080 buy",
    "hl": "en",
    "gl": "us"
    }

# https://docs.python-requests.org/en/master/user/quickstart/#custom-headers
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4758.87 Safari/537.36",
    }

html = requests.get("https://www.google.com/search", params=params, headers=headers, timeout=30)
soup = BeautifulSoup(html.text, "lxml")

data = []

# if top block shopping ads appears
if soup.select_one(".commercial-unit-desktop-top"):
    for index, shopping_ad in enumerate(soup.select(".mnr-c.pla-unit"), start=1):
        title = shopping_ad.select_one(".pymv4e").text
        link = shopping_ad.select_one(".pla-unit-title-link")["href"]
        price = shopping_ad.select_one(".e10twf").text
        source = shopping_ad.select_one(".LbUacb .zPEcBd").text

        data.append({
            "position": index,
            "block_position": "top_block",
            "title": title,
            "link": link,
            "price": price,
            "source": source
            })

# if right block shopping ads appears
elif soup.select_one(".commercial-unit-desktop-rhs"):
    for index, shopping_ad in enumerate(soup.select(".mnr-c.pla-unit"), start=1):
        title = shopping_ad.select_one(".pymv4e").text
        link = shopping_ad.select_one(".pla-unit-title-link")["href"]
        price = shopping_ad.select_one(".e10twf").text
        source = shopping_ad.select_one(".LbUacb, .zPEcBd").text

        data.append({
            "position": index,
            "block_position": "right_block",
            "title": title,
            "link": link,
            "price": price,
            "source": source
            })

print(json.dumps(data, indent=2, ensure_ascii=False))

"""
[
  {
    "position": "right_block",
    "title": "RTX 3060Ti 8GB MSI VENTUS 2X 8G OCV1 LHR Hardware/Electronic",
    "link": "https://www.grooves.land/msi-geforce-rtx-3060-ventus-ocv1-lhr-grafikkarten-rtx-3060-gddr6-pcie-hdmi-displayport-msi-hardware-electronic-pZZa1-2100386549.html?language=en&currency=EUR&_z=ua",
    "price": "UAH 21,016.52",
    "source": "Grooves.LandGrooves.Land"
  },
  {
    "position": "right_block",
    "title": "Відеокарта Colorful RTX 3060 iGame bilibili E-sports Edition OC 12G L-V (RTX 3060 bilibili E-sports Edition)",
    "link": "https://ktc.ua/goods/videokarta_colorful_rtx_3060_igame_bilibili_e_sports_edition_oc_12g_l_v_rtx_3060_bilibili_e_sports_edition.html",
    "price": "UAH 23,999.00",
    "source": "KTC.uaKTC.ua"
  }
]
"""