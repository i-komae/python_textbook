import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import os

os.makedirs("../assets/figures", exist_ok=True)

plt.style.use("my_style.mplstyle")

def linear_model(x, a, b):
    return a * x + b

# ガウスノイズを持ったデータを作成だが、一部のデータにエラーバーが極端に大きい（信頼性の低い点）を混ぜる
np.random.seed(0)
xdata = np.linspace(0, 10, 15)
y_true = 2.0 * xdata + 5.0
y_err = np.ones_like(xdata) * 1.5
# 意図的に外れ値を作り、その点のエラーバーを非常に大きくする
ydata = y_true + np.random.randn(len(xdata)) * y_err
ydata[12] += 20.0  # 外れ値
y_err[12] = 20.0   # ただしこの点は測定エラーも非常に大きい（信頼すべきではない）

# 1. 失敗例：sigma を無視してフィット
popt_bad, _ = curve_fit(linear_model, xdata, ydata)

# 2. 成功例：sigma を考慮してフィット
# absolute_sigma=True とすることで絶対誤差として扱う
popt_good, _ = curve_fit(linear_model, xdata, ydata, sigma=y_err, absolute_sigma=True)

fig, ax = plt.subplots(figsize=(6, 5))
ax.errorbar(xdata, ydata, yerr=y_err, fmt='ok', capsize=3, label="Data")
ax.plot(xdata, linear_model(xdata, *popt_bad), color='red', linestyle='--', label=f"Fit (No Sigma)\ny={popt_bad[0]:.1f}x+{popt_bad[1]:.1f}")
ax.plot(xdata, linear_model(xdata, *popt_good), color='blue', linestyle='-', label=f"Fit (With Sigma)\ny={popt_good[0]:.1f}x+{popt_good[1]:.1f}")

ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_title("Importance of Sigma in curve_fit")
ax.legend()
fig.tight_layout()
fig.savefig("../assets/figures/fit_sigma_comparison.pdf")
plt.close(fig)

print("Fit plot generated.")
