import re
import requests
from bs4 import BeautifulSoup


def get_content(url: str) -> list[str]:
    """
    Extract title, subtitle, and the full article text from an Al Jazeera article in html format.

    Args:
        article: the article

    Returns:
        The title, the subtitle, and the full text
    """

    page = requests.get(url)

    article = BeautifulSoup(page.content, "html.parser")

    title = get_title(article)
    subtitle = get_subtitle(article)
    text = get_text(article)

    return title, subtitle, text


def get_title(article: BeautifulSoup) -> str:
    """
    Extracts the title from an Al Jazeera html page.

    Args:
        article: The article

    Returns:
        The title
    """

    header = article.find("header", class_="article-header")
    title = header.find("h1").text

    return title


def get_subtitle(article: BeautifulSoup) -> str:
    """
    Extracts the subtitle from an Al Jazeera html page.

    Args:
        article: The article

    Returns:
        The subtitle
    """

    header = article.find("header", class_="article-header")
    title = header.find("p").text

    return title


def get_text(article: BeautifulSoup) -> str:
    """
    Extracts the main text from an Al Jazeera html page. This does not include the title or subtitle (see `get_title` and `get_subtitle`).

    Args:
        article: The article

    Returns:
        The main text
    """

    counter = 0

    if not article.find("main"):
        raise ValueError("No main body found.")

    for s in article.find("main"):

        is_content = False
        # skip non-class objects
        if not s.get("class"):
            continue

        # search for "all-content" object
        for c in s["class"]:
            if re.search("all-content", c):
                is_content = True
                counter += 1

        if is_content:
            text = []
            for p in s.find_all("p"):
                text.append(p.text)

            full_text = "\n".join(text)

    # error handling
    if counter == 0:
        raise ValueError("No main text found.")
    elif counter > 1:
        raise ValueError(f"Found {counter} main text element. Returning last one.")

    return full_text


def get_text_v2(article: BeautifulSoup) -> str:
    """
    Extracts the main text from an Al Jazeera html page. This does not include the title or subtitle (see `get_title` and `get_subtitle`).

    Args:
        article: The article

    Returns:
        The main text
    """

    counter = 0

    if not article.find("main"):
        raise ValueError("No main body found.")

    main = article.find("main")
    content = main.find_all(class_=re.compile(r"all-content"))

    text = []
    for p in content.find_all("p"):
        text.append(p.text)

    full_text = "\n".join(text)

    # error handling
    if len(content) == 0:
        raise ValueError("No main text found.")
    elif len(content) > 1:
        raise ValueError(f"Found {counter} main text element. Returning last one.")

    return full_text


def get_text_v3(article: BeautifulSoup) -> str:
    """
    Extracts all text withing a paragraph from an Al Jazeera html page.

    Args:
        article: The article

    Returns:
        The main text
    """

    if not article.find("p"):
        raise ValueError("No paragraphs found.")

    paragraphs = article.find_all("p", class_=None)

    text = []
    for p in paragraphs:
        text.append(p.text)

    full_text = "\n".join(text)

    return full_text


def get_text_v4(article: BeautifulSoup) -> str:
    """
    Extracts all text withing a paragraph from an Al Jazeera html page.

    Args:
        article: The article

    Returns:
        The main text
    """

    if not article.find("p"):
        raise ValueError("No paragraphs found.")

    paragraphs = article.find_all("p")

    text = []
    for p in paragraphs:
        text.append(p.text)

    full_text = "\n".join(text)

    return full_text
