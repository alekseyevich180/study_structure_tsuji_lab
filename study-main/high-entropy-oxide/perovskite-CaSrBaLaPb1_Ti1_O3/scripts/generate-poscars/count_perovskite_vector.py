"""
(Ca Sr Ba La Pb)0.2 Ti1 O3
   Ca  Sr  Ba  La  Pb  Ti    O
   5   5   5   6   6   27   81
"""

import os

from dotenv import load_dotenv

# .envファイルの読み込み
load_dotenv()

REMOTE_DIR = os.getenv("REMOTE_DIR")
WORK_DIR = os.getenv("WORK_DIR")

# パラメータの定義
DATA_CSV_OUTPUT_DIRECTORY = f"{REMOTE_DIR}{WORK_DIR}/calc"
CSV_FILE_NAME = "data.csv"

# 第２近接金属(5種金属同士では最近接)の座標
neighbor_coord_1st = [
    (1, 0, 0),
    (0, 1, 0),
    (0, 0, 1),
]


def main(
    local_coord_metal,
    local_id,
    local_features_ID_dictionary,
    local_id_features_dictionary,
    pairs,
):
    # 全特徴量名(key)とカウント数(value)を辞書登録しカウントできるようにする
    # カウント数は初期値0
    features_counts = {pair: 0 for pair in pairs}

    # 金属原子座標のタプルのリストを作成
    # (要素は変更不能な浮動小数のtuple)
    central_coords = []
    # 全ての金属原子に対する特徴量カウントを行う
    for coord in local_coord_metal:
        # 座標の組をそれぞれ３軸に分割してリストに格納
        central_coords.append(tuple(map(lambda x: round(float(x) * 3), coord.split())))
        # 金属原子27個のリストを作成
        atom_value = ["Ca"] * 5 + ["Sr"] * 5 + ["Ba"] * 5 + ["La"] * 6 + ["Pb"] * 6
        # 原子座標(keys)と原子名(value)をタプルとして結合させ、辞書を作成
        atom_search = dict(zip(central_coords, atom_value))
    site_check(central_coords, atom_search, features_counts)
    # site_checkの定義は後述

    # 特徴量の内訳
    # print(features_counts)
    # POSCAR_IDがiの時の特徴量の総和の確認
    # print("POSCAR_ID = ",local_id,"    特徴量の総和の確認 = ",sum(features_counts.values()))
    # 全カウント終了後、特徴量名に辞書登録した値をcsvファイルに書き出すコードを書く(目標)

    # features_countsのValue部分(特徴量のカウント)をリスト化する
    features_values = []
    for pair in pairs:
        features_values.append(features_counts[pair])

    # 同じ特徴量をもつことがないか確認する
    if tuple(features_values) in local_features_ID_dictionary:
        print("特徴量の重複を検出しました")
        return False
    else:
        local_id_features_dictionary[local_id] = tuple(features_values)
        # 特徴量数(key)とID(value)を紐づけた逆引き辞書をつくる
        local_features_ID_dictionary[tuple(features_values)] = local_id

        # print(local_features_ID_dictionary)
        return True


# 特徴量処理
def combinations(x, y, z, central_atom, atom_search, features_counts):
    for dx, dy, dz in neighbor_coord_1st:
        # 中心座標の値から最近接がとりうる座標を取得
        neighbor_coord = ((x + dx) % 3, (y + dy) % 3, (z + dz) % 3)
        # 最近接の座標から原子を特定(座標に原子が存在しない場合を省く)
        neighbor_atom = atom_search.get(neighbor_coord)
        if neighbor_atom is not None:
            o_fea = features_counts.get((central_atom, neighbor_atom))
            if o_fea is not None:
                features_counts[(central_atom, neighbor_atom)] += 1
            else:
                features_counts[(neighbor_atom, central_atom)] += 1

                # i→neighbor_atom, j→central_atom


def site_check(central_coords, atom_search, features_counts):
    for a in range(len(central_coords)):
        # 中心原子座標をxyz座標として取得
        x, y, z = central_coords[a]
        central_atom = atom_search[central_coords[a]]
        # 最近接との組み合わせを特徴量に加算
        combinations(x, y, z, central_atom, atom_search, features_counts)
