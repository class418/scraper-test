import requests
from bs4 import BeautifulSoup

URL = "https://quotes.toscrape.com/"

def scrape_quotes():
    res = requests.get(URL)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")

    quotes = []
    for quote_div in soup.find_all("div", class_="quote"):
        text = quote_div.find("span", class_="text").text.strip()
        author = quote_div.find("small", class_="author").text.strip()
        quotes.append(f"{text} — {author}")
    return quotes
