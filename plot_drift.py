import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(
    "/home/krishna/epa_twin_project/drift.csv"
)

plt.figure(figsize=(8,5))

plt.plot(
    df["time"],
    df["drift"]
)

plt.xlabel("Time (s)")
plt.ylabel("Drift (m)")
plt.title("Actual vs Predicted Leg Drift")

plt.grid(True)

plt.savefig(
    "/home/krishna/epa_twin_project/drift_plot.png"
)

plt.show()
