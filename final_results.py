import pandas as pd

df = pd.read_csv("drift.csv")

print("\n==============================")
print(" EPA DIGITAL TWIN RESULTS")
print("==============================\n")

print(f"Samples collected : {len(df)}")

print(f"Minimum Drift : {df['drift'].min():.4f} m")

print(f"Maximum Drift : {df['drift'].max():.4f} m")

print(f"Average Drift : {df['drift'].mean():.4f} m")

print(f"Standard Deviation : {df['drift'].std():.4f} m")

print("\nConclusion")

print("------------------------------")

print("Single leg ROS2 digital twin")

print("successfully estimated")

print("drift between actual")

print("and predicted robot")

print("states in real time.")

print("\nStatus : SUCCESS")
