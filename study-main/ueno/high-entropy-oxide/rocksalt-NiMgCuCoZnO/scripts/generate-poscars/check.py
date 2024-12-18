import os
import csv
from pymatgen.core.structure import Structure

# パラメータの定義
ROOT_PATH = "high-entropy-oxide/rocksalt-NiMgCuCoZnO/scripts/generate-poscars"
POSCAR_FOLDER = "POSCARs"
START_NUM = 1
END_NUM = 100
RESULT_CSV = "data.csv"
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


def check_poscar_combinations(file_path, start_num, end_num, result_csv):
    all_pairs = [
        frozenset([i, j])
        for i in METAL_ELEMENTS.keys()
        for j in METAL_ELEMENTS.keys()
        if list(METAL_ELEMENTS.keys()).index(i) <= list(METAL_ELEMENTS.keys()).index(j)
    ]
    header = ["ID"] + ["_".join(pair) for pair in all_pairs]

    with open(result_csv, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)

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

                atom_combinations = find_all_metal_combinations(
                    metal_sites, metal_coords
                )
                print(f"all atom combinations: {sum(atom_combinations.values())}")

                row = [num] + [atom_combinations.get(pair, 0) for pair in all_pairs]
                writer.writerow(row)


check_poscar_combinations(
    f"{ROOT_PATH}/{POSCAR_FOLDER}", START_NUM, END_NUM, f"{ROOT_PATH}/{RESULT_CSV}"
)
