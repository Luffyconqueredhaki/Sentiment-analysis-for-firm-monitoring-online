import pandas as pd

df = pd.read_csv("monitoring/metrics/latest_metrics.csv")
print(df.tail())

