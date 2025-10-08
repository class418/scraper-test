import requests

THREAD_BASE_URL = "https://bbs.eddibb.cc/liveedge/dat/"

def fetch_thread(dat_id):
    """指定 dat のスレを取得・整形"""
    url = THREAD_BASE_URL + dat_id
    res = requests.get(url)
    res.encoding = 'utf-8'
    text = res.text
    return parse_thread(text)

def parse_thread(dat_text):
    lines = dat_text.splitlines()
    parsed = []

    for line in lines:
        if not line.strip():
            continue
        parts = line.split("<>")
        if len(parts) >= 3:
            name = parts[0]
            datetime_id = parts[1]
            content = parts[2]
            # HTML エスケープを復元
            content = content.replace("&gt;", ">").replace("&lt;", "<").replace("&amp;", "&")
            # <>sage<> は小さく表示
            content = content.replace("<>sage<>", "<small>sage</small>")
            parsed.append({
                "name": name,
                "datetime_id": datetime_id,
                "content": content
            })
    return parsed
