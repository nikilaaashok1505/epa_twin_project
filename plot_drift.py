import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("drift.csv")

# Take every 20th point
df = df.iloc[::20]

plt.figure(figsize=(10,5))

plt.plot(
    df["time"],
    df["drift"],
    linewidth=2
)

plt.xlabel("Time (s)")
plt.ylabel("Drift (m)")
plt.title("Actual vs Predicted Foot Drift")

plt.grid(True)

plt.tight_layout()

plt.savefig("drift_plot_clean.png")

plt.show()
