import pandas as pd
from sklearn.metrics import accuracy_score, f1_score
from transformers import AutoModelForSequenceClassification, AutoTokenizer, TextClassificationPipeline

MODEL_PATH = "model/"
DATA_PATH = "monitoring/data/new_data.csv"
THRESHOLD_F1 = 0.70

def load_model():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
    pipeline = TextClassificationPipeline(model=model, tokenizer=tokenizer)
    return pipeline

def load_data(path):
    df = pd.read_csv(path)
    return df["text"].tolist(), df["label"].tolist()

def evaluate(pipeline, texts, labels):
    preds = pipeline(texts)
    y_pred = [p['label'] for p in preds]
    acc = accuracy_score(labels, y_pred)
    f1 = f1_score(labels, y_pred, average='weighted')
    return acc, f1

def save_metrics(acc, f1):
    df = pd.DataFrame([{"accuracy": acc, "f1": f1}])
    df.to_csv("monitoring/metrics/latest_metrics.csv", index=False)

def main():
    pipeline = load_model()
    texts, labels = load_data(DATA_PATH)
    acc, f1 = evaluate(pipeline, texts, labels)
    save_metrics(acc, f1)
    print(f"Accuracy: {acc:.4f}, F1: {f1:.4f}")

    if f1 < THRESHOLD_F1:
        print("Performance drop detected — retraining required")

if __name__ == "__main__":
    main()

