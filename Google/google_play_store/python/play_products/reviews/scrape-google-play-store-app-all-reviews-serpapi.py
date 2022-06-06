from serpapi import GoogleSearch
import os, json

# TODO: when Google Play Product Reviews API Fix is there -> update code.
params = {
    # https://docs.python.org/3/library/os.html#os.getenv
    "api_key": os.getenv("API_KEY"),   # serpapi API key
    "engine": "google_play_product",
    "store": "apps",
    "gl": "us",
    "product_id": "com.google.android.youtube"
}

search = GoogleSearch(params)          # where data extraction happens

user_comments = []

while True:
    
    print(f"Extracted #{params['ijn']} page.")
    
    # JSON -> Python dict (actual data is here)
    results = search.get_dict()

    # checks for "Google hasn't returned any results for this query."
    if "error" not in results:
        for image in results["images_results"]:
            if image["original"] not in user_comments:  
                user_comments.append(image["original"])
        
        # update to the next page
        params["ijn"] += 1
        print(params["ijn"])
    else:
        print(results["error"])
        break

print(json.dumps(user_comments, indent=2))
print(len(user_comments))