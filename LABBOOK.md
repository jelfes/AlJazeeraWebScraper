# LabBook

##
- There are aljazeera urls that share an id but different url
- Unique id form url? --> Hash function

## 22 / 04 / 2024
- about 30% of washington post articles have `word_count=0`. This seems to be for diverse reasons. The `politics` section has a very low fraction of zero lenght articles (2%). THe `world` section has a very high one (70%). `Busisness` has 40% and `opinions` 7%.
- For the `world` section a lot of URLs seem to be not reachable. When checking them by hand, they forward me to the `washingtonpost.com` main page
- Slightly less than half of the zero word politics articles are `interactive` pages such as [this one](https://www.washingtonpost.com/politics/interactive/2024/14th-amendment-trump-ballot/).
- Maybe limit coverage to the 5000 politics articles?


## 18 / 04 / 2024
- Updated the extraction procedure. We now save the whole webpage as html. Further we extract the text and add it to the csv
- Everthing else might break the csv
- Later we will merge all CSVs and put them in a SQLite database
- Extracting a washington post article takes about 10 seconds. We will split up the ~60k articles in 6 jobs of 10k

## 18 / 04 / 2024
- First extraction of 1000 Washington Post articles using SONIC
- 14 articles were not wrapped in `<p>` tags
- Rest of the articles had a good looking word count distribution


## 02 / 04 / 2024
- Test if i can remove the `"Follow Al Jazeera English"` and `"In Pictures"` lines from the text. Works!
- settle on output naming convention for article retrieval: `ir_data_aljazeera_Timestamp_StartId.csv`
- start information retrieval on line 0
- Extraction stopped after index 7718
- Log: `ir_logs_20240402_095003.log`
- There is a peak of below 50 word articles. Most of them do not seem to be "In Pictures" but videos or news updates. 
- There are many of the type `"As the Russia-Ukraine war enters its 220th day, we take a look at the main developments."`
- Next starting index 7719
- Finished at 14099: `ir_logs_20240402_115240.log`
- Next starting index 14100
- Finished at 14177: `ir_logs_20240402_142642.log`
    - this was probably because I closed my Laptop
- Next starting index: 14178
- Finished at 14734: `ir_logs_20240402_143154.log`
    - this was probably because I closed my Laptop
- Next starting index: 14735
- Finished at 22247: `ir_logs_20240402_144032.log`
    - connection error (left building and WIFI)
- Next starting index: 22248
- Finished at 23348: `ir_logs_20240402_161959.log`
    - closed the laptop
- Next starting index: 23349

## 27 / 03 / 2024
- [Full article](https://www.aljazeera.com/economy/2022/12/12/cvs-walgreens-finalise-10bn-in-deals-to-settle-opioid-lawsuits) was not parsed correctly and had zeor words. Why?
- Article was properly wrapped in `<p> </p>` tags, but they had a class like `"Component-root-0-2-484 p Component-p-0-2-470"`. They were included due to this rule: `paragraphs = article.find_all("p", class_=None)` in the `get_text_v3` method.
- Scraper also extracted gallery content such as [this one](https://www.aljazeera.com/gallery/2022/9/14/photos-fire-crews-battle-massive-blazes-across-us-west), but only the text body.
- The new wrapper (without class exclusion), includes `"Follow Al Jazeera English:"` at the end of the artilce and the heading `"In Pictures"` for galleries.
- But only 3.16% (38 / 1201) of articles of have length zero --> maybe leave the wrapper more strict and add a second round without class restriction?
- [This article](https://www.aljazeera.com/news/2022/10/13/indias-supreme-court-panel-split-on-allowing-hijab-in-classrooms) has mixed paragraphs, some with and some without class
- Update outputpath of `article_retrieval.py` to adapt to the args


## 22 / 03 / 2024
- Tried parsing the content of Al Jazeera articles through different ways (`get_text_v1`, `get_text_v2`, and `get_text_v3`).
- Initially looking for a tag where the class contains "all-content".
- But in articles, each paragraph is wrapped within `<p> </p>` and so far it seems that these are the only things wrapped within these tag.
- Therfore, just extracting all text within paragraph tags gives us the whole articles, leaving out stuff like images, "Read Further", or newsletter signup forms.
- It also does not include title and subtitle of the article.
- The content of articles such as [videos](https://www.aljazeera.com/program/the-bottom-line/2024/3/10/will-israel-be-allowed-to-continue-its-gaza-starvation-strategy?traffic_source=rss), or [news briefs in bullet points](https://www.aljazeera.com/news/2024/3/10/israels-war-on-gaza-list-of-key-events-day-156?traffic_source=rss) is not in p-tags and thereofore they have a word count of 0 after parsing like that.
- But, this might be OK, as it is sensible to leave them out anyway.