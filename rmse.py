import pandas as pd
import numpy as np

df = pd.read_csv("drift.csv")

rmse = np.sqrt(np.mean(df["drift"]**2))

print("RMSE =", round(rmse,4),"m")
print("Maximum Drift =", round(df["drift"].max(),4),"m")
print("Average Drift =", round(df["drift"].mean(),4),"m")
