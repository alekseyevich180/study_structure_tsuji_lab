# import os
import math


def check_main(additional_lines, ID, features_counts):
    elements_list = []

    # 各元素を指定された行数分だけ追加
    elements_list.extend(["Zn"] * 5)  # 1~5行目までZn
    elements_list.extend(["Fe"] * 4)  # 6~9行目までFe
    elements_list.extend(["Ni"] * 5)  # 10~14行目までNi
    elements_list.extend(["Co"] * 5)  # 15~19行目までCo
    elements_list.extend(["Mn"] * 5)

    central_coords = []
    for line in additional_lines:
        central_coords.append(tuple(map(float, line.split())))

    check_site_check(central_coords, elements_list, features_counts)

    # 特徴量の内訳
    # print(features_counts)
    # POSCAR_IDがiの時の特徴量の総和の確認
    # print("POSCAR_ID = ",ID,"    特徴量の総和の確認 = ",sum(features_counts.values()))
    # features_countsのvalueの値がすべて０の時にtrueを返す
    print(all(value == 0 for value in features_counts.values()))


def check_site_check(central_coords, elements_list, features_counts):
    for c in range(len(central_coords)):
        x, y, z = central_coords[c]
        # 座標から中心原子がtet_siteかoct_siteを判別し、最近接との組み合わせを特徴量に加算
        if x / 0.125 % 2 == 0:
            check_oct_combinations(
                c, central_coords, x, y, z, elements_list, features_counts
            )
        else:
            check_tet_combinations(
                c, central_coords, x, y, z, elements_list, features_counts
            )


def check_oct_combinations(c, central_coords, x, y, z, elements_list, features_counts):
    for d in range(len(central_coords)):
        x1, y1, z1 = central_coords[d]
        distance = (x1 - x) ** 2 + (y1 - y) ** 2 + (z1 - z) ** 2
        if distance == 0.125 or distance == 0.625 or distance == 1.125:
            central_atom = elements_list[c]
            neighbor_atom = elements_list[d]

            o_fea = features_counts.get(("o", central_atom, neighbor_atom))
            if o_fea is not None:
                features_counts[("o", central_atom, neighbor_atom)] -= 0.5
            else:
                features_counts[("o", neighbor_atom, central_atom)] -= 0.5


def check_tet_combinations(c, central_coords, x, y, z, elements_list, features_counts):
    for d in range(len(central_coords)):
        x1, y1, z1 = central_coords[d]
        dx = math.fabs(x1 - x)
        dy = math.fabs(y1 - y)
        dz = math.fabs(z1 - z)
        check_number = min(dx, 1 - dx) + min(dy, 1 - dy) + min(dz, 1 - dz)
        if check_number == 0.625:
            central_atom = elements_list[c]
            neighbor_atom = elements_list[d]

            o_fea = features_counts.get(("t", central_atom, neighbor_atom))
            if o_fea is not None:
                features_counts[("t", central_atom, neighbor_atom)] -= 1
            else:
                features_counts[("t", neighbor_atom, central_atom)] -= 1
