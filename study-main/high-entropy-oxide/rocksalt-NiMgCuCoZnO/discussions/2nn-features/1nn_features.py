import csv
import os

from pymatgen.core.structure import Structure

# パラメータの定義
MAIN_PATH = "high-entropy-oxide/rocksalt-NiMgCuCoZnO"
START_NUM = 1
END_NUM = 1000000
RESULT_CSV = "data_1nn.csv"
METAL_ELEMENTS = {"Ni": 6, "Mg": 6, "Cu": 6, "Co": 7, "Zn": 7}

# NaCl構造の近接オフセット
neighbor_offsets = [
    (0, 0.25, 0.25),
    (0.25, 0, 0.25),
    (0.25, 0.25, 0),
    (0, 0.25, -0.25),
    (0.25, 0, -0.25),
    (0.25, -0.25, 0),
]


def load_energy_data(energy_csv):
    energy_data = {}
    with open(energy_csv, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            energy_data[int(row["ID"])] = row["energy"]
    return energy_data


def find_all_metal_combinations(metal_sites, metal_coords):
    total_atom_combinations = {}
    coord_to_atom = {coord: metal_sites[i] for i, coord in enumerate(metal_coords)}

    for central_coord, central_atom in coord_to_atom.items():
        for offset in neighbor_offsets:
            neighbor_coord = tuple(
                (central_coord[i] + offset[i]) % 1.0 for i in range(3)
            )
            if neighbor_coord in coord_to_atom:
                neighbor_atom = coord_to_atom[neighbor_coord]
                atom_pair = frozenset([central_atom.symbol, neighbor_atom.symbol])
                total_atom_combinations[atom_pair] = (
                    total_atom_combinations.get(atom_pair, 0) + 1
                )

    return total_atom_combinations


def check_poscar_combinations(file_path, start_num, end_num, result_csv, energy_data):
    all_pairs = [
        frozenset([i, j])
        for i in METAL_ELEMENTS.keys()
        for j in METAL_ELEMENTS.keys()
        if list(METAL_ELEMENTS.keys()).index(i) <= list(METAL_ELEMENTS.keys()).index(j)
    ]
    header = ["ID"] + ["_".join(pair) for pair in all_pairs] + ["energy"]

    rows = []
    for num in range(start_num, end_num + 1):
        poscar_file = os.path.join(file_path, f"POSCAR_{num}")
        if os.path.isfile(poscar_file):
            structure = Structure.from_file(poscar_file)

            metal_sites = []
            metal_coords = []

            for site in structure:
                if site.specie.symbol != "O":  # Exclude oxygen atoms
                    metal_sites.append(site.specie)
                    metal_coords.append(tuple(site.frac_coords))

            atom_combinations = find_all_metal_combinations(metal_sites, metal_coords)

            row = [num] + [atom_combinations.get(pair, 0) for pair in all_pairs]
            row.append(energy_data.get(num, ""))  # エネルギーデータを追加
            rows.append(row)

    with open(result_csv, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        writer.writerows(rows)


# エネルギーデータをロード
energy_data = load_energy_data(f"{MAIN_PATH}/discussions/bo/data.csv")

# POSCARファイルの組み合わせをチェック
check_poscar_combinations(
    f"{MAIN_PATH}/scripts/generate-poscars/POSCARs",
    START_NUM,
    END_NUM,
    f"{MAIN_PATH}/discussions/2nn-features/{RESULT_CSV}",
    energy_data,
)
