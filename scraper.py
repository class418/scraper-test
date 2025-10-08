import requests
from bs4 import BeautifulSoup
import html

BASE_URL = "http://bbs.eddibb.cc/liveedge"

def fetch_subject_txt():
    """subject.txt を取得して行ごとに返す"""
    url = f"{BASE_URL}/subject.txt"
    res = requests.get(url)
    res.raise_for_status()
    text = res.text
    return text.strip().splitlines()


def fetch_thread(dat_id):
    """スレッド .dat を取得して整形したリストを返す"""
    if dat_id.endswith(".dat"):
        dat_id = dat_id[:-4]  # 念のため
    url = f"{BASE_URL}/dat/{dat_id}.dat"
    res = requests.get(url)
    res.raise_for_status()
    raw = res.text
    return parse_thread(raw)


def parse_thread(raw):
    """raw データをレス番号付きで整形"""
    posts = []
    # <> で分割。空白や改行を除去
    segments = [s.strip() for s in raw.split("<>") if s.strip()]
    
    for idx, seg in enumerate(segments):
        # HTML エスケープ解除（絵文字復元）
        seg = html.unescape(seg)
        # sage を小さく灰色表示
        seg = seg.replace("sage", "<span style='color:gray; font-size:0.8em;'>sage</span>")
        posts.append((idx, seg))
    return posts
