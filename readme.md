# News Travels?

--- 

## Explanation

---

The expression ”News travels fast”, is often taken literally;however, how much truth is found within this expression? This project aims to investigate the aforementioned expression answering questions such as: how fast does news travel? What localized news events hold most importance? What is the scope of spread for a single localized news event? Through dynamic data scraping and Data Mining techniques, we provide substantial answers to the validity of the age old expression ”News travels fast”

--- 

## Methodology

* Given an initial location, local news publishers are found
* Every found publisher site is scraped for current news articles
* Through a user provided radius, cities within the area are found
* These cities local news publishers are also found and scraped.
* News stories between cities are compared to find matching content.
* This process is repeated recursively until initial new stories are no longer written about.

---

## Viusalization

![Spread of like news sources from Kitimat, BC](https://raw.githubusercontent.com/Daniel-OReilly/Tracking-the-Spread-of-News/master/images/Kitimat.png)
![Spread of like news sources from Prince George, BC](https://raw.githubusercontent.com/Daniel-OReilly/Tracking-the-Spread-of-News/master/images/princeGeorge.png)
![Spread of like news sources from Winnipeg, MB](https://raw.githubusercontent.com/Daniel-OReilly/Tracking-the-Spread-of-News/master/images/Winnipeg.png)



