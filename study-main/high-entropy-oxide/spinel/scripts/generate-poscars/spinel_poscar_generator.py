import csv
import os
import random
import sys

from dotenv import load_dotenv

import spinel_count

# .envファイルの読み込み
load_dotenv()

REMOTE_DIR = os.getenv("REMOTE_DIR")
WORK_DIR = os.getenv("WORK_DIR")
# 生成する構造の数
num_structures = int(os.getenv("NUM_STRUCTURES") or 0)

# 出力先ディレクトリ
output_directory = f"{REMOTE_DIR}{WORK_DIR}/structures/one_million_models/POSCARs"

# ディレクトリが存在しない場合は作成
if not os.path.exists(output_directory):
    os.makedirs(output_directory)


# Znの数
num_zinc = 5

# 初めの行から追加する行までのテキスト
initial_text = """HEO_eq
1.0
        8.3941001892         0.0000000000         0.0000000000
        0.0000000000         8.3941001892         0.0000000000
        0.0000000000         0.0000000000         8.3941001892
   Zn Fe Ni Co Mn O
   5  4  5  5  5  32
Direct"""

# 追加する行
additional_lines_tet = [
    "0.125000000         0.125000000         0.125000000",
    "0.875000000         0.875000000         0.875000000",
    "0.625000000         0.125000000         0.625000000",
    "0.375000000         0.875000000         0.375000000",
    "0.125000000         0.625000000         0.625000000",
    "0.875000000         0.375000000         0.375000000",
    "0.625000000         0.625000000         0.125000000",
    "0.375000000         0.375000000         0.875000000",
]

additional_lines_oct = [
    "0.500000000         0.500000000         0.500000000",
    "0.250000000         0.750000000         0.000000000",
    "0.750000000         0.250000000         0.000000000",
    "0.750000000         0.000000000         0.250000000",
    "0.250000000         0.000000000         0.750000000",
    "0.000000000         0.250000000         0.750000000",
    "0.000000000         0.750000000         0.250000000",
    "0.500000000         0.000000000         0.000000000",
    "0.250000000         0.250000000         0.500000000",
    "0.750000000         0.750000000         0.500000000",
    "0.750000000         0.500000000         0.750000000",
    "0.250000000         0.500000000         0.250000000",
    "0.000000000         0.500000000         0.000000000",
    "0.500000000         0.250000000         0.250000000",
    "0.500000000         0.750000000         0.750000000",
    "0.000000000         0.000000000         0.500000000",
]

# 最後に追加するテキスト
final_text = """0.254900008         0.254900008         0.254900008
    0.745100021         0.745100021         0.745100021
    0.495099992         0.995100021         0.754899979
    0.504899979         0.004900008         0.245099992
    0.995100021         0.754899979         0.495099992
    0.004900008         0.245099992         0.504899979
    0.754899979         0.495099992         0.995100021
    0.245099992         0.504899979         0.004900008
    0.004900008         0.504899979         0.245099992
    0.995100021         0.495099992         0.754899979
    0.504899979         0.245099992         0.004900008
    0.495099992         0.754899979         0.995100021
    0.245099992         0.004900008         0.504899979
    0.754899979         0.995100021         0.495099992
    0.254900008         0.754899979         0.754899979
    0.745100021         0.245099992         0.245099992
    0.495099992         0.495099992         0.254900008
    0.504899979         0.504899979         0.745100021
    0.995100021         0.254900008         0.995100021
    0.004900008         0.745100021         0.004900008
    0.004900008         0.004900008         0.745100021
    0.995100021         0.995100021         0.254900008
    0.504899979         0.745100021         0.504899979
    0.495099992         0.254900008         0.495099992
    0.754899979         0.254900008         0.754899979
    0.245099992         0.745100021         0.245099992
    0.254900008         0.495099992         0.495099992
    0.745100021         0.504899979         0.504899979
    0.745100021         0.004900008         0.004900008
    0.254900008         0.995100021         0.995100021
    0.754899979         0.754899979         0.254900008
    0.245099992         0.245099992         0.745100021
"""


# 特徴量数(key)とID(value)を紐づけた逆引き辞書を入れる空の辞書を作る
features_ID_d = {}
ID_features_d = {}

metal_type = ["Zn", "Fe", "Ni", "Co", "Mn"]
# oct_siteの特徴量一覧を要素が被らないように作成
o_pairs = [
    tuple(["o", i, j])
    for i in metal_type[1:]
    for j in metal_type[1:]
    if metal_type.index(i) <= metal_type.index(j)
]
# tet_siteの特徴量一覧を要素が被らないように作成
t_pairs = [
    tuple(["t", i, j])
    for i in metal_type
    for j in metal_type[1:]
    if metal_type.index(i) <= metal_type.index(j)
]
# 両サイトの取りうるすべての特徴量一覧作成
all_pairs = tuple(o_pairs + t_pairs)

# 指定された数だけ構造を生成して出力
while len(features_ID_d) < num_structures:
    ID = len(features_ID_d) + 1
    # 出力ファイルのパス
    print("ID", ID)
    print(len(features_ID_d))
    output_file_path = os.path.join(output_directory, f"POSCAR_{ID}")

    if os.path.exists(output_file_path):
        print(f"{output_file_path} already exists.")
        sys.exit(1)

    # 初めの行から追加する行までのテキストを書き込み

    random.shuffle(additional_lines_tet)
    additional_lines_zinc = additional_lines_tet[:num_zinc]

    additional_lines_tet_and_oct = (
        additional_lines_tet[num_zinc:] + additional_lines_oct
    )
    random.shuffle(additional_lines_tet_and_oct)

    additional_lines = additional_lines_zinc + additional_lines_tet_and_oct

    count_result = spinel_count.main(
        additional_lines, ID, features_ID_d, ID_features_d, all_pairs
    )

    if count_result:
        with open(output_file_path, "w") as output_file:
            output_file.write(initial_text + "\n")
            for line in additional_lines:
                output_file.write(line + "\n")
            output_file.write(final_text)

if len(features_ID_d) == num_structures:
    with open(
        f"{REMOTE_DIR}{WORK_DIR}/calc/data.csv", "w", newline="", encoding="utf-8"
    ) as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["ID"] + ["_".join(pair) for pair in all_pairs] + ["result"])
        for ID in range(1, num_structures + 1):
            features_values = list(ID_features_d[ID])
            writer.writerow([ID] + features_values + [""])

else:
    print("Error: csv data number does not match the number of structures.")
    sys.exit(1)
# print(features_ID_d)
# print(len(additional_lines))
