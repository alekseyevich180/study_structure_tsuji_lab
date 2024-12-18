import csv
import os
import random
import sys

from dotenv import load_dotenv

load_dotenv()

LOCAL_DIR = os.getenv("LOCAL_DIR")
REMOTE_DIR = os.getenv("REMOTE_DIR")
WORK_DIR = os.getenv("WORK_DIR")
JOB_USER = os.getenv("JOB_USER")
INIT_NUM = os.getenv("INIT_NUM")
BO_NUM = os.getenv("BO_NUM")

# POSCARs ディレクトリのパスを指定
directory = f"{REMOTE_DIR}{WORK_DIR}/structures/one_million_models/POSCARs"
# ディレクトリが存在しない場合は作成する
os.makedirs(directory, exist_ok=True)

features_ID_d = {}

ROOT_PATH = f"{REMOTE_DIR}{WORK_DIR}/calc"

for i in range(1, 300):
    feature_a = random.randint(-10, -1)
    feature_b = random.randint(1, 10)
    feature_c = random.randint(1, 10)
    feature_d = random.randint(1, 10)
    fe_nsw = 2000 if random.random() < 0.1 else 0
    fe_force = 1 if random.random() < 0.1 else 0.01
    fe_ene = feature_a * feature_b * feature_c * feature_d

    features_values = [feature_a, feature_b, feature_c, feature_d]

    if tuple(features_values) in features_ID_d:
        print("Features are duplicated")
        sys.exit(1)
    else:
        # 特徴量数(key)とID(value)を紐づけた逆引き辞書をつくる
        features_ID_d[tuple(features_values)] = i

        filename = os.path.join(directory, f"POSCAR_{i}")
        with open(filename, "w") as file:
            file.write(f"{fe_nsw}\t{fe_force}\t{fe_ene}\t{i}\n")

        if i == 1:
            try:
                with open(
                    f"{ROOT_PATH}/data.csv", "r", newline="", encoding="utf-8"
                ) as csvfile:
                    reader = csv.reader(csvfile)
                    first_row = next(reader, None)
            except FileNotFoundError:
                first_row = None
                pass
            if first_row is not None:
                print("data.csv already exists")
                # 強制終了
                sys.exit(1)
            else:
                with open(
                    f"{ROOT_PATH}/data.csv", "a", newline="", encoding="utf-8"
                ) as csvfile:
                    # csvファイルに書き込むためのライターオブジェクトを作成
                    writer = csv.writer(csvfile)
                    writer.writerow(
                        ["ID"]
                        + ["feature_a"]
                        + ["feature_b"]
                        + ["feature_c"]
                        + ["feature_d"]
                        + ["energy"]
                    )
                    # 一行に構造ID,特徴量カウントの順に書き込みエネルギー欄の枠も作る
                    writer.writerow([i] + features_values + [""])

        else:
            with open(
                f"{ROOT_PATH}/data.csv", "a", newline="", encoding="utf-8"
            ) as csvfile:
                # csvファイルに書き込むためのライターオブジェクトを作成
                writer = csv.writer(csvfile)
                # POSCARファイルが1番目以外の時
                writer.writerow([i] + features_values + [""])
