from flask import Flask, render_template_string, request
from scraper import scrape_quotes
from datetime import datetime

app = Flask(__name__)

HTML = """
<!doctype html>
<html>
<head>
<title>Scraper</title>
</head>
<body>
<h1>Quotes Scraper</h1>
<form method="post">
    <button type="submit">Scrape Now</button>
</form>
{% if quotes %}
<h2>Scraped at {{ scraped_at }}</h2>
<ul>
{% for q in quotes %}
    <li>{{ q }}</li>
{% endfor %}
</ul>
{% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    quotes = None
    scraped_at = None
    if request.method == "POST":
        quotes = scrape_quotes()
        scraped_at = datetime.now()
    return render_template_string(HTML, quotes=quotes, scraped_at=scraped_at)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
