import requests
import html

SUBJECT_URL = "http://bbs.eddibb.cc/liveedge/subject.txt"
THREAD_BASE_URL = "http://bbs.eddibb.cc/liveedge/dat/"

def fetch_subject_txt():
    """
    subject.txt からスレ一覧を取得
    返り値: [{'dat': dat_id, 'title': title}, ...]
    """
    res = requests.get(SUBJECT_URL)
    res.raise_for_status()
    lines = res.text.splitlines()
    threads = []

    for line in lines:
        if "<>" in line:
            dat, title_with_count = line.split("<>", 1)
            dat = dat.strip().replace(".dat", "")  # .dat が二重にならないように
            title = html.unescape(title_with_count.strip())
            threads.append({
                "dat": dat,
                "title": title
            })
    return threads


def fetch_thread(dat_id):
    """
    スレの .dat を取得して整形
    返り値: [{'no': 0, 'name': ..., 'datetime': ..., 'id': ..., 'text': ...}, ...]
    """
    dat_id = dat_id.replace(".dat", "")  # 念のため .dat を除去
    url = THREAD_BASE_URL + dat_id + ".dat"
    res = requests.get(url)
    res.raise_for_status()
    lines = res.text.splitlines()

    posts = []
    for i, line in enumerate(lines):
        if "<>" in line:
            parts = line.split("<>")
            name = parts[0].strip()
            post_datetime = parts[1].strip() if len(parts) > 1 else ""
            user_id = parts[2].strip() if len(parts) > 2 else ""
            text = parts[3].strip() if len(parts) > 3 else ""

            # HTML エスケープ復元
            text = html.unescape(text)

            # <>sage<> を小さく sage 表示
            text = text.replace("<>sage<>", "sage")

            posts.append({
                "no": i,
                "name": name,
                "datetime": post_datetime,
                "id": user_id,
                "text": text
            })
    return posts
