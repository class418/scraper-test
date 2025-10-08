import requests
import html

SUBJECT_URL = "http://bbs.eddibb.cc/liveedge/subject.txt"
THREAD_BASE_URL = "http://bbs.eddibb.cc/liveedge/dat/"

def fetch_subject_txt():
    """subject.txt からスレ一覧を取得"""
    res = requests.get(SUBJECT_URL)
    res.raise_for_status()
    lines = res.text.splitlines()
    threads = []
    for line in lines:
        if "<>" in line:
            dat, title_with_count = line.split("<>", 1)
            title = html.unescape(title_with_count)
            threads.append({
                "dat": dat.strip(),
                "title": title.strip()
            })
    return threads

def fetch_thread(dat_id):
    """指定 dat のスレを取得・整形"""
    url = THREAD_BASE_URL + dat_id + ".dat"
    res = requests.get(url)
    res.raise_for_status()
    lines = res.text.splitlines()
    posts = []

    for i, line in enumerate(lines):
        if not line.strip():
            continue
        parts = line.split("<>")
        # parts: [名前, 日付ID, 本文]
        name = html.unescape(parts[0]) if len(parts) > 0 else ""
        date_id = html.unescape(parts[1]) if len(parts) > 1 else ""
        content = html.unescape(parts[2]) if len(parts) > 2 else ""

        # sage を小さく
        if "sage" in date_id:
            date_id = date_id.replace("sage", "<small>sage</small>")

        # 0レス目はタイトルとして保存
        title = content if i == 0 else None

        posts.append({
            "num": i,
            "name": name,
            "date_id": date_id,
            "content": content,
            "title": title
        })
    return posts
