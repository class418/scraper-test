import os
from flask import Flask, render_template_string, request
from scraper import fetch_subject_txt, fetch_thread
from datetime import datetime

app = Flask(__name__)

HTML_INDEX = """
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

{% if threads %}
<h2>Scraped at {{ scraped_at }}</h2>
<ul>
{% for thread in threads %}
    <li><a href="/thread/{{ thread.id }}">{{ thread.title }} — {{ thread.count }}レス</a></li>
{% endfor %}
</ul>
{% endif %}
</body>
</html>
"""

HTML_THREAD = """
<!doctype html>
<html>
<head>
<title>Thread {{ thread_id }}</title>
</head>
<body>
<h1>Thread {{ thread_id }}</h1>
<a href="/">戻る</a>
<hr>
{% for time, user_id, text in posts %}
<div style="margin-bottom: 1em; padding: 0.5em; border:1px solid #ccc;">
    <b>{{ time }} {{ user_id }}</b><br>
    <pre>{{ text }}</pre>
</div>
{% endfor %}
</body>
</html>
"""

# スレ一覧
@app.route("/", methods=["GET", "POST"])
def index():
    threads = []
    scraped_at = None
    if request.method == "POST":
        lines = fetch_subject_txt()
        scraped_at = datetime.now()
        for line in lines:
            if "—" in line:
                title, count = line.split("—", 1)
                dat_id = title.split()[0]  # 先頭ID部分
                threads.append({"id": dat_id, "title": title, "count": count.strip()})
    return render_template_string(HTML_INDEX, threads=threads, scraped_at=scraped_at)

# スレ内容表示
@app.route("/thread/<thread_id>")
def thread(thread_id):
    posts = fetch_thread(thread_id)
    return render_template_string(HTML_THREAD, thread_id=thread_id, posts=posts)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
