Contents: introduction, project goals, tools used, data extraction, data cleaning, data visualization, observations, conclusions, kaggle-github links.

#### Introduction
Hey! My name is Dimitry Zub, currently transitioning from 3D modeling to Data Analytics (~over a month) and Python Programming (~3 months) field. Recently completed Google Data Analytics Professional Certificate from Coursera.

#### Project goals

The goals of this project were to better understand the process of gathering data, processing, cleaning, analyzing, and visualizing using industry tools. Besides that, I wanted to understand what is the most popular software, tag, affiliation among artists on Artstation.

#### Tools used
To scrape data these Python libraries/packages were used:
- `requests`
- `json`
- `googlesheets api`
- `selenium`
- `regex`

To clean, analyze and visualize data:
- `googlesheets`
- `tableau`

#### Data extraction
To extract data Python was used. Jump to the GitHub source code:
- [Scrape artwork links](https://github.com/dimitryzub/artstation-artwork-analysis/blob/main/scrape_links.py)
- [Scrape artworks itself](https://github.com/dimitryzub/artstation-artwork-analysis/blob/main/scrape_artworks.py)

#### Data cleaning

To clean and prepare data I used Google Sheets. Functions that were used:
```
=IMPORTRANGE()
=FILTER()
=SPLIT() or =SPLIT() + CHAR(10)
=IF() or =IF() + =ISBLANK()
=ISBLANK()
=COUNTIF()
=ROW()
```
`=IMPORTRANGE("SHEET_URL","'SHEET_NAME'!RANGE")` was used to import specific column(s) to different sheet in order to clean, analyze them.

`=FILTER()` was used to, well, filter specific word from the range, e.g. `=FILTER(A1:A, A1:A="Student")` will filter word "Student" from a whole column.

`=SPLIT()` + were used to split multiline cell:
```lang-none
# multi-line cell
ZBrush
Maya
Substance Painter
Mari
Photoshop
____
=SPLIT(A1,CHAR(10)) 
will split multiline cell to separate columns like so: 
ZBrush	Maya	Substance Painter	Mari	Photoshop
```

`=IF()` was used to check if the cell is blank, leave it blank.

`=ISBLANK()` was used in combination with `=IF()` to check if the cell is blank.

`=COUNTIF()` was used to count number of word occurrences in specific range, e.g. `=COUNTIF(SHEET_NAME!RANGE,"Word or cell reference")`

`=ROW()` was used to create unique ID's, e.g. `=ROW(A1)-1` will create `ID 1` rather than `ID 2` because of subtraction.

#### Data visualization

[Tableau public dashboard](https://public.tableau.com/app/profile/dimitry.zub/viz/Artstationanalysis/ArtstationDashboard)

![image](https://user-images.githubusercontent.com/78694043/119978304-23cb0380-bfc2-11eb-8b70-e84100fa7630.png)

![image](https://user-images.githubusercontent.com/78694043/119978269-1ada3200-bfc2-11eb-981f-b8ad2c2c0ff1.png)

![image](https://user-images.githubusercontent.com/78694043/119978237-101f9d00-bfc2-11eb-9285-e0d9bcf688ee.png)

Note: *following visualizations contains data bias. Not every tag, affiliation has taken to count due to the difficulties of data extraction, and the mistakes I made.*

#### Observations
##### Observations on personal mistakes made:
**The problem** is that each cell contained multiline `string` and when I was trying to `=SPLIT()` using `\n` delimiter it doesn't do anything. Instead I had to use `=SPLIT(CELL,CHAR(10))`

One of the options would be to distribute Tags directly to different variables inside Python code and enter them into the table under different columns so there no wasting time afterwards.

It would be a good idea to check right away in the table whether I get what was expected or not🙂

##### Observations about Artstation:
The description of the role / type of affiliation in most cases is not clear, confusing, not specific.

In this regard, from Recruiter point of view it may be difficult to find candidates due to the fact that simply something else is indicated in the brief role description.
Although from the point of view of professionalism the artist may be extremely good.

Consequence - an artist simply may not fall into the horizon of the Recruiter or anyone else who's looking for specific artist role.

As I see it, the type of employment should be standardized using drop-down list, keyword search or anything similar to the choice of the program used when publishing an artwork.

There everything is clear and understandable, e.g. "Software used: Blender, Photoshop", nothing like:
- "*Award winning Tattoo artist, digital art, 3d character art*": too much in one line, how to understand in which position person will show himself in best the light?
- "*I draw stuff*": not clear, specific, confusing.

#### Conclusions

The analysis of artists is very interesting. The next step(s) might be to understand the relationship between:
- the number of views to likes and comments.
- the number of views to the used program.
- the number of views and used tags.
- top 10 popular programs and top 10 popular tags.

Understand, what is the most popular genre and why.

#### Links:
* [Kaggle dataset](https://www.kaggle.com/dimitryzub/artstation)
* [GitHub repository](https://github.com/dimitryzub/artstation-artwork-analysis) with available source code that was used to extract data from the Artstation.

*Thank you for going all the way to these words! Hope you get a bit of value out of this post.*