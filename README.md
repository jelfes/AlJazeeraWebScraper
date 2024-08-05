This repository contains code to scrape news websites. The files `aljazeera_article_retrieval.py` and `washingtonpost_article_retrieval.py` are adapted to specifically scrape Al Jazeera and the Washington Post. `general_article_retrieval.py` can be used as basic template. 

## Setup
Make a local copy of `config_global.py` called `config_local.py` and fill in your local constants.

The general scraper expects a `file_path` to a csv file with URLs. The file needs the following columns `["hash_id", "title", "Index", "url"]`. This follows the format of [Media Cloud](https://search.mediacloud.org/), which can be used to get the URLs of news articles for a specific topic, source, time frame.