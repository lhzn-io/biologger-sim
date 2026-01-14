import sys

import numpy as np
import pandas as pd


def compare(file1: str, file2: str) -> None:
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    # Slice to same length for comparison
    n = min(len(df1), len(df2))
    df1_slice = df1.iloc[:n]
    df2_slice = df2.iloc[:n]

    print(f"Comparing first {n} records...")

    # Columns to compare (Self vs Baseline)
    # Both use: Depth, pseudo_x, pseudo_y

    results = {}

    # 1. Depth
    results["depth_mae"] = np.abs(df1_slice["Depth"] - df2_slice["Depth"]).mean()
    results["depth_max_err"] = np.abs(df1_slice["Depth"] - df2_slice["Depth"]).max()

    # 2. X Track
    results["x_mae"] = np.abs(df1_slice["pseudo_x"] - df2_slice["pseudo_x"]).mean()
    results["x_max_err"] = np.abs(df1_slice["pseudo_x"] - df2_slice["pseudo_x"]).max()

    # 3. Y Track
    results["y_mae"] = np.abs(df1_slice["pseudo_y"] - df2_slice["pseudo_y"]).mean()
    results["y_max_err"] = np.abs(df1_slice["pseudo_y"] - df2_slice["pseudo_y"]).max()

    # Print results
    for k, v in results.items():
        print(f"{k}: {v:.6f}")

    # Check for spikes (where depth error > 1.0m)
    spikes = np.where(np.abs(df1_slice["Depth"] - df2_slice["Depth"]) > 1.0)[0]
    if len(spikes) > 0:
        print(f"Found {len(spikes)} depth spikes (>1.0m error)")
        print("First 5 spike indices:", spikes[:5])
        for idx in spikes[:5]:
            v1 = df1_slice["Depth"].iloc[idx]
            v2 = df2_slice["Depth"].iloc[idx]
            print(f"Index {idx}: Self={v1:.2f}, Baseline={v2:.2f}")
    else:
        print("No depth spikes (>1.0m) found in the comparison.")


if __name__ == "__main__":
    compare(sys.argv[1], sys.argv[2])
