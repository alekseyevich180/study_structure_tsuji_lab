import os

from dotenv import load_dotenv


# .envファイルの読み込み
load_dotenv()
# print(os.environ['MAIN_DIR'])

REMOTE_DIR = os.getenv("REMOTE_DIR")
WORK_DIR = os.getenv("WORK_DIR")

# パラメータの定義
ROOT_PATH = f"{REMOTE_DIR}{WORK_DIR}/calc"

# sys.exit(0)
# 八面体間隙の近接オフセット
neighbor_oct = [
    (0, 0.25, 0.25),
    (0.25, 0, 0.25),
    (0.25, 0.25, 0),
    (0, 0.25, -0.25),
    (0.25, 0, -0.25),
    (0.25, -0.25, 0),
]

# 四面体間隙の近接オフセット
neighbor_tet = [
    (0.375, 0.125, 0.125),
    (0.125, 0.375, 0.125),
    (0.125, 0.125, 0.375),
    (-0.375, 0.125, 0.125),
    (-0.125, 0.375, 0.125),
    (-0.125, 0.125, 0.375),
    (0.375, -0.125, 0.125),
    (0.125, -0.375, 0.125),
    (0.125, -0.125, 0.375),
    (0.375, 0.125, -0.125),
    (0.125, 0.375, -0.125),
    (0.125, 0.125, -0.375),
    (-0.375, -0.125, 0.125),
    (-0.125, -0.375, 0.125),
    (-0.125, -0.125, 0.375),
    (-0.375, 0.125, -0.125),
    (-0.125, 0.375, -0.125),
    (-0.125, 0.125, -0.375),
    (0.375, -0.125, -0.125),
    (0.125, -0.375, -0.125),
    (0.125, -0.125, -0.375),
    (-0.375, -0.125, -0.125),
    (-0.125, -0.375, -0.125),
    (-0.125, -0.125, -0.375),
]


def main(additional_lines, ID, features_ID_d, ID_features_d, all_pairs):
    # 全特徴量名(key)と0(value)を辞書登録しカウントできるようにする
    features_counts = {pair: 0 for pair in all_pairs}

    central_coords = []
    # 金属原子座標を3列のリストとして作成し、要素を変更不能な浮動小数扱いのtupleにする
    for line in additional_lines:
        central_coords.append(tuple(map(float, line.split())))
        # POSCARの順番に原子名を並べた24×1のリストを作成
        atom_value = ["Zn"] * 5 + ["Fe"] * 4 + ["Ni"] * 5 + ["Co"] * 5 + ["Mn"] * 5
        # 原子座標(keys)と原子名(value)を辞書対応させる
        atom_search = dict(zip(central_coords, atom_value))
    # 全ての金属原子に対する特徴量カウントを行う
    site_check(central_coords, atom_search, features_counts)

    # 特徴量の内訳
    # print(features_counts)
    # POSCAR_IDがiの時の特徴量の総和の確認
    # print("POSCAR_ID = ",ID,"    特徴量の総和の確認 = ",sum(features_counts.values()))
    # 全カウント終了後、特徴量名に辞書登録した値をcsvファイルに書き出すコードを書く(目標)

    # features_countsのValue部分(特徴量のカウント)をリスト化する
    features_values = []
    for pair in all_pairs:
        features_values.append(features_counts[pair])

    # 同じ特徴量をもつことがないか確認する
    if tuple(features_values) in features_ID_d:
        print("Features are duplicated")
        return False
    else:
        ID_features_d[ID] = tuple(features_values)
        # 特徴量数(key)とID(value)を紐づけた逆引き辞書をつくる
        features_ID_d[tuple(features_values)] = ID
        # print(features_ID_d)
        return True
    # check_features.pyのcheck_main関数を実行し、特徴量の総和が0かどうかを確認する
    # check_features.check_main(additional_lines, ID, features_counts)


# 中心原子がoct_siteに位置するときの特徴量処理
def oct_combinations(x, y, z, central_atom, atom_search, features_counts):
    for dx, dy, dz in neighbor_oct:
        # 中心座標の値から最近接がとりうる座標を取得
        neighbor_coord = ((x + dx) % 1, (y + dy) % 1, (z + dz) % 1)
        # 最近接の座標から原子を特定(座標に原子が存在しない場合を省く)
        neighbor_atom = atom_search.get(neighbor_coord)
        if neighbor_atom is not None:
            o_fea = features_counts.get(("o", central_atom, neighbor_atom))
            if o_fea is not None:
                features_counts[("o", central_atom, neighbor_atom)] += 1
            else:
                features_counts[("o", neighbor_atom, central_atom)] += 1


# 中心原子がtet_siteに位置するときの特徴量処理
def tet_combinations(x, y, z, central_atom, atom_search, features_counts):
    for dx, dy, dz in neighbor_tet:
        # 中心座標の値から最近接がとりうる座標を取得
        neighbor_coord = ((x + dx) % 1, (y + dy) % 1, (z + dz) % 1)
        # 最近接の座標から原子を特定(座標に原子が存在しない場合を省く)
        neighbor_atom = atom_search.get(neighbor_coord)
        # 最近接座標候補に原子が存在するときを条件づける
        if neighbor_atom is not None:
            t_fea = features_counts.get(("t", central_atom, neighbor_atom))
            if t_fea is not None:
                features_counts[("t", central_atom, neighbor_atom)] += 1
            else:
                features_counts[("t", neighbor_atom, central_atom)] += 1


def site_check(central_coords, atom_search, features_counts):
    for a in range(len(central_coords)):
        # 中心原子座標をxyz座標として取得
        x, y, z = central_coords[a]
        central_atom = atom_search[central_coords[a]]
        # 座標から中心原子がtet_siteかoct_siteを判別し、最近接との組み合わせを特徴量に加算
        if x / 0.125 % 2 == 0:
            oct_combinations(x, y, z, central_atom, atom_search, features_counts)
        else:
            tet_combinations(x, y, z, central_atom, atom_search, features_counts)
