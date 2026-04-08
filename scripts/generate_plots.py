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

print("Figures generated successfully.")
