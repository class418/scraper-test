import os
from flask import Flask, render_template_string, request
from scraper import fetch_subject_txt, fetch_thread
import html

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
<meta charset="utf-8">
<title>{{ posts[0].content if posts else 'Thread' }}</title>
</head>
<body>
<a href="/">戻る</a>
{% if posts %}
    <!-- 0レス目はタイトルとして大きく表示 -->
    <h2 style="font-size:1.5em;">{{ posts[0].content|safe }}</h2>
    <p><strong>{{ posts[0].name }}</strong> {{ posts[0].datetime_id }}</p>

    <!-- それ以降のレス -->
    <ul>
    {% for p in posts[1:] %}
        <li>
            <strong>#{{ loop.index }} {{ p.name }}</strong> {{ p.datetime_id }}<br>
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

        # 整形処理
        for p in posts:
            # HTMLエスケープ
            p['content'] = html.escape(p['content'])

            # <>sage<> を小さく
            p['content'] = p['content'].replace("&lt;&gt;sage&lt;&gt;", "<small>sage</small>")

            # <> を消す
            p['content'] = p['content'].replace("&lt;&gt;", "")

            # URLをリンクに変換 (http/https)
            import re
            p['content'] = re.sub(r"(https?://\S+)", r'<a href="\1">\1</a>', p['content'])

            # 画像リンクを <img> に変換
            p['content'] = re.sub(r'(https?://\S+\.(?:jpg|jpeg|png|gif))', r'<br><img src="\1" style="max-width:300px;"><br>', p['content'])

    except Exception as e:
        posts = []
        app.logger.error(f"Error fetching thread {dat_id}: {e}")

    return render_template_string(HTML_THREAD, posts=posts)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
