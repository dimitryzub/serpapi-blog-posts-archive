from parsel import Selector
from playwright.sync_api import sync_playwright
import json

def scrape_researchgate_publication(publication: str):
    
    with sync_playwright() as p:
        
        browser = p.chromium.launch(headless=True, slow_mo=50)
        page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36",
                                java_script_enabled=True)
        page.goto(f"https://www.researchgate.net/publication/{publication}")
        selector = Selector(text=page.content())
        
        pubilication_data = {
            "publication_info": {},
            "references": [],
            "recomendations": []   
        }
        
        pubilication_data["publication_info"]["publication_title"] = selector.css(".research-detail-header-section__title::text").get()
        pubilication_data["publication_info"]["publication_type"] = selector.css(".research-detail-header-section__badge:nth-child(2)::text").get()
        pubilication_data["publication_info"]["publication_authors"] = selector.css(".nova-legacy-v-person-list-item__align-content div::text").getall()
        pubilication_data["publication_info"]["publication_date"] = selector.css(".nova-legacy-e-text--color-grey-700 .nova-legacy-e-list__item:nth-child(1)::text").get()
        pubilication_data["publication_info"]["pdf_availability"] = selector.css(".research-detail-header-section__badge:nth-child(3)::text").get()
        pubilication_data["publication_info"]["pdf_link"] = f'https://www.researchgate.net{selector.css(".research-detail-header-cta__buttons a:nth-child(1)::attr(href)").get()}'
        pubilication_data["publication_info"]["publication_full_text_link"] = selector.css(".research-detail-header-cta__buttons a:nth-child(2)::attr(href)").get()
        pubilication_data["publication_info"]["publication_journal"] = selector.css(".nova-legacy-e-text--color-grey-700+ .nova-legacy-e-text--color-grey-700 .nova-legacy-e-link--theme-decorated::text").get()
        pubilication_data["publication_info"]["publication_journal_link"] = f'https://www.researchgate.net{selector.css(".nova-legacy-e-text--color-grey-700+ .nova-legacy-e-text--color-grey-700 .nova-legacy-e-link--theme-decorated::attr(href)").get()}'
        pubilication_data["publication_info"]["project_title"] = selector.css(".nova-legacy-e-text--color-grey-700+ .nova-legacy-e-text--color-grey-700 .nova-legacy-e-list__item .nova-legacy-e-link--theme-decorated::text").get()
        pubilication_data["publication_info"]["project_link"] = f'https://www.researchgate.net{selector.css(".nova-legacy-e-text--color-grey-700+ .nova-legacy-e-text--color-grey-700 .nova-legacy-e-list__item .nova-legacy-e-link--theme-decorated::attr(href)").get()}'
        pubilication_data["publication_info"]["citation_link"] = selector.css(".nova-legacy-l-flex__item.hide-l a:nth-child(1)::attr(href)").get()
        
        for reference in selector.css(".publication-citations__item--redesign"):
            pubilication_data["references"].append({
                "title": reference.css(".nova-legacy-v-publication-item__title::text").get(),
                "link": f'https://www.researchgate.net{reference.css(".nova-legacy-v-publication-item__title a::attr(href)").get()}',
                "reference_type": reference.css(".nova-legacy-v-publication-item__type::text").get(),
                "full_text_availability": reference.css(".nova-legacy-v-publication-item__fulltext::text").get(),
                "authors": reference.css(".nova-legacy-v-person-inline-item__fullname::text").getall(),
                "publication_date": reference.css(".nova-legacy-v-publication-item__meta-data-item:nth-child(1) span::text").get(),
            })
        
        for recommendation in selector.css(".nova-legacy-c-card__body.nova-legacy-c-card__body--spacing-inherit"):
            pubilication_data["recomendations"].append({
                "type": recommendation.css(".nova-legacy-e-badge::text").get(),
                "title": recommendation.css(".nova-legacy-e-text.nova-legacy-e-text--size-l a::text").get(),
                "link": recommendation.css(".nova-legacy-e-text.nova-legacy-e-text--size-l a::attr(href)").get(),
                "authors": recommendation.css(".nova-legacy-v-person-inline-item__fullname::text").getall(),
                "date": recommendation.css(".nova-legacy-e-text span:nth-child(1)::text").getall(),
            })

        print(json.dumps(pubilication_data, indent=2, ensure_ascii=False))
        
        browser.close()


# accepts publication ID: 340715390
# as well as full path: researchgate.net/publication/340715390_Transforming_Technology_for_Global_Business_Acceleration_and_Change_Management
scrape_researchgate_publication(publication="352677424_Improving_Context-Aware_Habit-Support_Interventions_Using_Egocentric_Visual_Contexts")