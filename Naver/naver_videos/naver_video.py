import requests, os, json
from parsel import Selector
from serpapi import NaverSearch


def parsel_scrape_naver_videos():
    # https://docs.python-requests.org/en/master/user/quickstart/#passing-parameters-in-urls
    params = {
        "query": "minecraft",
        "where": "video"  # video results
    }

    # https://docs.python-requests.org/en/master/user/quickstart/#custom-headers
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.87 Safari/537.36",
    }

    html = requests.get("https://search.naver.com/search.naver", params=params, headers=headers, timeout=30)
    selector = Selector(html.text)

    video_results = []

    for video in selector.css(".video_bx"):
        title = video.css(".text::text").get()
        link = video.css(".info_title::attr(href)").get()
        thumbnail = video.css(".thumb_area img::attr(src)").get()
        channel = video.css(".channel::text").get()
        origin = video.css(".origin::text").get()
        video_duration = video.css(".time::text").get()
        views = video.css(".desc_group .desc:nth-child(1)::text").get()
        date_published = video.css(".desc_group .desc:nth-child(2)::text").get()

        video_results.append({
            "title": title,
            "link": link,
            "thumbnail": thumbnail,
            "channel": channel,
            "origin": origin,
            "video_duration": video_duration,
            "views": views,
            "date_published": date_published
        })

    print(json.dumps(video_results, indent=2, ensure_ascii=False))


def serpapi_scrape_naver_videos():
    params = {
        "api_key": os.getenv("API_KEY"),
        "engine": "naver",
        "query": "minecraft",
        "where": "video"
    }

    search = NaverSearch(params)
    results = search.get_dict()

    video_results = []

    for video in results["video_results"]:
        video_results.append({
            "title": video["title"],
            "link": video["link"],
            "duration": video["duration"],
            "views": video.get("views"),
            "pub_date": video.get("publish_date"),
            "thumbnail": video["thumbnail"],
            "channel_name": video.get("channel", {}).get("name"),
            "channel_link": video.get("channel", {}).get("link")
        })

    print(json.dumps(video_results, indent=2, ensure_ascii=False))


    # for loop equivalent to map() ---> slower
    # videos = list(map(lambda video_result:
    #                   {"title": video_result["title"],
    #                    "link": video_result["link"],
    #                    "duration": video_result["duration"],
    #                    "views": video_result.get("views"),
    #                    "pub_date": video_result.get("publish_date"),
    #                    "thumbnail": video_result["thumbnail"],
    #                    "channel_name": video_result.get("channel", {}).get("name"),
    #                    "channel_link": video_result.get("channel", {}).get("link")
    #                    }, results["video_results"]))



    # print(json.dumps(videos, indent=2, ensure_ascii=False))

# serpapi_scrape_naver_videos()