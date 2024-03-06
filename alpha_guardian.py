import os
import requests
from bs4 import BeautifulSoup

API_KEY = os.environ.get("KEY_GUARDIAN")

url = f"https://content.guardianapis.com/search?api-key={API_KEY}"
page = requests.get(url)

print(page.json())
