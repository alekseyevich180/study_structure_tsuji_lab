"""
generate_nacl_poscar.py

岩塩構造のPOSCARファイルを生成するスクリプト

- 金属原子と酸素原子の座標を生成し、POSCARファイルを保存する
- 金属原子間の組み合わせを取得し、CSVファイルに書き込む
"""

import random
import os
import csv
from pymatgen.core.structure import Structure, Lattice, Element
from datetime import datetime

LATTICE_SIZE = 4  # 4x4x4の結晶
FILE_PATH = "high-entropy-oxide/rocksalt-NiMgCuCoZnO/discussions/spc_features"
FOLDER_NAME = "POSCARs"
METAL_ELEMENTS = {"Ni": 6, "Mg": 6, "Cu": 6, "Co": 7, "Zn": 7}
LATTICE_CONSTANT = 8.5

os.makedirs(os.path.join(FILE_PATH, FOLDER_NAME), exist_ok=True)


def load_existing_data(csv_file_path):
    reverse_existing_data = {}
    if os.path.isfile(csv_file_path):
        with open(csv_file_path, "r", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip header
            for row in reader:
                id_ = int(row[0])
                features = ",".join(row[1:-1])  # Skip energy column
                reverse_existing_data[features] = id_
        return reverse_existing_data, len(reverse_existing_data) + 1
    return {}, 1


def generate_metal_coords(n, lattice_size):
    coords = []
    for i in range(lattice_size):
        for j in range(lattice_size):
            for k in range(lattice_size):
                if (i + j + k) % 2 == 0:  # 岩塩構造の金属位置
                    coords.append(
                        (i / lattice_size, j / lattice_size, k / lattice_size)
                    )
    return random.sample(coords, n)


def find_all_metal_combinations(metal_sites, metal_coords):
    total_atom_combinations = {}
    neighbor_offsets = [
        (0, 0.25, 0.25),
        (0.25, 0, 0.25),
        (0.25, 0.25, 0),
        (0, 0.25, -0.25),
        (0.25, 0, -0.25),
        (0.25, -0.25, 0),
    ]

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


def generate_poscar_and_combinations():
    total_metal_atoms = sum(METAL_ELEMENTS.values())

    reverse_existing_data, _ = load_existing_data(f"{FILE_PATH}/spc_data.csv")

    # now = datetime.now()
    # formatted_date = now.strftime("%y%m%d_%H%M%S")

    all_pairs = [
        frozenset([i, j])
        for i in METAL_ELEMENTS.keys()
        for j in METAL_ELEMENTS.keys()
        if list(METAL_ELEMENTS.keys()).index(i) <= list(METAL_ELEMENTS.keys()).index(j)
    ]

    new_data = {}
    reverse_new_data = {}

    remaining_features = list(reverse_existing_data.keys())

    print("Remaining features:", remaining_features)

    while remaining_features:
        metal_coords = generate_metal_coords(total_metal_atoms, LATTICE_SIZE)
        oxygen_coords = [
            (i / LATTICE_SIZE, j / LATTICE_SIZE, k / LATTICE_SIZE)
            for i in range(LATTICE_SIZE)
            for j in range(LATTICE_SIZE)
            for k in range(LATTICE_SIZE)
            if (i + j + k) % 2 == 1
        ]

        metal_sites = []
        for element, count in METAL_ELEMENTS.items():
            metal_sites.extend([Element(element)] * count)

        metal_sites_coords = random.sample(metal_coords, total_metal_atoms)
        lattice = Lattice.cubic(LATTICE_CONSTANT)
        structure = Structure(
            lattice,
            metal_sites + ["O"] * len(oxygen_coords),
            list(metal_sites_coords) + list(oxygen_coords),
        )

        atom_combinations = find_all_metal_combinations(metal_sites, metal_sites_coords)
        feature_vector = [atom_combinations.get(pair, 0) for pair in all_pairs]
        feature_vector_str = ",".join(map(str, feature_vector))

        if feature_vector_str in remaining_features:
            now = datetime.now()
            formatted_date = now.strftime("%y%m%d_%H%M%S_%f")
            print(now, feature_vector_str)

            new_data[formatted_date] = feature_vector_str
            reverse_new_data[feature_vector_str] = formatted_date
            poscar_file_path = os.path.join(
                FILE_PATH, FOLDER_NAME, f"POSCAR_{formatted_date}"
            )
            structure.to(fmt="poscar", filename=poscar_file_path)
            remaining_features.remove(feature_vector_str)

            # CSVファイルに追記
            with open(
                f"{FILE_PATH}/spc_data.csv", "a", newline="", encoding="utf-8"
            ) as csvfile:
                writer = csv.writer(csvfile)
                if not reverse_existing_data:
                    writer.writerow(
                        ["ID"] + ["_".join(pair) for pair in all_pairs] + ["energy"]
                    )
                writer.writerow([formatted_date] + feature_vector_str.split(",") + [""])


generate_poscar_and_combinations()