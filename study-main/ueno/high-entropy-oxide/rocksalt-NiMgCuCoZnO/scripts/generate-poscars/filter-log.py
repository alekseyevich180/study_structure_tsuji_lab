import re

# ログファイル
log_file_path = "high-entropy-oxide/rocksalt-NiMgCuCoZnO/discussions/bo/bo.log"

# log_file_path = "high-entropy-oxide/rocksalt-NiMgCuCoZnO/discussions/random/random.log"

# 日付形式の正規表現パターン
date_pattern = re.compile(
    r"^[A-Za-z]{3} [A-Za-z]{3} \d{2} \d{2}:\d{2}:\d{2} [A-Z]{3} \d{4}"
)

# フィルタリングされた行を一時的に保持するリスト
filtered_lines = []

# ログファイルのフィルタリング
with open(log_file_path, "r") as log_file:
    for line in log_file:
        if date_pattern.match(line):
            filtered_lines.append(line)

# フィルタリング後の行を元のファイルに上書き保存
with open(log_file_path, "w") as log_file:
    log_file.writelines(filtered_lines)

print(f"Filtered log file saved as '{log_file_path}'.")
