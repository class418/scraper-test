import requests
from bs4 import BeautifulSoup

URL = "https://www.scrapethissite.com/pages/countries/"

def main():
    res = requests.get(URL)
    res.raise_for_status()  # エラーがあれば停止

    soup = BeautifulSoup(res.text, "html.parser")

    countries = []
    for country_div in soup.find_all("div", class_="country"):
        name = country_div.find("h3", class_="country-name").text.strip()
        population = country_div.find("span", class_="country-population").text.strip()
        gdp = country_div.find("span", class_="country-gdp").text.strip()
        countries.append({
            "name": name,
            "population": population,
            "gdp": gdp
        })

    for c in countries:
        print(c)

if __name__ == "__main__":
    main()
