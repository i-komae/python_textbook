import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import matplotlib.colors as mcolors
import os

os.makedirs("../assets/figures", exist_ok=True)

plt.style.use("my_style.mplstyle")
# Keep labels readable after the figures are fitted to the textbook's text width.
plt.rcParams.update({"font.size": 14})

def gaussian_pdf(x, mean, sigma):
    return (1.0 / (np.sqrt(2 * np.pi) * sigma)) * np.exp(-0.5 * ((x - mean) / sigma)**2)

def exponential_pdf(x, tau):
    return (1.0 / tau) * np.exp(-x / tau)

# 0. Figure, Axes, Axis, and Artist, with labels outside the data
from matplotlib.patches import Rectangle

x = np.linspace(0.4, 3.6, 300)
y1 = 3.8 - 0.7 * x + 0.15 * (x - 3.2) ** 2
y2 = 0.9 + 0.35 * x - 0.25 * np.sin(1.2 * x)
pts_x = np.array([0.7, 0.9, 1.1, 1.3, 1.5, 1.8, 2.0, 2.2, 2.5, 2.8, 3.1, 3.3])
pts_y = np.array([2.8, 2.1, 1.9, 2.5, 2.2, 1.7, 2.3, 1.6, 1.9, 1.5, 1.8, 2.0])
fig, ax = plt.subplots(figsize=(10, 8))
fig.subplots_adjust(left=0.24, right=0.90, bottom=0.25, top=0.80)
fig.add_artist(Rectangle((0.015, 0.015), 0.97, 0.97, transform=fig.transFigure,
                         fill=False, edgecolor="0.6", linestyle="--", linewidth=1))
ax.plot(x, y1, lw=2.5, label="Blue signal")
ax.plot(x, y2, lw=2.5, label="Orange signal")
ax.scatter(pts_x, pts_y, s=90, marker="s", facecolors="none",
           edgecolors="mediumpurple", linewidths=2)
ax.set(xlim=(0, 4), ylim=(0, 4), xlabel="x axis label", ylabel="y axis label")
ax.set_title("Anatomy of a figure", fontsize=18, pad=10)
ax.legend(loc="upper right", fontsize=14, frameon=True)
ax.grid(True, linestyle="--", linewidth=0.7, alpha=0.6)
arrow = {"arrowstyle": "->", "color": "0.3", "linewidth": 1.2}
box = {"facecolor": "white", "edgecolor": "none", "pad": 3}
ax.annotate("Figure\nplt.figure", xy=(0.025, 0.98), xycoords="figure fraction",
            xytext=(0.16, 0.94), textcoords="figure fraction", ha="center",
            va="center", fontsize=14, arrowprops=arrow, bbox=box)
ax.annotate("Axes\nfig.subplots", xy=(1, 1), xycoords="axes fraction",
            xytext=(0.82, 0.94), textcoords="figure fraction", ha="center",
            va="center", fontsize=14, arrowprops=arrow, bbox=box)
ax.annotate("y Axis\nax.yaxis", xy=(0, 0.25), xycoords="axes fraction",
            xytext=(0.09, 0.47), textcoords="figure fraction", ha="center",
            va="center", fontsize=14, arrowprops=arrow, bbox=box)
ax.annotate("x Axis\nax.xaxis", xy=(0.75, 0), xycoords="axes fraction",
            xytext=(0.58, 0.08), textcoords="figure fraction", ha="center",
            va="center", fontsize=14, arrowprops=arrow, bbox=box)
ax.annotate("Artist (line)\nax.plot", xy=(1.8, np.interp(1.8, x, y1)),
            xytext=(0.15, 3.3), fontsize=14, arrowprops=arrow, bbox=box)
ax.annotate("Artist (markers)\nax.scatter", xy=(2.2, 1.6), xytext=(2.4, 0.5),
            fontsize=14, arrowprops=arrow, bbox=box)
fig.savefig("../assets/figures/anatomy_example.pdf", bbox_inches="tight", pad_inches=0.1)
plt.close(fig)

# 1. Basic histogram example
np.random.seed(7)
rng = np.random.default_rng(7)
values = rng.normal(loc=0.0, scale=1.2, size=2500)
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

# 1d. Subplots example (same inputs as the textbook)
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(29)
values1 = rng.normal(loc=0.0, scale=1.0, size=3000)
values2 = rng.normal(loc=0.5, scale=1.2, size=3000)

bin_edges = np.linspace(min(values1.min(), values2.min()),
                        max(values1.max(), values2.max()), 41)
fig, axes = plt.subplots(1, 2, figsize=(10, 4), sharex=True, sharey=True)
axes[0].hist(values1, bins=bin_edges, alpha=0.7, label="sample A")
axes[0].set_title("sample A")
axes[0].set_xlabel("value")
axes[0].set_ylabel("count")

axes[1].hist(values2, bins=bin_edges, alpha=0.7, label="sample B")
axes[1].set_title("sample B")
axes[1].set_xlabel("value")

for ax in axes:
    ax.legend(loc="upper right")
    ax.set_axisbelow(True)

fig.tight_layout()
fig.savefig("../assets/figures/subplots_example.pdf")
plt.close(fig)

# 1. Distribution examples: fit parameters from the displayed samples.
from scipy import stats
rng = np.random.default_rng(37)
gauss_data = rng.normal(loc=3.0, scale=0.8, size=3000)
exp_data = rng.exponential(scale=2.5, size=3000)
mean, sigma = stats.norm.fit(gauss_data)
_, tau = stats.expon.fit(exp_data, floc=0)
fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))
axes[0].hist(gauss_data, bins=40, density=True, alpha=0.7, label="sample")
x_g = np.linspace(gauss_data.min(), gauss_data.max(), 300)
axes[0].plot(x_g, stats.norm.pdf(x_g, loc=mean, scale=sigma),
             label=fr"Normal fit: $\mu={mean:.2f},\ \sigma={sigma:.2f}$")
axes[0].set_xlabel("value")
axes[0].set_ylabel("Probability density")
axes[0].legend(loc="lower center", bbox_to_anchor=(0.5, 1.02), fontsize=14)
axes[1].hist(exp_data, bins=40, density=True, alpha=0.7, label="sample")
x_e = np.linspace(0, exp_data.max(), 300)
axes[1].plot(x_e, stats.expon.pdf(x_e, scale=tau),
             label=fr"Exponential fit: $\tau={tau:.2f}$")
axes[1].set_xlabel("Waiting time [s]")
axes[1].set_ylabel("Probability density [1/s]")
axes[1].legend(loc="lower center", bbox_to_anchor=(0.5, 1.02), fontsize=14)
fig.tight_layout()
fig.savefig("../assets/figures/distribution_examples.pdf")
plt.close(fig)

# 2. Vectorization Benchmark mock
fig, ax = plt.subplots(figsize=(6, 4))
labels = ['slow Python loop', 'NumPy', 'pandas']
times = [182.4, 2.1, 8.5]
ax.bar(labels, times, color=['#d9534f', '#5bc0de', '#5cb85c'])
ax.set_yscale('log')
ax.set_ylabel("Illustrative relative time")
ax.set_title("Illustration (not measured)")
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

# 4. Errorbar and log scale (same inputs as the textbook)
import numpy as np
import matplotlib.pyplot as plt

x_val = np.geomspace(1.0, 100.0, 12)
y_val = 5.0 * x_val ** (-1.2)
y_err = 0.15 * y_val

fig, axes = plt.subplots(1, 2, figsize=(10, 4))

# fmt='o' は点を丸で描き、capsize=3 は端部の横棒を 3 point にする
axes[0].errorbar(x_val, y_val, yerr=y_err, fmt='o', capsize=3, label="data")
axes[0].set_xlabel("x")
axes[0].set_ylabel("y")

axes[1].errorbar(x_val, y_val, yerr=y_err, fmt='o', capsize=3, label="data")
axes[1].set_yscale('log')
axes[1].set_xscale('log')
axes[1].set_xlabel("x")
axes[1].set_ylabel("y")

fig.tight_layout()
fig.savefig("../assets/figures/errorbar_example.pdf")
plt.close(fig)

# 5. Weighted fit with sigma
def linear_model(x, a, b):
    return a * x + b

x_fit_data = np.array([0.0, 1.0, 2.0, 3.0, 4.0])
y_fit_data = np.array([1.1, 2.0, 3.2, 4.1, 5.1])
y_err_fit = np.array([0.2, 0.2, 1.5, 0.2, 0.2])

popt_bad, _ = curve_fit(linear_model, x_fit_data, y_fit_data)
popt_good, cov_good = curve_fit(
    linear_model,
    x_fit_data,
    y_fit_data,
    sigma=y_err_fit,
    absolute_sigma=True,
)
fit_errors = np.sqrt(np.diag(cov_good))
x_fit_line = np.linspace(0.0, 4.0, 200)

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
    label=fr"without sigma: $y={popt_bad[0]:.3f}x+{popt_bad[1]:.3f}$",
)
ax.plot(
    x_fit_line,
    linear_model(x_fit_line, *popt_good),
    color="#1f77b4",
    lw=2,
    label=fr"with sigma: $y={popt_good[0]:.3f}x+{popt_good[1]:.3f}$",
)
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.legend(loc="upper left", fontsize=12)
ax.grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig("../assets/figures/fit_sigma_comparison.pdf")
plt.close(fig)

# 6. Output from the reusable histogram-and-fit example
rng = np.random.default_rng(42)
module_data = rng.normal(loc=5.0, scale=1.2, size=4000)
module_counts, module_edges = np.histogram(module_data, bins=35)
module_centers = 0.5 * (module_edges[:-1] + module_edges[1:])
module_width = module_edges[1] - module_edges[0]
module_p0 = [module_counts.max(), module_data.mean(), module_data.std(), 0.0]
module_popt, _ = curve_fit(
    lambda x, amplitude, mean, sigma, offset: (
        amplitude * np.exp(-0.5 * ((x - mean) / sigma) ** 2) + offset
    ),
    module_centers,
    module_counts,
    p0=module_p0,
)
module_x = np.linspace(module_edges[0], module_edges[-1], 500)
module_y = (
    module_popt[0]
    * np.exp(-0.5 * ((module_x - module_popt[1]) / module_popt[2]) ** 2)
    + module_popt[3]
)

fig, ax = plt.subplots(figsize=(6.4, 4.2))
ax.hist(
    module_data,
    bins=module_edges,
    histtype="step",
    color="#1f4e79",
    linewidth=1.6,
    label="data",
)
ax.plot(
    module_x,
    module_y,
    color="#c44e52",
    linewidth=2,
    label=fr"Gaussian fit: $\mu={module_popt[1]:.2f}$, $\sigma={abs(module_popt[2]):.2f}$",
)
ax.set_xlabel("signal [mV]")
ax.set_ylabel(f"counts / {module_width:.2f} mV")
ax.legend(
    loc="lower center",
    bbox_to_anchor=(0.5, 1.02),
    ncol=2,
    frameon=False,
)
fig.tight_layout()
fig.savefig("../assets/figures/histfit_module_example.pdf")
plt.close(fig)

# 7. Heatmap and colorbars (same inputs and axes as the textbook)
from matplotlib.colors import LogNorm

x = np.linspace(-3.0, 3.0, 160)
y = np.linspace(-2.5, 2.5, 140)
xx, yy = np.meshgrid(x, y)
image = np.exp(-(xx**2 + 1.6 * yy**2)) + 0.02
rng = np.random.default_rng(1234)
sample_x = rng.normal(loc=0.0, scale=1.0, size=80000)
sample_y = 0.7 * sample_x + rng.normal(loc=0.0, scale=0.8, size=80000)

fig, axes = plt.subplots(1, 2, figsize=(10, 4))
im = axes[0].imshow(image, origin="lower", cmap="viridis", aspect="auto")
fig.colorbar(im, ax=axes[0], label="intensity")
h = axes[1].hist2d(sample_x, sample_y, bins=90, norm=LogNorm(), cmap="magma")
fig.colorbar(h[3], ax=axes[1], label="counts")
fig.tight_layout()
fig.savefig("../assets/figures/heatmap_colorbar_example.pdf")
plt.close(fig)

# 8. Projections of the same synthetic points as the textbook
lon_deg = np.linspace(-180.0, 180.0, 241)
lat_deg = 25.0 * np.sin(np.deg2rad(2.0 * lon_deg))
lon = np.deg2rad(lon_deg)
lat = np.deg2rad(lat_deg)

fig = plt.figure(figsize=(10, 4))
ax1 = fig.add_subplot(1, 2, 1, projection="hammer")
ax2 = fig.add_subplot(1, 2, 2, projection="mollweide")
ax1.scatter(lon, lat, s=8)
ax2.scatter(lon, lat, s=8)
ax1.set_title("Hammer")
ax2.set_title("Mollweide")
ax1.tick_params(labelsize=14)
ax2.tick_params(labelsize=14)
ax1.set_longitude_grid(60)
ax2.set_longitude_grid(60)
ax1.set_latitude_grid(30)
ax2.set_latitude_grid(30)
ax1.grid(True)
ax2.grid(True)
fig.tight_layout()
fig.savefig("../assets/figures/projection_examples.pdf")
plt.close(fig)

# 9. Basic drawing functions (same arrays as the textbook)
rng = np.random.default_rng(1234)
t = np.linspace(0.0, 10.0, 80)
y = np.sin(t) * np.exp(-t / 12.0)
y_noise = y + 0.12 * rng.normal(size=t.size)
y_err = 0.10 + 0.03 * np.cos(t / 2.0) ** 2
fig, axes = plt.subplots(2, 2, figsize=(10, 7))
axes[0, 0].plot(t, y, marker="o")
axes[0, 1].scatter(t, y_noise, c=t, cmap="viridis")
axes[1, 0].plot(t, y_noise)
axes[1, 0].axvline(3.0, linestyle="--")
axes[1, 0].axhline(0.0, linestyle=":")
axes[1, 1].errorbar(t[::4], y_noise[::4], yerr=y_err[::4], fmt="o")
for ax, title in zip(axes.flat, ["plot", "scatter", "axvline / axhline", "errorbar"]):
    ax.set_title(title)
fig.tight_layout()
fig.savefig("../assets/figures/basic_plot_types_example.pdf")
plt.close(fig)

# 10. Mosaic layout (same arrays and panel names as the textbook)
values = np.random.default_rng(42).normal(size=2000)
x = np.linspace(0.0, 10.0, 150)
y_top = np.exp(-x / 5.0) * np.cos(2.0 * x)
x_sc = np.linspace(0.0, 1.0, 25)
y_sc = x_sc**2 + 0.05 * np.sin(20.0 * x_sc)
layout = [["A", "A"], ["B", "C"]]
fig, axes = plt.subplot_mosaic(layout, figsize=(10, 6))
axes["A"].plot(x, y_top)
axes["B"].hist(values, bins=40)
axes["C"].scatter(x_sc, y_sc)
for key, title in [("A", "line plot"), ("B", "histogram"), ("C", "scatter")]:
    axes[key].set_title(f"{key}: {title}")
fig.tight_layout()
fig.savefig("../assets/figures/subplot_mosaic_example.pdf")
plt.close(fig)

# 11. Reference chart for the markers, line styles, and colors in the text
fig, axes = plt.subplots(1, 3, figsize=(10, 4.8))
groups = [(["o", "s", "^", "D", "x"], "Markers"),
          (["-", "--", ":", "-."], "Line styles"),
          ([f"C{i}" for i in range(6)], "Default colors")]
for column, (labels, title) in enumerate(groups):
    ax = axes[column]
    for row, label in enumerate(labels):
        if column == 0:
            ax.plot([0.5], [row], marker=label, markersize=9)
        elif column == 1:
            ax.plot([0.1, 0.9], [row, row], linestyle=label, color="C0", linewidth=2)
        else:
            ax.plot([0.1, 0.9], [row, row], color=label, linewidth=3)
    ax.set(xlim=(0, 1), ylim=(len(labels) - 0.5, -0.5), title=title)
    ax.set_xticks([])
    ax.set_yticks(range(len(labels)), labels)
    ax.tick_params(axis="y", length=0)
    ax.grid(False)
fig.tight_layout()
fig.savefig("../assets/figures/style_reference_example.pdf")
plt.close(fig)

print("Figures generated successfully.")
