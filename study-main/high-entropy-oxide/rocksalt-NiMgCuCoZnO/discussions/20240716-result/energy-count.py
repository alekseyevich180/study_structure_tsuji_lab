import pandas as pd

csv_file = "high-entropy-oxide/rocksalt-NiMgCuCoZnO/discussions/bo/data.csv"
csv_file = "high-entropy-oxide/rocksalt-NiMgCuCoZnO/discussions/random/data.csv"
SPECIFIED_ID = 101
SPECIFIED_ENERGY = -336.2

df = pd.read_csv(csv_file)

filtered_df = df[df["ID"] >= SPECIFIED_ID]
filtered_df = filtered_df[
    pd.to_numeric(filtered_df["energy"], errors="coerce") <= SPECIFIED_ENERGY
]

count = filtered_df.shape[0]

print(f"ID {SPECIFIED_ID}以上, energy {SPECIFIED_ENERGY}ev以下: {count}")
