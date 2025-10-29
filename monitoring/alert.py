import pandas as pd

THRESHOLD_ACC = 0.75
THRESHOLD_F1 = 0.7

def check_alerts():
    df = pd.read_csv("monitoring/metrics_log.csv", names=["timestamp", "accuracy", "f1_score"])
    latest = df.tail(1).iloc[0]

    if latest["accuracy"] < THRESHOLD_ACC or latest["f1_score"] < THRESHOLD_F1:
        print(" X Alert: model performance degraded")
    else:
        print(" VVV Model performance within safe range")

if __name__ == "__main__":
    check_alerts()
