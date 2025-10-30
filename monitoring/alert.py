import pandas as pd

THRESHOLD_F1 = 0.70
METRICS_FILE = "monitoring/metrics/latest_metrics.csv"

df = pd.read_csv(METRICS_FILE)
latest_f1 = df['f1'].iloc[-1]

if latest_f1 < THRESHOLD_F1:
    print(" XXX: Model performance degraded — retraining recommended")
else:
    print(" VVV Model performing well")
