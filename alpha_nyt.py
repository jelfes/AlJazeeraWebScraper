import os
import requests

API_KEY = os.environ.get("KEY_NYT")

url = f"https://api.nytimes.com/svc/search/v2/articlesearch.json?q=election&api-key={API_KEY}"
page = requests.get(url)

print(page.json())
