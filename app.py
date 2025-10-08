import os
from flask import Flask, render_template_string, request
from scraper import fetch_subject_txt, fetch_thread
from datetime import datetime

app = Flask(__name__)

HTML_INDEX = """
<!doctype html>
<html>
<head>
<title>スレ一覧</title>
</head>
<body>
<h1>スレ一覧</h1>
<form method="post">
    <button type="submit">取得</button>
</form>

{% if threads %}
<h2>取得日時: {{ scraped_at }}</h2>
<ul>
{% for thread in threads %}
    <li>
        <a href="/thread/{{ thread.id }}">{{ thread.title }} — {{ thread.count }}</a>
    </li>
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
<a href="/">戻る</a>
<hr>
{% for num, post in posts %}
    {% if num == 0 %}
    <!-- タイトルは大きく表示 -->
    <div style="margin-bottom:1em; padding:0.5em; border:1px solid #ccc; font-size:1.5em; font-weight:bold;">
        #{{ num }} {{ post|safe }}
    </div>
    {% else %}
    <div style="margin-bottom:1em; padding:0.5em; border:1px solid #ccc;">
        <b>#{{ num }}</b><br>
        <pre>{{ post|safe }}</pre>
    </div>
    {% endif %}
{% endfor %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    threads = []
    scraped_at = None
    if request.method == "POST":
        lines = fetch_subject_txt()
        scraped_at = datetime.now()
        for line in lines:
            if "<>" in line:
                dat_id, rest = line.split("<>", 1)
                dat_id = dat_id.strip()
                if dat_id.endswith(".dat"):
                    dat_id = dat_id[:-4]
                if "—" in rest:
                    title, count = rest.split("—", 1)
                else:
                    title = rest
                    count = "0レス"
                threads.append({"id": dat_id, "title": title.strip(), "count": count.strip()})
    return render_template_string(HTML_INDEX, threads=threads, scraped_at=scraped_at)


@app.route("/thread/<thread_id>")
def thread(thread_id):
    posts = fetch_thread(thread_id)
    return render_template_string(HTML_THREAD, thread_id=thread_id, posts=posts)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
