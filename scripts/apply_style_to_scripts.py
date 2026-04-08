import os
import glob

# 置換対象の古い rcParams パターン (スクリプトによって改行やインデントが微妙に違う可能性があるため、
# もっと大胆に "mpl.rcParams.update({" から "})" までを削除するか、正規表現を使う
import re

scripts = ["generate_plots.py", "generate_step_plots.py", "generate_fit_plot.py"]

# パターン: "mpl.rcParams.update({" で始まり、次の "})" までを最短マッチで取得
pattern = re.compile(r'mpl\.rcParams\.update\(\{.*?\n\}\)', re.DOTALL)

for script in scripts:
    path = os.path.join(".", script)
    if not os.path.exists(path):
        continue
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 置換
    new_content = pattern.sub('plt.style.use("my_style.mplstyle")', content)
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"Updated {script}")
