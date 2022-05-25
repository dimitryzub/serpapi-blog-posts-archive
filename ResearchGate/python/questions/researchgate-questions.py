from parsel import Selector
from playwright.sync_api import sync_playwright
import json


def scrape_researchgate_questions(query: str):
    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True, slow_mo=50)
        page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36")
        
        questions = []
        page_num = 1

        while True:
            page.goto(f"https://www.researchgate.net/search/question?q={query}&page={page_num}")
            selector = Selector(text=page.content())
            
            for question in selector.css(".nova-legacy-c-card__body--spacing-inherit"):
                title = question.css(".nova-legacy-v-question-item__title .nova-legacy-e-link--theme-bare::text").get().title()
                title_link = f'https://www.researchgate.net{question.css(".nova-legacy-v-question-item__title .nova-legacy-e-link--theme-bare::attr(href)").get()}'
                question_type = question.css(".nova-legacy-v-question-item__badge::text").get()
                question_date = question.css(".nova-legacy-v-question-item__meta-data-item:nth-child(1) span::text").get()
                
                views = question.css(".nova-legacy-v-question-item__metrics-item:nth-child(1) .nova-legacy-e-link--theme-bare::text").get()
                views_link = question.css(".nova-legacy-v-question-item__metrics-item:nth-child(1) .nova-legacy-e-link--theme-bare::attr(href)").get()

                answer = question.css(".nova-legacy-v-question-item__metrics-item+ .nova-legacy-v-question-item__metrics-item .nova-legacy-e-link--theme-bare::text").get()
                answer_link = question.css(".nova-legacy-v-question-item__metrics-item+ .nova-legacy-v-question-item__metrics-item .nova-legacy-e-link--theme-bare::attr(href)").get()

                questions.append({
                    "title": title,
                    "link": title_link,
                    "question_type": question_type,
                    "question_date": question_date,
                    "views": {
                        "views_count": views,
                        "views_link": views_link
                        },
                    "answer": {
                        "answer_count": answer,
                        "answers_link": answer_link
                    }
                })

            print(f"page number: {page_num}")

            # checks if next page arrow key is greyed out `attr(rel)` (inactive) and breaks out of the loop
            if selector.css(".nova-legacy-c-button-group__item:nth-child(9) a::attr(rel)").get():
                break
            else:
                page_num += 1


        print(json.dumps(questions, indent=2, ensure_ascii=False))
        browser.close()
        

scrape_researchgate_questions(query="coffee")