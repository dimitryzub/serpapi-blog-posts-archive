After analysis a couple of things noticed:
- The highest amount of reviews is located in Lviv which is a consequence of the most active place where coffee shops are in demand (*based on sample size and data gathered from Google maps*).
- Mariupol has the least coffee shop attendance (*based on sample size and data gathered from Google maps*).

Contents: intro, data, project goals, tools used, data preparation, code, visualization, links, conclusions, outro and next step.

### Intro
A personal portfolio project to analyze coffee shops from 10 Ukrainian cities.

### Data
- Each city contains only 20 data points to analyze.
- The [sample size](https://www.scribbr.com/methodology/population-vs-sample/#:~:text=A%20population%20is%20the%20entire,t%20always%20refer%20to%20people.) is not calculated to better represents the total [population](https://www.scribbr.com/methodology/population-vs-sample/#:~:text=A%20population%20is%20the%20entire,t%20always%20refer%20to%20people.).
- Data was scraped from Google Maps Local Results.

### Project goals
- Data extraction and preparation.
- Data cleaning.
- Data analysis.
- Data visualization.
- Data analysis life cycle.

### Tools used
- [Google Maps Locals Results API](https://serpapi.com/maps-local-results) from SerpApi.
- Python
- Google Sheets
- Tableau

### Data preparation
There were a number of empty rows. To avoid uncertain results, [delete empty rows](https://optakey.com/delete-empty-rows/) Google sheets add-on was used to get the job done.

### Code
The following block of code scrapes: place name, type, rating, reviews, price, delivery, dine in and takeout options.
```python
from serpapi import GoogleSearch
import csv

params = {
  "api_key": "YOUR_API_KEY",
  "engine": "google_maps",
  "type": "search",
  "google_domain": "google.com",
  "q": "кофе мариуполь",
  "ll": "@47.0919234,37.5093148,12z"
}

search = GoogleSearch(params)
results = search.get_dict()


with open('mariupol_coffee_data.csv', mode='w', encoding='utf8') as csv_file:
    fieldnames = ['Place name', 'Place type', 'Rating', 'Reviews', 'Price', 'Delivery option', 'Dine in option', 'Takeout option']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    coffee_data = []

    for result in results['local_results']:
        place_name = result['title']
        place_type = result['type']
        try:
            rating = result['rating']
        except:
            rating = None
        try:
            reviews = result['reviews']
        except:
            reviews = None
        try:
            price = result['price']
        except:
            price = None
        try:
            delivery_option = result['service_options']['delivery']
        except:
            delivery_option = None
        try:
            dine_in_option = result['service_options']['dine_in']
        except:
            dine_in_option = None
        try:
            takeout_option = result['service_options']['takeout']
        except:
            takeout_option = None

        coffee_data.append({
            'Place name': place_name,
            'Place type': place_type,
            'Rating': rating,
            'Reviews': reviews,
            'Price': price,
            'Delivery option': delivery_option,
            'Dine in option': dine_in_option,
            'Takeout option': takeout_option,
        })

    for data in coffee_data:
        writer.writerow(data)

print('Finished')
```

Google Maps Locals Results API from SerpApi is a paid API with a free trial of 5,000 searches.

If you're using Python, you can do the same thing with `Selenium` browser automation.

The main differences between writing your own code and using an API is that you don't have to tinker to find certain elements of the page to scrape, it's already done for the end-user with a `JSON` output, or dueling with Google to avoid CAPTCHA or finding proxies if they are needed, or other things that might encounter.

The whole process (20 places from each city (10 in total)) took ~30 minutes to scrape all needed data.

### Visualization
![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/aue8dfirp9oq20cnukef.png)

### Links
1. [Tableau visualization](https://public.tableau.com/app/profile/dimitry.zub/viz/UkraineCoffeePlaces/ComboChartRatingReviews).
2. [Google Maps Local Results API](https://serpapi.com/maps-local-results) from SerpApi.
3. [Kaggle dataset](https://www.kaggle.com/dimitryzub/10-coffee-places-from-ukrainian-cities).
4. Code also available as [GitHub Gist](https://gist.github.com/dimitryzub/a52247dfbc79985199b6b6c3c42f0456).

### Conclusions
- The highest amount of reviews is located in Lviv.
- Mariupol has the least place attendance.

### Outro and next step
Thank you for reading this far. The next steps might be to find:
- correlation between the workload hours of the place and the number of reviews this place gains.
- correlation between available delivery, dine in, takeout options and the number of reviews or rating gained from these available options.
- reason why some places have a lowest/highest ratings. Analyze those places by scraping peoples comments in combination with NLP to identify certain word patterns that are repeated in one or other cases.

> Yours,
D.