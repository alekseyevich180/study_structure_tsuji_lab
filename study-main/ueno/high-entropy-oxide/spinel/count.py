import os
import csv
from pymatgen.core.structure import Structure


def find_all_metal_combinations(structure, threshold=4.0):
    total_atom_combinations = {}

    # Iterate over all metal atoms in the structure (excluding oxygen)
    for central_atom_index, central_atom in enumerate(structure):
        if central_atom.specie.symbol != "O":  # Exclude oxygen atoms

            # Iterate over other atoms to find nearby metal atoms, starting from the atom next to the central atom
            for i in range(central_atom_index + 1, len(structure)):
                atom = structure[i]
                if atom.specie.symbol != "O":  # Exclude oxygen atoms
                    distance = structure.get_distance(central_atom_index, i)
                    if distance <= threshold:
                        # Create a set for the combination of central atom and nearby atom
                        atom_pair = frozenset([central_atom.specie.symbol, atom.specie.symbol])

                        # Update the dictionary with the atom pair
                        total_atom_combinations[atom_pair] = total_atom_combinations.get(atom_pair, 0) + 1

    return total_atom_combinations

def create_csv_with_combinations(poscar_dir, csv_file_path):
    # CSVファイルを開く
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        # CSVライターを作成
        writer = csv.writer(csvfile)

        # ヘッダー行を書き込む
        # 金属の種類の組み合わせを列として追加
        # 金属元素が Ni, Mg, Cu, Co, Zn の5種類であることを想定
        metal_elements = ['Ni', 'Mg', 'Cu', 'Co', 'Zn']
        all_pairs = [frozenset([i, j]) for i in metal_elements for j in metal_elements if metal_elements.index(i) <= metal_elements.index(j)]
        header = ['ID'] + ['_'.join(pair) for pair in all_pairs] + ['energy']
        writer.writerow(header)

        # POSCARファイルのディレクトリを走査
        for file_name in os.listdir(poscar_dir):
            if 'POSCAR' in file_name:
                # ファイルパスを作成
                file_path = os.path.join(poscar_dir, file_name)

                # POSCARファイルを読み込み、構造を取得
                structure = Structure.from_file(file_path)

                # 金属原子間の組み合わせの辞書を取得
                atom_combinations = find_all_metal_combinations(structure)
                # print(file_name, atom_combinations)

                # 1行にまとめてCSVファイルに書き込む
                row = [file_name] + [atom_combinations.get(pair, 0) for pair in all_pairs] + []
                writer.writerow(row)

create_csv_with_combinations('POSCARs', 'data.csv')
