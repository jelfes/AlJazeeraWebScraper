import re
import pandas as pd
import logging
import argparse
import requests

from csv import writer
from bs4 import BeautifulSoup
from tqdm import tqdm
from pathlib import Path
from datetime import datetime
from config_local import DATA_DIR
from content_parsing import get_text_v4


parser = argparse.ArgumentParser()
parser.add_argument(
    "-s",
    "--start_row",
    type=int,
    default=0,
    help="The first row to start from.",
)
parser.add_argument(
    "-p",
    "--output_path",
    type=str,
    default="output.csv",
    help="Path to the output file.",
)

args = vars(parser.parse_args())

OUTPUT_PATH = Path(args["output_path"])
# load urls
aljazeera_urls = pd.read_csv(Path(DATA_DIR, "mc_aljazeera_01082022_10032024.csv"))

# setup output format
df_header = pd.DataFrame(
    {
        "id": [],
        "url": [],
        "title": [],
        "retrieval_time": [],
        "full_text": [],
        "word_count": [],
    }
)


# logging
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

logging.basicConfig(
    filename=f"logs/ir_logs_{timestamp}.log",
    encoding="utf-8",
    format="%(asctime)s %(message)s",
    level=logging.INFO,
)
logging.captureWarnings(True)
logging.info("Start logging")
logging.info(f"Starting row: {args['start_row']}")
logging.info(f"Output is saved to: {OUTPUT_PATH.absolute()}")
logging.info("##############################################################\n")


# create file if it does not yet exist
with open(OUTPUT_PATH, "a") as f:
    df_header.to_csv(f, header=f.tell() == 0, index=False)

# iterate over articles
url_subset = aljazeera_urls.iloc[args["start_row"] :]  # .head(1000)

from config_local import SEED

url_subset = url_subset.sample(25, random_state=SEED)


for row in tqdm(url_subset.itertuples(), total=len(url_subset)):
    page = requests.get(row.url)

    logging.info(f"Article ID: \t{row.id}")
    logging.info(f"Article title: \t{row.title}")
    logging.info(f"Row: \t\t\t{row.Index}")
    logging.info(f"URL: \t\t\t{row.url}")
    logging.info(f"Request status:\t{page.status_code}")

    article = BeautifulSoup(page.content, "html.parser")
    full_text = get_text_v4(article)
    word_count = len(full_text.split())
    retrieval_time = datetime.now()

    new_row = [row.id, row.url, row.title, retrieval_time, full_text, word_count]

    with open(OUTPUT_PATH, "a") as f:
        writer_object = writer(f)

        writer_object.writerow(new_row)

    logging.info("##############################################################\n")
