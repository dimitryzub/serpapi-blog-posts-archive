from playwright.sync_api import sync_playwright
import json, time, re

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, slow_mo=50)
    page = browser.new_page(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36', 
                            viewport={'width': 1920, 'height': 1080})
    page.goto('https://play.google.com/store/apps/details?id=com.topsecurity.android&hl=en_GB&gl=US')

    # open user reviews window
    page.locator('button.VfPpkd-LgbsSe.aLey0c', has_text='See all reviews').click()
    time.sleep(1)

    user_comments = []

    if page.query_selector('.VfPpkd-wzTsW'):

        last_height = page.evaluate("document.querySelector('.fysCi').scrollHeight;")
        page.screenshot(path='start_of_the_reviews.png', full_page=True)

        while True:
            print('Scrolling..')

            # Scroll down
            page.evaluate("document.querySelector('.fysCi').scrollTo(0, document.querySelector('.fysCi').scrollHeight);")
            time.sleep(0.5)

            current_height = page.evaluate("document.querySelector('.fysCi').scrollHeight;")
            print(f'last height = {last_height}')
            print(f'current height = {current_height}')

            if current_height == last_height:
                break
            else:
                last_height = current_height
    else:
        print('Looks like the review window does not appear.')

    print('Extracting reviews...')

    for index, comment in enumerate(page.query_selector_all('.RHo1pe'), start=1):
        user_comments.append({
            'position': index,
            'name': comment.query_selector('.X5PpBb').text_content(),
            'avatar': comment.query_selector('.gSGphe img').get_attribute('src'),
            'rating': re.search(r'\d+', comment.query_selector('.Jx4nYe .iXRFPc').get_attribute('aria-label')).group(),
            'comment_likes': comment.query_selector('[jscontroller=SWD8cc]').get_attribute('data-original-thumbs-up-count'),
            'date': comment.query_selector('.bp9Aid').text_content(),
            'comment': comment.query_selector('.h3YV2d').text_content(),
        })
        
    print(json.dumps(user_comments, indent=2, ensure_ascii=False))
    page.screenshot(path='end_of_the_reviews.png', full_page=True)

    browser.close()