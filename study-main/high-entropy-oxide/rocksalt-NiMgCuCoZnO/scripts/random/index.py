import pandas as pd
import sys

data_path = sys.argv[1] + "/data.csv"
num_candidates = int(sys.argv[2])

# データの読み込み
df = pd.read_csv(data_path, engine="python", encoding="utf-8")

# IDをインデックスに設定
df = df.set_index("ID")

# 'energy'列にデータがない行のみを抽出
df_without_energy = df[df["energy"].isnull()]

# ランダムにNUM_CANDIDATESのIDを選択
random_candidates = df_without_energy.sample(num_candidates).index.tolist()

# 選択されたIDを出力
print("\n".join(map(str, random_candidates)))
