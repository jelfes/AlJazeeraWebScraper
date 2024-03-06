import requests
from bs4 import BeautifulSoup

url = "https://www.aljazeera.com/news/2024/3/6/trumps-talk-on-gaza-highlights-stark-choice-for-voters-in-us-election"
page = requests.get(url)

soup = BeautifulSoup(page.content, "html.parser")

print(soup.find("header", class_="article-header").find("h1"))
