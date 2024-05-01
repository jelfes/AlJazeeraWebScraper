import re
import pandas as pd
import sqlite3
import logging
import argparse
import requests

from csv import writer
from bs4 import BeautifulSoup
from tqdm import tqdm
from pathlib import Path
from datetime import datetime
from config_local import DATA_DIR
from content_parsing import get_paragraphs, merge_paragraphs


parser = argparse.ArgumentParser()
parser.add_argument(
    "-s",
    "--start_row",
    type=int,
    default=0,
    help="The first row to start from.",
)
parser.add_argument(
    "-e",
    "--end_row",
    type=int,
    default=0,
    help="The row to end.",
)
parser.add_argument(
    "-t",
    "--test",
    type=bool,
    default=False,
    help="Setting to test mode.",
)


args = vars(parser.parse_args())

# load urls
conn = sqlite3.connect(Path(DATA_DIR, "database.db"))
QUERY = """
    SELECT *
    FROM aljazeera_urls_01082022_10032024
    """
aljazeera_urls = pd.read_sql(QUERY, conn)

# setup output format
df_header = pd.DataFrame(
    {
        "hash_id": [],
        "url": [],
        "title": [],
        "retrieval_time": [],
        "web_page": [],
        "full_text": [],
        "word_count": [],
    }
)


# logging
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

OUTPUT_PATH = Path(
    DATA_DIR,
    f"ir_data_aljazeera_{timestamp}_{args['start_row']}_{args['end_row']}.csv",
)

if args["test"]:
    OUTPUT_PATH = Path(
        DATA_DIR,
        "tests",
        f"ir_data_aljazeera_{timestamp}_{args['start_row']}_{args['end_row']}.csv",
    )


logging.basicConfig(
    filename=f"logs/ir_logs_{timestamp}.log",
    encoding="utf-8",
    format="%(asctime)s %(message)s",
    level=logging.INFO,
)
logging.captureWarnings(True)
logging.info("Start logging")
logging.info(f"Starting row:\t\t{args['start_row']}")
logging.info(f"End row:\t\t\t{args['end_row']}")
logging.info(f"Output is saved to:\t{OUTPUT_PATH.absolute()}")
logging.info("##############################################################\n")


# create file if it does not yet exist
with open(OUTPUT_PATH, "a") as f:
    df_header.to_csv(f, header=f.tell() == 0, index=False)

# iterate over articles
url_subset = aljazeera_urls.iloc[args["start_row"] : args["end_row"]]


for row in tqdm(url_subset.itertuples(), total=len(url_subset)):
    page = requests.get(row.url)

    logging.info(f"Article ID: \t{row.hash_id}")
    logging.info(f"Article title: \t{row.title}")
    logging.info(f"Row: \t\t\t{row.Index}")
    logging.info(f"URL: \t\t\t{row.url}")
    logging.info(f"Request status:\t{page.status_code}")

    article = BeautifulSoup(page.content, "html.parser")
    paragraphs = get_paragraphs(article)
    full_text = merge_paragraphs(paragraphs, None, None)
    word_count = len(full_text.split())
    retrieval_time = datetime.now()

    article_file_path = Path("web_pages", f"{row.hash_id}.html")

    # save article
    with open(Path(DATA_DIR, article_file_path), "w", encoding="utf-8") as file:
        file.write(article.prettify())

    new_row = [
        row.hash_id,
        row.url,
        row.title,
        retrieval_time,
        article_file_path,
        full_text,
        word_count,
    ]

    with open(OUTPUT_PATH, "a") as f:
        writer_object = writer(f)

        writer_object.writerow(new_row)

    logging.info("##############################################################\n")
