# scraper.py
import requests

def fetch_subject_txt():
    """
    subject.txt を取得して行ごとのリストとして返す
    """
    URL = "http://bbs.eddibb.cc/liveedge/subject.txt"
    try:
        res = requests.get(URL)
        res.raise_for_status()
        lines = res.text.splitlines()
        return lines
    except requests.RequestException as e:
        print(f"取得エラー: {e}")
        return []
