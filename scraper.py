# scraper.py
import requests

def fetch_subject_txt():
    URL = "http://bbs.eddibb.cc/liveedge/subject.txt"
    try:
        res = requests.get(URL)
        res.raise_for_status()
        lines = res.text.splitlines()
        formatted_lines = []

        for line in lines:
            if "<>" in line:
                file_id, rest = line.split("<>", 1)
                # タイトルとレス数を分割
                if "(" in rest and rest.endswith(")"):
                    title, count = rest.rsplit("(", 1)
                    count = count.rstrip(")")
                else:
                    title = rest
                    count = "0"
                formatted_lines.append(f"{title.strip()} — {count}レス")
        return formatted_lines

    except requests.RequestException as e:
        print(f"取得エラー: {e}")
        return []
