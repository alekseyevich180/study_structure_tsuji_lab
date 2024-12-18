# 〇〇の定義
def find_all_metal_combinations(structure, threshold=4.0):
    total_atom_combinations = {}

    # Iterate over all metal atoms in the structure (excluding oxygen)
    for central_atom_index, central_atom in enumerate(structure):
        # iterate「反復する」
        # 辞書について
        # 「for キー,値 in 辞書名.items()」
        # enumurate「列挙する」
        # 「for i,d in enumerate(list)」list内のd(i番目)にiというインデックスを付ける

        if central_atom.specie.symbol != "O":  # Exclude oxygen atoms
            # 「!=」等しくない

            # Iterate over other atoms to find nearby metal atoms, starting from the atom next to the central atom
            for i in range(central_atom_index + 1, len(structure)):
                atom = structure[i]

                # i番目の〇〇が0でない時〇〇
                if atom.specie.symbol != "O":  # Exclude oxygen atoms
                    distance = structure.get_distance(central_atom_index, i)

                    # 〇〇距離がthreshold(4.0)より近い時
                    if distance <= threshold:
                        # Create a set for the combination of central atom and nearby atom
                        atom_pair = frozenset(
                            [central_atom.specie.symbol, atom.specie.symbol]
                        )
                        # 「frozenset」順不同の型

                        # Update the dictionary with the atom pair
                        total_atom_combinations[atom_pair] = (
                            total_atom_combinations.get(atom_pair, 0) + 1
                        )

    return total_atom_combinations
