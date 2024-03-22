import requests
from bs4 import BeautifulSoup

url = "https://www.aljazeera.com/gallery/2024/3/10/180000-women-unite-against-violence-in-mexico-city-on-international-women?traffic_source=rss"
page = requests.get(url)

soup = BeautifulSoup(page.content, "html.parser")

# save fiel
with open("parsed_page.html", "w", encoding="utf-8") as file:
    file.write(soup.prettify())

# print(soup.find("header", class_="article-header").find("h1"))
main_content = soup.find("main", id="main-content-area")

with open("parsed_main_content.html", "w", encoding="utf-8") as file:
    file.write(main_content.prettify())


print(main_content.text)
