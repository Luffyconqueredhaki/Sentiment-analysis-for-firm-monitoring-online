import pandas as pd
import matplotlib.pyplot as plt

# Carica il CSV con le metriche
df = pd.read_csv("monitoring/metrics_log.csv", names=["timestamp", "accuracy", "f1_score"])

plt.figure(figsize=(8,4))
plt.plot(df["timestamp"], df["accuracy"], marker="o", label="Accuracy")
plt.plot(df["timestamp"], df["f1_score"], marker="x", label="F1-score")
plt.xticks(rotation=45)
plt.legend()
plt.title("Model Performance Over Time")
plt.tight_layout()
plt.show()
