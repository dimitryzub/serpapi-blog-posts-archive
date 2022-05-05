from parsel import Selector
# import requests, json, time, cloudscraper
from playwright.sync_api import sync_playwright
import re, json


def scrape_institution_members(institution: str):

    with sync_playwright() as p:
        
        institution_memebers = []
        page_num = 1 
        
        members_is_present = True
        while members_is_present:
            
            browser = p.chromium.launch(headless=True, slow_mo=50)
            page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36")
            page.goto(f"https://www.researchgate.net/institution/{institution}/members/{page_num}")
            selector = Selector(text=page.content())
            
            print(f"page number: {page_num}")
            
            for member in selector.css(".nova-legacy-v-person-list-item"):
                name = member.css(".nova-legacy-v-person-list-item__align-content a::text").get()
                link = member.css(".nova-legacy-v-person-list-item__align-content a::attr(href)").get()
                profile_photo = member.css(".nova-legacy-l-flex__item img::attr(src)").get()
                # department = member.css("").get()
                desciplines = member.css("span .nova-legacy-e-link::text").getall()
                
                institution_memebers[0]["member_info"].append({
                    "name": name,
                    "link": link,
                    "profile_photo": profile_photo,
                    "descipline": desciplines
                })
                
            # check for Page not found selector
            if selector.css(".headline::text").get():
                members_is_present = False
            else:
                page_num += 1 # pagination

        print(json.dumps(institution_memebers, indent=2, ensure_ascii=False))
        print(len(institution_memebers))


        browser.close()
        











        
        # https://regex101.com/r/8qjfnH/1
        # extracted_data = re.findall(r"\s+RGCommons\.react\.mountWidgetTree\(({\"data\":{\"menu\".*:true})\);;",
        #                        str(page.content()))[0]
        # json_data = json.loads(extracted_data)
        # print(json_data)
        

    # https://docs.python-requests.org/en/master/user/quickstart/#custom-headers
    # headers = {
    #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36",
    # }
    
    # session = requests.Session()
    # html = session.get(f"https://www.researchgate.net/institution/{institution}/members", headers=headers, timeout=30)
    
    # institution_memebers = []
    
    # for member in selector.css(".nova-legacy-v-person-list-item"):
    #     name = member.css(".nova-legacy-v-person-list-item__align-content a::text").get()
    #     link = member.css(".nova-legacy-v-person-list-item__align-content a::attr(href)").get()
    #     profile_photo = member.css(".nova-legacy-l-flex__item img::attr(src)").get()
    #     # department = member.css("").get()
    #     desciplines = member.css("span .nova-legacy-e-link::text").getall()
    #     desciplines_link = member.css("span .nova-legacy-e-link::attr(href)").getall()
        
    #     institution_memebers.append({
    #         "name": name,
    #         "link": link,
    #         "profile_photo": profile_photo,
    #         "desciplines": desciplines,
    #         "desciplines_link": desciplines_link
    #     })
        
    # print(json.dumps(institution_memebers, indent=2, ensure_ascii=False))
        
    
scrape_institution_members(institution="EM-Normandie-Business-School")