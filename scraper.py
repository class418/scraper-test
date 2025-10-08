import requests

def fetch_subject_txt():
    """
    subject.txt を取得して整形済みリストを返す
    戻り値: ["タイトル — 123レス", ...]
    """
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
                formatted_lines.append(f"{file_id}<> {title.strip()} — {count}レス")
        return formatted_lines

    except requests.RequestException as e:
        print(f"取得エラー: {e}")
        return []


def fetch_thread(dat_id):
    """
    .dat ファイルを取得して整形済みリストを返す
    dat_id: 例 "1759901460"
    戻り値: [(time, ID, text), ...]
    """
    URL = f"http://bbs.eddibb.cc/liveedge/dat/{dat_id}.dat"
    try:
        res = requests.get(URL)
        res.raise_for_status()
        content = res.text

        posts = []

        lines = content.splitlines()
        for line in lines:
            if "<>" in line:
                parts = line.split("<>", 2)
                if len(parts) < 3:
                    continue
                time, user_id, text = parts

                # 不要タグ除去、改行保持
                text = text.replace("<br>", "\n")
                text = text.replace("<b>", "").replace("</b>", "")

                # HTMLエスケープ
                text = text.replace("&gt;", ">").replace("&lt;", "<").replace("&amp;", "&")

                # <>sage<> を sage に置換
                text = text.replace("<>sage<>", "sage")

                posts.append((time.strip(), user_id.strip(), text.strip()))
        return posts

    except requests.RequestException as e:
        print(f"取得エラー: {e}")
        return []
