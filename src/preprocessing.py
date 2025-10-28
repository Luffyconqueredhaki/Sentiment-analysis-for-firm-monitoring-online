# src/preprocessing.py
import html
import re
import emoji

def preprocess_social(text: str) -> str:
    #Pulisce un testo proveniente da social media
    if not isinstance(text, str):
        return ""
    t = html.unescape(text)
    t = re.sub(r"@\w+", "@user", t)
    t = re.sub(r"http\S+|www\.\S+", "http", t)
    t = re.sub(r"#(\w+)", r"\1", t)
    t = emoji.demojize(t)
    t = re.sub(r"\s+", " ", t).strip()
    return t
