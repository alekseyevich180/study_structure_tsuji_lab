import pandas as pd
import GPy
from GPy import kern as gp_kern
import numpy as np
from scipy.stats import norm
import sys

data_path = sys.argv[1] + "/data.csv"
log_path = sys.argv[1] + "/bo-py.log"
num_candidates = int(sys.argv[2])


def log_message(message):
    with open(log_path, "a") as log_file:
        log_file.write(message + "\n")


def acquisition_lcb(mean, std, kappa):
    return mean - kappa * std


def acquisition_EI(mean, std, min_value, xi=0.001):
    imp = min_value - mean - xi
    Z = imp / std
    ei = imp * norm.cdf(Z) + std * norm.pdf(Z)
    return ei


log_message("Starting Python script")

# データの読み込み
df = pd.read_csv(data_path, engine="python", encoding="utf-8")

# IDをインデックスに設定
df = df.set_index("ID")

# 'energy'列にデータがある行のみを抽出
df_with_energy = df.dropna(subset=["energy"])

# 'energy'列にデータがない行のみを抽出
df_without_energy = df[df["energy"].isnull()].drop(columns=["energy"])

# 特徴量とターゲット変数の分割
X = df_with_energy.iloc[:, :-1]
y = df_with_energy.iloc[:, -1:]

# ガウス過程回帰モデルの設定と訓練
num = X.shape[1]
kernel = gp_kern.RBF(num) * gp_kern.Bias(num) + gp_kern.Linear(num) * gp_kern.Bias(num)
model = GPy.models.GPRegression(X.values, y.values, kernel=kernel, normalizer=True)
model.optimize()

# 各特徴量での獲得関数の計算
min_value = min(df["energy"])
means = []
stds = []
acs_ei = []
acs_lcb = []

itera = df_without_energy.values
for item in itera:
    mean, val = model.predict(np.array(item).reshape(1, -1))
    std = np.sqrt(val)

    ac_ei = acquisition_EI(mean, std, min_value)
    ac_lcb = acquisition_lcb(mean, std, 7)

    means.append(mean.flatten()[0])
    stds.append(std.flatten()[0])
    acs_ei.append(ac_ei.flatten()[0])
    acs_lcb.append(ac_lcb.flatten()[0])

# 提案された特徴量を Pandas データフレームとして出力
result_df = pd.DataFrame(df_without_energy)
result_df = result_df.assign(mean=means, std=stds, EI=acs_ei, LCB=acs_lcb)

# 候補の ID を出力
result_df_sort = result_df.sort_values("LCB", ascending=True)
log_message(f"Sorted result: {result_df_sort.head(num_candidates*2)}")

candidates = result_df_sort.head(num_candidates).index.tolist()
print("\n".join(map(str, candidates)))
log_message("Python script finished")
