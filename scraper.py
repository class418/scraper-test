import requests
from bs4 import BeautifulSoup
from datetime import datetime

URL = "https://quotes.toscrape.com/"

def main():
    res = requests.get(URL)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")

    quotes = []
    for quote_div in soup.find_all("div", class_="quote"):
        text = quote_div.find("span", class_="text").text.strip()
        author = quote_div.find("small", class_="author").text.strip()
        quotes.append(f"{text} — {author}")

    print(f"Scraped at {datetime.now()}")
    for q in quotes:
        print(q)

if __name__ == "__main__":
    main()
