from timeit import default_timer as timer
import requests, lxml, re, json, urllib.request
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36"
}

params = {
    "q": "mincraft wallpaper 4k", # search query
    "tbm": "isch",                # image results
    "hl": "en",                   # language of the search
    "gl": "us",                   # country where search comes from
    "ijn": "0"                    # page number
}


def return_html():
    html = requests.get("https://www.google.com/search", params=params, headers=headers, timeout=30)
    soup = BeautifulSoup(html.text, "lxml")

    return soup

def get_images_with_request_headers():
    del params['ijn']
    params["content-type"] = "image/png"

    soup = return_html()
    images = [img["src"] for img in soup.select("img")]

    return images

def get_suggested_search_data():
    soup = return_html()
    print(soup)

    suggested_searches = []

    # for suggested_search in soup.select(".PKhmud.sc-it.tzVsfd"):
    #     suggested_searches.append({
    #         "suggested_search_name": suggested_search.select_one(".VlHyHc").text,
    #         "suggested_search_link": f"https://www.google.com{suggested_search.a['href']}",
    #         # https://regex101.com/r/y51ZoC/1
    #         "suggested_search_chips": ''.join(re.findall(r"=isch&chips=(.*?)&hl=en-US", suggested_search.a["href"])) 
    #     })

    all_script_tags = soup.select("script")

    # https://regex101.com/r/48UZhY/6
    matched_images_data = ''.join(re.findall(r"AF_initDataCallback\(({key: 'ds:1'.*?)\);</script>", str(all_script_tags)))
    
    # https://kodlogs.com/34776/json-decoder-jsondecodeerror-expecting-property-name-enclosed-in-double-quotes
    # if you try to json.loads() without json.dumps it will throw an error:
    # "Expecting property name enclosed in double quotes"
    matched_images_data_fix = json.dumps(matched_images_data)
    matched_images_data_json = json.loads(matched_images_data_fix)

    # search for only suggested search thumbnails related
    # https://regex101.com/r/ITluak/2
    suggested_search_thumbnails_data = ','.join(re.findall(r'{key(.*?)\[null,\"Size\"', matched_images_data_json))

    # https://regex101.com/r/MyNLUk/1
    suggested_search_thumbnail_links_not_fixed = re.findall(r'\"(https:\/\/encrypted.*?)\"', suggested_search_thumbnails_data)

    # for suggested_search_fixed_thumbnail in suggested_search_thumbnail_links_not_fixed:
    #     suggested_searches.append({
    #         # https://stackoverflow.com/a/4004439/15164646 comment by Frédéric Hamidi
    #         "suggested_search_thumbnail": bytes(suggested_search_fixed_thumbnail, 'ascii').decode('unicode-escape')    
    #     })

    # return suggested_searches

# print(json.dumps(get_suggested_search_data(), indent=2))

def get_original_images():
    soup = return_html()
    
    print('\nGoogle Images Metadata:')
    for google_image in soup.select('.isv-r.PNCib.MSM1fd.BUooTd'):
        title = google_image.select_one('.VFACy.kGQAp.sMi44c.lNHeqe.WGvvNb')['title']
        source = google_image.select_one('.fxgdke').text
        link = google_image.select_one('.VFACy.kGQAp.sMi44c.lNHeqe.WGvvNb')['href']
        
        print(f'{title}\n{source}\n{link}\n')

    all_script_tags = soup.select('script')

    # https://regex101.com/r/48UZhY/4
    matched_images_data = ''.join(re.findall(r"AF_initDataCallback\(([^<]+)\);", str(all_script_tags)))
    
    # https://kodlogs.com/34776/json-decoder-jsondecodeerror-expecting-property-name-enclosed-in-double-quotes
    # if you try to json.loads() without json.dumps() it will throw an error:
    # "Expecting property name enclosed in double quotes"
    matched_images_data_fix = json.dumps(matched_images_data)
    matched_images_data_json = json.loads(matched_images_data_fix)

    # https://regex101.com/r/pdZOnW/3
    matched_google_image_data = re.findall(r'\[\"GRID_STATE0\",null,\[\[1,\[0,\".*?\",(.*),\"All\",', matched_images_data_json)

    # https://regex101.com/r/NnRg27/1
    matched_google_images_thumbnails = ', '.join(
        re.findall(r'\[\"(https\:\/\/encrypted-tbn0\.gstatic\.com\/images\?.*?)\",\d+,\d+\]',
                   str(matched_google_image_data))).split(', ')

    print('Google Image Thumbnails:')  # in order
    for fixed_google_image_thumbnail in matched_google_images_thumbnails:
        # https://stackoverflow.com/a/4004439/15164646 comment by Frédéric Hamidi
        google_image_thumbnail_not_fixed = bytes(fixed_google_image_thumbnail, 'ascii').decode('unicode-escape')

        # after first decoding, Unicode characters are still present. After the second iteration, they were decoded.
        google_image_thumbnail = bytes(google_image_thumbnail_not_fixed, 'ascii').decode('unicode-escape')
        print(google_image_thumbnail)

    # removing previously matched thumbnails for easier full resolution image matches.
    removed_matched_google_images_thumbnails = re.sub(
        r'\[\"(https\:\/\/encrypted-tbn0\.gstatic\.com\/images\?.*?)\",\d+,\d+\]', '', str(matched_google_image_data))

    # https://regex101.com/r/fXjfb1/4
    # https://stackoverflow.com/a/19821774/15164646
    matched_google_full_resolution_images = re.findall(r"(?:'|,),\[\"(https:|http.*?)\",\d+,\d+\]",
                                                       removed_matched_google_images_thumbnails)

    print('\nFull Resolution Images:')  # in order
    for index, fixed_full_res_image in enumerate(matched_google_full_resolution_images):
        
        # https://stackoverflow.com/a/4004439/15164646 comment by Frédéric Hamidi
        original_size_img_not_fixed = bytes(fixed_full_res_image, 'ascii').decode('unicode-escape')
        original_size_img = bytes(original_size_img_not_fixed, 'ascii').decode('unicode-escape')

        print(original_size_img)


        # Download original images
        # print(f'Downloading {index} image...')
        
        # opener=urllib.request.build_opener()
        # opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36')]
        # urllib.request.install_opener(opener)

        # urllib.request.urlretrieve(original_size_img, f'Bs4_Images/original_size_img_{index}.jpg')

get_original_images()