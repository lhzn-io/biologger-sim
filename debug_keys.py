import pandas as pd

data_path = (
    "/home/lhzn/Projects/whoi-mpg/datasets/Swordfish-RED001_20220812_19A0564/"
    "RED001_20220812_19A0564.csv"
)
df = pd.read_csv(
    data_path, comment=";", index_col=False, engine="python", on_bad_lines="warn", nrows=10
)
print("Columns:", df.columns.tolist())
record = df.iloc[5].to_dict()
print("Record keys:", record.keys())
print("Value for 'int aX':", record.get("int aX"))
print("Value for '\"int aX\"':", record.get('"int aX"'))
