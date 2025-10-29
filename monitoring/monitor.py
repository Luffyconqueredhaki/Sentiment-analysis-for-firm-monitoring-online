import pandas as pd
import datetime
import random

def log_metrics():
    metrics = {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "accuracy": round(random.uniform(0.70, 0.95), 3),
        "f1_score": round(random.uniform(0.65, 0.90), 3)
    }
    df = pd.DataFrame([metrics])
    df.to_csv("monitoring/metrics_log.csv", mode="a", index=False, header=False)
    print("✅ Metrics logged:", metrics)

if __name__ == "__main__":
    log_metrics()
