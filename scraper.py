import requests
from bs4 import BeautifulSoup

def main():
    url = "https://example.com"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    
    # h2タグを抽出して表示
    titles = [t.text for t in soup.find_all("h2")]
    print("Titles:", titles)

if __name__ == "__main__":
    main()
