import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import matplotlib.colors as mcolors
import os

os.makedirs("../assets/figures", exist_ok=True)

plt.style.use("my_style.mplstyle")

def gaussian_pdf(x, mean, sigma):
    return (1.0 / (np.sqrt(2 * np.pi) * sigma)) * np.exp(-0.5 * ((x - mean) / sigma)**2)

def exponential_pdf(x, tau):
    return (1.0 / tau) * np.exp(-x / tau)

# 0. Anatomy example
from matplotlib.patches import Circle

# -----------------------------
# データ
# -----------------------------
x = np.linspace(0.4, 3.6, 300)

# 緩やかな2本の曲線
y1 = 3.8 - 0.7 * x + 0.15 * (x - 3.2) ** 2
y2 = 0.9 + 0.35 * x - 0.25 * np.sin(1.2 * x)

# 散布図用
pts_x = np.array([0.7, 0.9, 1.1, 1.3, 1.5, 1.8, 2.0, 2.2, 2.5, 2.8, 3.1, 3.3])
pts_y = np.array([2.8, 2.1, 1.9, 2.5, 2.2, 1.7, 2.3, 1.6, 1.9, 1.5, 1.8, 2.0])

# -----------------------------
# 図
# -----------------------------
fig, ax = plt.subplots(figsize=(10, 10), dpi=160)
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

ax.plot(x, y1, lw=2.5, label="Blue signal")
ax.plot(x, y2, lw=2.5, label="Orange signal")
ax.scatter(
    pts_x, pts_y,
    s=90, marker="s",
    facecolors="none", edgecolors="mediumpurple", linewidths=2
)

ax.set_xlim(0, 4)
ax.set_ylim(0, 4)
ax.set_title("Anatomy of a figure", fontsize=22, pad=14)
ax.set_xlabel("x axis label", fontsize=15)
ax.set_ylabel("y axis label", fontsize=15)

ax.grid(True, linestyle="--", linewidth=0.7, alpha=0.6)
ax.legend(loc="upper right", fontsize=14, frameon=True)

# -----------------------------
# 座標変換
# -----------------------------
def data_to_fig(x, y):
    """data座標をfigure座標へ変換"""
    disp = ax.transData.transform((x, y))
    return fig.transFigure.inverted().transform(disp)

def axes_to_fig(x, y):
    """axes座標をfigure座標へ変換"""
    disp = ax.transAxes.transform((x, y))
    return fig.transFigure.inverted().transform(disp)

# -----------------------------
# figure上に注釈を置く関数
# -----------------------------
def add_circle_label(fig_xy, title, subtitle=None, radius=0.025):
    # 丸
    c = Circle(
        fig_xy, radius=radius,
        transform=fig.transFigure,
        fill=False, lw=2.2, ec="#6b79a8"
    )
    fig.add_artist(c)

    # タイトル
    fig.text(
        fig_xy[0], fig_xy[1] - radius - 0.012,
        title,
        ha="center", va="top",
        fontsize=13, fontstyle="italic", fontweight="bold",
        color="#0b1e66", backgroundcolor='w'
    )

    # サブタイトル
    if subtitle is not None:
        fig.text(
            fig_xy[0], fig_xy[1] - radius - 0.036,
            subtitle,
            ha="center", va="top",
            fontsize=11, family="monospace", color="black", backgroundcolor='w'
        )

# -----------------------------
# 各要素の位置
# -----------------------------

# Figure全体の要素
add_circle_label((0.9, 0.93), "Figure", "plt.figure")

# title の近く
add_circle_label((0.47, 0.91), "Title", "ax.set_title")

# legend の近く
add_circle_label((0.81, 0.84), "Legend", "ax.legend")

# grid の中央付近
add_circle_label(data_to_fig(3.0, 3.0), "Grid", "ax.grid")

# line 上
add_circle_label(data_to_fig(1.8, np.interp(1.8, x, y1)), "Line", "ax.plot")

# scatter の代表点
add_circle_label(data_to_fig(2.2, 1.6), "Markers", "ax.scatter")

# x axis label の近く
add_circle_label((0.50, 0.076), "xlabel", "ax.set_xlabel")
add_circle_label((0.27, 0.11), "x Axis", "ax.xaxis")

# y axis label の近く
add_circle_label((0.076, 0.48), "ylabel", "ax.set_ylabel")
add_circle_label((0.125, 0.25), "y Axis", "ax.yaxis")

# axes 全体
add_circle_label((0.65, 0.25), "Axes", "fig.subplots")

# spine の右側
add_circle_label((0.9, 0.24), "Spine", "ax.spines")

fig.savefig("../assets/figures/anatomy_example.pdf")
plt.close(fig)

# 1. Basic histogram example
np.random.seed(7)
values = np.random.normal(loc=0.0, scale=1.2, size=2500)
fig, ax = plt.subplots(figsize=(6, 4))
ax.hist(values, bins=40, alpha=0.8, color="#4C72B0")
ax.set_xlabel("value")
ax.set_ylabel("count")
fig.tight_layout()
fig.savefig("../assets/figures/basic_histogram_example.pdf")
plt.close(fig)

# 1b. Labeled line example
x_line = np.linspace(0.0, 10.0, 60)
y_line = np.exp(-x_line / 4.0) * (1.0 + 0.08 * np.sin(2.5 * x_line))
fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(x_line, y_line, marker="o", ms=3, lw=1.5, label="sample A")
ax.set_xlabel(r"$t\,[\mathrm{s}]$")
ax.set_ylabel("signal")
ax.set_title("Labeled line example")
ax.set_xticks([0, 2, 4, 6, 8, 10])
ax.legend(loc="upper right")
fig.tight_layout()
fig.savefig("../assets/figures/labeled_plot_example.pdf")
plt.close(fig)

# 1c. String axis pitfall
x_str = ["1", "2", "10", "20"]
y_cat = [1.0, 4.0, 2.0, 5.0]
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
axes[0].plot(x_str, y_cat, marker="o")
axes[0].set_title("Strings become categories")
axes[0].set_xlabel("x")
axes[0].set_ylabel("y")

x_num = np.array([1, 2, 10, 20])
axes[1].plot(x_num, y_cat, marker="o")
axes[1].set_title("Numeric axis")
axes[1].set_xlabel("x")
axes[1].set_ylabel("y")
fig.tight_layout()
fig.savefig("../assets/figures/string_axis_example.pdf")
plt.close(fig)

# 1d. Subplots example
np.random.seed(24)
values1 = np.random.normal(loc=0.0, scale=1.0, size=2500)
values2 = np.random.normal(loc=0.8, scale=1.3, size=2500)
fig, axes = plt.subplots(1, 2, figsize=(10, 4), sharey=True)
axes[0].hist(values1, bins=40, alpha=0.7, label="sample A")
axes[0].set_title("sample A")
axes[0].set_xlabel("value")
axes[0].set_ylabel("count")

axes[1].hist(values2, bins=40, alpha=0.7, label="sample B")
axes[1].set_title("sample B")
axes[1].set_xlabel("value")

for ax in axes:
    ax.legend(loc="upper right")
    ax.set_axisbelow(True)

fig.tight_layout()
fig.savefig("../assets/figures/subplots_example.pdf")
plt.close(fig)

# 1. Distribution Examples
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
np.random.seed(42)
gauss_data = np.random.normal(0, 1.5, 5000)
exp_data = np.random.exponential(2.5, 5000)

axes[0].hist(gauss_data, bins=40, density=True, alpha=0.7, label="data")
x_g = np.linspace(-6, 6, 100)
axes[0].plot(x_g, gaussian_pdf(x_g, 0, 1.5), lw=2, label="fit: Gaussian")
axes[0].set_xlabel("Value")
axes[0].set_ylabel("Density")
axes[0].legend()

counts, bins, _ = axes[1].hist(exp_data, bins=40, range=(0, 15), density=True, alpha=0.7, label="data")
x_e = np.linspace(0, 15, 100)
axes[1].plot(x_e, exponential_pdf(x_e, 2.5), lw=2, label="fit: Exponential")
axes[1].set_xlabel("Wait Time")
axes[1].set_ylabel("Density")
axes[1].legend()
fig.tight_layout()
fig.savefig("../assets/figures/distribution_examples.pdf")
plt.close(fig)

# 2. Vectorization Benchmark mock
fig, ax = plt.subplots(figsize=(6, 4))
labels = ['slow Python loop', 'NumPy', 'pandas']
times = [182.4, 2.1, 8.5]
ax.bar(labels, times, color=['#d9534f', '#5bc0de', '#5cb85c'])
ax.set_yscale('log')
ax.set_ylabel("Execution Time [s]")
ax.set_title("Vectorization Performance Comparison")
fig.tight_layout()
fig.savefig("../assets/figures/vectorization_benchmark.pdf")
plt.close(fig)

# 3. Heatmap (2D Histogram) Example
np.random.seed(42)
x = np.random.randn(100000)
y = x * 0.7 + np.random.randn(100000) * 0.3
fig, ax = plt.subplots(figsize=(6, 5))
h = ax.hist2d(x, y, bins=50, norm=mcolors.LogNorm(), cmap='viridis')
cbar = fig.colorbar(h[3], ax=ax, label="Counts (Log Scale)")
ax.set_xlabel("X value (e.g., Energy)")
ax.set_ylabel("Y value (e.g., Pulse Shape)")
ax.set_title("2D Histogram (LogNorm)")
fig.tight_layout()
fig.savefig("../assets/figures/heatmap_example.pdf")
fig.savefig("../assets/figures/heatmap_example.png", dpi=150) # Raster example for explanation
plt.close(fig)

# 4. Errorbar and Log Scale
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
x_val = np.logspace(0, 3, 15)
y_val = 1000 * np.exp(-x_val / 50) + np.abs(np.random.randn(15) * 5)
y_err = np.sqrt(np.abs(y_val) + 1)

axes[0].errorbar(x_val, y_val, yerr=y_err, fmt='o', capsize=3, label="data")
axes[0].set_xlabel("Time [ns]")
axes[0].set_ylabel("Rate [Hz]")
axes[0].legend()

axes[1].errorbar(x_val, y_val, yerr=y_err, fmt='o', capsize=3, label="data")
axes[1].set_yscale('log')
axes[1].set_xscale('log')
axes[1].set_xlabel("Time [ns] (Log Scale)")
axes[1].set_ylabel("Rate [Hz] (Log Scale)")
axes[1].legend()

fig.tight_layout()
fig.savefig("../assets/figures/errorbar_example.pdf")
plt.close(fig)

# 5. Weighted fit with sigma
def linear_model(x, a, b):
    return a * x + b

x_fit_data = np.linspace(0.0, 10.0, 11)
y_true = linear_model(x_fit_data, 1.8, 6.8)
y_noise = np.array([1.0, -0.7, 0.6, 1.4, -0.8, -1.1, -0.6, 0.0, 1.8, 0.7, 0.9])
y_fit_data = y_true + y_noise
y_fit_data[8] = 43.0
y_err_fit = np.full_like(x_fit_data, 1.5)
y_err_fit[8] = 20.0

popt_bad, _ = curve_fit(linear_model, x_fit_data, y_fit_data)
popt_good, cov_good = curve_fit(
    linear_model,
    x_fit_data,
    y_fit_data,
    sigma=y_err_fit,
    absolute_sigma=True,
)
fit_errors = np.sqrt(np.diag(cov_good))
x_fit_line = np.linspace(0.0, 10.0, 200)

fig, ax = plt.subplots(figsize=(6.6, 4.6))
ax.errorbar(
    x_fit_data,
    y_fit_data,
    yerr=y_err_fit,
    fmt="o",
    color="black",
    capsize=3,
    label="data",
)
ax.plot(
    x_fit_line,
    linear_model(x_fit_line, *popt_bad),
    "r--",
    lw=2,
    label=fr"without sigma: $y={popt_bad[0]:.1f}x+{popt_bad[1]:.1f}$",
)
ax.plot(
    x_fit_line,
    linear_model(x_fit_line, *popt_good),
    color="#1f77b4",
    lw=2,
    label=fr"with sigma: $y={popt_good[0]:.1f}x+{popt_good[1]:.1f}$",
)
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.legend(loc="upper left", fontsize=10)
ax.grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig("../assets/figures/fit_sigma_comparison.pdf")
plt.close(fig)

print("Figures generated successfully.")
