import pandas as pd

# CSVファイルの読み込み
CSV_FILE_PATH = "high-entropy-oxide/rocksalt-NiMgCuCoZnO/scripts/generate-poscars/data.csv"
data = pd.read_csv(CSV_FILE_PATH)

# 'ID'と'energy'列を無視してデータを比較
data_without_id_energy = data.drop(columns=["ID", "energy"])

# 重複する行を見つける
duplicates = data_without_id_energy.duplicated(keep=False)

# 重複する行のIDの集合のリストを作成
duplicate_ids = (
    data[duplicates]
    .groupby(list(data_without_id_energy.columns))
    .agg(list)["ID"]
    .tolist()
)

# 結果の概要を出力
print(f"Number of duplicates: {len(duplicate_ids)}")

# 結果の出力
# for ids in duplicate_ids:
#     print(ids)
