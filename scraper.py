import requests
from bs4 import BeautifulSoup

def fetch_thread(dat_id):
    """
    dat_id: 例 "1759901460"
    戻り値: 書き込みリスト [(time, ID, text), ...]
    """
    URL = f"http://bbs.eddibb.cc/liveedge/dat/{dat_id}.dat"
    try:
        res = requests.get(URL)
        res.raise_for_status()
        content = res.text

        posts = []

        # 行ごとに分割
        lines = content.splitlines()
        for line in lines:
            if "<>" in line:
                parts = line.split("<>", 2)
                if len(parts) < 3:
                    continue
                time, user_id, text = parts
                # 不要なタグを除去
                text = text.replace("<br>", "\n")
                text = text.replace("<b>", "").replace("</b>", "")
                text = text.replace("&gt;", ">").replace("&lt;", "<").replace("&amp;", "&")
                posts.append((time.strip(), user_id.strip(), text.strip()))
        return posts
    except requests.RequestException as e:
        print(f"取得エラー: {e}")
        return []
