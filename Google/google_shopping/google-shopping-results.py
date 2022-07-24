from bs4 import BeautifulSoup
import requests, lxml, re, json

# https://docs.python-requests.org/en/master/user/quickstart/#passing-parameters-in-urls
params = {
    "q": "shoes",
    "hl": "en",     # language
    "gl": "us",     # country of the search, US -> USA
    "tbm": "shop"   # google search shopping
}

# https://docs.python-requests.org/en/master/user/quickstart/#custom-headers
headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
}

html = requests.get("https://www.google.com/search", params=params, headers=headers, timeout=30)
soup = BeautifulSoup(html.text, 'lxml')


def get_original_images():
	all_script_tags = soup.select('script')
	
	image_urls = []
	
	for result in soup.select(".Qlx7of .sh-dgr__grid-result"):
		for script_tag in all_script_tags:
			# https://regex101.com/r/udjFUq/1
			url_with_unicode = re.findall(rf"var\s?_u='(.*)';var\s?_i='{result['data-pck']}';", str(script_tag))
			
			if url_with_unicode:
				url_decode = bytes(url_with_unicode[0], 'ascii').decode('unicode-escape')
				image_urls.append(url_decode)
				break
	
	# download_original_images(image_urls)
					
	return image_urls


def download_original_images(image_urls):
	for index, image_url in enumerate(image_urls, start=1):
		image = requests.get(image_url, headers=headers, timeout=30)
	
		if image.status_code == 200:
			print(f'Downloading {index} image...')
			with open(f"images/image_{index}.jpeg", 'wb') as file:
				file.write(image.content)


def get_suggested_search_data():
	google_shopping_data = []
	
	for result, thumbnail in zip(soup.select(".Qlx7of .i0X6df"), get_original_images()):
		
		title = result.select_one(".Xjkr3b").text
		product_link = f"https://www.google.com" + result.select_one(".Lq5OHe").get("href")
	
		try:
			reviews_and_rating = result.select_one(".NzUzee div").get("aria-label").split(", ")
			product_rating = reviews_and_rating[0]
			product_reviews = reviews_and_rating[1]
		except:
			product_rating = None
			product_reviews = None
	
		price = result.select_one(".a8Pemb").text
		store = result.select_one(".aULzUe").text
		store_link = "https://www.google.com" + result.select_one(".eaGTj div a").get("href")
		delivery = result.select_one(".vEjMR").text
	
		try:
			container = result.select_one(".zLPF4b div").next_sibling
			store_rating = container.select_one(".QIrs8").text
			store_reviews_link = "https://www.google.com" + container.select_one(".QhE5Fb").get('href')
			if container.select_one(".i55gLe"):
				store_reviews = container.select_one(".i55gLe").text
			else:
				store_reviews = container.select_one(".ugFiYb").text
		except:
			store_rating = None
			store_reviews_link = None
			store_reviews = None

		try:
			compare_prices_link = "https://www.google.com" + result.select_one(".Ldx8hd .iXEZD").get('href')
		except:
			compare_prices_link = None

		google_shopping_data.append({
			"thumbnail": thumbnail,
			"title": title,
			"product_link": product_link,
			"product_rating": product_rating,
			"product_reviews": product_reviews,
			"price": price,
			"store": store,
			"store_link": store_link,
			"delivery": delivery,
			"store_rating": store_rating,
			"store_reviews": store_reviews,
			"store_reviews_link": store_reviews_link,
			"compare_prices_link": compare_prices_link,
		})
		
		print(json.dumps(google_shopping_data, indent=2, ensure_ascii=False))
