import pandas as pd

# CSVファイルのパス
csv_file1 = "high-entropy-oxide/rocksalt-NiMgCuCoZnO/discussions/bo/data.csv"
csv_file2 = "high-entropy-oxide/rocksalt-NiMgCuCoZnO/discussions/random/data.csv"

# CSVファイルの読み込み
df1 = pd.read_csv(csv_file1)
df2 = pd.read_csv(csv_file2)

# ID列をインデックスに設定（必要に応じて）
df1 = df1.set_index("ID")
df2 = df2.set_index("ID")

# energy列がNaNの場合にdf2のenergy値をdf1にコピー
for index, row in df1.iterrows():
    if pd.isna(row["energy"]):
        if not pd.isna(df2.loc[index, "energy"]):
            df1.at[index, "energy"] = df2.loc[index, "energy"]

# マージ後のデータフレームをCSVファイルに保存
df1.to_csv("high-entropy-oxide/rocksalt-NiMgCuCoZnO/discussions/bo/merged_data.csv")

print("マージが完了しました")
