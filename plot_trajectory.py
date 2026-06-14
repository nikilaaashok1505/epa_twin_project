import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("foot_trajectory.csv")

plt.plot(df["time"], df["z"])

plt.xlabel("Time (s)")
plt.ylabel("Foot Height Z (m)")
plt.title("EPA Foot Trajectory")

plt.grid(True)

plt.show()
