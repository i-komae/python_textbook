import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import os

os.makedirs("../assets/figures", exist_ok=True)

plt.style.use("my_style.mplstyle")

# Same 600,000 synthetic points as the textbook listing.
rng = np.random.default_rng(19)
x = rng.normal(loc=0.0, scale=1.0, size=600_000)
y = 0.65 * x + rng.normal(loc=0.0, scale=0.55, size=x.size)

# 1. 失敗例: 散布図 (Scatter)
fig, ax = plt.subplots(figsize=(6, 5))
# s=10, alphaを指定しないことで完全に黒潰れさせる
ax.scatter(x, y, s=10, c='black')
ax.set_xlabel("X value")
ax.set_ylabel("Y value")
ax.set_title("Scatter Plot (Overplotted)")
fig.tight_layout()
# 散布図で点を数十万個打つとPDFが重くなるため PNG で保存
fig.savefig("../assets/figures/scatter_bad.png", dpi=150)
plt.close(fig)

# 2. 失敗例: 線形スケールの2次元ヒストグラム
fig, ax = plt.subplots(figsize=(6, 5))
h_lin = ax.hist2d(x, y, bins=50, cmap='viridis')
cbar = fig.colorbar(h_lin[3], ax=ax, label="Counts (Linear)")
ax.set_xlabel("X value")
ax.set_ylabel("Y value")
ax.set_title("2D Histogram (Linear Scale)")
fig.tight_layout()
fig.savefig("../assets/figures/hist2d_linear_bad.pdf")
plt.close(fig)

# 3. 成功例: LogNormを用いた2次元ヒストグラム
fig, ax = plt.subplots(figsize=(6, 5))
h_log = ax.hist2d(x, y, bins=50, norm=mcolors.LogNorm(), cmap='viridis')
cbar = fig.colorbar(h_log[3], ax=ax, label="Counts (Log Scale)")
ax.set_xlabel("X value")
ax.set_ylabel("Y value")
ax.set_title("2D Histogram (LogNorm)")
fig.tight_layout()
fig.savefig("../assets/figures/hist2d_lognorm_good.pdf")
plt.close(fig)

# 4. Pandasのパフォーマンス比較ダミー図
fig, ax = plt.subplots(figsize=(6, 4))
labels = ['for loop\n(iterrows)', 'apply()', 'Pandarallel']
times = [315.2, 12.4, 4.1]
ax.bar(labels, times, color=['#d9534f', '#f0ad4e', '#5cb85c'])
ax.set_yscale('log')
# テキストが上端に見切れないようY軸の上限を意図的に広げる
ax.set_ylim(bottom=1, top=2000)

for i, v in enumerate(times):
    ax.text(i, v * 1.3, f"{v}", ha='center')
ax.set_ylabel("Illustrative relative time")
ax.set_title("Illustration (not measured)")
fig.tight_layout()
fig.savefig("../assets/figures/pandas_benchmark.pdf")
plt.close(fig)

print("Step-by-step plots generated.")
