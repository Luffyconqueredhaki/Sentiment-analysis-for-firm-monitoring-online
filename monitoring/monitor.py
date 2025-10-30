import pandas as pd
from transformers import pipeline
from datasets import load_dataset
from sklearn.metrics import accuracy_score, f1_score
from datetime import datetime
import os
import sys

# Import preprocessing from src
sys.path.append(".")
from src.preprocessing import preprocess_social

MODEL = "cardiffnlp/twitter-roberta-base-sentiment-latest"
CSV_PATH = "monitoring/metrics.csv"
N_SAMPLES = 30
COMPANY_KEYWORD = "Tesla"

def load_fresh_tweets(keyword):
    ds = load_dataset("cardiffnlp/tweet_sentiment_multilingual","english", split="train")
    df = ds.to_pandas()
    df = df[df["text"].str.contains(keyword, case=False, na=False)]
    return df.sample(min(N_SAMPLES, len(df)))

def convert_label(label):
    # map HF 3-class to binary
    if label == 2: return 1   # positive
    if label == 1: return 0   # neutral
    return 0                  # negative

def map_prediction(pred):
    if pred == "positive": return 1
    return 0

def run_monitoring():
    print("Loading tweets...")
    tweets = load_fresh_tweets(COMPANY_KEYWORD)
    tweets["clean"] = tweets["text"].apply(preprocess_social)
    tweets["true"] = tweets["label"].apply(convert_label)

    clf = pipeline("sentiment-analysis", model=MODEL)

    print("Running inference")
    tweets["pred"] = tweets["clean"].apply(lambda x: map_prediction(clf(x)[0]["label"]))

    acc = accuracy_score(tweets["true"], tweets["pred"])
    f1 = f1_score(tweets["true"], tweets["pred"])

    print(f"Accuracy: {acc:.4f}, F1: {f1:.4f}")

    row = pd.DataFrame([{
        "timestamp": datetime.now(),
        "accuracy": acc,
        "f1": f1
    }])

    mode = "a" if os.path.exists(CSV_PATH) else "w"
    header = not os.path.exists(CSV_PATH)

    row.to_csv(CSV_PATH, mode=mode, header=header, index=False)
    print("Metrics saved.")

if __name__ == "__main__":
    run_monitoring()

