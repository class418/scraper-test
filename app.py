import os
from flask import Flask, render_template_string, request
from scraper import fetch_subject_txt
from datetime import datetime

app = Flask(__name__)

HTML = """
<!doctype html>
<html>
<head>
<title>Subject.txt Scraper</title>
</head>
<body>
<h1>Subject.txt Scraper</h1>
<form method="post">
    <button type="submit">Scrape Now</button>
</form>

{% if lines %}
<h2>Scraped at {{ scraped_at }}</h2>
<ul>
{% for line in lines %}
    <li>{{ line }}</li>
{% endfor %}
</ul>
{% endif %}

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    lines = []
    scraped_at = None

    if request.method == "POST":
        try:
            lines = fetch_subject_txt()
            scraped_at = datetime.now()
            for line in lines:
                app.logger.info(line)
        except Exception as e:
            app.logger.error(f"Scraping error: {e}")
            lines = [f"Error: {e}"]

    return render_template_string(HTML, lines=lines, scraped_at=scraped_at)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
