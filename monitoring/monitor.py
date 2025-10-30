import pandas as pd
from sklearn.metrics import accuracy_score, f1_score
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from datetime import datetime

MODEL_PATH = "model"  
DATA_FILE = "monitoring/data/new_data.csv"
METRICS_FILE = "monitoring/metrics.csv"

def load_model():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
    return pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

def preprocess_label(label):
    mapping = {"positive": "LABEL_2", "neutral": "LABEL_1", "negative": "LABEL_0"}
    return mapping[label]

def invert_pred(pred):
    mapping = {"LABEL_2": "positive", "LABEL_1": "neutral", "LABEL_0": "negative"}
    return mapping[pred]

def main():
    df = pd.read_csv(DATA_FILE)
    classifier = load_model()

    preds = [classifier(text)[0]["label"] for text in df["text"]]
    preds = [invert_pred(p) for p in preds]

    acc = accuracy_score(df["label"], preds)
    f1 = f1_score(df["label"], preds, average='macro')

    row = {"timestamp": datetime.now(), "accuracy": acc, "f1": f1}
    pd.DataFrame([row]).to_csv(METRICS_FILE, mode='a', header=not pd.io.common.file_exists(METRICS_FILE), index=False)

if __name__ == "__main__":
    main()
