import os
import random

WORK_DIR = "high-entropy-oxide/rocksalt-NiMgCuCoZnO/discussions/fix-cu"
FILE_NAME = "POSCAR"
DIR_NAME = "structures"

# POSCARファイルを読み込む
with open(f"{WORK_DIR}/{FILE_NAME}", "r") as file:
    lines = file.readlines()

# ヘッダー部分と座標部分を分ける
header = lines[:8]
coordinates = lines[8:]

# 各元素の行を分ける
ni_lines = [line for line in coordinates if "Ni" in line]
mg_lines = [line for line in coordinates if "Mg" in line]
co_lines = [line for line in coordinates if "Co" in line]
zn_lines = [line for line in coordinates if "Zn" in line]
cu_lines = [line for line in coordinates if "Cu" in line]
o_lines = [line for line in coordinates if "O" in line]

# structuresディレクトリを作成
os.makedirs(f"{WORK_DIR}/{DIR_NAME}", exist_ok=True)

# 新しいPOSCARファイルを10個生成
for i in range(10):
    # Ni, Mg, Co, Znの行をランダムに並び替える
    random.shuffle(ni_lines)
    random.shuffle(mg_lines)
    random.shuffle(co_lines)
    random.shuffle(zn_lines)

    # 新しい座標リストを作成
    new_coordinates = ni_lines + mg_lines + cu_lines + co_lines + zn_lines + o_lines

    # 新しいPOSCARファイルの内容を作成
    new_poscar_content = header + new_coordinates

    # 新しいPOSCARファイルを保存
    with open(f"{WORK_DIR}/{DIR_NAME}/{FILE_NAME}_{i+1}", "w") as new_file:
        new_file.writelines(new_poscar_content)
