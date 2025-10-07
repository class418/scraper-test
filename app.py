import os
from flask import Flask, render_template_string, request
from scraper import scrape_quotes
from datetime import datetime

app = Flask(__name__)

HTML = """
<!doctype html>
<html>
<head>
<title>Quotes Scraper</title>
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
    quotes = []  # GET時も安全にループできるよう空リストに
    scraped_at = None

    if request.method == "POST":
        try:
            quotes = scrape_quotes()
            scraped_at = datetime.now()
            # ログに出力して Render でも確認可能
            for q in quotes:
                app.logger.info(q)
        except Exception as e:
            app.logger.error(f"Scraping error: {e}")
            quotes = [f"Error: {e}"]

    return render_template_string(HTML, quotes=quotes, scraped_at=scraped_at)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    # 開発用サーバーではなく gunicorn など本番WSGIで起動推奨
    app.run(host="0.0.0.0", port=port)
