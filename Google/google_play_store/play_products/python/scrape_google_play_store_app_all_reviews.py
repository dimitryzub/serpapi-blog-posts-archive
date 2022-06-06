import time, json
from playwright.sync_api import sync_playwright


def run(playwright):
    # currently runs only with headful mode. 
    page = playwright.chromium.launch(headless=True).new_page()
    page.goto("https://play.google.com/store/apps/details?id=com.instantbrands.app&gl=US&showAllReviews=true")

    page.mouse.wheel(deltaY=50)
    last_height = page.evaluate("() => document.body.scrollHeight")  # scrollHeight: 5879

    reached_end = False
    while not reached_end:
        if page.query_selector('[jsname=i3y3Ic]'):
            page.query_selector('[jsname=i3y3Ic]').click(force=True)
            time.sleep(4)
        else:
            page.keyboard.press("End")
            time.sleep(4)

        new_height = page.evaluate("() => document.body.scrollHeight")
        if new_height == last_height:
            reached_end = True
        else:
            last_height = new_height

    app_user_comments = []

    for comment in page.query_selector_all(".zc7KVe"):
        user_name = comment.query_selector(".X43Kjb").inner_text()
        print(user_name)

        try:
            user_avatar = comment.query_selector(".vDSMeb.bAhLNe img").get_attribute("src")
        except: user_avatar = None

        try:
            user_comment = comment.query_selector("[jsname=fbQN7e]").inner_text()
        except: user_comment = None

        try:
            comment_likes = comment.query_selector(".jUL89d.y92BAb").inner_text()
        except: comment_likes = None

        try:
            app_rating = comment.query_selector(".pf5lIe div[role=img]").get_attribute("aria-label").split(" ")[1]
        except: app_rating = None

        try:
            comment_date = comment.query_selector(".p2TkOb").inner_text()
        except: comment_date = None

        if user_name and user_avatar and user_comment and comment_likes and app_rating and comment_date not in app_user_comments and not None:
            app_user_comments.append({
                "user_name": user_name,
                "user_avatar": user_avatar,
                "user_comment": user_comment,
                "comment_likes": comment_likes,
                "app_rating": app_rating,
                "comment_date": comment_date
            })

    print(json.dumps(app_user_comments, indent=2))

    page.close()


with sync_playwright() as playwright:
    run(playwright)