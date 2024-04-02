# LabBook

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