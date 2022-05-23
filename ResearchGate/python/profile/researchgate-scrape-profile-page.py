from parsel import Selector
from playwright.sync_api import sync_playwright
import json, re 


def scrape_researchgate_profile(profile: str):
    with sync_playwright() as p:
        
        profile_data = {
            "basic_info": {},
            "about": {},
            "co_authors": [],
            "publications": [],
            }
        
        browser = p.chromium.launch(headless=True, slow_mo=50)
        page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36")
        page.goto(f"https://www.researchgate.net/profile/Agnis-Stibe")
        selector = Selector(text=page.content())
        
        profile_data["basic_info"]["name"] = selector.css(".nova-legacy-e-text.nova-legacy-e-text--size-xxl::text").get()
        profile_data["basic_info"]["institution"] = selector.css(".nova-legacy-v-institution-item__stack-item a::text").get()
        profile_data["basic_info"]["department"] = selector.css(".nova-legacy-e-list__item.nova-legacy-v-institution-item__meta-data-item:nth-child(1)").xpath("normalize-space()").get()
        profile_data["basic_info"]["current_position"] = selector.css(".nova-legacy-e-list__item.nova-legacy-v-institution-item__info-section-list-item").xpath("normalize-space()").get()
        profile_data["basic_info"]["lab"] = selector.css(".nova-legacy-o-stack__item .nova-legacy-e-link--theme-bare b::text").get()
        
        profile_data["about"]["number_of_publications"] = re.search(r"\d+", selector.css(".nova-legacy-c-card__body .nova-legacy-o-grid__column:nth-child(1)").xpath("normalize-space()").get()).group()
        profile_data["about"]["reads"] = re.search(r"\d+", selector.css(".nova-legacy-c-card__body .nova-legacy-o-grid__column:nth-child(2)").xpath("normalize-space()").get()).group()
        profile_data["about"]["citations"] = re.search(r"\d+", selector.css(".nova-legacy-c-card__body .nova-legacy-o-grid__column:nth-child(3)").xpath("normalize-space()").get()).group()
        profile_data["about"]["introduction"] = selector.css(".nova-legacy-o-stack__item .Linkify").xpath("normalize-space()").get()
        profile_data["about"]["skills"] = selector.css(".nova-legacy-l-flex__item .nova-legacy-e-badge ::text").getall()
        
        for co_author in selector.css(".nova-legacy-c-card--spacing-xl .nova-legacy-c-card__body--spacing-inherit .nova-legacy-v-person-list-item"):
            profile_data["co_authors"].append({
                "name": co_author.css(".nova-legacy-v-person-list-item__align-content .nova-legacy-e-link::text").get(),
                "link": co_author.css(".nova-legacy-l-flex__item a::attr(href)").get(),
                "avatar": co_author.css(".nova-legacy-l-flex__item .lite-page-avatar img::attr(data-src)").get(),
                "current_institution": co_author.css(".nova-legacy-v-person-list-item__align-content li").xpath("normalize-space()").get()
            })

        for publication in selector.css("#publications+ .nova-legacy-c-card--elevation-1-above .nova-legacy-o-stack__item"):
            profile_data["publications"].append({
                "title": publication.css(".nova-legacy-v-publication-item__title .nova-legacy-e-link--theme-bare::text").get(),
                "date_published": publication.css(".nova-legacy-v-publication-item__meta-data-item span::text").get(),
                "authors": publication.css(".nova-legacy-v-person-inline-item__fullname::text").getall(),
                "publication_type": publication.css(".nova-legacy-e-badge--theme-solid::text").get(),
                "description": publication.css(".nova-legacy-v-publication-item__description::text").get(),
                "publication_link": publication.css(".nova-legacy-c-button-group__item .nova-legacy-c-button::attr(href)").get(),
            })
            
            
        print(json.dumps(profile_data, indent=2, ensure_ascii=False))

        browser.close()
        
    
scrape_researchgate_profile(profile="Agnis-Stibe")