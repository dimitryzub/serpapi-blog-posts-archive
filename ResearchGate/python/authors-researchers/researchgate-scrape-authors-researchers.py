from parsel import Selector
from playwright.sync_api import sync_playwright
import json


def scrape_researchgate_profile(query: str):
    with sync_playwright() as p:
        
        browser = p.chromium.launch(headless=True, slow_mo=50)
        page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36")

        authors = []
        page_num = 1

        while True:
            page.goto(f"https://www.researchgate.net/search/researcher?q={query}&page={page_num}")
            selector = Selector(text=page.content())

            for author in selector.css(".nova-legacy-c-card__body--spacing-inherit"):
                name = author.css(".nova-legacy-v-person-item__title a::text").get()
                thumbnail = author.css(".nova-legacy-v-person-item__image img::attr(src)").get()
                profile_page = f'https://www.researchgate.net/{author.css("a.nova-legacy-c-button::attr(href)").get()}'
                institution = author.css(".nova-legacy-v-person-item__stack-item:nth-child(3) span::text").get()
                department = author.css(".nova-legacy-v-person-item__stack-item:nth-child(4) span").xpath("normalize-space()").get()
                skills = author.css(".nova-legacy-v-person-item__stack-item:nth-child(5) span").xpath("normalize-space()").getall()
                last_publication = author.css(".nova-legacy-v-person-item__info-section-list-item .nova-legacy-e-link--theme-bare::text").get()
                last_publication_link = f'https://www.researchgate.net{author.css(".nova-legacy-v-person-item__info-section-list-item .nova-legacy-e-link--theme-bare::attr(href)").get()}'

                authors.append({
                    "name": name,
                    "profile_page": profile_page,
                    "institution": institution,
                    "department": department,
                    "thumbnail": thumbnail,
                    "last_publication": {
                        "title": last_publication,
                        "link": last_publication_link
                    },
                    "skills": skills,
                })
            
            print(f"page number: {page_num}")

            # checks if next page arrow key is greyed out `attr(rel)` (inactive) and breaks out of the loop
            if selector.css(".nova-legacy-c-button-group__item:nth-child(9) a::attr(rel)").get():
                break
            else:
                page_num += 1


        print(json.dumps(authors, indent=2, ensure_ascii=False))

        browser.close()
        
    
scrape_researchgate_profile(query="coffee")