import os
from flask import Flask, render_template_string, request
from scraper import fetch_subject_txt, fetch_thread

app = Flask(__name__)

HTML_INDEX = """
<!doctype html>
<html>
<head>
<title>Edge Board Threads</title>
</head>
<body>
<h1>Edge Board Threads</h1>
<ul>
{% for t in threads %}
    <li><a href="/thread/{{ t.dat }}">{{ t.title }}</a></li>
{% endfor %}
</ul>
</body>
</html>
"""

HTML_THREAD = """
<!doctype html>
<html>
<head>
<title>{{ posts[0].title if posts else 'Thread' }}</title>
</head>
<body>
<a href="/">戻る</a>
{% if posts %}
    <h2 style="font-size:1.5em;">{{ posts[0].title }}</h2>
    <ul>
    {% for p in posts %}
        <li>
            <strong>#{{ p.num }} {{ p.name }}</strong> {{ p.date_id }}<br>
            {{ p.content|safe }}
        </li>
    {% endfor %}
    </ul>
{% else %}
    <p>スレが見つかりません。</p>
{% endif %}
</body>
</html>
"""

@app.route("/")
def index():
    try:
        threads = fetch_subject_txt()
    except Exception as e:
        threads = []
        app.logger.error(f"Error fetching subject.txt: {e}")
    return render_template_string(HTML_INDEX, threads=threads)

@app.route("/thread/<dat_id>")
def thread(dat_id):
    try:
        posts = fetch_thread(dat_id)
    except Exception as e:
        posts = []
        app.logger.error(f"Error fetching thread {dat_id}: {e}")
    return render_template_string(HTML_THREAD, posts=posts)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
