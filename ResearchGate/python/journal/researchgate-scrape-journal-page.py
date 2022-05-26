from parsel import Selector
from playwright.sync_api import sync_playwright
import json, re


def scrape_researchgate_journal(journal_name: str):
    with sync_playwright() as p:
        
        journal_data = {
            "basic_info": {},
            "publications": [],
            "top_cited_authors": []
        }
        
        browser = p.chromium.launch(headless=True, slow_mo=50)
        page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36")
        page.goto(f"https://www.researchgate.net/journal/{journal_name}")
        selector = Selector(text=page.content())

        journal_data["basic_info"]["title"] = selector.css("nova-legacy-o-stack__item h1::text").get()
        
        for cited_author in selector.css(".nova-legacy-v-person-list-item"):
            name = cited_author.css("nova-legacy-v-person-list-item__title::text").get()
            link = f'https://www.researchgate.net{cited_author.css("nova-legacy-v-person-list-item__title a::attr(href)").get()}'
            avatar = cited_author.css(".nova-legacy-l-flex__item img::attr(src)").get()
            institution = cited_author.css(".nova-legacy-v-person-list-item__meta-item::text").get()
            citations = cited_author.css(".nova-legacy-v-person-list-item__metrics-item::text").get()        
        
            journal_data["top_cited_authors"].append({
                "name": name,
                "link": link,
                "avatar": avatar,
                "institution": institution,
                "citations": citations,
            })
        
        # scrape publications from the first page
        for publication in selector.css(".nova-legacy-v-publication-item"):
            title = publication.css("nova-legacy-v-publication-item__title::text").get()
            link = f'https://www.researchgate.net{publication.css("nova-legacy-v-publication-item__title a::attr(href)").get()}'
            publication_type = publication.css("nova-legacy-v-publication-item__type::text").get()
            publication_date = publication.css(".nova-legacy-v-publication-item__meta-data-item::text").get()
            authors_name = publication.css(".nova-legacy-v-person-inline-item::text").get()
            snippet = publication.css("nova-legacy-e-expandable-text__container::text").get()
            reads = re.search(r"\d+", publication.css(".nova-legacy-v-publication-item__metrics-item::nth-child(1)::text").get()).group()
            citations = re.search(r"\d+", publication.css(".nova-legacy-v-publication-item__metrics-item::nth-child(2)").get()).group()
            
            journal_data["publications"].append({
                "title": title,
                "link": link,
                "publication_type": publication_type,
                "publication_date": publication_date,
                "authors": authors_name,
                "snippet": snippet,
                "reads": reads,
                "citations": citations
            })
            
        # scrape rest of the data starting from the second page
        page_num = 2
        
        while True:
            page.goto(f"https://www.researchgate.net/journal/{journal_name}/{page_num}")
            selector = Selector(text=page.content())

            for publication in selector.css(".nova-legacy-v-publication-item"):
                title = publication.css("nova-legacy-v-publication-item__title::text").get()
                link = f'https://www.researchgate.net{publication.css("nova-legacy-v-publication-item__title a::attr(href)").get()}'
                publication_type = publication.css("nova-legacy-v-publication-item__type::text").get()
                publication_date = publication.css(".nova-legacy-v-publication-item__meta-data-item::text").get()
                authors_name = publication.css(".nova-legacy-v-person-inline-item::text").get()
                snippet = publication.css("nova-legacy-e-expandable-text__container::text").get()
                reads = re.search(r"\d+", publication.css(".nova-legacy-v-publication-item__metrics-item::nth-child(1)::text").get()).group()
                citations = re.search(r"\d+", publication.css(".nova-legacy-v-publication-item__metrics-item::nth-child(2)").get()).group()
                
                journal_data["publications"].append({
                    "title": title,
                    "link": link,
                    "publication_type": publication_type,
                    "publication_date": publication_date,
                    "authors": authors_name,
                    "snippet": snippet,
                    "reads": reads,
                    "citations": citations
                })
            
            
            # checks for selector responsible for disabled pagination
            # if there's no page to paginate -> break
            if selector.css(".nova-legacy-c-pagination__next.is-disabled").get():
                break
            
            page_num += 1

        
        print(json.dumps(journal_data, indent=2, ensure_ascii=False))
        browser.close()
              
        
scrape_researchgate_journal(journal_name="Journal-of-Global-Information-Technology-Management-1097-198X")